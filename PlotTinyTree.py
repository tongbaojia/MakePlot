###Tony: improve to load branches for faster processing
###Performance is not garanteened. The way to register hists are slow
###For a quick on the fly anaysis, great.
###For a more proper anlaysis, do the c++ standard way please
import ROOT, rootlogon, helpers
import config as CONF
import time, os, subprocess, glob, argparse
#for parallel processing!
import multiprocessing as mp
#import tree configuration
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('TinyTree.C')

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iter", default=0)
    return parser.parse_args()

#returns a dictionary of weights
def get_reweight(folder, filename):
    reweightfolder = CONF.outputpath + folder + "/" + "Reweight/"
    f_reweight = open(reweightfolder + filename, "r")
    par_weight = {}
    for line in f_reweight:
        lstline =  line.split()
        #print lstline
        if "par0" in line:
            par_weight["par0"] = float(lstline[1])
        if "par1" in line:
            par_weight["par1"] = float(lstline[1])
        if "par2" in line:
            par_weight["par2"] = float(lstline[1])
        if "par3" in line:
            par_weight["par3"] = float(lstline[1])
    #print par_weight
    f_reweight.close()
    return par_weight

#calculate the weight based on the input dictionary as the instruction
def calc_reweight(dic, event):
    totalweight = 1
    maxscale = 0.5 #this means the maximum correction is this for each reweighting
    for x, v in dic.iteritems():
        tempweight = 1
        tempweight = v["par0"] + v["par1"] * eval(x) + v["par2"] * eval(x) ** 2 + v["par3"] * eval(x) ** 3
        if tempweight < maxscale:
            tempweight = maxscale
        if tempweight > 1 + maxscale:
            tempweight = 1 + maxscale
        totalweight *= tempweight
    #also contrain the totalweight
    if totalweight < maxscale:
        totalweight = maxscale
    if totalweight > 1 + maxscale:
        totalweight = 1 + maxscale
    return totalweight

class eventHists:

    fullhist = True # will take 3 minutes to generate all histograms; 3 times more time...

    def __init__(self, region, outputroot, reweight=False):
        outputroot.cd()
        outputroot.mkdir(region)
        outputroot.cd(region)
        self.region = region
        self.reweight = reweight
        #add in all the histograms
        self.mHH_l        = ROOT.TH1F("mHH_l",              ";mHH [GeV]",        76,  200, 4000)
        self.mHH_pole     = ROOT.TH1F("mHH_pole",           ";mHH [GeV]",        76,  200, 4000)
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
            self.h0_m_s       = ROOT.TH1F("leadHCand_Mass_s",   ";Mass [GeV]",       40,   70,  170)
            self.h1_m_s       = ROOT.TH1F("sublHCand_Mass_s",   ";Mass [GeV]",       40,   70,  170)
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
            self.h0_trkpt_diff= ROOT.TH1F("leadHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 22, -0.05, 1.05)
            self.h1_trkpt_diff= ROOT.TH1F("sublHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 22, -0.05, 1.05)
            self.mH0H1        = ROOT.TH2F("mH0H1",              ";mH1 [GeV]; mH2 [GeV];", 50,  50,  300,  50,  50,  300)

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
            self.h0_trkpt_diff.Fill((event.j0_trk0_pt - event.j0_trk1_pt)/(event.j0_trk0_pt + event.j0_trk1_pt), weight)
            self.h1_trkpt_diff.Fill((event.j1_trk0_pt - event.j1_trk1_pt)/(event.j1_trk0_pt + event.j1_trk1_pt), weight)

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
            self.h0_trkpt_diff.Write()
            self.h1_trkpt_diff.Write()

class massregionHists:
    def __init__(self, region, outputroot, reweight=False):
        self.Incl = eventHists(region + "_" + "Incl", outputroot)
        self.Sideband = eventHists(region + "_" + "Sideband", outputroot, reweight)
        self.Control = eventHists(region + "_" + "Control", outputroot, reweight)
        self.Signal = eventHists(region + "_" + "Signal", outputroot, reweight)
        self.ZZ = eventHists(region + "_" + "ZZ", outputroot, reweight)
        #for specific studies!
        self.studylst = []
        # for i, cut in enumerate(range(20, 160, 20)):
        #     for j, masssplit in enumerate([" and event.j0_m > 125 and event.j1_m > 114",\
        #     " and event.j0_m < 125 and event.j1_m > 114",\
        #     " and event.j0_m < 125 and event.j1_m < 114",\
        #     " and event.j0_m > 125 and event.j1_m < 114"]):
        #         tempdic = {}
        #         tempdic["histname"] = region + "_" + "r" + str(j) + "_" + "Rhh" + str(cut)
        #         tempdic["eventHists"] = eventHists(tempdic["histname"], outputroot)
        #         tempdic["evencondition"] = "event.Xhh > 1.6 and event.Rhh < " + str(cut) + " and event.Rhh > " + str(cut - 20) + masssplit
        #         self.studylst.append(tempdic)

    def Fill(self, event, weight=-1):
        self.Incl.Fill(event)
        if event.Xhh < 1.6:
            self.Signal.Fill(event, weight)
        elif event.Rhh < 35.8:
            self.Control.Fill(event, weight)
        elif event.Rhh < 63:
            self.Sideband.Fill(event, weight)
        if event.Xhh > 1.6 and event.Xzz < 2.1:
            self.ZZ.Fill(event, weight)
        #for specific studies!
        for tempdic in self.studylst:
            if eval(tempdic["evencondition"]):
                tempdic["eventHists"].Fill(event, weight)


    def Write(self, outputroot):
        self.Incl.Write(outputroot)
        self.Sideband.Write(outputroot)
        self.Control.Write(outputroot)
        self.Signal.Write(outputroot)
        self.ZZ.Write(outputroot)
        #for specific studies!
        for tempdic in self.studylst:
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
            self.Trk2s_dic = {}
            self.Trk3_dic = {}
            self.Trk4_dic = {}
            #setup all the reweighting parameters here
            tempname_lead_pt = "(event.j0_pt)"
            tempname_subl_pt = "(event.j1_pt)"
            tempname_lead_trk0_pt = "(event.j0_trk0_pt)"
            tempname_subl_trk0_pt = "(event.j1_trk0_pt)"
            tempname_lead_trk1_pt = "(event.j0_trk1_pt)"
            tempname_subl_trk1_pt = "(event.j1_trk1_pt)"
            tempname_lead_trkasy = "(event.j0_trk0_pt - event.j0_trk1_pt)/(event.j0_trk0_pt + event.j0_trk1_pt)"
            tempname_subl_trkasy = "(event.j1_trk0_pt - event.j1_trk1_pt)/(event.j1_trk0_pt + event.j1_trk1_pt)"
            #for 2tag split region
            #self.Trk2s_dic["(event.Rhh)"] = get_reweight("reweight_0", "r0_TwoTag_split_Sideband_Rhh.txt")
            self.Trk2s_dic[tempname_lead_trk0_pt] = get_reweight("reweight_0", "r0_TwoTag_split_Sideband_leadHCand_trk0_Pt.txt")
            self.Trk2s_dic[tempname_subl_trk0_pt] = get_reweight("reweight_0", "r0_TwoTag_split_Sideband_sublHCand_trk0_Pt.txt")
            self.Trk2s_dic[tempname_lead_trk1_pt] = get_reweight("reweight_1", "r0_TwoTag_split_Sideband_leadHCand_trk1_Pt.txt")
            self.Trk2s_dic[tempname_subl_trk1_pt] = get_reweight("reweight_1", "r0_TwoTag_split_Sideband_sublHCand_trk1_Pt.txt")
            self.Trk2s_dic[tempname_lead_pt] = get_reweight("reweight_2", "r0_TwoTag_split_Sideband_leadHCand_Pt_m.txt")
            self.Trk2s_dic[tempname_subl_pt] = get_reweight("reweight_2", "r0_TwoTag_split_Sideband_sublHCand_Pt_m.txt")
            #self.Trk2s_dic[tempname_lead_trkasy] = get_reweight("reweight_0", "r0_TwoTag_split_Sideband_leadHCand_trk_pt_diff_frac.txt")
            #self.Trk2s_dic[tempname_subl_trkasy] = get_reweight("reweight_0", "r0_TwoTag_split_Sideband_sublHCand_trk_pt_diff_frac.txt")
            #for 4tag region
            #self.Trk3_dic["(event.Rhh)"] = get_reweight("reweight_0", "r0_ThreeTag_Sideband_Rhh.txt")
            self.Trk3_dic[tempname_lead_trk0_pt] = get_reweight("reweight_0", "r0_ThreeTag_Sideband_leadHCand_trk0_Pt.txt")
            self.Trk3_dic[tempname_subl_trk0_pt] = get_reweight("reweight_0", "r0_ThreeTag_Sideband_sublHCand_trk0_Pt.txt")
            self.Trk3_dic[tempname_lead_trk1_pt] = get_reweight("reweight_1", "r0_ThreeTag_Sideband_leadHCand_trk1_Pt.txt")
            self.Trk3_dic[tempname_subl_trk1_pt] = get_reweight("reweight_1", "r0_ThreeTag_Sideband_sublHCand_trk1_Pt.txt")
            self.Trk3_dic[tempname_lead_pt] = get_reweight("reweight_2", "r0_ThreeTag_Sideband_leadHCand_Pt_m.txt")
            self.Trk3_dic[tempname_subl_pt] = get_reweight("reweight_2", "r0_ThreeTag_Sideband_sublHCand_Pt_m.txt")
            #self.Trk3_dic[tempname_lead_trkasy] = get_reweight("reweight_0", "r0_ThreeTag_Sideband_leadHCand_trk_pt_diff_frac.txt")
            #self.Trk3_dic[tempname_subl_trkasy] = get_reweight("reweight_0", "r0_ThreeTag_Sideband_sublHCand_trk_pt_diff_frac.txt")
            #for 4tag region
            #self.Trk3_dic["(event.Rhh)"] = get_reweight("reweight_0", "r0_FourTag_Sideband_Rhh.txt")
            self.Trk4_dic[tempname_lead_trk0_pt] = get_reweight("reweight_0", "r0_FourTag_Sideband_leadHCand_trk0_Pt.txt")
            self.Trk4_dic[tempname_subl_trk0_pt] = get_reweight("reweight_0", "r0_FourTag_Sideband_sublHCand_trk0_Pt.txt")
            self.Trk4_dic[tempname_lead_trk1_pt] = get_reweight("reweight_1", "r0_FourTag_Sideband_leadHCand_trk1_Pt.txt")
            self.Trk4_dic[tempname_subl_trk1_pt] = get_reweight("reweight_1", "r0_FourTag_Sideband_sublHCand_trk1_Pt.txt")
            self.Trk4_dic[tempname_lead_pt] = get_reweight("reweight_2", "r0_FourTag_Sideband_leadHCand_Pt_m.txt")
            self.Trk4_dic[tempname_subl_pt] = get_reweight("reweight_2", "r0_FourTag_Sideband_sublHCand_Pt_m.txt")
            #self.Trk4_dic[tempname_lead_trkasy] = get_reweight("reweight_0", "r0_FourTag_Sideband_leadHCand_trk_pt_diff_frac.txt")
            #self.Trk4_dic[tempname_subl_trkasy] = get_reweight("reweight_0", "r0_FourTag_Sideband_sublHCand_trk_pt_diff_frac.txt")
            #print self.Trk2s_dic, self.Trk3_dic, self.Trk4_dic

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


def analysis(inputconfig, DEBUG=False):
    inputfile = inputconfig["inputfile"]
    inputroot = inputconfig["inputroot"]
    outputroot = inputconfig["outputroot"]
    DEBUG = inputconfig["DEBUG"]

    helpers.checkpath(outputpath + inputfile)
    outroot = ROOT.TFile.Open(outputpath + inputfile + "/" + outputroot, "recreate")
    AllHists = regionHists(outroot, turnon_reweight)
    #read the input file
    f = ROOT.TFile(inputpath + inputfile + "/" + inputroot, "read")
    #load the target tree
    t = ROOT.TinyTree(f.Get("TinyTree"))
    #save the cutflow histograms
    cutflow_weight = f.Get("CutFlowWeight").Clone()
    cutflow = f.Get("CutFlowNoWeight").Clone()
    outroot.cd()
    cutflow_weight.Write()
    cutflow.Write()
    #start looping through events
    N = t.fChain.GetEntries()
    for i in range(N):
    # get the next tree in the chain and verify
        if DEBUG & (i > 100000):
            break
        if i %20000 == 0:
            helpers.drawProgressBar(i/(N*1.0))
            #print i, " events done!"
        t.fChain.GetEntry(i)
        #print t.Xzz
        #place a cut if necessary
        if ((t.j0_pt) < 450.0):
            continue
        AllHists.Fill(t)

    #write all the output
    AllHists.Write(outroot)
    print "DONE with the " + inputfile,  outputroot  + " analysis!"
    #close the input file;
    del(t)
    outroot.Close()
    del(AllHists)
    del(cutflow_weight)
    del(cutflow)

#pack the input into a configuration dictionary
def pack_input(inputfile, inputsplit=-1):
    dic = {}
    dic["inputfile"] = inputfile
    dic["inputroot"] = "hist-MiniNTuple" + ("_" + str(inputsplit) if inputsplit  >= 0 else "") + ".root"
    dic["outputroot"] = "hist-MiniNTuple" + ("_" + str(inputsplit) if inputsplit >= 0 else "") + ".root"
    dic["DEBUG"] = False
    return dic

def main():
    start_time = time.time()
    ops = options()

    global inputpath
    inputpath = CONF.inputpath + "TEST-16/"
    global iter_reweight #iterative reweight or not
    iter_reweight = int(ops.iter)
    global turnon_reweight #reweight or not
    turnon_reweight = False
    if iter_reweight > 0:
        turnon_reweight = True
    global outputpath
    outputpath = CONF.outputpath + "b77_c00-16/"
    #outputpath = CONF.outputpath + "reweight_" + str(iter_reweight) + "/"
    helpers.checkpath(outputpath)
    #for testing
    #analysis(pack_input("zjets_test"))

    #real job; full chain 2 mins...just data is 50 seconds
    nsplit = 14
    split_list = ["data_test", "ttbar_comb_test"] #["data_test", "ttbar_comb_test", "signal_QCD"]
    inputtasks = []
    for split_file in split_list:
        for i in range(nsplit):
            inputtasks.append(pack_input(split_file, inputsplit=i))    
    inputtasks.append(pack_input("zjets_test"))
    for i, mass in enumerate(CONF.mass_lst):
        inputtasks.append(pack_input("signal_G_hh_c10_M" + str(mass)))
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


    #analysis("data_test") #2 mins! 4 mins with expanded...
    #analysis("signal_QCD") #2 mins! 10 mins...
    print("--- %s seconds ---" % (time.time() - start_time))
    print "Finish!"

#def clearbranches():
if __name__ == "__main__":
    main()
