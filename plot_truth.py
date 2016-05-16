import ROOT, rootlogon
import argparse
import copy
import glob
import helpers
import os
import sys
import time
#end of import for now

ROOT.gROOT.SetBatch(True)

#set global variables
#set output directory
outputdir = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Plot/"
mass_lst = [1000, 2000, 3000]
#mass_lst = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]


def main():

    ops = options()
    # create output file
    output = ROOT.TFile.Open("/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Plot/sig_truth.root", "recreate")
    # select the cuts
    cut_lst = ["truth_2j_2trk/nh_matched", "truth_2j_2trk/nb_matched", \
    "truth_2j_2trk/nh_double_matched", "truth_2j_2trk/nb_double_matched",\
    "truth_3j_3trk/nh_matched", "truth_3j_3trk/nb_matched", \
    "truth_3j_3trk/nh_double_matched", "truth_3j_3trk/nb_double_matched"]

    # # Draw the efficiency plot relative to the all normalization
    DrawSignalTruth(output, cut_lst, "TEST", "truth_")

    output.Close()


def DrawSignalTruth(outputroot, cut_lst, inputdir, outputname="", normalization=0):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region

    # setup basic plot parameters
    lowmass = -50
    highmass = 3150
    # load input MC file
    maxbincontent = 1
    minbincontent = -0.01

    for i, cut in enumerate(cut_lst):

        canv = ROOT.TCanvas(inputdir + "_" + outputname + str(normalization), "Efficiency", 800, 800)
        xleg, yleg = 0.55, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)

        for j, mass in enumerate(mass_lst):
            #here could be changed to have more options
            input_mc = ROOT.TFile.Open("/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/" + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass)
            temp_mc = input_mc.Get(cut).Clone()
            outputroot.cd()
            temp_mc.SetName("RSG" + "_" + str(mass) + "_" + cut.replace("/", "_"))
            temp_mc.Write()
            truth_mc = outputroot.Get(temp_mc.GetName())
            truth_mc.SetLineColor(1 + j)
            truth_mc.SetMarkerStyle(20 + j)
            truth_mc.SetMarkerColor(1 + j)
            truth_mc.SetMarkerSize(1)
            truth_mc.Scale(1/truth_mc.Integral())
            truth_mc.SetMaximum(maxbincontent * 1.5)
            truth_mc.SetMinimum(minbincontent)
            canv.cd()
            if j==0: 
                truth_mc.Draw("epl")
            else: 
                truth_mc.Draw("same epl")

            legend.AddEntry(truth_mc, str(mass) + " GeV", "apl")
            input_mc.Close()
        
        legend.SetBorderSize(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.04)
        legend.Draw()

        # draw watermarks
        xatlas, yatlas = 0.35, 0.87
        atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
        hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0")
        lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
        watermarks = [atlas, hh4b, lumi]

        for wm in watermarks:
            wm.SetTextAlign(22)
            wm.SetTextSize(0.04)
            wm.SetTextFont(42)
            wm.SetNDC()
            wm.Draw()

        # finish up
        outputroot.cd()
        canv.SaveAs(outputdir + cut.replace("/", "_") + "_" + canv.GetName() + ".pdf")
        canv.Close()


def ratioerror(a, b):
    if a > 0:
        return a / b * ROOT.TMath.Sqrt(1.0/a + 1.0/b)
    else:
        return 0

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="TEST")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def warn(message):
    print
    print "Warning in %s: %s" % (__file__, message)
    print

if __name__ == "__main__":
    main()
