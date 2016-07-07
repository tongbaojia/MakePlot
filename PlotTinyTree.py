###Tony: improve to load branches for faster processing
###Performance is not garanteened. The way to register hists are slow
###For a quick on the fly anaysis, great.
###For a more proper anlaysis, do the c++ standard way please
import ROOT, helpers
import config as CONF
import time, os, subprocess, glob, argparse, compiler
#for parallel processing!
import multiprocessing as mp
import numpy as np
#import tree configuration
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('TinyTree.C')

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",  default="TEST_c10-cb")
    parser.add_argument("--outputdir", default="test")
    parser.add_argument("--dosyst",    default=None)
    parser.add_argument("--reweight",  default=None)
    parser.add_argument("--iter",      default=0)
    return parser.parse_args()

#returns a dictionary of weights
def get_parameter(filename="test.txt"):
    #the input file need to be the following format; change to lists of tuples
    #iteration; Ntrk; parameter; inputfolder; parameterfile
    def get_info(lstline):
        return compiler.compile(lstline[2], '<string>', 'eval'), get_reweight(lstline[3], lstline[4])

    f_reweight = open("script/" + filename + ".txt", "r")
    TwoTagDic = []
    ThreeTagDic = []
    FourTagDic = []
    for line in f_reweight:
        if "#" in line:
            continue
        lstline =  line.split()
        #check which iteration it is; don't go beyond! start with 1
        #print lstline[0], ops.iter
        if int(lstline[0]) > int(ops.iter):
            continue
        #now proceed normally
        if "2bs" in line:
            TwoTagDic.append(get_info(lstline))
        elif "3b" in line:
            ThreeTagDic.append(get_info(lstline))
        elif "4b" in line:
            FourTagDic.append(get_info(lstline))
    #print par_weight
    f_reweight.close()
    #print TwoTagDic
    return (TwoTagDic, ThreeTagDic, FourTagDic)

#returns a dictionary of weights
def get_reweight(folder, filename):
    reweightfolder = CONF.outputpath + folder + "/" + "Reweight/"
    f_reweight = open(reweightfolder + filename, "r")
    par_weight = {}
    for line in f_reweight:
        lstline =  line.split()#default split by space
        #print lstline
        if "par0" in line:
            par_weight["par0"] = float(lstline[1])
        elif "par1" in line:
            par_weight["par1"] = float(lstline[1])
        elif "par2" in line:
            par_weight["par2"] = float(lstline[1])
        elif "par3" in line:
            par_weight["par3"] = float(lstline[1])
        elif "low" in line:
            par_weight["low"] = float(lstline[1])
        elif "high" in line:
            par_weight["high"] = float(lstline[1])
    #print par_weight
    f_reweight.close()
    return par_weight

#calculate the weight based on the input dictionary as the instruction
def calc_reweight(dic, event):
    totalweight = 1
    maxscale = 2.0 #this means the maximum correction is this for each reweighting
    minscale = 0.1 #this means the minimum correction is this for each reweighting
    for x, v in dic:#this "dic" really is not a dic, but a tuple!
        value = eval(x)
        #outside fit range, do the end point value extrapolation
        if (v["low"] > value):
            value =  v["low"] 
        elif (v["high"] < value): 
            value =  v["high"]
        #start calculated reweight factor
        tempweight = 1
        tempweight = v["par0"] + v["par1"] * value + v["par2"] * value ** 2 + v["par3"] * value ** 3
        #this protects each individual weight; tight this up a bit
        if tempweight < 0.7:
            tempweight = 0.7
        elif tempweight > 1.3:
            tempweight = 1.3
        totalweight *= tempweight

    #print totalweight
    #also contrain the totalweight
    if totalweight < minscale:
        totalweight = minscale
    elif totalweight > maxscale:
        totalweight = maxscale
    return totalweight

#get Xhh and Rhh values; for variations's sake
def GetExp(XhhCenterX=124., XhhCenterY=115., XhhCut=1.6, RhhCenterX=124., RhhCenterY=115., RhhCut=35.8):
    #XhhExp = "ROOT.TMath.Sqrt(ROOT.TMath.Power((event.j0_m - %s)/(0.1*event.j0_m), 2) + ROOT.TMath.Power((event.j1_m - %s)/(0.1*event.j1_m), 2)) < %s" % (XhhCenterX, XhhCenterY, XhhCut)
    RhhExp = "ROOT.TMath.Sqrt(ROOT.TMath.Power(event.j0_m - %s, 2) + ROOT.TMath.Power(event.j1_m - %s, 2)) < %s" % (RhhCenterX, RhhCenterY, RhhCut)
    return RhhExp



class eventHists:
    # will take 3 minutes to generate all histograms; 3 times more time...

    def __init__(self, region, outputroot, reweight=False):
        outputroot.cd()
        outputroot.mkdir(region)
        outputroot.cd(region)
        self.fullhist =  True #ops.dosyst is None ##option to turn it off
        self.region = region
        self.reweight = reweight
        #add in all the histograms
        self.mHH_l        = ROOT.TH1F("mHH_l",              ";mHH [GeV]",        78,  200, 4000)
        self.mHH_pole     = ROOT.TH1F("mHH_pole",           ";mHH [GeV]",        78,  200, 4000)
        self.h0_m         = ROOT.TH1F("leadHCand_Mass",     ";Mass [GeV]",       60,   0,  300)
        self.h1_m         = ROOT.TH1F("sublHCand_Mass",     ";Mass [GeV]",       60,   0,  300)
        self.h0_trk0_pt   = ROOT.TH1F("leadHCand_trk0_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
        self.h1_trk0_pt   = ROOT.TH1F("sublHCand_trk0_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
        self.h0_trk1_pt   = ROOT.TH1F("leadHCand_trk1_Pt",  ";p_{T} [GeV]",      80,  0,   400)
        self.h1_trk1_pt   = ROOT.TH1F("sublHCand_trk1_Pt",  ";p_{T} [GeV]",      80,  0,   400)
        self.Rhh          = ROOT.TH1F("Rhh",                ";Rhh",              100,  0,  200)

        if self.fullhist:
            self.h_deta       = ROOT.TH1F("hCandDeta",          "hCand #Delta#eta",  40,    0,  2.0)
            self.h_dphi       = ROOT.TH1F("hCandDphi",          "hCand #Delta#phi",  66, -3.3,  3.3)
            self.h_dr         = ROOT.TH1F("hCandDr",            "hCand #Deltar",     100,   0,    5)
            self.h_pt_assy    = ROOT.TH1F("hCand_Pt_assy",      ";hCand p_{T} assym", 22, -0.05, 1.05)
            self.h0_m_s       = ROOT.TH1F("leadHCand_Mass_s",   ";Mass [GeV]",       14,   60,  200)
            self.h1_m_s       = ROOT.TH1F("sublHCand_Mass_s",   ";Mass [GeV]",       14,   60,  200)
            self.h0_pt_m      = ROOT.TH1F("leadHCand_Pt_m",     ";p_{T} [GeV]",      200,   200,  2200)
            self.h1_pt_m      = ROOT.TH1F("sublHCand_Pt_m",     ";p_{T} [GeV]",      200,   200,  2200)
            self.h0_eta       = ROOT.TH1F("leadHCand_Eta",      ";#Eta",             42, -2.1,  2.1)
            self.h1_eta       = ROOT.TH1F("sublHCand_Eta",      ";#Eta",             42, -2.1,  2.1)
            self.h0_phi       = ROOT.TH1F("leadHCand_Phi",      ";#Phi",             64, -3.2,  3.2)
            self.h1_phi       = ROOT.TH1F("sublHCand_Phi",      ";#Phi",             64, -3.2,  3.2)
            self.h0_trk_dr    = ROOT.TH1F("leadHCand_trk_dr",   ";trkjet #Deltar",   42, -0.1,    2)
            self.h1_trk_dr    = ROOT.TH1F("sublHCand_trk_dr",   ";trkjet #Deltar",   42, -0.1,    2)
            self.h0_ntrk      = ROOT.TH1F("leadHCand_ntrk",     "number of trkjet",  7,  -0.5, 6.5)
            self.h1_ntrk      = ROOT.TH1F("sublHCand_ntrk",     "number of trkjet",  7,  -0.5, 6.5)
            self.h0_trkpt_diff= ROOT.TH1F("leadHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 80,  0,   800)
            self.h1_trkpt_diff= ROOT.TH1F("sublHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 80,  0,   800)
            self.h0_trks_pt   = ROOT.TH1F("leadHCand_trks_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
            self.h1_trks_pt   = ROOT.TH1F("sublHCand_trks_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
            self.trks_pt      = ROOT.TH1F("trks_Pt",            ";p_{T} [GeV]",      400,  0,   2000)
            self.mH0H1        = ROOT.TH2F("mH0H1",              ";mH1 [GeV]; mH2 [GeV];", 50,  50,  250,  50,  50,  250)

    def Fill(self, event, weight=-1):
        if (weight < 0):#default will use event.weight!
            weight = event.weight
        #fill the branches
        self.mHH_l.Fill(event.mHH, weight)
        self.mHH_pole.Fill(event.mHH_pole, weight)  
        self.h0_m.Fill(event.j0_m, weight)   
        self.h1_m.Fill(event.j1_m, weight) 
        self.h0_trk0_pt.Fill(event.j0_trk0_pt, weight)
        self.h1_trk0_pt.Fill(event.j1_trk0_pt, weight)
        self.h0_trk1_pt.Fill(event.j0_trk1_pt, weight)
        self.h1_trk1_pt.Fill(event.j1_trk1_pt, weight)
        self.Rhh.Fill(event.Rhh, weight)

        if self.fullhist:
            self.mH0H1.Fill(event.j0_m, event.j1_m, weight)
            self.h_deta.Fill(event.detaHH, weight)    
            self.h_dphi.Fill(event.dphiHH, weight)    
            self.h_dr.Fill(event.drHH, weight) 
            self.h_pt_assy.Fill((event.j0_pt - event.j1_pt)/(event.j0_pt + event.j1_pt), weight)
            self.h0_m_s.Fill(event.j0_m, weight)   
            self.h1_m_s.Fill(event.j1_m, weight)    
            self.h0_pt_m.Fill(event.j0_pt, weight)
            self.h1_pt_m.Fill(event.j1_pt, weight)    
            self.h0_eta.Fill(event.j0_eta, weight) 
            self.h1_eta.Fill(event.j1_eta, weight)     
            self.h0_phi.Fill(event.j0_phi, weight)    
            self.h1_phi.Fill(event.j1_phi, weight)   
            self.h0_trk_dr.Fill(helpers.dR(event.j0_trk0_eta, event.j0_trk0_phi, event.j0_trk1_eta, event.j0_trk1_phi), weight) 
            self.h1_trk_dr.Fill(helpers.dR(event.j1_trk0_eta, event.j1_trk0_phi, event.j1_trk1_eta, event.j1_trk1_phi), weight) 
            self.h0_ntrk.Fill(event.j0_nTrk, weight)    
            self.h1_ntrk.Fill(event.j1_nTrk, weight)    
            self.h0_trks_pt.Fill(event.j0_trk0_pt, weight)
            self.h0_trks_pt.Fill(event.j0_trk1_pt, weight)
            self.h1_trks_pt.Fill(event.j1_trk0_pt, weight)
            self.h1_trks_pt.Fill(event.j1_trk1_pt, weight)
            self.trks_pt.Fill(event.j0_trk0_pt, weight)
            self.trks_pt.Fill(event.j0_trk1_pt, weight)
            self.trks_pt.Fill(event.j1_trk0_pt, weight)
            self.trks_pt.Fill(event.j1_trk1_pt, weight)
            self.h0_trkpt_diff.Fill((event.j0_trk0_pt - event.j0_trk1_pt), weight)
            self.h1_trkpt_diff.Fill((event.j1_trk0_pt - event.j1_trk1_pt), weight)

    def Write(self, outputroot):
        outputroot.cd(self.region)
        #write all the histograms
        self.mHH_l.Write()     
        self.mHH_pole.Write()     
        self.h0_m.Write()      
        self.h1_m.Write()  
        self.h0_trk0_pt.Write()
        self.h1_trk0_pt.Write()
        self.h0_trk1_pt.Write()
        self.h1_trk1_pt.Write()
        self.Rhh.Write()
        if self.fullhist:
            self.mH0H1.Write() 
            self.h_deta.Write()    
            self.h_dphi.Write()    
            self.h_dr.Write()  
            self.h_pt_assy.Write()   
            self.h0_m_s.Write()   
            self.h1_m_s.Write()  
            self.h0_pt_m.Write()    
            self.h1_pt_m.Write()    
            self.h0_eta.Write()    
            self.h1_eta.Write()   
            self.h0_phi.Write()    
            self.h1_phi.Write()    
            self.h0_trk_dr.Write() 
            self.h1_trk_dr.Write() 
            self.h0_ntrk.Write()   
            self.h1_ntrk.Write()   
            self.h0_trks_pt.Write() 
            self.h1_trks_pt.Write()   
            self.trks_pt.Write()
            self.h0_trkpt_diff.Write()
            self.h1_trkpt_diff.Write()



#split things in to mass regions, also possible systematic variation
class massregionHists:
    #these are the regions and cuts;
    def __init__(self, region, outputroot, reweight=False):
        #define control/sb variations
        self.RegionDict = {
            "Incl"     : "True",
            "Signal"   : SR_cut,
            "Control"  : CR_cut,
            "Sideband" : SB_cut,
            "ZZ"       : "not " + SR_cut  + " and " + "event.Xzz < 2.1",
        }
        self.regionlst = []
        #for specific studies; for systemtaics
        for name, cut in self.RegionDict.items():
            tempdic = {}
            tempdic["name"] = name
            tempdic["histname"] = region + "_" + name
            tempdic["eventHists"] = eventHists(tempdic["histname"], outputroot, reweight)
            tempdic["evencondition"] = compiler.compile(cut, '<string>', 'eval')
            self.regionlst.append(tempdic)

    def Fill(self, event, weight=-1):
        #for specific studies!
        for tempdic in self.regionlst:
            if eval(tempdic["evencondition"]):
                tempdic["eventHists"].Fill(event, weight)

    def Write(self, outputroot):
        #for specific studies!
        for tempdic in self.regionlst:
            tempdic["eventHists"].Write(outputroot)


#reweighting is done here: what a genius design
class trkregionHists:
    def __init__(self, region, outputroot, reweight=False):
        self.reweight = reweight
        self.Trk0  = massregionHists(region, outputroot, reweight)
        #self.Trk1  = massregionHists(region + "_" + "1Trk", outputroot)
        #self.Trk2  = massregionHists(region + "_" + "2Trk", outputroot)
        self.Trk2s = massregionHists(region + "_" + "2Trk_split", outputroot, reweight)
        self.Trk3  = massregionHists(region + "_" + "3Trk", outputroot, reweight)
        self.Trk4  = massregionHists(region + "_" + "4Trk", outputroot, reweight)
        if self.reweight:
            self.Trk2s_dic, self.Trk3_dic, self.Trk4_dic = get_parameter(filename=ops.reweight)

    def Fill(self, event, weight=-1):
        self.Trk0.Fill(event, weight)
        # if event.j0_nTrk >= 1 or event.j1_nTrk >= 1:
        #     self.Trk1.Fill(event)
        # if event.j0_nTrk >= 2 or event.j1_nTrk >= 2:
        #     self.Trk2.Fill(event)
        if event.j0_nTrk >= 1 and event.j1_nTrk >= 1:
            if self.reweight:
                weight = event.weight * calc_reweight(self.Trk2s_dic, event)
            self.Trk2s.Fill(event, weight)
        if (event.j0_nTrk >= 1 and event.j1_nTrk >= 2) or (event.j0_nTrk >= 2 and event.j1_nTrk >= 1):
            if self.reweight:
                weight = event.weight * calc_reweight(self.Trk3_dic, event)
            self.Trk3.Fill(event, weight)
        if event.j0_nTrk >= 2 and event.j1_nTrk >= 2:
            if self.reweight:
                weight = event.weight * calc_reweight(self.Trk4_dic, event)
            self.Trk4.Fill(event, weight)

    def Write(self, outputroot):
        self.Trk0.Write(outputroot)
        #self.Trk1.Write(outputroot)
        #self.Trk2.Write(outputroot)
        self.Trk2s.Write(outputroot)
        self.Trk3.Write(outputroot)
        self.Trk4.Write(outputroot)

class regionHists:
    def __init__(self, outputroot, reweight):
        self.NoTag  = trkregionHists("NoTag", outputroot, reweight)
        self.OneTag = massregionHists("OneTag", outputroot) #if test 1 tag fit, needs to enable this
        self.TwoTag = massregionHists("TwoTag", outputroot)
        self.TwoTag_split = massregionHists("TwoTag_split", outputroot)
        self.ThreeTag = massregionHists("ThreeTag", outputroot)
        self.FourTag = massregionHists("FourTag", outputroot)

    def Fill(self, event):
        if event.j0_nb + event.j1_nb == 4:
            self.FourTag.Fill(event)
        elif event.j0_nb + event.j1_nb == 3:
            self.ThreeTag.Fill(event)
        elif event.j0_nb == 1 and event.j1_nb == 1:
            self.TwoTag_split.Fill(event)
        elif event.j0_nb + event.j1_nb == 2:
            self.TwoTag.Fill(event)
        elif event.j0_nb + event.j1_nb == 1:
            self.OneTag.Fill(event)
        elif event.j0_nb + event.j1_nb == 0:
            self.NoTag.Fill(event, event.weight)

    def Write(self, outputroot):
        self.NoTag.Write(outputroot)
        self.OneTag.Write(outputroot)
        self.TwoTag.Write(outputroot)
        self.TwoTag_split.Write(outputroot)
        self.ThreeTag.Write(outputroot)
        self.FourTag.Write(outputroot)

def pass_dRcut(t):
    # first check if all the jets are valid
    for j_pt in [t.j0_trk0_pt, t.j0_trk1_pt, t.j1_trk0_pt, t.j1_trk1_pt]:
	if j_pt < 10:
	    return True

    j0_deltaR = helpers.dR(t.j0_trk0_eta, t.j0_trk0_phi, t.j0_trk1_eta, t.j0_trk1_phi)
    j1_deltaR = helpers.dR(t.j1_trk0_eta, t.j1_trk0_phi, t.j1_trk1_eta, t.j1_trk1_phi)
    mass = t.mHH
    j0pt = t.j0_pt
    j1pt = t.j1_pt

    def c0(pt, dR):
	if pt > 1000:
	    return True
	else:
	    return abs(270.0/pt - dR) < 0.125
    def c1(pt, dR):
	if pt > 1000:
	    return True
	else:
	    return abs(250.0/pt - dR) < 0.125
    
    chk0 = chk1 = True

    return ( (c0(j0pt,j0_deltaR) or not chk0) and (c1(j1pt, j1_deltaR) or not chk1))

def analysis(inputconfig, DEBUG=False):
    predR = 0
    postdR = 0
    inputfile = inputconfig["inputfile"]
    inputroot = inputconfig["inputroot"]
    outputroot = inputconfig["outputroot"]

    outroot = ROOT.TFile.Open(outputpath + inputfile + "/" + outputroot, "recreate")
    AllHists = regionHists(outroot, turnon_reweight)
    #read the input file
    f = ROOT.TFile(inputpath + inputfile + "/" + inputroot, "read")
    #load the target tree
    t = ROOT.TinyTree(f.Get("TinyTree"))
    #save the cutflow histograms
    hist_list = ["CutFlowWeight", "CutFlowNoWeight", "h_leadHCand_pT_pre_trig", "h_leadHCand_pT_aft_trig"]
    for hist in hist_list:
        temp_hist = f.Get(hist).Clone()
        outroot.cd()
        temp_hist.Write()
        del(temp_hist)
    #start looping through events
    N = t.fChain.GetEntries()
    for i in range(N):
    # get the next tree in the chain and verify
        # if DEBUG & (i > 100000):
        #     break
        if i % 20000 == 0:
            helpers.drawProgressBar(i/(N*1.0))

        t.fChain.GetEntry(i)
        #print t.Xzz
        #place a cut if necessary
        if ((t.j0_pt) < 450.0):
            continue

	predR = predR + 1
	# dR cut
	if not pass_dRcut(t):
	    continue
	postdR = postdR + 1

        ##place a cut if necessary
        ##if ((t.mHH) < 1000.0):
             ##continue
        AllHists.Fill(t)

    #write all the output
    AllHists.Write(outroot)
    print "DONE with the " + inputfile,  outputroot  + " analysis!", N, " events!"
    #close the input file;
    del(t)
    outroot.Close()
    del(AllHists)

    print("PRE DR CUT: %d\n POST DR CUT: %d\n" % (predR, postdR))


#pack the input into a configuration dictionary
def pack_input(inputfile, inputsplit=-1):
    dic = {}
    dic["inputfile"] = inputfile
    dic["inputroot"] = "hist-MiniNTuple" + ("_" + str(inputsplit) if inputsplit  >= 0 else "") + ".root"
    dic["outputroot"] = "hist-MiniNTuple" + ("_" + str(inputsplit) if inputsplit >= 0 else "") + ".root"
    #make sure the output directory exist here; resolve the conflicts
    helpers.checkpath(outputpath + inputfile)
    return dic

def main():
    print "Start TinyTree--->Plots!"
    start_time = time.time()
    global DEBUG
    DEBUG = False
    global ops
    ops = options()
    global inputpath
    inputpath = CONF.inputpath + ops.inputdir + "/"
    #for reweight options
    global turnon_reweight #reweight or not
    turnon_reweight = False
    if ops.reweight is not None:
        turnon_reweight = True
    #set the output directory of all the hist-files
    global outputpath
    outputpath = CONF.outputpath + ops.outputdir + ("_" + ops.dosyst if (ops.dosyst is not None) else "") +  "/"
    helpers.checkpath(outputpath)

    ##setup control region size, and sideband region size
    global Syst_cut
    CR_size = 35.8
    SB_size = 63
    Syst_cut = {
        "SR"         : "event.Xhh < 1.6",
        "CR"         : "event.Rhh < %s" % str(CR_size) ,
        "SB"         : "event.Rhh < %s" % str(SB_size) ,
        "CR_High"    : GetExp(RhhCenterX=124.+5, RhhCenterY=115.+5, RhhCut=CR_size),
        "CR_Low"     : GetExp(RhhCenterX=124.-5, RhhCenterY=115.-5, RhhCut=CR_size),
        "CR_Small"   : "event.Xhh > 2.0 and event.Rhh < %s" % str(CR_size) ,
        "SB_High"    : GetExp(RhhCenterX=124.+5, RhhCenterY=115.+5, RhhCut=SB_size),
        "SB_Low"     : GetExp(RhhCenterX=124.-5, RhhCenterY=115.-5, RhhCut=SB_size),
        "SB_Large"   : "event.Rhh < %s" % str(SB_size + 5) ,
        "SB_Small"   : "event.Rhh < %s" % str(SB_size - 5) ,
        }
    global SR_cut
    SR_cut = Syst_cut["SR"]
    global CR_cut
    CR_cut = "not " + Syst_cut["SR"] + " and " + Syst_cut["CR"]
    global SB_cut
    SB_cut = "not " + Syst_cut["CR"] + " and " + Syst_cut["SB"]
    if ops.dosyst is not None:
        if "CR" in ops.dosyst:
            CR_cut = "not " + Syst_cut["SR"] + " and " + Syst_cut[ops.dosyst]
            if "Small" in ops.dosyst: #sepecial treatment for this asshole
                SB_cut = "%s < event.Rhh < %s" % (str(CR_size), str(SB_size))
        elif "SB" in ops.dosyst:
            SB_cut = "not " + Syst_cut["CR"] + " and " + Syst_cut[ops.dosyst]

    ##for testing
    if (DEBUG):
        analysis(pack_input("zjets_test"))
        print("--- %s seconds ---" % (time.time() - start_time))
        return

    print "OUTPUTDIR: " + outputpath

    #real job; full chain 2 mins...just data is 50 seconds
    nsplit = 14
    split_list = ["data_test", "ttbar_comb_test"] #["data_test", "ttbar_comb_test", "signal_QCD"]
    inputtasks = []
    for split_file in split_list:
        for i in range(nsplit):
            inputtasks.append(pack_input(split_file, inputsplit=i))    
    inputtasks.append(pack_input("zjets_test"))
    for i, mass in enumerate(CONF.mass_lst):
        #do not reweight signal samples; create links to the original files instead
        if not turnon_reweight:
            inputtasks.append(pack_input("signal_G_hh_c10_M" + str(mass)))
        else:#if reweight, creat the folders and the links to the files
            print "creating links of signal samples", "signal_G_hh_c10_M" + str(mass)
            helpers.checkpath(outputpath + "signal_G_hh_c10_M" + str(mass))
            #this is a really bad practice and temp fix now!
            ori_link = inputpath.replace("F_c10", "f_c10") + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root"
            dst_link = outputpath + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root"
            if os.path.islink(dst_link):
                os.unlink(dst_link)
            os.symlink(ori_link, dst_link)
    ##if reweight, reweight everything
    # #parallel compute!
    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool  = mp.Pool(npool)
    pool.map(analysis, inputtasks)
    
    #all the other extra set of MCs
    for split_file in split_list:
        targetpath = outputpath + split_file + "/"
        targetfiles = []
        for i in range(nsplit):
            targetfiles += glob.glob(targetpath + ("hist-MiniNTuple_%s"% str(i)) + ".root")
        haddcommand = ["hadd", "-f", targetpath + "hist-MiniNTuple" + ".root"]
        haddcommand += targetfiles
        #print haddcommand
        subprocess.call(haddcommand)
        #clean up the sub process outputs
        for i in range(nsplit):
            hrmcommand = ["rm"]
            hrmcommand += glob.glob(targetpath + ("hist-MiniNTuple_%s"% str(i)) + ".root")
            subprocess.call(hrmcommand)


    #analysis("data_test") #2 mins! 4 mins with expanded...
    #analysis("signal_QCD") #2 mins! 10 mins...
    print("--- %s seconds ---" % (time.time() - start_time))
    print "Finish!"


#def clearbranches():
if __name__ == "__main__":
    main()
