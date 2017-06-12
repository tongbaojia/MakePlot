import ROOT, rootlogon
import argparse
import copy
import glob
import helpers
import os
import sys
import time
import config as CONF
from array import array
import numpy as np
#end of import for now
##Created by Gray. Not useful for now.

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.SetAtlasStyle()

#set global variables
#set output directory
outputdir = CONF.outplotpath
mass_lst = [1000, 1500, 2000, 2500, 3000]
# mass_lst = [700, 800, 900, 1000, 1100, 1200, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
# mass_lst = mass_lst[3:-1]

def main():

    ops = options()
    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")

    print output
    # select the cuts
    cut_lst = [path + data for path in ["truth_general_data/"]
		for data in ["h0b0_dR"]]
    """
		for data in ["nh0_pt", "nh1_pt", "nb0_pt", "nb1_pt", "nb2_pt", 
				"nb3_pt", "h0h1_dR", "h0b0_dR", "h1b2_dR", 
				"b0b1_dR", "b2b3_dR"]]
    """
    # # Draw the efficiency plot relative to the all normalization
    DrawSignalTruth(output, cut_lst, "BTAG_TEST", "truth_")
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
    maxbincontent = .4 # approx
    minbincontent = -0.01

    for i, cut in enumerate(cut_lst):
        canv = ROOT.TCanvas(inputdir + "_" + outputname + str(normalization), "Efficiency", 800, 800)
        xleg, yleg = 0.55, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)

        for j, mass in enumerate(mass_lst):
            #here could be changed to have more options
            input_mc = ROOT.TFile.Open(CONF.inputpath + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass)
	    if not input_mc:
		print CONF.inputpath + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass
	    try:
                temp_mc = input_mc.Get(cut).Clone()
	    except:
		print CONF.inputpath + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass
		print cut
		print mass
		raise

	    # rebin the hist for pt
	    # set other options
	    if cut.split("_")[-1] == "pt":
		temp_mc.Rebin(10)
		temp_mc.GetXaxis().SetTitle( temp_mc.GetXaxis().GetTitle() + " [GeV]")
	    else:
		#temp_mc.GetXaxis().SetTitle( temp_mc.GetXaxis().GetTitle().replace("dR","#DeltaR") )
		temp_mc.GetXaxis().SetTitle( "#DeltaR between H, child b")
		dR_type = cut.split("/")[1][0:4]
		if dR_type != "h0h1":
		    temp_mc.GetXaxis().SetRangeUser(0, 3)
		    maxbincontent = 1.0/1.5
		else:
		    maxbincontent = .5
		if dR_type == "h1b2" or dR_type == "h0b0":
		    dR1_line = ROOT.TLine(1, 0, 1, maxbincontent)
		    dR04_line = ROOT.TLine(.4, 0, .4, maxbincontent)
		    dR1_line.Draw("")	
		    dR04_line.Draw("")
		elif dR_type == "b0b1" or dR_type == "b2b3":
		    dR1_line = ROOT.TLine(2, 0, 2, maxbincontent)
                    dR04_line = ROOT.TLine(.8, 0, .8, maxbincontent)
                    dR1_line.Draw("")           
                    dR04_line.Draw("") 	


            outputroot.cd()
            temp_mc.SetName("RSG" + "_" + str(mass) + "_" + cut.replace("/", "_"))
            temp_mc.Write()
            truth_mc = outputroot.Get(temp_mc.GetName())
            truth_mc.SetLineColor(CONF.clr_lst[j])
            truth_mc.SetMarkerStyle(20 + j)
            truth_mc.SetMarkerColor(CONF.clr_lst[j])
            truth_mc.SetMarkerSize(1)
            truth_mc.Scale(1/truth_mc.Integral())
            truth_mc.SetMaximum(maxbincontent * 1.5)
            truth_mc.SetMinimum(minbincontent)
            canv.cd()
            if j==0: 
                truth_mc.Draw("")
            else: 
                truth_mc.Draw("same")

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
