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

ROOT.gROOT.SetBatch(True)

#set global variables
#set output directory
outputdir = CONF.outplotpath
# mass_lst = [1000, 1500, 2000, 2500, 3000]
mass_lst = [700, 800, 900, 1000, 1100, 1200, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]

def main():

    ops = options()
    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")

    print output
    # select the cuts
    cut_lst = [path + data for path in ["truth_general_data/"]
		# for data in ["h0_tj_pt_dR", "h1_tj_pt_dR"]]
		for data in ["h0_tj_pt_dR", "h1_tj_pt_dR", "h0_tj_match_pt_dR", "h1_tj_match_pt_dR"]] 

    # # Draw the efficiency plot relative to the all normalization
    DrawHists(output, cut_lst, "TEST", "MC_")
    output.Close()

def DrawHists(outputroot, cut_lst, inputdir, outputname="", normalization=0):
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

	bigmc = ROOT.TH2F(cut, "dR between lead, subleading track jet", 350, 0, 3500, 130, 0, 6.5)
	temp_mcs = []
	ROOT.SetOwnership(bigmc, False)

	dir_list = ["/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass for mass in mass_lst]
	# dir_list = ["/data_test/hist-MiniNTuple.root"]
        for j, d in enumerate(dir_list):
            #here could be changed to have more options
            input_mc = ROOT.TFile.Open(CONF.inputpath + inputdir + d)
	    if not input_mc:
		print CONF.inputpath + inputdir + d
	    try:
		temp_mcs.append( input_mc.Get(cut).Clone() )
		# temp_mcs[j].Scale(1/temp_mcs[j].Integral())
		bigmc.Add( temp_mcs[j] )
	    except:
		print CONF.inputpath + inputdir + d
		print cut
		raise

            input_mc.Close()

        # bigmc.Scale(1/bigmc.Integral())
        canv.cd()
	canv.SetLogz(1)
        bigmc.Draw("colz")
        # finish up
        outputroot.cd()
	canv.SetRightMargin(0.15)
        canv.SaveAs(outputdir + cut.replace("/", "_") + "_" + canv.GetName() + ".pdf")
        
	#profile x
	prename = cut.replace("/", "_")
	temp_prox = bigmc.ProfileX()
	temp_prox.GetYaxis().SetTitle(bigmc.GetYaxis().GetTitle())
	temp_prox.SetMaximum(temp_prox.GetMaximum() * 1.5)
	canv.Clear()
	temp_prox.Draw()
	# for wm in watermarks:
	#     wm.Draw()
	canv.SaveAs(outputdir + prename + "_" +  canv.GetName() + "_profx.pdf")
	#profile y
	canv.Clear()
	temp_proy = bigmc.ProfileY()
	temp_proy.GetYaxis().SetTitle(bigmc.GetXaxis().GetTitle())
	temp_proy.SetMaximum(temp_proy.GetMaximum() * 1.5)
	temp_proy.Draw()
	# for wm in watermarks:
	#    wm.Draw()
	canv.SaveAs(outputdir + prename + "_" +  canv.GetName() + "_profy.pdf")
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
