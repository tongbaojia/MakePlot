###Tony: improve to load branches for faster processing
###Performance is not garanteened. The way to register hists are slow
###For a quick on the fly anaysis, great.
###For a more proper anlaysis, do the c++ standard way please
import ROOT, rootlogon
import time, os
#import tree configuration
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('TinyTree.C')
#ROOT.gSystem.Load('TinyTree.h')

#input file path
def drawProgressBar(percent, barLen = 20):
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        elif i == int(barLen * percent):
            progress += ">"
        else:
            progress += " "
    print ("[ %s ] %.2f%%" % (progress, percent * 100))

def checkpath(outputpath):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

class eventHists:
    def __init__(self, region, outputroot):
        outputroot.cd()
        outputroot.mkdir(region)
        outputroot.cd(region)
        self.region = region
        self.mHH_l    = ROOT.TH1F("mHH_l", ";mHH [GeV]",  76,  200, 4000)
        self.mHH_pole = ROOT.TH1F("mHH_pole", ";mHH [GeV]",  76,  200, 4000)
        self.h0_m     = ROOT.TH1F("leadHCand_Mass", ";Mass [GeV]",    100,  0,   500)
        self.h1_m     = ROOT.TH1F("sublHCand_Mass", ";Mass [GeV]",    100,  0,   500)

    def Fill(self, event):
        self.mHH_l.Fill(event.mHH, event.weight)
        self.mHH_pole.Fill(event.mHH_pole, event.weight)
        self.h0_m.Fill(event.j0_m, event.weight)
        self.h1_m.Fill(event.j1_m, event.weight)

    def Write(self, outputroot):
        outputroot.cd(self.region)
        self.mHH_l.Write()
        self.mHH_pole.Write()
        self.h0_m.Write()
        self.h1_m.Write()

class massregionHists:
    def __init__(self, region, outputroot):
        #self.Incl = eventHists(region + "_" + "Incl", outputroot)
        self.Sideband = eventHists(region + "_" + "Sideband", outputroot)
        self.Control = eventHists(region + "_" + "Control", outputroot)
        self.Signal = eventHists(region + "_" + "Signal", outputroot)
        self.ZZ = eventHists(region + "_" + "ZZ", outputroot)
        self.Rhh20  = eventHists(region + "_" + "Rhh20", outputroot)
        self.Rhh30  = eventHists(region + "_" + "Rhh30", outputroot)
        self.Rhh40  = eventHists(region + "_" + "Rhh40", outputroot)
        self.Rhh50  = eventHists(region + "_" + "Rhh50", outputroot)
        self.Rhh60  = eventHists(region + "_" + "Rhh60", outputroot)
        self.Rhh70  = eventHists(region + "_" + "Rhh70", outputroot)
        self.Rhh80  = eventHists(region + "_" + "Rhh80", outputroot)
        self.Rhh90  = eventHists(region + "_" + "Rhh90", outputroot)
        self.Rhh100 = eventHists(region + "_" + "Rhh100", outputroot)
        self.Rhh110 = eventHists(region + "_" + "Rhh110", outputroot)
        self.Rhh120 = eventHists(region + "_" + "Rhh120", outputroot)
        self.Rhh130 = eventHists(region + "_" + "Rhh130", outputroot)
        self.Rhh140 = eventHists(region + "_" + "Rhh140", outputroot)
        self.Rhh150 = eventHists(region + "_" + "Rhh150", outputroot)
    def Fill(self, event):
        #self.Incl.Fill(event)
        if event.Xhh < 1.6:
            self.Signal.Fill(event)
        elif event.Rhh < 35.8:
            self.Control.Fill(event)
        elif event.Rhh < 108:
            self.Sideband.Fill(event)
        if event.Xhh > 1.6 and event.Xzz < 2.1:
            self.ZZ.Fill(event)

        #for mass mu qcd test
        if event.Xhh > 1.6 and event.Rhh < 20:
            self.Rhh20.Fill(event)
        elif event.Rhh < 30:
            self.Rhh30.Fill(event)
        elif event.Rhh < 30: 
            self.Rhh30.Fill(event)
        elif event.Rhh < 40: 
            self.Rhh40.Fill(event)
        elif event.Rhh < 50: 
            self.Rhh50.Fill(event)
        elif event.Rhh < 60: 
            self.Rhh60.Fill(event)
        elif event.Rhh < 70: 
            self.Rhh70.Fill(event)
        elif event.Rhh < 80: 
            self.Rhh80.Fill(event)
        elif event.Rhh < 90: 
            self.Rhh90.Fill(event)
        elif event.Rhh < 100: 
            self.Rhh100.Fill(event)
        elif event.Rhh < 110: 
            self.Rhh110.Fill(event)
        elif event.Rhh < 120: 
            self.Rhh120.Fill(event)
        elif event.Rhh < 130: 
            self.Rhh130.Fill(event)
        elif event.Rhh < 140: 
            self.Rhh140.Fill(event)
        elif event.Rhh < 150: 
            self.Rhh150.Fill(event)

    def Write(self, outputroot):
        #self.Incl.Write(outputroot)
        self.Sideband.Write(outputroot)
        self.Control.Write(outputroot)
        self.Signal.Write(outputroot)
        self.ZZ.Write(outputroot)
        self.Rhh20.Write(outputroot)
        self.Rhh30.Write(outputroot) 
        self.Rhh40.Write(outputroot) 
        self.Rhh50.Write(outputroot) 
        self.Rhh60.Write(outputroot) 
        self.Rhh70.Write(outputroot) 
        self.Rhh80.Write(outputroot) 
        self.Rhh90.Write(outputroot)
        self.Rhh100.Write(outputroot)
        self.Rhh110.Write(outputroot)
        self.Rhh120.Write(outputroot)
        self.Rhh130.Write(outputroot)
        self.Rhh140.Write(outputroot)
        self.Rhh150.Write(outputroot)


class trkregionHists:
    def __init__(self, region, outputroot):
        self.Trk0  = massregionHists(region, outputroot)
        #self.Trk1  = massregionHists(region + "_" + "1Trk", outputroot)
        #self.Trk2  = massregionHists(region + "_" + "2Trk", outputroot)
        self.Trk2s = massregionHists(region + "_" + "2Trk_split", outputroot)
        self.Trk3  = massregionHists(region + "_" + "3Trk", outputroot)
        self.Trk4  = massregionHists(region + "_" + "4Trk", outputroot)
    def Fill(self, event):
        self.Trk0.Fill(event)
        # if event.j0_nTrk >= 1 or event.j1_nTrk >= 1:
        #     self.Trk1.Fill(event)
        if event.j0_nTrk >= 1 and event.j1_nTrk >= 1:
            self.Trk2s.Fill(event)
        # if event.j0_nTrk >= 2 or event.j1_nTrk >= 2:
        #     self.Trk2.Fill(event)
        if (event.j0_nTrk >= 1 and event.j1_nTrk >= 2) or (event.j0_nTrk >= 2 and event.j1_nTrk >= 1):
            self.Trk3.Fill(event)
        if event.j0_nTrk >= 2 and event.j1_nTrk >= 2:
            self.Trk4.Fill(event)
    def Write(self, outputroot):
        self.Trk0.Write(outputroot)
        #self.Trk1.Write(outputroot)
        #self.Trk2.Write(outputroot)
        self.Trk2s.Write(outputroot)
        self.Trk3.Write(outputroot)
        self.Trk4.Write(outputroot)


class regionHists:
    def __init__(self, outputroot):
        self.NoTag  = trkregionHists("NoTag", outputroot)
        self.OneTag = trkregionHists("OneTag", outputroot)
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
            self.NoTag.Fill(event)

    def Write(self, outputroot):
        self.NoTag.Write(outputroot)
        self.OneTag.Write(outputroot)
        self.TwoTag.Write(outputroot)
        self.TwoTag_split.Write(outputroot)
        self.ThreeTag.Write(outputroot)
        self.FourTag.Write(outputroot)


def analysis(inputfile, outname="", DEBUG=False):
    checkpath(outputpath + inputfile)
    outroot = ROOT.TFile.Open(outputpath + inputfile + "/" + "hist.root", "recreate")
    AllHists = regionHists(outroot)
    #read the input file
    f = ROOT.TFile(inputpath + inputfile + "/" + "hist-MiniNTuple.root", "read")
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
            drawProgressBar(i/(N*1.0))
            #print i, " events done!"
        t.fChain.GetEntry(i)
        #print t.Xzz
        AllHists.Fill(t)

    #write all the output
    AllHists.Write(outroot)
    print "DONE with the " + inputfile  + " analysis!"
    #close the input file;
    del(t)
    outroot.Close()

def main():
    start_time = time.time()
    global inputpath
    inputpath = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/TEST/"
    global outputpath
    outputpath = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/mutest/"
    checkpath(outputpath)
    #full set of analysis
    # analysis("data_test")
    # analysis("zjets_test")
    # analysis("ttbar_comb_test")
    # mass_lst = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    # for i, mass in enumerate(mass_lst):
    #     analysis("signal_G_hh_c10_M" + str(mass))
    #all the other extra set of MCs
    analysis("signal_QCD") #2 mins!
    print("--- %s seconds ---" % (time.time() - start_time))
    print "Finish!"

#def clearbranches():
if __name__ == "__main__":
    main()
