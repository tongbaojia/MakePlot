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
#mass_lst = [700, 800, 900, 1000, 1100, 1200, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
mass_lst = [700, 800, 900, 1000, 1100, 1200, 1400, 1500, 2000, 2250, 2750, 3000]

def main():

    ops = options()
    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")

    print output
    cut_lst = [path + data for path in ["AllTag_Signal/"]
		for data in ["hh_deta"]]
		#for data in ["h0_tj0_pt_ratio", "h1_tj0_pt_ratio"]]
		#for data in ["h0_tj_pt_dR", "h1_tj_pt_dR", "h0_tj_match_pt_dR", "h1_tj_match_pt_dR"]] 

    tfiles = ["/signal_2HDM_hh_c10_M%i/hist-MiniNTuple.root" % mass for mass in mass_lst]
    #tfiles = ["/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass for mass in mass_lst]
    #tfiles = ["/data_test15/hist-MiniNTuple.root", "/data_test16/hist-MiniNTuple.root"]

    # # Draw the efficiency plot relative to the all normalization
    DrawHists(output, cut_lst, "F_c10-cb-b77-rhist2", tfiles, "2HDM_", Xrange=(0, 3500))
    output.Close()


def DrawHists(outputroot, cut_lst, inputdir, tfiles, outputname="", normalization=0, cutvals=None, Xrange=(0, 3500)):
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

	#bigmc = ROOT.TH2F(cut, "pt ratio of leading track jet", 350, 0, 3500, 300, 0, 3);
	bigmc = ROOT.TH2F(cut, "dR between lead, subleading track jet", 350, 0, 3500, 130, 0, 6.5)
	temp_mcs = []
	ROOT.SetOwnership(bigmc, False)


        for j, tf in enumerate(tfiles):
            #here could be changed to have more options
            input_mc = ROOT.TFile.Open(CONF.inputpath + inputdir + tf)
	    if not input_mc:
		print CONF.inputpath + inputdir + tf
	    try:
		temp_mcs.append( input_mc.Get(cut).Clone() )
		temp_mcs[j].Scale(1/temp_mcs[j].Integral())
		bigmc.Add( temp_mcs[j] )
	    except:
		print CONF.inputpath + inputdir + tf
		print cut
		raise

            input_mc.Close()

	bigmc.Rebin2D(10, 10)
	# rebin more for profile plots
        bigmc.GetYaxis().SetRangeUser(0,2)
	bigmc.GetXaxis().SetRangeUser(*Xrange)
	bigmc.GetXaxis().SetLabelSize(0.035)
	#bigmc.GetZaxis().SetRangeUser(.05, 0.5)
	bigmc.GetXaxis().SetTitle("Higgs pT [MeV]")
	bigmc.GetYaxis().SetTitle("trkjet #DeltaR")
	#bigmc.GetXaxis().SetTitle("Dijet Mass [MeV]")
	#bigmc.GetYaxis().SetTitle("hh #Delta#eta")
	# set contour
	# contours = np.array(reversed([1.0/(10^i) for i in range(6)]))
        # bigmc.SetContour(6, contours)
	# bigmc.GetZaxis().SetRangeUser(1e-7, 1e-2)

        canv.cd()
	canv.SetLogz(1)
        bigmc.Draw("colz")

	# cut line
	if cutvals is not None:
	    (mcut, dcut) = cutvals
	    xs = np.arange(Xrange[0], 1000, 10, dtype="float")
	    ys = np.array([mcut*2/x + dcut for x in xs])
	    cutline = ROOT.TPolyLine(xs.shape[0], xs, ys)
	    cutline.SetLineWidth(4)

	    xs2 = np.arange(Xrange[0], 1000, 10,dtype="float")
	    ys2 = np.array([mcut*2/x - dcut for x in xs2])
	    cutline2 = ROOT.TPolyLine(xs2.shape[0], xs2, ys2)
	    cutline2.SetLineWidth(4)

	    # cut line two
	    dashline = ROOT.TLine(1000.0, 0, 1000.0, 2.0)
	    dashline.SetLineWidth(4)
	    dashline.SetLineStyle(9)

	    cutline.Draw()
	    cutline2.Draw()
	    dashline.Draw()


	# print out bins
	for b in [1500, 2500]:
	    ix = bigmc.GetXaxis().FindBin(b)
	    ny = bigmc.GetNbinsY()
	    bins = []
	    print bigmc.GetXaxis().GetBinCenter(ix)
	    for iy in range(ny):
	        print bigmc.GetYaxis().GetBinCenter(iy), bigmc.GetBinContent(ix, iy)
	        bins.append( bigmc.GetBinContent(ix, iy) )

	    print sum([bins[i] * bigmc.GetYaxis().GetBinCenter(i) for i in range(ny)]) / sum(bins)

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
