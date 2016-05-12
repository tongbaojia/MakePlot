import argparse
import array
import copy
import os
import sys
import ROOT
import glob
import Xhh4bUtils.BkgFit.smoothfit as smoothfit

treename  = "XhhMiniNtuple"
ROOT.gROOT.SetBatch()
mass_lst = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
cut_lst = ["TwoTag_split", "ThreeTag", "FourTag"]

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

def main():
    ops = options()
    inputdir = ops.inputdir
    #setup basics
    dump(inputdir)

def dump(filename):

    ops = options()
    inputpath = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/" + filename 
    outputpath = inputpath + "/Limitinput/"
    ifile = ROOT.TFile(inputpath + "/" + "sum_" + filename + ".root")

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    for c in cut_lst:
        print "start ", c, " file conversion "
        outfile  = ROOT.TFile("%s/%s_limit_%s.root" % (outputpath, filename, c), "RECREATE")
        #get the mass plot
        cut = c + "_Signal_mHH_l" 
        savehist(ifile, outfile, "data_est_" + cut,  "data_hh")#blind data now
        savehist(ifile, outfile, "data_est_" + cut,  "totalbkg_hh", True)
        savehist(ifile, outfile, "qcd_est_" + cut,   "qcd_hh", True)
        savehist(ifile, outfile, "ttbar_est_" + cut, "ttbar_hh", True, smoothfunc="Exp")
        savehist(ifile, outfile, "zjet_" + cut,      "zjet_hh")

        for mass in mass_lst:
            savehist(ifile, outfile, "RSG1_" + str(mass) + "_" + cut, "signal_RSG_c10_hh_m" + str(mass))
        outfile.Close()

    ifile.Close()
    print "Done! "

def savehist(inputroot, outputroot, inname, outname, dosmooth=False, smoothrange = (1000, 2500), smoothfunc="Dijet"):
    hist  = inputroot.Get(inname).Clone()
    if dosmooth:
        sm = smoothfit.smoothfit(hist, fitFunction = smoothfunc, fitRange = smoothrange, \
            makePlots = True, verbose = False, outfileName=outputroot.GetName()[:-5] + "_" + outname + "_fit.root")
        hist = smoothfit.MakeSmoothHisto(hist, sm["nom"])
    hist.SetName(outname)
    hist.SetTitle(outname)
    #hist.SetBins(60, 200, 3200)
    outputroot.cd()
    hist.Write()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

if __name__ == '__main__': 
    main()
