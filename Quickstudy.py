###Tony: this is designed to plot directly from the TinyTree; could be adapted to draw from MiniTree
import ROOT, helpers
import config as CONF
import time, os, subprocess, glob, argparse, compiler
#for parallel processing!
import multiprocessing as mp
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
            self.plotdic[name] = ROOT.TH1F(name, title, nbinsx, nbinsy, xmin, xmax, ymin, ymax)
        self.plotdic[name].Fill(x, y, weight)

    def Write(self, outputroot):
        outputroot.cd()
        for pltname in self.plotdic:
            self.plotdic[pltname].Write(
                )
            #save hist as pdf as well
            canv = ROOT.TCanvas(pltname, " ", 600, 600)
            self.plotdic[pltname].Draw()
            canv.SaveAs(outputpath + self.
                outname + "_" + pltname + ".pdf")
            del(canv)

def TinyAnalysis(inputfile, outname="", DEBUG=False):
    #read the input file
    f = ROOT.TFile(inputfile, "read")
    #load the target tree
    t = ROOT.TinyTree(f.Get("TinyTree"))
    #load the plotter
    outroot = ROOT.TFile.Open(outputpath + outname + "temp.root", "recreate")
    plt = TempPlots(outroot, outname)
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
        if (t.j0_pt > 500): #& (t.j1_pt < 800):
            if (t.j0_nTrk == 1):
                if (t.Xzz > 2.1) & (t.Xzz < 4.2): 
                    plt.Plot1D("m_ZZ_control", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)
                    plt.Plot1D("j0_pt_ZZ_control", "j0 pT; j0 pT, GeV;", t.j0_pt, 60, 500, 2500)
                elif (t.Xzz < 2.1):     
                    plt.Plot1D("m_ZZ_signal", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)
                    plt.Plot1D("j0_pt_ZZ_signal", "j0 pT; j0 pT, GeV;", t.j0_pt, 60, 500, 2500)

                if (t.Xhh > 2.1) & (t.Xhh < 4.2): 
                    plt.Plot1D("m_HH_control", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)
                elif (t.Xhh < 2.1):     
                    plt.Plot1D("m_HH_signal", "mass JJ; MJJ, GeV;", t.mHH, 25, 500, 4500) #, t.weight)

    plt.Write(outroot)           
    print "DONE with the analysis!"
    #close the input file;
    del(t)
    outroot.Close()


def MiniAnalysis(inputfile, outname="", DEBUG=False):
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
        if i %10000 == 0:
            helpers.drawProgressBar(i/(N*1.0))
        else:
            pass

        t.fChain.GetEntry(i)
        #print t.Xzz
        if (t.hcand_boosted_pt[0] > 500 * 1000): #& (t.j1_pt < 800):
            if (t.jet_ak2track_asso_n[0] == 1): #& (t.j1_pt < 800):
                plt.Plot1D("nTrks_1trkjet", "Number of tracks; nTrks;", t.hcand_boosted_nTrack[0], 80, -0.5, 79.5) #, t.weight)
            elif (t.jet_ak2track_asso_n[0] > 1):
                plt.Plot1D("nTrks_2trkjet", "Number of tracks; nTrks;", t.hcand_boosted_nTrack[0], 80, -0.5, 79.5) #, t.weight)
        else:
            pass

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
    #start analysis on TinyNtuple
    mass = 1400
    TinyAnalysis(inputpath + "signal_G_hh_c10_M" + str(mass) + "/" + "hist-MiniNTuple.root", "signal_M" + str(mass)) #MC
    #TinyAnalysis(inputpath + "data_test/" + "hist-MiniNTuple.root", "data") #data
    ##start analysis on MiniNtuple
    #MiniAnalysis(glob.glob(eosmcpath + "*G_hh_bbbb_c10*" + str(mass) + ".hh4b*.root_skim")[0], "signal_M" + str(mass)) #MC

    #finish
    print("--- %s seconds ---" % (time.time() - start_time))


#####################################
if __name__ == '__main__':
    main()

