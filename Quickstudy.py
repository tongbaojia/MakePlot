###Tony: this is designed to plot directly from the TinyTree; could be adapted to draw from MiniTree
###Note the functions here; one ability is to draw time wise comparison
import ROOT, helpers
import config as CONF
import time, os, subprocess, glob, argparse, compiler, csv
#for parallel processing!
import multiprocessing as mp
import rootlogon
#import tree configuration
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('TinyTree.C')
ROOT.gROOT.LoadMacro('MiniTree.C')
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",  default="TEST")
    parser.add_argument("--outputdir",  default="TEST")
    return parser.parse_args()

class TempPlots:
    def __init__(self, outputroot, outname):
        outputroot.cd()
        self.outname  = outname
        self.plotdic  = {}

    def Plot1D(self, name, title, x, nbinsx, xmin, xmax, weight=1.):
        if name not in self.plotdic:
            self.plotdic[name] = ROOT.TH1F(name, title, nbinsx, xmin, xmax)
        self.plotdic[name].Fill(x, weight)

    def Plot2D(self, name, title, x, y, nbinsx, nbinsy, xmin, xmax, ymin, ymax, weight=1.):
        if name not in self.plotdic:
            self.plotdic[name] = ROOT.TH2F(name, title, nbinsx, nbinsy, xmin, xmax, ymin, ymax)
        self.plotdic[name].Fill(x, y, weight)

    def Write(self, outputroot):
        outputroot.cd()
        for pltname in self.plotdic:
            self.plotdic[pltname].Write()
            #save hist as pdf as well
            canv = ROOT.TCanvas(pltname, " ", 600, 600)
            if self.plotdic[pltname].InheritsFrom("TH2"):
                self.plotdic[pltname].Draw("colz")
                canv.SaveAs(outputpath + self.outname + "_" + pltname + ".pdf")

                canv.Clear()
                temp_prox = self.plotdic[pltname].ProfileX()
                temp_prox.GetYaxis().SetTitle(self.plotdic[pltname].GetYaxis().GetTitle())
                temp_prox.SetMaximum(self.plotdic[pltname].GetYaxis().GetBinUpEdge(self.plotdic[pltname].GetYaxis().GetNbins()))
                canv.Clear()
                temp_prox.Draw()
                canv.SaveAs(outputpath + self.outname + "_" +  canv.GetName() + "_profx.pdf")
            else:
                self.plotdic[pltname].Draw()
                canv.SaveAs(outputpath + self.outname + "_" + pltname + ".pdf")
            del(canv)

def TinyAnalysis(inputfile, outname="", DEBUG=False):
    '''this runs on Tiny Ntuple; quick studies and checks'''
    #read the input file
    f = ROOT.TFile(inputfile, "read")
    #load the target tree
    t = ROOT.TinyTree(f.Get("TinyTree"))
    #load the plotter
    outroot = ROOT.TFile.Open(outputpath + outname + "temp.root", "recreate")
    plt = TempPlots(outroot, outname)
    #if need lumi for each run
    with open('script/lumitable.csv', mode='r') as infile:
        reader = csv.reader(infile)
        lumitable = dict((rows[0],rows[6]) for rows in reader)
    firstrun = 276262
    lastrun  = 311481
    #print lumitable
    #start looping through events
    N = t.fChain.GetEntries()
    for i in range(N):
    # get the next tree in the chain and verify
        if DEBUG & (i > 100000):
            break
        if i %50000 == 0:
            helpers.drawProgressBar(i/(N*1.0))

        t.fChain.GetEntry(i)


        #print t.Xzz
        ''' ##this peak can be faked because around 1250, 2m/pT ~ 0.2, thus the two track jet start to merge to one
            ##so requiring a large R jet to have one and only one track jet basically is selecting 
            ##the high pT jets that will merge, and hence the bump '''
        # if (t.j0_pt > 500): #& (t.j1_pt < 800):
        #     if (t.j0_nTrk == 1):
        #         if (t.Xzz > 2.1) & (t.Xzz < 4.2): 
        #             plt.Plot1D("m_ZZ_control", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)
        #             plt.Plot1D("j0_pt_ZZ_control", "j0 pT; j0 pT, GeV;", t.j0_pt, 60, 500, 2500)
        #         elif (t.Xzz < 2.1):     
        #             plt.Plot1D("m_ZZ_signal", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)
        #             plt.Plot1D("j0_pt_ZZ_signal", "j0 pT; j0 pT, GeV;", t.j0_pt, 60, 500, 2500)

        #         if (t.Xhh > 2.1) & (t.Xhh < 4.2): 
        #             plt.Plot1D("m_HH_control", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)
        #         elif (t.Xhh < 2.1):     
        #             plt.Plot1D("m_HH_signal", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)

        ''' check the Xhh vs pT '''
        XhhExp = (ROOT.TMath.Sqrt(ROOT.TMath.Power((t.j0_m - 124)/(0.085*t.j0_m), 2) + ROOT.TMath.Power((t.j1_m - 115)/(0.12*t.j1_m), 2))) ##with pT dependent cut
        plt.Plot2D("pT_Xhh", ";pT leadH; Xhh;", t.j0_pt, XhhExp, 50, 500, 2000, 42, -0.1, 2)
        plt.Plot2D("pT_Xhh_Corr", ";pT leadH; Xhh Corr;", t.j0_pt, t.Xhh, 50, 500, 2000, 42, -0.1, 2)

        '''check if the number of events in consistent in runs'''
        # if t.Xhh > 1.6 and t.Rhh < 35.8:
        #     #print t.runNumber
        #     if (t.j0_nb == 0 and t.j1_nb == 0) :
        #         plt.Plot1D("N_0b_CR", "N_0b; RunNumber; 0b-tag events in CR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 1 and t.j1_nb == 0) or (t.j0_nb == 0 and t.j1_nb == 1) :
        #         plt.Plot1D("N_1b_CR", "N_1b; RunNumber; 1b-tag events in CR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 2 and t.j1_nb == 0) or (t.j0_nb == 0 and t.j1_nb == 2) :
        #         plt.Plot1D("N_2b_CR", "N_2b; RunNumber; 2b-tag events in CR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 1 and t.j1_nb == 1):
        #         plt.Plot1D("N_2bs_CR", "N_2bs; RunNumber; 2bs-tag events in CR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 1 and t.j1_nb == 2) or (t.j0_nb == 2 and t.j1_nb == 1) :
        #         plt.Plot1D("N_3b_CR", "N_3b; RunNumber; 3b-tag events in CR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 2 and t.j1_nb == 2):
        #         plt.Plot1D("N_4b_CR", "N_4b; RunNumber; 4b-tag events in CR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        # if t.Xhh < 1.6:
        #     #print t.runNumber
        #     if (t.j0_nb == 0 and t.j1_nb == 0) :
        #         plt.Plot1D("N_0b_SR", "N_0b; RunNumber; 0b-tag events in SR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 1 and t.j1_nb == 0) or (t.j0_nb == 0 and t.j1_nb == 1) :
        #         plt.Plot1D("N_1b_SR", "N_1b; RunNumber; 1b-tag events in SR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 2 and t.j1_nb == 0) or (t.j0_nb == 0 and t.j1_nb == 2) :
        #         plt.Plot1D("N_2b_SR", "N_2b; RunNumber; 2b-tag events in SR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 1 and t.j1_nb == 1):
        #         plt.Plot1D("N_2bs_SR", "N_2bs; RunNumber; 2bs-tag events in SR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 1 and t.j1_nb == 2) or (t.j0_nb == 2 and t.j1_nb == 1) :
        #         plt.Plot1D("N_3b_SR", "N_3b; RunNumber; 3b-tag events in SR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        #     if (t.j0_nb == 2 and t.j1_nb == 2):
        #         plt.Plot1D("N_4b_SR", "N_4b; RunNumber; 4b-tag events in SR per ipb", t.runNumber,  lastrun - firstrun + 10000, firstrun - 5000, lastrun + 5000, 1/float(lumitable[str(int(t.runNumber))]))
        
        ##for signal region studies
        #if t.Xhh < 1.6:
            ## understad if 2b events, the b-tagged jet and the un-b tagged jet have any difference ##
            # if (t.j0_nb == 2 and t.j1_nb == 0):
            #     plt.Plot1D("2b_bjet_pT", "pT; b-tagged large R jet, pT, GeV;", t.j0_pt,  36, 200, 2000) #, t.weight)
            #     plt.Plot1D("2b_non_bjet_pT", "pT; non b-tagged large R jet, pT, GeV;", t.j1_pt,  36, 200, 2000) #, t.weight)
            #     #trkjets
            #     plt.Plot1D("2b_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j0_trk0_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot1D("2b_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j0_trk1_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot1D("2b_non_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j1_trk0_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot1D("2b_non_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j1_trk1_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot2D("2b_bjet_pT_drtrk", "pT J vs trk dR; b-tagged large R jet, pT, GeV; dR trkjets;", t.j0_pt, helpers.dR(t.j0_trk0_eta, t.j0_trk0_phi, t.j0_trk1_eta, t.j0_trk1_phi), 36, 200, 2000, 11, -0.2, 2) #, t.weight)
            #     plt.Plot2D("2b_non_bjet_pT_drtrk", "pT J vs trk dR; b-tagged large R jet, pT, GeV; dR trkjets;", t.j1_pt, helpers.dR(t.j1_trk0_eta, t.j1_trk0_phi, t.j1_trk1_eta, t.j1_trk1_phi), 36, 200, 2000, 11, -0.2, 2) #, t.weight)

            # elif (t.j0_nb == 0 and t.j1_nb == 2):
            #     plt.Plot1D("2b_bjet_pT", "pT; b-tagged large R jet, pT, GeV;", t.j1_pt,  36, 200, 2000) #, t.weight)
            #     plt.Plot1D("2b_non_bjet_pT", "pT; non b-tagged large R jet, pT, GeV;", t.j0_pt,  36, 200, 2000) #, t.weight)
            #     #trkjets
            #     plt.Plot1D("2b_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j1_trk0_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot1D("2b_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j1_trk1_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot1D("2b_non_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j0_trk0_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot1D("2b_non_bjet_trkpT", "trkpT; b-tagged jet, trackjet, pT, GeV;", t.j0_trk1_pt,  20, 0, 500) #, t.weight)
            #     plt.Plot2D("2b_bjet_pT_drtrk", "pT J vs trk dR; b-tagged large R jet, pT, GeV; dR trkjets;", t.j1_pt, helpers.dR(t.j1_trk0_eta, t.j1_trk0_phi, t.j1_trk1_eta, t.j1_trk1_phi), 36, 200, 2000, 11, -0.2, 2) #, t.weight)
            #     plt.Plot2D("2b_non_bjet_pT_drtrk", "pT J vs trk dR; b-tagged large R jet, pT, GeV; dR trkjets;", t.j0_pt, helpers.dR(t.j0_trk0_eta, t.j0_trk0_phi, t.j0_trk1_eta, t.j0_trk1_phi), 36, 200, 2000, 11, -0.2, 2) #, t.weight)


            ### test rest frame reco ###
            # if (t.mHH > 2300 or t.mHH < 1700):
            #     continue
            # hcand0 = ROOT.TLorentzVector()
            # hcand0.SetPtEtaPhiM(t.j0_pt, t.j0_eta, t.j0_phi, t.j0_m)
            # hcand1 = ROOT.TLorentzVector()
            # hcand1.SetPtEtaPhiM(t.j1_pt, t.j1_eta, t.j1_phi, t.j1_m)
            # hcand0_b0 = ROOT.TLorentzVector()
            # hcand0_b0.SetPtEtaPhiM(t.j0_trk0_pt, t.j0_trk0_eta, t.j0_trk0_phi, t.j0_trk0_m)
            # hcand0_b1 = ROOT.TLorentzVector()
            # hcand0_b1.SetPtEtaPhiM(t.j0_trk1_pt, t.j0_trk1_eta, t.j0_trk1_phi, t.j0_trk1_m)
            # hcand1_b0 = ROOT.TLorentzVector()
            # hcand1_b0.SetPtEtaPhiM(t.j1_trk0_pt, t.j1_trk0_eta, t.j1_trk0_phi, t.j1_trk0_m)
            # hcand1_b1 = ROOT.TLorentzVector()
            # hcand1_b1.SetPtEtaPhiM(t.j1_trk1_pt, t.j1_trk1_eta, t.j1_trk1_phi, t.j1_trk1_m)
            # hcand0_boost = hcand0.BoostVector()
            # G_boost = (hcand0 + hcand1).BoostVector()
            # ##see if the hcand boosted backwards is back to back
            # #hcand0.Boost(-G_boost)
            # #hcand1.Boost(-G_boost)
            # sumTrk = hcand0_b0 + hcand0_b1  + hcand1_b0 + hcand1_b1
            # sumTrk.Boost(-G_boost)
            # plt.Plot1D("m_frac", "mass fraction; mass fraction;", (hcand0_b0 + hcand0_b1 + hcand1_b0 + hcand1_b1 ).M()/(hcand0 + hcand1).M(), 20, 0, 1)
            # plt.Plot1D("pt_frac", "pt fraction; pt fraction;", (hcand0_b0 + hcand0_b1  + hcand1_b0 + hcand1_b1 ).Pt()/(hcand0 + hcand1).Pt(), 20, 0, 1)
            # plt.Plot1D("dr_frac", "dR 4 trkjets; dR 4trkjets-2largejets;", (hcand0_b0 + hcand0_b1  + hcand1_b0 + hcand1_b1 ).DeltaR(hcand0 + hcand1), 31, -0.2, 6) #, t.weight)
            # plt.Plot1D("dphi_frac", "dphi 4 trkjets; dphi 4trkjets-2largejets;", (hcand0_b0 + hcand0_b1  + hcand1_b0 + hcand1_b1 ).DeltaPhi(hcand0 + hcand1), 31, -0.2, 6) #, t.weight)
            # plt.Plot1D("sum_trkpt", "pt 4 trkjets; pt 4trkjets GeV;", (sumTrk).Pt(), 100, 0, 200) #, t.weight)
            
            # if t.j0_nTrk >= 2:                
            #     hcand0_b0.Boost(-hcand0_boost)
            #     hcand0_b1.Boost(-hcand0_boost)
            #     plt.Plot1D("drtrk_rest", "dR trkjets; dR trkjets rest;", hcand0_b0.DeltaR(hcand0_b1), 31, -0.2, 6) #, t.weight)
            #     plt.Plot1D("trk0_rest_pt", "trk0_rest_pt; trk0 pT rest, GeV;", hcand0_b0.Pt(), 100, 0, 200) #, t.weight)
            #     plt.Plot1D("trk0_rest_m", "trk0_rest_m; trk0 Mass rest, GeV;", hcand0_b0.M(), 100, 0, 200) #, t.weight)
            #     plt.Plot1D("trk1_rest_pt", "trk1_rest_pt; trk1 pT rest, GeV;", hcand0_b1.Pt(), 100, 0, 200) #, t.weight)


            #hcand1 = ROOT.TLorentzVector()
            #hcand1.SetPtEtaPhiM(t.j1_pt, t.j1_eta, t.j1_phi, t.j1_m)
            # plt.Plot2D("drtrk_mHH_signal", "pT JJ; MJJ, GeV; dR trkjets;", t.mHH, helpers.dR(t.j0_trk0_eta, t.j0_trk0_phi, t.j0_trk1_eta, t.j0_trk1_phi), 50, 0, 4000, 44, -0.2, 2) #, t.weight)
            # plt.Plot2D("drtrk_mHH_signal", "pT JJ; MJJ, GeV; dR trkjets;", t.mHH, helpers.dR(t.j1_trk0_eta, t.j1_trk0_phi, t.j1_trk1_eta, t.j1_trk1_phi), 50, 0, 4000, 44, -0.2, 2) #, t.weight)

    plt.Write(outroot)           
    print "DONE with the analysis!"
    #close the input file;
    del(t)
    outroot.Close()

def MiniAnalysis(inputfile, outname="", DEBUG=True):
    '''this runs on Mini Ntuple; in depth studies'''
    #read the input file
    f = ROOT.TFile(inputfile, "read")
    #load the target tree
    t = ROOT.MiniTree(f.Get("XhhMiniNtuple"))
    #load the plotter
    outroot = ROOT.TFile.Open(outputpath + outname + "temp.root", "recreate")
    plt = TempPlots(outroot, outname)
    #start looping through events
    N = t.fChain.GetEntries()
    for i in range(N):
    # get the next tree in the chain and verify
        if DEBUG:
            #debug trigger list
            for trig in t.passedTriggers:
                print trig
            if i > 1:
                break

        if i %10000 == 0:
            helpers.drawProgressBar(i/(N*1.0))
        else:
            pass

        t.fChain.GetEntry(i)
        #print t.Xzz
        # if (t.hcand_boosted_pt[0] > 500 * 1000): #& (t.j1_pt < 800):
        #     if (t.jet_ak2track_asso_n[0] == 1): #& (t.j1_pt < 800):
        #         plt.Plot1D("nTrks_1trkjet", "Number of tracks; nTrks;", t.hcand_boosted_nTrack[0], 80, -0.5, 79.5) #, t.weight)
        #     elif (t.jet_ak2track_asso_n[0] > 1):
        #         plt.Plot1D("nTrks_2trkjet", "Number of tracks; nTrks;", t.hcand_boosted_nTrack[0], 80, -0.5, 79.5) #, t.weight)
        # else:
        #     pass

        ##for quick trigger studies
        # TriggerDecision = False
        # TriggerDecision_4j = False
        # TriggerDecision_ht = False
        # TriggerDecision_lcw = False
        # for trig in t.passedTriggers:
        #     if "HLT_4j100" == trig:
        #         plt.Plot1D("HLT_4j100", "HLT_4j100; jetpt;", t.hcand_boosted_pt[0]/1000.0, 40, 0, 2000) #, t.weight)
        #         TriggerDecision = True
        #         TriggerDecision_4j = True
        #     if "HLT_ht1000_L1J100" == trig:
        #         plt.Plot1D("HLT_ht1000_L1J100", "HLT_ht1000_L1J100; jetpt;", t.hcand_boosted_pt[0]/1000.0, 40, 0, 2000) #, t.weight)
        #         TriggerDecision = True
        #         TriggerDecision_ht = True
        #     if "HLT_j420_a10_lcw_sub_L1J100" == trig:
        #         #print trig
        #         TriggerDecision_lcw = True
        #         TriggerDecision = True
        # if TriggerDecision_lcw:
        #     plt.Plot1D("HLT_j420_a10_lcw_sub_L1J100", "HLT_j420_a10_lcw_sub_L1J100; jetpt;", t.hcand_boosted_pt[0]/1000.0, 40, 0, 2000) #, t.weight)
        # if not TriggerDecision_lcw and TriggerDecision_ht:
        #     plt.Plot1D("HLT_recover", "HLT_recover; jetpt;", t.hcand_boosted_pt[0]/1000.0, 40, 0, 2000) #, t.weight)
        # if TriggerDecision:
        #     plt.Plot1D("HLT_all", "HLT_all; jetpt;", t.hcand_boosted_pt[0]/1000.0, 40, 0, 2000) #, t.weight)


    plt.Write(outroot)           
    print "DONE with the analysis!"
    #close the input file;
    del(t)
    outroot.Close()

def main():
    start_time = time.time()
    global ops
    ops = options()
    global inputpath
    inputpath = CONF.inputpath + ops.inputdir + "/"
    global outputpath
    outputpath = CONF.outputpath + ops.outputdir + "/tempplot/"
    helpers.checkpath(outputpath)

    #if do eos
    eosmcpath = CONF.toppath + "/eos/atlas/user/b/btong/bb/mc/v02-00-00/gridOutput/MiniNTuple/*mc15_13TeV"
    eosdatapath = CONF.toppath + "/eos/atlas/user/b/btong/bb/data/v02-00-00/gridOutput/MiniNTuple/*16_*periodB.*.root_skim"
    #start analysis on TinyNtuple
    mass = 3000
    TinyAnalysis(inputpath + "signal_G_hh_c10_M" + str(mass) + "/" + "hist-MiniNTuple.root", "signal_M" + str(mass)) #MC
    #TinyAnalysis(inputpath + "data_test/" + "hist-MiniNTuple.root", "data") #data
    #TinyAnalysis(inputpath + "data_test16/" + "hist-MiniNTuple.root", "data") #data
    ##start analysis on MiniNtuple
    #MiniAnalysis(glob.glob(eosmcpath + "*G_hh_bbbb_c10*" + str(mass) + ".hh4b*.root_skim")[0], "signal_M" + str(mass)) #MC
    #MiniAnalysis(glob.glob(eosdatapath)[0], "data16") #data
    #MiniAnalysis(glob.glob("../test_mini/data-MiniNTuple/*.root_skim")[0], "signal_M" + str(mass)) #MC

    #finish
    print("--- %s seconds ---" % (time.time() - start_time))


#####################################
if __name__ == '__main__':
    main()

