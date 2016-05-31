###Tony: improve to load branches for faster processing
###Performance is not garanteened. The way to register hists are slow
###For a quick on the fly anaysis, great.
###For a more proper anlaysis, do the c++ standard way please
import ROOT, rootlogon, helpers
import config as CONF
import time, os, subprocess, glob
#for parallel processing!
import multiprocessing as mp
#import tree configuration
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('TinyTree.C')


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
        self.h0_m         = ROOT.TH1F("leadHCand_Mass",     ";Mass [GeV]",       100,   0,  500)
        self.h1_m         = ROOT.TH1F("sublHCand_Mass",     ";Mass [GeV]",       100,   0,  500)
        self.h0_trk0_pt   = ROOT.TH1F("leadHCand_trk0_Pt",  ";p_{T} [GeV]",      100,  0,   500)
        self.h1_trk0_pt   = ROOT.TH1F("sublHCand_trk0_Pt",  ";p_{T} [GeV]",      100,  0,   500)
        self.h0_trk1_pt   = ROOT.TH1F("leadHCand_trk1_Pt",  ";p_{T} [GeV]",      100,  0,   500)
        self.h1_trk1_pt   = ROOT.TH1F("sublHCand_trk1_Pt",  ";p_{T} [GeV]",      100,  0,   500)

        if self.fullhist:
            self.h_deta       = ROOT.TH1F("hCandDeta",          "hCand #Delta#eta",  66,    0,  3.3)
            self.h_dphi       = ROOT.TH1F("hCandDphi",          "hCand #Delta#phi",  66, -3.3,  3.3)
            self.h_dr         = ROOT.TH1F("hCandDr",            "hCand #Deltar",     100,   0,    5)
            self.h0_m_s       = ROOT.TH1F("leadHCand_Mass_s",   ";Mass [GeV]",       40,   70,  170)
            self.h1_m_s       = ROOT.TH1F("sublHCand_Mass_s",   ";Mass [GeV]",       40,   70,  170)
            self.h0_pt_m      = ROOT.TH1F("leadHCand_Pt_m",     ";p_{T} [GeV]",      200,   0,  2000)
            self.h1_pt_m      = ROOT.TH1F("sublHCand_Pt_m",     ";p_{T} [GeV]",      200,   0,  2000)
            self.h0_eta       = ROOT.TH1F("leadHCand_Eta",      ";#Eta",             60, -3.2,  3.2)
            self.h1_eta       = ROOT.TH1F("sublHCand_Eta",      ";#Eta",             60, -3.2,  3.2)
            self.h0_phi       = ROOT.TH1F("leadHCand_Phi",      ";#Phi",             64, -3.2,  3.2)
            self.h1_phi       = ROOT.TH1F("sublHCand_Phi",      ";#Phi",             64, -3.2,  3.2)
            self.h0_trk_dr    = ROOT.TH1F("leadHCand_trk_dr",   ";trkjet #Deltar",   42, -0.1,    2)
            self.h1_trk_dr    = ROOT.TH1F("sublHCand_trk_dr",   ";trkjet #Deltar",   42, -0.1,    2)
            self.h0_ntrk      = ROOT.TH1F("leadHCand_ntrk",     "number of trkjet",  10,  -0.5, 9.5)
            self.h1_ntrk      = ROOT.TH1F("sublHCand_ntrk",     "number of trkjet",  10,  -0.5, 9.5)
            self.h0_trkpt_diff= ROOT.TH1F("leadHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 22, -0.1, 1)
            self.h1_trkpt_diff= ROOT.TH1F("sublHCand_trk_pt_diff_frac",  ";trackjet p_{T} assym", 22, -0.1, 1)
            self.mH0H1        = ROOT.TH2F("mH0H1",              ";mH1 [GeV]; mH2 [GeV];", 60,  0,  300, 60,  0,  300)

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

        if self.fullhist:
            self.mH0H1.Fill(event.j0_m, event.j1_m, weight)
            self.h_deta.Fill(event.detaHH, weight)    
            self.h_dphi.Fill(event.dphiHH, weight)    
            self.h_dr.Fill(event.drHH, weight)    
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
        if self.fullhist:
            self.mH0H1.Write() 
            self.h_deta.Write()    
            self.h_dphi.Write()    
            self.h_dr.Write()     
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
        #self.Incl = eventHists(region + "_" + "Incl", outputroot)
        self.Sideband = eventHists(region + "_" + "Sideband", outputroot, reweight)
        self.Control = eventHists(region + "_" + "Control", outputroot, reweight)
        self.Signal = eventHists(region + "_" + "Signal", outputroot, reweight)
        self.ZZ = eventHists(region + "_" + "ZZ", outputroot, reweight)
        # self.Rhh20  = eventHists(region + "_" + "Rhh20", outputroot)
        # self.Rhh30  = eventHists(region + "_" + "Rhh30", outputroot)
        # self.Rhh40  = eventHists(region + "_" + "Rhh40", outputroot)
        # self.Rhh50  = eventHists(region + "_" + "Rhh50", outputroot)
        # self.Rhh60  = eventHists(region + "_" + "Rhh60", outputroot)
        # self.Rhh70  = eventHists(region + "_" + "Rhh70", outputroot)
        # self.Rhh80  = eventHists(region + "_" + "Rhh80", outputroot)
        # self.Rhh90  = eventHists(region + "_" + "Rhh90", outputroot)
        # self.Rhh100 = eventHists(region + "_" + "Rhh100", outputroot)
        # self.Rhh110 = eventHists(region + "_" + "Rhh110", outputroot)
        # self.Rhh120 = eventHists(region + "_" + "Rhh120", outputroot)
        # self.Rhh130 = eventHists(region + "_" + "Rhh130", outputroot)
        # self.Rhh140 = eventHists(region + "_" + "Rhh140", outputroot)
        # self.Rhh150 = eventHists(region + "_" + "Rhh150", outputroot)

    def Fill(self, event, weight=-1):
        #self.Incl.Fill(event)
        if event.Xhh < 1.6:
            self.Signal.Fill(event, weight)
        elif event.Rhh < 35.8:
            self.Control.Fill(event, weight)
        elif event.Rhh < 108:
            self.Sideband.Fill(event, weight)
        if event.Xhh > 1.6 and event.Xzz < 2.1:
            self.ZZ.Fill(event, weight)

        #for mass mu qcd test
        # if event.Xhh > 1.6 and event.Rhh < 20:
        #     self.Rhh20.Fill(event)
        # elif event.Rhh < 30:
        #     self.Rhh30.Fill(event)
        # elif event.Rhh < 30: 
        #     self.Rhh30.Fill(event)
        # elif event.Rhh < 40: 
        #     self.Rhh40.Fill(event)
        # elif event.Rhh < 50: 
        #     self.Rhh50.Fill(event)
        # elif event.Rhh < 60: 
        #     self.Rhh60.Fill(event)
        # elif event.Rhh < 70: 
        #     self.Rhh70.Fill(event)
        # elif event.Rhh < 80: 
        #     self.Rhh80.Fill(event)
        # elif event.Rhh < 90: 
        #     self.Rhh90.Fill(event)
        # elif event.Rhh < 100: 
        #     self.Rhh100.Fill(event)
        # elif event.Rhh < 110: 
        #     self.Rhh110.Fill(event)
        # elif event.Rhh < 120: 
        #     self.Rhh120.Fill(event)
        # elif event.Rhh < 130: 
        #     self.Rhh130.Fill(event)
        # elif event.Rhh < 140: 
        #     self.Rhh140.Fill(event)
        # elif event.Rhh < 150: 
        #     self.Rhh150.Fill(event)

    def Write(self, outputroot):
        #self.Incl.Write(outputroot)
        self.Sideband.Write(outputroot)
        self.Control.Write(outputroot)
        self.Signal.Write(outputroot)
        self.ZZ.Write(outputroot)
        # self.Rhh20.Write(outputroot)
        # self.Rhh30.Write(outputroot) 
        # self.Rhh40.Write(outputroot) 
        # self.Rhh50.Write(outputroot) 
        # self.Rhh60.Write(outputroot) 
        # self.Rhh70.Write(outputroot) 
        # self.Rhh80.Write(outputroot) 
        # self.Rhh90.Write(outputroot)
        # self.Rhh100.Write(outputroot)
        # self.Rhh110.Write(outputroot)
        # self.Rhh120.Write(outputroot)
        # self.Rhh130.Write(outputroot)
        # self.Rhh140.Write(outputroot)
        # self.Rhh150.Write(outputroot)

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
    def Fill(self, event, weight=-1):
        self.Trk0.Fill(event, weight)
        # if event.j0_nTrk >= 1 or event.j1_nTrk >= 1:
        #     self.Trk1.Fill(event)
        if event.j0_nTrk >= 1 and event.j1_nTrk >= 1:
            if self.reweight:
                weight = event.weight
                tempw0 = 0.77 + 0.0077 * event.j0_trk1_pt - 4.2E-05 * event.j0_trk1_pt ** 2
                if tempw0 > 0:
                    weight *= tempw0
                tempw1 = 0.73 + 0.0087 * event.j1_trk1_pt - 4.7E-05 * event.j1_trk1_pt ** 2
                if tempw1 > 0:
                    weight *= tempw1
            self.Trk2s.Fill(event, weight)
        # if event.j0_nTrk >= 2 or event.j1_nTrk >= 2:
        #     self.Trk2.Fill(event)
        if (event.j0_nTrk >= 1 and event.j1_nTrk >= 2) or (event.j0_nTrk >= 2 and event.j1_nTrk >= 1):
            if self.reweight:
                weight = event.weight
                tempw0 = 0.41 + 0.017  * event.j0_trk1_pt - 7.8E-05 * event.j0_trk1_pt ** 2
                if tempw0 > 0:
                    weight *= tempw0
                tempw1 = 0.46 + 0.017 * event.j1_trk1_pt - 8.2E-05 * event.j1_trk1_pt ** 2
                if tempw1 > 0:
                    weight *= tempw1
            self.Trk3.Fill(event, weight)
        if event.j0_nTrk >= 2 and event.j1_nTrk >= 2:
            if self.reweight:
                weight = event.weight
                tempw0 = 0.41 + 0.017  * event.j0_trk1_pt - 7.8E-05 * event.j0_trk1_pt ** 2
                if tempw0 > 0:
                    weight *= tempw0
                tempw1 = 0.46 + 0.017 * event.j1_trk1_pt - 8.2E-05 * event.j1_trk1_pt ** 2
                if tempw1 > 0:
                    weight *= tempw1
            self.Trk4.Fill(event, weight)
    def Write(self, outputroot):
        self.Trk0.Write(outputroot)
        #self.Trk1.Write(outputroot)
        #self.Trk2.Write(outputroot)
        self.Trk2s.Write(outputroot)
        self.Trk3.Write(outputroot)
        self.Trk4.Write(outputroot)

class regionHists:
    def __init__(self, outputroot):
        self.NoTag  = trkregionHists("NoTag", outputroot, reweight=True)
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
    AllHists = regionHists(outroot)
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
        AllHists.Fill(t)

    #write all the output
    AllHists.Write(outroot)
    print "DONE with the " + inputfile,  outputroot  + " analysis!"
    #close the input file;
    del(t)
    outroot.Close()

#pack the input into a configuration dictionary
def pack_input(inputfile, inputsplit=-1):
    dic = {}
    dic["inputfile"] = inputfile
    dic["inputroot"] = "hist-MiniNTuple" + ("_" + str(inputsplit) if inputsplit  >= 0 else "") + ".root"
    dic["outputroot"] = "hist" + ("_" + str(inputsplit) if inputsplit >= 0 else "") + ".root"
    dic["DEBUG"] = False
    return dic

def main():
    start_time = time.time()
    global inputpath
    inputpath = CONF.inputpath + "TEST/"
    global outputpath
    outputpath = CONF.outputpath + "test/"
    helpers.checkpath(outputpath)
    #for testing
    #analysis(pack_input("zjets_test"))

    #real job; full chain 2 mins...just data is 50 seconds
    nsplit = 7
    inputtasks = []
    # inputtasks.append(pack_input("ttbar_comb_test"))
    # inputtasks.append(pack_input("zjets_test"))
    # for i, mass in enumerate(CONF.mass_lst):
    #     inputtasks.append(pack_input("signal_G_hh_c10_M" + str(mass)))
    for i in range(nsplit):
        inputtasks.append(pack_input("data_test", inputsplit=i))
    #parallel compute!
    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool = mp.Pool(npool)
    pool.map(analysis, inputtasks)
    #all the other extra set of MCs
    targetpath = outputpath + "data_test/"
    targetfiles = glob.glob(targetpath + "hist_*.root")
    haddcommand = ["hadd", "-f", targetpath + "hist.root"]
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
