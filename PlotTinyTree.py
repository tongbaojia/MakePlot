###Tony: improve to load branches for faster processing
###Performance is not garanteened. The way to register hists are slow
###For a quick on the fly anaysis, great.
###For a more proper anlaysis, do the c++ standard way please
import ROOT, helpers
import config as CONF
import time, os, subprocess, glob, argparse, compiler, gc
#for parallel processing!
import multiprocessing as mp
#import tree configuration
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('TinyTree.C')

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",  default="TEST")
    parser.add_argument("--outputdir", default="b70")
    parser.add_argument("--dosyst",    default=None)
    parser.add_argument("--reweight",  default=None)
    parser.add_argument("--iter",      default=0)
    parser.add_argument("--MV2",       default=0.6455) #0.3706, 0.6455
    parser.add_argument("--CR",        default=33) ##default CR size is 33
    parser.add_argument("--SB",        default=58) ##default SB size is 58
    parser.add_argument("--SBshift",   default=10) ##default SBshift size is 10
    parser.add_argument("--resveto",   action='store_true')
    parser.add_argument("--Xhh",       default=CONF.doallsig) #do 2HDM and c20 samples if necessary
    parser.add_argument("--dijet",     action='store_true') #do Dijet samples if necessary
    parser.add_argument("--debug",     action='store_true')

    return parser.parse_args()

#returns a dictionary of weights
def get_parameter(filename="test.txt", region=""):
    #the input file need to be the following format; change to lists of tuples
    #iteration; Ntrk(option); parameter; inputfolder; parameterfile; (evaluation condition)
    def get_info(lstline):
        if len(lstline) > 5: ##return what to reweight, reweight dictionary, reweight condition
            return compiler.compile(lstline[2], '<string>', 'eval'), get_reweight(lstline[0], lstline[3], lstline[4]), compiler.compile(lstline[5], '<string>', 'eval')
        else:##return what to reweight, reweight dictionary
            return compiler.compile(lstline[2], '<string>', 'eval'), get_reweight(lstline[0], lstline[3], lstline[4]), "True"

    f_reweight = open("script/" + filename + ".txt", "r")
    TagDic = []
    for line in f_reweight:
        if "#" in line:
            continue
        lstline =  line.split()
        #check which iteration it is; don't go beyond! start with 1
        #print lstline[0], ops.iter
        if int(lstline[0]) > int(ops.iter):
            continue
        #now proceed normally
        if "2bs" in lstline[1]:
            if "2Trk" in region:
                TagDic.append(get_info(lstline))
            if "split_lead" in lstline[3] and "split_lead" in region:
                TagDic.append(get_info(lstline))
            elif "split_subl" in lstline[3] and "split_subl" in region:
                TagDic.append(get_info(lstline))
        if "3b" in lstline[1]:
            if "3Trk" in region:
                TagDic.append(get_info(lstline))
            if "split_lead" in lstline[3] and "split_lead" in region:
                TagDic.append(get_info(lstline))
            elif "split_subl" in lstline[3] and "split_subl" in region:
                TagDic.append(get_info(lstline))
        if "4b" in lstline[1]:
            if "4Trk" in region:
                TagDic.append(get_info(lstline))
            if "split_lead" in lstline[3] and "split_lead" in region:
                TagDic.append(get_info(lstline))
            elif "split_subl" in lstline[3] and "split_subl" in region:
                TagDic.append(get_info(lstline))
    #print par_weight
    f_reweight.close()
    #print TagDic
    return TagDic

#returns a dictionary of weights
def get_reweight(curriter, folder, filename, spline=True):
    reweightfolder = CONF.outputpath + folder + "/" + "Reweight/"
    f_reweight = open(reweightfolder + filename, "r")
    par_weight = {}
    for line in f_reweight:
        lstline =  line.split() #default split by space
        #print lstline
        if "par0" in line:
            par_weight["par0"] = float(lstline[1]) if abs(float(lstline[1])) > 1E-13 else 0
        elif "par1" in line:
            par_weight["par1"] = float(lstline[1]) if abs(float(lstline[1])) > 1E-13 else 0
        elif "par2" in line:
            par_weight["par2"] = float(lstline[1]) if abs(float(lstline[1])) > 1E-13 else 0
        elif "par3" in line:
            par_weight["par3"] = float(lstline[1]) if abs(float(lstline[1])) > 1E-13 else 0
        elif "low" in line:
            par_weight["low"]  = float(lstline[1]) if abs(float(lstline[1])) > 1E-13 else 0
        elif "high" in line:
            par_weight["high"] = float(lstline[1]) if abs(float(lstline[1])) > 1E-13 else 0
        #for spline weights
        par_weight["name"]     = filename.replace("r" + curriter + "_", "rs" + curriter + "_").replace("txt", "cxx")
    #print par_weight
    f_reweight.close()
    #load spline function
    if spline:
        ROOT.gROOT.LoadMacro(reweightfolder + par_weight["name"])
    return par_weight

#calculate the weight based on the input dictionary as the instruction
def calc_reweight(dic, event, poly=False, spline=True):
    totalweight = 1
    maxscale = 5.0 #this means the maximum correction is this for each reweighting; used to be 1.5
    minscale = 0.1 #this means the minimum correction is this for each reweighting; used to be 0.5
    for x, v, cond in dic:#this "dic" really is not a dic, but a tuple! #variable, weight, condition
        if not eval(cond): ##if doesn't pass the condition, do not apply the weight!
            continue
        value = eval(x)
        #outside fit range, do the end point value extrapolation
        if (v["low"] > value):
            value =  v["low"] 
        elif (v["high"] < value): 
            value =  v["high"]
        #start calculated reweight factor
        tempweight = 1
        if poly: #use polynomial fits
            tempweight = v["par0"] + v["par1"] * value + v["par2"] * value ** 2 + v["par3"] * value ** 3
        if spline: #use spline functions!
            tempweight = eval("ROOT." + v["name"].replace(".cxx", "(%d)" % value))
            #print "new: ", tempweight, "old: ", v["par0"] + v["par1"] * value + v["par2"] * value ** 2 + v["par3"] * value ** 3
        # if ((event.j0_nb==1)and(event.j1_nb==0)):
        #     print value, tempweight, x, v, cond
        #this protects each individual weight; tight this up a bit; used to be 0.8 and 1.2s
        if tempweight < 0.6:
            tempweight = 0.6
        elif tempweight > 1.6:
            tempweight = 1.6

        if ops.iter < 3: ##first several iterations, slow down the convergence
            totalweight *= (tempweight - 1) * 0.618 + 1 #reduce the correction to tune convergence; :)
        else: ##larger interations, just rock on
            totalweight *= tempweight
        #totalweight *= tempweight

    #print totalweight
    #also contrain the totalweight
    if totalweight < minscale:
        totalweight = minscale
        #print totalweight, tempweight
    elif totalweight > maxscale:
        totalweight = maxscale
    #print x, v, cond, totalweight
    return totalweight

#get Xhh and Rhh values; for variations's sake
def GetRhh(XhhCenterX=124., XhhCenterY=115., XhhCut=1.6, RhhCenterX=124., RhhCenterY=115., RhhCut=35.8):
    #XhhExp = "ROOT.TMath.Sqrt(ROOT.TMath.Power((event.j0_m - %s)/(0.1*event.j0_m), 2) + ROOT.TMath.Power((event.j1_m - %s)/(0.1*event.j1_m), 2)) < %s" % (XhhCenterX, XhhCenterY, XhhCut)
    RhhExp = "ROOT.TMath.Sqrt(ROOT.TMath.Power(event.j0_m - %s, 2) + ROOT.TMath.Power(event.j1_m - %s, 2)) < %s" % (RhhCenterX, RhhCenterY, RhhCut)
    return RhhExp

def GetXhh(XhhCenterX=124., XhhCenterY=115., XhhCut=1.6):
    #XhhExp = "(ROOT.TMath.Sqrt(ROOT.TMath.Power((event.j0_m - %s)/(0.085*event.j0_m), 2) + ROOT.TMath.Power((event.j1_m - %s)/(0.12*event.j1_m), 2)) < %s + (0 if (event.j0_pt < 900) else (event.j0_pt - 900)/900.0 * 0.4) )" % (XhhCenterX, XhhCenterY, XhhCut) ##with pT dependent cut
    #just pT dependent
    #XhhExp = "(ROOT.TMath.Sqrt(ROOT.TMath.Power((event.j0_m - %s)/(0.1*event.j0_m), 2) + ROOT.TMath.Power((event.j1_m - %s)/(0.1*event.j1_m), 2)) < %s + (0 if (event.j0_pt < 900) else (event.j0_pt - 900)/900.0 * 0.4) )" % (XhhCenterX, XhhCenterY, XhhCut) ##with pT dependent cut
    #just assymetric resolution
    #XhhExp = "(ROOT.TMath.Sqrt(ROOT.TMath.Power((event.j0_m - %s)/(0.085*event.j0_m), 2) + ROOT.TMath.Power((event.j1_m - %s)/(0.12*event.j1_m), 2)) < %s)" % (XhhCenterX, XhhCenterY, XhhCut)
    #old definition
    XhhExp = "(ROOT.TMath.Sqrt(ROOT.TMath.Power((event.j0_m - %s)/(0.1*event.j0_m), 2) + ROOT.TMath.Power((event.j1_m - %s)/(0.1*event.j1_m), 2)) < %s)" % (XhhCenterX, XhhCenterY, XhhCut)
    return XhhExp

class eventHists:
    # will take 3 minutes to generate all histograms; 3 times more time...
    def __init__(self, region, outputroot, reweight=False):
        outputroot.cd()
        outputroot.mkdir(region)
        outputroot.cd(region)
        self.fullhist = CONF.fullstudy #ops.dosyst is None ##option to turn it off
        self.region   = region
        self.reweight = reweight
        #add in all the histograms
        self.mHH_l        = ROOT.TH1F("mHH_l",              ";mHH [GeV]",        700,  0, 7000) #plot range changed for 7 TeV signals
        self.mHH_pole     = ROOT.TH1F("mHH_pole",           ";mHH [GeV]",        700,  0, 7000)
        self.h0_m         = ROOT.TH1F("leadHCand_Mass",     ";Mass [GeV]",       60,   0,  300)
        self.h1_m         = ROOT.TH1F("sublHCand_Mass",     ";Mass [GeV]",       60,   0,  300)
        self.h0_trk0_pt   = ROOT.TH1F("leadHCand_trk0_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
        self.h1_trk0_pt   = ROOT.TH1F("sublHCand_trk0_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
        self.h0_trk1_pt   = ROOT.TH1F("leadHCand_trk1_Pt",  ";p_{T} [GeV]",      80,  0,   400)
        self.h1_trk1_pt   = ROOT.TH1F("sublHCand_trk1_Pt",  ";p_{T} [GeV]",      80,  0,   400)
        self.h0_pt_m      = ROOT.TH1F("leadHCand_Pt_m",     ";p_{T} [GeV]",      300,   200,  3200)
        self.h1_pt_m      = ROOT.TH1F("sublHCand_Pt_m",     ";p_{T} [GeV]",      300,   200,  3200)
        self.mH0H1        = ROOT.TH2F("mH0H1",              ";m_{J}^{lead} [GeV]; m_{J}^{subl} [GeV];", 200,  50,  250,  200,  50,  250)

        if self.fullhist:
            self.h_deta       = ROOT.TH1F("hCandDeta",          "hCand #Delta#eta",  40,    0,  2.0)
            self.h_dphi       = ROOT.TH1F("hCandDphi",          "hCand #Delta#phi",  66, -3.3,  3.3)
            self.h_dr         = ROOT.TH1F("hCandDr",            "hCand #Deltar",     100,   0,    5)
            self.h_pt_assy    = ROOT.TH1F("hCand_Pt_assy",      ";hCand p_{T} assym",22, -0.05, 1.05)
            self.h0_m_s       = ROOT.TH1F("leadHCand_Mass_s",   ";Mass [GeV]",       14,   60,  200)
            self.h1_m_s       = ROOT.TH1F("sublHCand_Mass_s",   ";Mass [GeV]",       14,   60,  200)
            self.h0_eta       = ROOT.TH1F("leadHCand_Eta",      ";#Eta",             42, -2.1,  2.1)
            self.h1_eta       = ROOT.TH1F("sublHCand_Eta",      ";#Eta",             42, -2.1,  2.1)
            self.h0_phi       = ROOT.TH1F("leadHCand_Phi",      ";#Phi",             64, -3.2,  3.2)
            self.h1_phi       = ROOT.TH1F("sublHCand_Phi",      ";#Phi",             64, -3.2,  3.2)
            self.h0_trk_dr    = ROOT.TH1F("leadHCand_trk_dr",   ";trkjet #Deltar",   42, -0.1,    2)
            self.h1_trk_dr    = ROOT.TH1F("sublHCand_trk_dr",   ";trkjet #Deltar",   42, -0.1,    2)
            self.h0_ntrk      = ROOT.TH1F("leadHCand_ntrk",     "number of trkjet",  10,  -0.5, 9.5)
            self.h1_ntrk      = ROOT.TH1F("sublHCand_ntrk",     "number of trkjet",  10,  -0.5, 9.5)
            self.h0_trkpt_diff= ROOT.TH1F("leadHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 80,  0,   800)
            self.h1_trkpt_diff= ROOT.TH1F("sublHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 80,  0,   800)
            #self.h0_trks_pt   = ROOT.TH1F("leadHCand_trks_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
            #self.h1_trks_pt   = ROOT.TH1F("sublHCand_trks_Pt",  ";p_{T} [GeV]",      400,  0,   2000)
            self.h0_trk0_eta  = ROOT.TH1F("leadHCand_trk0_Eta", ";#eta",               50, -2.5,  2.5)
            self.h0_trk0_phi  = ROOT.TH1F("leadHCand_trk0_Phi", ";#phi",               64, -3.2,  3.2)
            self.h1_trk0_eta  = ROOT.TH1F("sublHCand_trk0_Eta", ";#eta",               50, -2.5,  2.5)
            self.h1_trk0_phi  = ROOT.TH1F("sublHCand_trk0_Phi", ";#phi",               64, -3.2,  3.2)
            self.Rhh          = ROOT.TH1F("Rhh",                ";Rhh",              100,  0,  200)
            #self.trks_pt      = ROOT.TH1F("trks_Pt",            ";p_{T} [GeV]",      400,  0,   2000)
            self.dRH0H1       = ROOT.TH2F("dRH0H1",             ";#Deltar_{trk}^{lead}; #Deltar_{trk}^{subl};", 50, 0.2,  1.2, 50, 0.2, 1.2)
            self.MV2          = ROOT.TH1F("MV2",                ";MV2",              110,  -1.1,  1.1)
            #self.trkfracH0H1  = ROOT.TH2F("trkfracH0H1",        ";H0:p_{T}^{Trk0}/(p_{T}^{Trk0} + p_{T}^{Trk1});H1:p_{T}^{Trk0}}/(p_{T}^{Trk0} + p_{T}^{Trk1});", 50, 0.5, 1.0, 50, 0.5, 1.0)
            #self.mHHdRH0      = ROOT.TH2F("mHHdRH0",            ";mHH [GeV]; #Deltar_{trk}^{lead};", 300, 500, 3500,  50, 0.2,  1.2)
            #self.MV2H0H1      = ROOT.TH2F("MV2H0H1",              ";MV2 sum H0;MV2 sum H1;", 400,  -2,  2,  400,  -2,  2)
            #self.MV2H0        = ROOT.TH2F("MV2H0",                ";MV2 H0, j0;MV2 H0, j1;", 400,  -2,  2,  400,  -2,  2)
            #self.MV2H1        = ROOT.TH2F("MV2H1",                ";MV2 H1, j0;MV2 H1, j1;", 400,  -2,  2,  400,  -2,  2)
        #save reweight weights
        if self.reweight:
            self.mHH_weight          = ROOT.TH2F("mHH_l_weight",             ";mHH [GeV]; reweight",        80,   0,    4000, 32, 0.3, 1.9)
            self.h0_trk0_pt_weight   = ROOT.TH2F("leadHCand_trk0_Pt_weight", ";p_{T} [GeV]; reweight",      100,  0,    2000, 32, 0.3, 1.9)
            self.h1_trk0_pt_weight   = ROOT.TH2F("sublHCand_trk0_Pt_weight", ";p_{T} [GeV]; reweight",      80,   0,     400, 32, 0.3, 1.9)
            self.h0_pt_m_weight      = ROOT.TH2F("leadHCand_Pt_m_weight",    ";p_{T} [GeV]; reweight",      100,  200,  2200, 32, 0.3, 1.9)

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
        self.h0_pt_m.Fill(event.j0_pt, weight)
        self.h1_pt_m.Fill(event.j1_pt, weight) 
        self.mH0H1.Fill(event.j0_m, event.j1_m, weight)

        if self.fullhist:
            self.h_deta.Fill(event.detaHH, weight)    
            self.h_dphi.Fill(event.dphiHH, weight)    
            self.h_dr.Fill(event.drHH, weight) 
            self.h_pt_assy.Fill((event.j0_pt - event.j1_pt)/(event.j0_pt + event.j1_pt), weight)
            self.h0_m_s.Fill(event.j0_m, weight)   
            self.h1_m_s.Fill(event.j1_m, weight)      
            self.h0_eta.Fill(event.j0_eta, weight) 
            self.h1_eta.Fill(event.j1_eta, weight)     
            self.h0_phi.Fill(event.j0_phi, weight)    
            self.h1_phi.Fill(event.j1_phi, weight)   
            self.h0_trk_dr.Fill(event.j0_trkdr, weight) 
            self.h1_trk_dr.Fill(event.j1_trkdr, weight) 
            self.h0_ntrk.Fill(event.j0_nTrk, weight)    
            self.h1_ntrk.Fill(event.j1_nTrk, weight)    
            #self.h0_trks_pt.Fill(event.j0_trk0_pt, weight)
            #self.h0_trks_pt.Fill(event.j0_trk1_pt, weight)
            #self.h1_trks_pt.Fill(event.j1_trk0_pt, weight)
            #self.h1_trks_pt.Fill(event.j1_trk1_pt, weight)
            #self.trks_pt.Fill(event.j0_trk0_pt, weight)
            #self.trks_pt.Fill(event.j0_trk1_pt, weight)
            #self.trks_pt.Fill(event.j1_trk0_pt, weight)
            #self.trks_pt.Fill(event.j1_trk1_pt, weight)
            self.h0_trk0_eta.Fill(event.j0_trk0_eta, weight)
            self.h0_trk0_phi.Fill(event.j0_trk0_phi, weight)
            self.h1_trk0_eta.Fill(event.j1_trk0_eta, weight)
            self.h1_trk0_phi.Fill(event.j1_trk0_phi, weight)
            self.Rhh.Fill(event.Rhh, weight) 
            self.h0_trkpt_diff.Fill((event.j0_trk0_pt - event.j0_trk1_pt), weight)
            self.h1_trkpt_diff.Fill((event.j1_trk0_pt - event.j1_trk1_pt), weight)
            self.dRH0H1.Fill(event.j0_trkdr, event.j1_trkdr, weight)
            self.MV2.Fill(event.j0_trk0_Mv2, weight)
            self.MV2.Fill(event.j0_trk1_Mv2, weight)
            self.MV2.Fill(event.j1_trk0_Mv2, weight)
            self.MV2.Fill(event.j1_trk1_Mv2, weight)
            #self.trkfracH0H1.Fill(event.j0_trk0_pt/(event.j0_trk0_pt + event.j0_trk1_pt), event.j1_trk0_pt/(event.j1_trk0_pt + event.j1_trk1_pt), weight)
            #self.mHHdRH0.Fill(event.mHH, event.j0_trkdr, weight)
            #self.MV2H0H1.Fill(event.j0_trk0_Mv2 + event.j0_trk1_Mv2, event.j1_trk0_Mv2 + event.j1_trk1_Mv2, weight)
            #self.MV2H0.Fill(event.j0_trk0_Mv2, event.j0_trk1_Mv2, weight)
            #self.MV2H1.Fill(event.j1_trk0_Mv2, event.j1_trk1_Mv2, weight)
        if self.reweight:
            self.mHH_weight.Fill(event.mHH, weight)
            self.h0_trk0_pt_weight.Fill(event.j0_trk0_pt, weight)
            self.h1_trk0_pt_weight.Fill(event.j1_trk0_pt, weight)
            self.h0_pt_m_weight.Fill(event.j0_pt, weight)

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
        self.h0_pt_m.Write()    
        self.h1_pt_m.Write() 
        self.mH0H1.Write() 

        if self.fullhist:
            self.h_deta.Write()    
            self.h_dphi.Write()    
            self.h_dr.Write()  
            self.h_pt_assy.Write()   
            self.h0_m_s.Write()   
            self.h1_m_s.Write()     
            self.h0_eta.Write()    
            self.h1_eta.Write()   
            self.h0_phi.Write()    
            self.h1_phi.Write()    
            self.h0_trk_dr.Write() 
            self.h1_trk_dr.Write() 
            self.h0_trk0_eta.Write() 
            self.h0_trk0_phi.Write() 
            self.h1_trk0_eta.Write() 
            self.h1_trk0_phi.Write() 
            self.h0_ntrk.Write()   
            self.h1_ntrk.Write()   
            #self.h0_trks_pt.Write() 
            #self.h1_trks_pt.Write()   
            #self.trks_pt.Write()
            self.Rhh.Write()
            self.h0_trkpt_diff.Write()
            self.h1_trkpt_diff.Write()
            self.dRH0H1.Write()
            self.MV2.Write()
            #self.trkfracH0H1.Write()
            #self.mHHdRH0.Write()
            #self.MV2H0H1.Write()
            #self.MV2H0.Write()
            #self.MV2H1.Write()
        if self.reweight:
            self.mHH_weight.Write()
            self.h0_trk0_pt_weight.Write()
            self.h1_trk0_pt_weight.Write()
            self.h0_pt_m_weight.Write()

#split things in to mass regions, also possible systematic variation
class massregionHists:
    #these are the regions and cuts;
    def __init__(self, region, outputroot, reweight=False):
        #define control/sb variations
        self.RegionDict = {
            "Incl"     : Syst_cut["SB"], #"True", ##this is going to be inclusive SB + CR + SR region now
            "Signal"   : SR_cut,
            "Control"  : CR_cut,
            "Sideband" : SB_cut,
        }
        self.regionlst = []
        #for specific studies; for systemtaics
        for name, cut in self.RegionDict.items():
            tempdic = {}
            tempdic["name"]          = name
            tempdic["histname"]      = region + "_" + name
            tempdic["eventHists"]    = eventHists(tempdic["histname"], outputroot, reweight)
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
class bkgregionHists:
    def __init__(self, region, outputroot, reweight=False):
        self.reweight = reweight
        self.region   = region
        self.default  = massregionHists(region, outputroot, reweight)
        if self.reweight:
            self.reweight_dic = get_parameter(filename=ops.reweight, region=self.region)

    def Fill(self, event, weight=-1):
        if self.reweight:
                weight = event.weight * calc_reweight(self.reweight_dic, event)
        self.default.Fill(event, weight)

    def Write(self, outputroot):
        self.default.Write(outputroot)


#these are the different regions
class regionHists:
    def __init__(self, outputroot, reweight, isData=False):
        reweight = reweight and isData ##only reweight in data case!
        self.AllTag                    = massregionHists("AllTag", outputroot)
        self.NoTag                     = massregionHists("NoTag", outputroot)
        self.OneTag                    = massregionHists("OneTag", outputroot) #if test 1 tag fit, needs to enable this
        self.TwoTag                    = massregionHists("TwoTag", outputroot)
        self.TwoTag_split              = massregionHists("TwoTag_split", outputroot)
        self.ThreeTag                  = massregionHists("ThreeTag", outputroot)
        self.FourTag                   = massregionHists("FourTag", outputroot)
        #for background modeling; not really NoTag!!!
        self.TwoTag_split_bkg          = bkgregionHists("NoTag" + "_" + "2Trk_split", outputroot, reweight)
        self.TwoTag_split_lead_bkg     = bkgregionHists("NoTag" + "_" + "2Trk_split_lead", outputroot, reweight)
        self.TwoTag_split_subl_bkg     = bkgregionHists("NoTag" + "_" + "2Trk_split_subl", outputroot, reweight)
        # self.TwoTag_split_lead_lead_bkg= bkgregionHists("NoTag" + "_" + "2Trk_split_lead_lead", outputroot, reweight)
        # self.TwoTag_split_subl_lead_bkg= bkgregionHists("NoTag" + "_" + "2Trk_split_subl_lead", outputroot, reweight)
        # self.TwoTag_split_lead_subl_bkg= bkgregionHists("NoTag" + "_" + "2Trk_split_lead_subl", outputroot, reweight)
        # self.TwoTag_split_subl_subl_bkg= bkgregionHists("NoTag" + "_" + "2Trk_split_subl_subl", outputroot, reweight)
        self.ThreeTag_bkg              = bkgregionHists("NoTag" + "_" + "3Trk", outputroot, reweight)
        self.ThreeTag_lead_bkg         = bkgregionHists("NoTag" + "_" + "3Trk_lead", outputroot, reweight)
        self.ThreeTag_subl_bkg         = bkgregionHists("NoTag" + "_" + "3Trk_subl", outputroot, reweight)
        # self.ThreeTag_lead_lead_bkg    = bkgregionHists("NoTag" + "_" + "3Trk_lead_lead_lead", outputroot, reweight)
        # self.ThreeTag_subl_lead_bkg    = bkgregionHists("NoTag" + "_" + "3Trk_subl_lead_lead", outputroot, reweight)
        # self.ThreeTag_lead_subl_bkg    = bkgregionHists("NoTag" + "_" + "3Trk_lead_subl", outputroot, reweight)
        # self.ThreeTag_subl_subl_bkg    = bkgregionHists("NoTag" + "_" + "3Trk_subl_subl", outputroot, reweight)
        self.FourTag_bkg               = bkgregionHists("NoTag" + "_" + "4Trk", outputroot, reweight)
        self.FourTag_lead_bkg          = bkgregionHists("NoTag" + "_" + "4Trk_lead", outputroot, reweight)
        self.FourTag_subl_bkg          = bkgregionHists("NoTag" + "_" + "4Trk_subl", outputroot, reweight)
        # #for extra studies
        self.OneTag_lead               = massregionHists("OneTag_lead", outputroot) #1tag, lead H tag
        self.OneTag_subl               = massregionHists("OneTag_subl", outputroot) #1tag, subl H tag
        self.TwoTag_lead               = massregionHists("TwoTag_lead", outputroot) #2tag, lead H tag
        self.TwoTag_subl               = massregionHists("TwoTag_subl", outputroot) #2tag, lead H tag
        self.ThreeTag_lead             = massregionHists("ThreeTag_lead", outputroot) #2tag, lead H tag 2 tag
        self.ThreeTag_subl             = massregionHists("ThreeTag_subl", outputroot) #2tag, subl H tag 2 tag
        # # # ##for extra extra b-tagging on which jet studies
        # self.TwoTag_split_lead_lead    = massregionHists("TwoTag_split_lead_lead", outputroot) #2bs, lead H lead trk tag, subl H lead trk tag
        # self.TwoTag_split_subl_subl    = massregionHists("TwoTag_split_subl_subl", outputroot) #2bs, lead H subl trk tag, subl H subl trk tag
        # self.TwoTag_split_lead_subl    = massregionHists("TwoTag_split_lead_subl", outputroot) #2bs, lead H lead trk tag, subl H subl trk tag
        # self.TwoTag_split_subl_lead    = massregionHists("TwoTag_split_subl_lead", outputroot) #2bs, lead H subl trk tag, subl H lead trk tag
        self.isData   = isData ##this is for special treatments to data
        self.doDetail = False ##to split events into halves for bkg estimation; for ttbar as well...
        self.split_factor = CONF.split_factor
        if self.doDetail:
            self.OneTag_lead_lead          = massregionHists("OneTag_lead_lead", outputroot) #1tag, lead H tag, lead trk tag
            self.OneTag_subl_subl          = massregionHists("OneTag_subl_subl", outputroot) #1tag, subl H tag, subl trk tag
            self.OneTag_lead_subl          = massregionHists("OneTag_lead_subl", outputroot) #1tag, lead H tag, lead trk tag
            self.OneTag_subl_lead          = massregionHists("OneTag_subl_lead", outputroot) #1tag, subl H tag, subl trk tag

    def Fill(self, event):
        ##modeling requires at least one track jets on each side
        if (event.j0_nTrk < 1 or event.j1_nTrk < 1):
            pass
        else:
            b_tagging_cut = float(ops.MV2) #0.3706 as 77% default value; -0.1416 85%; 0.6455 70%; 0.8529 as 60%;0.9452 as 50%;-0.1416 as 85% value
            nb_j0 = 0
            nb_j1 = 0
            nb_j0 += 1 if event.j0_trk0_Mv2 > b_tagging_cut else 0
            nb_j0 += 1 if event.j0_trk1_Mv2 > b_tagging_cut else 0
            nb_j1 += 1 if event.j1_trk0_Mv2 > b_tagging_cut else 0
            nb_j1 += 1 if event.j1_trk1_Mv2 > b_tagging_cut else 0

            #for testing
            # b_tagging_tight_cut = float(ops.MV2) #50; 
            # nb_j0_tight = 0
            # nb_j1_tight = 0
            # nb_j0_tight += 1 if event.j0_trk0_Mv2 > b_tagging_tight_cut else 0
            # nb_j0_tight += 1 if event.j0_trk1_Mv2 > b_tagging_tight_cut else 0
            # nb_j1_tight += 1 if event.j1_trk0_Mv2 > b_tagging_tight_cut else 0
            # nb_j1_tight += 1 if event.j1_trk1_Mv2 > b_tagging_tight_cut else 0

            ##fill the tag regions
            self.AllTag.Fill(event)
            ##fill the specific b-tag regions
            if nb_j0 + nb_j1 == 4:
                self.FourTag.Fill(event) #this is always the tightest one
            elif nb_j0 + nb_j1 == 3:
                self.ThreeTag.Fill(event) #this is 3 tight 1 tight; if not the last tight, then 3b
            elif nb_j0 == 1 and nb_j1 == 1:
                #if (event.j0_trk0_Mv2 > b_tagging_cut) and (event.j1_trk0_Mv2 > b_tagging_cut):
                self.TwoTag_split.Fill(event) #this is 2 tight 2 tight, on both side; if not the last tight, then 2bs
                # ##for extra extra b-tagging on which jet studies
                # if (event.j0_trk0_Mv2 > b_tagging_cut) and (event.j1_trk0_Mv2 > b_tagging_cut):
                #     self.TwoTag_split_lead_lead.Fill(event)
                # elif (event.j0_trk0_Mv2 > b_tagging_cut) and (event.j1_trk0_Mv2 < b_tagging_cut):
                #     self.TwoTag_split_lead_subl.Fill(event)
                # elif (event.j0_trk1_Mv2 > b_tagging_cut) and (event.j1_trk0_Mv2 < b_tagging_cut):
                #     self.TwoTag_split_subl_subl.Fill(event)
                # elif (event.j0_trk1_Mv2 > b_tagging_cut) and (event.j1_trk0_Mv2 > b_tagging_cut):
                #    self.TwoTag_split_subl_lead.Fill(event)

            elif (nb_j0 == 2 and nb_j1 == 0) or (nb_j0 == 0 and nb_j1 == 2): 
                self.TwoTag.Fill(event) #this is 2 tight 2 tight, on either side
            elif nb_j0 + nb_j1 == 1:
                self.OneTag.Fill(event) #this is 1 tight 4 tight, on either side
            elif nb_j0 + nb_j1 == 0:
                self.NoTag.Fill(event)
            
            #for bkg modeling; from Notag
            # if nb_j0 + nb_j1 == 0 and event.j0_nTrk >= 1 and event.j1_nTrk >= 1:
            #     self.TwoTag_split_bkg.Fill(event)
            # if nb_j0 + nb_j1 == 0 and ((event.j0_nTrk >= 1 and event.j1_nTrk >= 2) or (event.j0_nTrk >= 2 and event.j1_nTrk >= 1)):
            #     self.ThreeTag_bkg.Fill(event)
            # if nb_j0 + nb_j1 == 0 and event.j0_nTrk >= 2 and event.j1_nTrk >= 2:
            #     self.FourTag_bkg.Fill(event)

            ##new bkg modeling, from 1b and 2b ; keep the number of trackjet consistent here
            if ((nb_j0 == 1 and nb_j1 == 0) or (nb_j0 == 0 and nb_j1 == 1)):
                self.TwoTag_split_bkg.Fill(event)
                if (nb_j0 == 1 and nb_j1 == 0):
                    self.TwoTag_split_lead_bkg.Fill(event)
                    # if (event.j0_trk0_Mv2 > b_tagging_cut):
                    #     self.TwoTag_split_lead_lead_bkg.Fill(event)
                    # else:
                    #     self.TwoTag_split_lead_subl_bkg.Fill(event)
                elif (nb_j0 == 0 and nb_j1 == 1):
                    self.TwoTag_split_subl_bkg.Fill(event)
                    # if (event.j1_trk0_Mv2 > b_tagging_cut):
                    #     self.TwoTag_split_subl_lead_bkg.Fill(event)
                    # else:
                    #     self.TwoTag_split_subl_subl_bkg.Fill(event)
            # if ((nb_j0 == 1 and nb_j1 == 0) or (nb_j0 == 0 and nb_j1 == 1)) and ((event.j0_nTrk >= 1 and event.j1_nTrk >= 2) or (event.j0_nTrk >= 2 and event.j1_nTrk >= 1)):
            #     self.ThreeTag_bkg.Fill(event)
            #     if (nb_j0 == 1 and nb_j1 == 0):
            #         self.ThreeTag_lead_bkg.Fill(event)
            #     elif (nb_j0 == 0 and nb_j1 == 1):
            #         self.ThreeTag_subl_bkg.Fill(event)
            if ((nb_j0 == 2 and nb_j1 == 0) or (nb_j0 == 0 and nb_j1 == 2)) and ((event.j0_nTrk >= 1 and event.j1_nTrk >= 2) or (event.j0_nTrk >= 2 and event.j1_nTrk >= 1)):
                if (event.eventNumber%self.split_factor != 0 ): ##if true, then fill into 3b
                    self.ThreeTag_bkg.Fill(event)
                    if (nb_j0 == 2 and nb_j1 == 0):
                        self.ThreeTag_lead_bkg.Fill(event)
                    elif (nb_j0 == 0 and nb_j1 == 2):
                        self.ThreeTag_subl_bkg.Fill(event)

            if ((nb_j0 == 2 and nb_j1 == 0) or (nb_j0 == 0 and nb_j1 == 2)) and event.j0_nTrk >= 2 and event.j1_nTrk >= 2:
                if (event.eventNumber%self.split_factor == 0 and (event.nresj > -1.9 if ops.dosyst != "ZZ" else True)): ##if true, then fill into 4b; not for ZZ
                    self.FourTag_bkg.Fill(event)
                    ##sub this in
                    if (nb_j0 == 2 and nb_j1 == 0):
                        self.FourTag_lead_bkg.Fill(event)
                    elif (nb_j0 == 0 and nb_j1 == 2):
                        self.FourTag_subl_bkg.Fill(event)

            ##for extra studies; need to be moved to default; notice b-tagging is already sorted here
            if (nb_j0 == 1 and nb_j1 == 0):
                self.OneTag_lead.Fill(event)
                # ##for extra extra b-tagging on which jet studies
                if self.doDetail:
                    if (event.j0_trk0_Mv2 > b_tagging_cut):
                        self.OneTag_lead_lead.Fill(event)
                    else:
                        self.OneTag_lead_subl.Fill(event)
            elif (nb_j0 == 0 and nb_j1 == 1):
                self.OneTag_subl.Fill(event)
                # ##for extra extra b-tagging on which jet studies
                if self.doDetail:
                    if (event.j1_trk0_Mv2 > b_tagging_cut):
                        self.OneTag_subl_lead.Fill(event)
                    else:
                        self.OneTag_subl_subl.Fill(event)
            elif (nb_j0 == 2 and nb_j1 == 0):
                self.TwoTag_lead.Fill(event)
            elif (nb_j0 == 0 and nb_j1 == 2):
                self.TwoTag_subl.Fill(event)
            elif (nb_j0 == 2 and nb_j1 == 1):
                self.ThreeTag_lead.Fill(event)
            elif (nb_j0 == 1 and nb_j1 == 2):
                self.ThreeTag_subl.Fill(event)



    def Write(self, outputroot):
        self.AllTag.Write(outputroot)
        self.NoTag.Write(outputroot)
        self.OneTag.Write(outputroot)
        self.TwoTag.Write(outputroot)
        self.TwoTag_split.Write(outputroot)
        self.ThreeTag.Write(outputroot)
        self.FourTag.Write(outputroot)
        #for bkg modeling
        self.TwoTag_split_bkg.Write(outputroot)
        self.TwoTag_split_lead_bkg.Write(outputroot)
        self.TwoTag_split_subl_bkg.Write(outputroot)
        self.ThreeTag_bkg.Write(outputroot)
        self.ThreeTag_lead_bkg.Write(outputroot)
        self.ThreeTag_subl_bkg.Write(outputroot)
        self.FourTag_bkg.Write(outputroot)
        self.FourTag_lead_bkg.Write(outputroot)
        self.FourTag_subl_bkg.Write(outputroot)
        # self.TwoTag_split_lead_lead_bkg.Write(outputroot)
        # self.TwoTag_split_subl_lead_bkg.Write(outputroot)
        # self.TwoTag_split_lead_subl_bkg.Write(outputroot)
        # self.TwoTag_split_subl_subl_bkg.Write(outputroot)
        # #for other bkg modeling
        self.OneTag_lead.Write(outputroot)
        self.OneTag_subl.Write(outputroot)
        self.TwoTag_lead.Write(outputroot)
        self.TwoTag_subl.Write(outputroot)
        self.ThreeTag_lead.Write(outputroot)
        self.ThreeTag_subl.Write(outputroot)
        # ##for extra extra b-tagging on which jet studies
        if self.doDetail:
            self.OneTag_lead_lead.Write(outputroot)
            self.OneTag_subl_lead.Write(outputroot)
            self.OneTag_lead_subl.Write(outputroot)
            self.OneTag_subl_subl.Write(outputroot)
            # self.TwoTag_split_lead_lead.Write(outputroot)
            # self.TwoTag_split_subl_lead.Write(outputroot)
            # self.TwoTag_split_lead_subl.Write(outputroot)
            # self.TwoTag_split_subl_subl.Write(outputroot)


def analysis(inputconfig):
    inputfile  = inputconfig["inputfile"]
    inputroot  = inputconfig["inputroot"]
    outputroot = inputconfig["outputroot"]

    outroot = ROOT.TFile.Open(outputpath + inputfile + "/" + outputroot, "recreate")
    AllHists = regionHists(outroot, turnon_reweight, isData=("data" in inputfile))
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
    #print N, inputfile
    for i in range(N):
    # get the next tree in the chain and verify
        # if DEBUG & (i > 100000):
        #     break
        if i % 25000 == 0:
            helpers.drawProgressBar(i/(N*1.0))
        t.fChain.GetEntry(i)
        #print t.Xzz
        
        ##place a cut if necessary
        # def selection():
        #     passed = True
        #     return passed
        
        ##for debugging
        # if (t.j0_nb + t.j1_nb == 4 and t.Xhh < 1.6):
        #     print "WTF"
        # dR cut
        #if (helpers.dR(t.j0_trk0_eta, t.j0_trk0_phi, t.j0_trk1_eta, t.j0_trk1_phi) > 0.6 or helpers.dR(t.j1_trk0_eta, t.j1_trk0_phi, t.j1_trk1_eta, t.j1_trk1_phi) > 0.6):
            #continue

        ##speed up selection a bit; skip events with jet mass less than 65 for now
        if (t.j0_m < 60 or t.j1_m < 60): ##as far as the cut can go
            continue

        ##add blinding
        if (CONF.blind and "data" in inputfile):
            if (t.Xhh < 1.6):
                if (t.j0_nb + t.j1_nb >= 3): ##3b and 4b
                    continue
                elif (t.j0_nb == 1  and t.j1_nb == 1):##2b
                    continue

        #AllHists.Fill(t)
        ##or, add in resovled veto whenever feel like it
        #if (ops.resveto):
        ##enable resolved veto for now and on
        #print t.Xhh, (ROOT.TMath.Sqrt(ROOT.TMath.Power((t.j0_m - 124.0)/(0.1*t.j0_m), 2) + ROOT.TMath.Power((t.j1_m - 115.0)/(0.1*t.j1_m), 2)))
        #if (abs(t.nresj) < 4): ##veto all 4 jets
        #AllHists.Fill(t)
        if (t.nresj < -3.9): ##negative is SR regions
            pass
        else:
            AllHists.Fill(t)
        

    #write all the output
    AllHists.Write(outroot)
    print "DONE with the " + inputfile,  outputroot  + " analysis!", N, " events!"
    #close the input file;
    outroot.Close()
    del(AllHists)
    del(t)
    del(f)
    gc.collect()

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
    ##36-60 is not bad; but 4b CR is off
    CR_size = float(ops.CR) #this needs to be fixed; so good so far
    SB_size = float(ops.SB) #56 is the new default; should be between 48-58 due to stats
    CR_X    = 124. ##center for control region
    CR_Y    = 115. ##center for control region
    SB_X    = 124. + float(ops.SBshift) ##center for sideband region; 12 is also ok
    SB_Y    = 115. + float(ops.SBshift) ##center for sideband region; 12 is also ok
    Syst_cut = {
        "SR"         : "event.Xhh < 1.6", # #GetXhh(), #"event.Xhh < 1.6", #
        "CR"         : GetRhh(RhhCenterX=CR_X, RhhCenterY=CR_Y, RhhCut=CR_size), #"event.Rhh < %s" % str(CR_size) ,
        "SB"         : GetRhh(RhhCenterX=SB_X, RhhCenterY=SB_Y, RhhCut=SB_size), #"event.Rhh < %s" % str(SB_size) ,
        "CR_High"    : GetRhh(RhhCenterX=CR_X+3,  RhhCenterY=CR_Y+3,  RhhCut=CR_size),
        "CR_Low"     : GetRhh(RhhCenterX=CR_X-3,  RhhCenterY=CR_Y-3,  RhhCut=CR_size),
        "CR_Small"   : "event.Xhh > 2.0 and event.Rhh < %s" % str(CR_size) ,
        "SB_High"    : GetRhh(RhhCenterX=SB_X+3,  RhhCenterY=SB_Y+3,  RhhCut=SB_size),
        "SB_Low"     : GetRhh(RhhCenterX=SB_X-3,  RhhCenterY=SB_Y-3,  RhhCut=SB_size),
        "SB_Large"   : GetRhh(RhhCenterX=SB_X,    RhhCenterY=SB_Y,    RhhCut=SB_size + 3), #"event.Rhh < %s" % str(SB_size + 5) ,
        "SB_Small"   : GetRhh(RhhCenterX=SB_X,    RhhCenterY=SB_Y,    RhhCut=SB_size - 3), #"event.Rhh < %s" % str(SB_size - 5) ,
        "ZZ"         : GetXhh(XhhCenterX=103., XhhCenterY=96.,  XhhCut=1.6), #"event.Xzz < 1.6" , ##use to be 2.1
        "TT"         : GetXhh(XhhCenterX=164., XhhCenterY=155., XhhCut=1.6)  #"event.Xzz < 1.6" , ##use to be 2.1
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
            SB_cut = "not " + Syst_cut[ops.dosyst] + " and " + Syst_cut["SB"] ##fix this
            if "Small" in ops.dosyst: #sepecial treatment for this asshole
                SB_cut = ("event.Rhh > %s " % (str(CR_size))) + " and " + Syst_cut["SB"]
        elif "SB" in ops.dosyst:
            SB_cut = "not " + Syst_cut["CR"] + " and " + Syst_cut[ops.dosyst]
        elif "ZZ" in ops.dosyst or "TT" in ops.dosyst:
            SR_cut = "not " + Syst_cut["SR"] + " and " + Syst_cut[ops.dosyst]
            CR_cut = "not " + Syst_cut["SR"] + " and not " + Syst_cut[ops.dosyst] + " and " + Syst_cut["CR"]
            SB_cut = "not " + Syst_cut["CR"] + " and not " + Syst_cut[ops.dosyst] + " and " + Syst_cut["SB"]


    ##for testing
    if (DEBUG):
        analysis(pack_input("zjets_test"))
        print("--- %s seconds ---" % (time.time() - start_time))
        return

    ##real job; full chain 2 mins...just data is 50 seconds
    nsplit = CONF.splits
    split_list = ["data_test", "ttbar_comb_test"] #, "signal_QCD"] #if not turnon_reweight else  ["data_test"] #["data_test", "ttbar_comb_test", "signal_QCD"]
    #split_list = ["signal_QCD"]
    if turnon_reweight and ops.dosyst is None:
        split_list = ["data_test"]
    if (ops.dijet): ##only do dijet in this case, always
        split_list = ["signal_QCD"]

    #split_list = []
    inputtasks = []
    for split_file in split_list:
        for i in range(nsplit):
            inputtasks.append(pack_input(split_file, inputsplit=i))    
    ##for other MCs
    ##for reweighting condition; copy zjet and ttbar
    if not turnon_reweight or ops.dosyst is not None :
        if (not ops.dijet): 
            inputtasks.append(pack_input("zjets_test"))
    else:##if reweight or do syst
        linklist = ["zjets_test", "ttbar_comb_test"] ##don't reweight ttbar and zjets
        for target in linklist:
            helpers.checkpath(outputpath + target)
            ori_link = inputpath.replace(ops.inputdir, "Moriond") + target + "/hist-MiniNTuple.root"
            dst_link = outputpath + target + "/hist-MiniNTuple.root"
            try:
                os.remove(dst_link)
            except OSError:
                pass
            if os.path.islink(dst_link):
                os.unlink(dst_link)
            print ori_link, dst_link
            os.symlink(ori_link, dst_link)

    ##for signal samples; only need to process once
    sigMClist = ["signal_G_hh_c10_M"]
    if (ops.Xhh):
        sigMClist = ["signal_G_hh_c10_M", "signal_G_hh_c20_M", "signal_X_hh_M"]
    
    for i, mass in enumerate(CONF.mass_lst):
        if (ops.dijet): ##don't do anything for the dijet case
            continue
        #do not reweight signal samples; create links to the original files instead
        if not turnon_reweight or ops.dosyst is not None :
            for sigMC in sigMClist:
                if mass != 2750 and sigMC != "signal_G_hh_c20_M": ##no c20 2750 sample
                    inputtasks.append(pack_input(sigMC + str(mass)))
        else:#if reweight, creat the folders and the links to the files
            for sigMC in sigMClist:
                if mass != 2750 and sigMC != "signal_G_hh_c20_M": ##no c20 2750 sample
                    print "creating links of signal samples", sigMC + str(mass)
                    helpers.checkpath(outputpath + sigMC + str(mass))
                    #this is a really bad practice and temp fix now! need to watch this very carfully...
                    #ori_link = inputpath.replace("F_c10", "f_fin") + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root"
                    ori_link = inputpath.replace(ops.inputdir, "Moriond") + sigMC + str(mass) + "/hist-MiniNTuple.root"
                    dst_link = outputpath + sigMC + str(mass) + "/hist-MiniNTuple.root"
                    #print ori_link, dst_link
                    if os.path.islink(dst_link):
                        os.unlink(dst_link)
                    print ori_link, dst_link
                    os.symlink(ori_link, dst_link)
    #return
    ##if reweight, reweight everything
    
    ##for debug parallel
    #analysis(pack_input("ttbar_comb_test"))
    if ops.debug:
        analysis(inputtasks[0])
        return
    else:
        ##parallel compute!
        print " START: Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
        npool = min(len(inputtasks), mp.cpu_count()-1)  ##because herophysics sucks
        pool  = mp.Pool(npool)
        pool.map(analysis, inputtasks)
    
    ##all the other extra set of MCs
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


    #analysis(pack_input("signal_BQCD_200")) #2 mins! 4 mins with expanded...
    #analysis("signal_QCD") #2 mins! 10 mins...
    print("--- %s seconds ---" % (time.time() - start_time))
    print "Finish!"
    ##consistency check
    #f = ROOT.TFile(outputpath + "ttbar_comb_test" + "/hist-MiniNTuple.root", "read")
    f = ROOT.TFile(outputpath + "signal_G_hh_c10_M1000" + "/hist-MiniNTuple.root", "read")
    print f.Get("FourTag_Signal/mHH_l").GetEntries()
    f.Close()

#def clearbranches():
if __name__ == "__main__":
    main()
