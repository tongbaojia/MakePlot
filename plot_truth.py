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
# mass_lst = mass_lst[3:-1]

def main():

    ops = options()
    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")

    print output
    # select the cuts
    cut_lst = [path + data for path in ["truth_2j_2trk/"]
		for data in ["nh0_pt", "nh1_pt", "nb0_pt", "nb1_pt", "nb2_pt", 
				"nb3_pt", "h0h1_dR", "h0b0_dR", "h1b2_dR", 
				"b0b1_dR", "b2b3_dR"]]

    # # Draw the efficiency plot relative to the all normalization
    # DrawSignalTruth(output, cut_lst, "TEST", "truth_")
    # DrawJetTruthComp(output, "TEST", "truthcomp_")
    DrawMatchingStats(output, "TEST", "")
    output.Close()


def DrawMatchingStats(outputroot, inputdir, outputname, normalization=0):
    cut = "truth_2j_2trk/h0h1_jet_match"
    single_channel = ["h%d 0-count  ", "h%d match    ", "h%d mismatch ", "h%d 2-count  "]
    h0_channel = [s % 0 for s in single_channel]
    h1_channel = [s % 1 for s in single_channel]
 
    channel_strs = [x+y for y in h1_channel for x in h0_channel]
    channels = np.zeros( [len(mass_lst), len(channel_strs)] )

    canv = ROOT.TCanvas(inputdir + "_" + outputname + str(normalization), "Efficinecy", 1000, 1000)

    for i,mass in enumerate(mass_lst):
	inp = ROOT.TFile.Open(CONF.inputpath + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass)
	hist = inp.Get(cut).Clone()
	# normalize
	hist.Scale(1/hist.Integral())

	for j in range(1,len(channel_strs)):
	    channels[i,j-1] = hist.GetBinContent(j)

	inp.Close()
		     

    # now generate the lines
    lines = []
    strlist = []
    for i in range(len(channel_strs)):
	data = np.copy(channels[:,i]).astype("float64")
	if np.any(data > .005):
	    lines.append( ROOT.TGraph(len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
	    strlist.append(channel_strs[i])

    # add legend
    xleg, yleg = 0.5, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
 
    graph = ROOT.TMultiGraph()
    for j, (line, s) in enumerate(zip(lines,strlist)):
	line.SetMarkerStyle(20+j)
	line.SetMarkerColor(1+j)
	line.SetMarkerSize(1)
	graph.Add(line)
	legend.AddEntry(line, s, "apl")

    graph.SetMaximum(1.2) 
    graph.Draw("apc")

    # set axes
    # graph.GetXaxis().SetTitle("RSG Mass")
    # graph.GetYaxis().SetTitle("Percentage")
    # graph.SetTitle("Jet to truth higgs Matching Statistics")
 
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

    canv.SaveAs(outputdir + "matching_stats.pdf")
    canv.Close()

def DrawJetTruthComp(outputroot, inputdir, outputname, normalization=0):
    # set up the canvas
    cuts = ["truth_2j_2trk/" + data for data in ["h0_2comp_dR", "h1_2comp_dR", "b0_2comp_dR", "b1_2comp_dR", "b2_2comp_dR", "b3_2comp_dR"] ]
    mass_plots = []

    double_counted = []
    not_counted = []
    mismatched_pt = []
    matched = []

    dR = 1
    higgs_ind = 0

    for mass in mass_lst:
	inp = ROOT.TFile.Open(CONF.inputpath + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass)
	hist_h0 = inp.Get("truth_2j_2trk/h0_2comp_dR").Clone()
	hist_h1 = inp.Get("truth_2j_2trk/h1_2comp_dR").Clone()

	# scale to unity
	hist_h0.Scale(1.0/hist_h0.Integral())
	hist_h1.Scale(1.0/hist_h1.Integral())

	# calculate important numbers
	xlim = ylim = dR
	binratio = 20
	
	double_counted.append( (hist_h0.Integral(0,int(xlim*binratio), 0 , int(ylim*binratio)) , hist_h1.Integral(0,int(xlim*binratio), 0 , int(ylim*binratio))) )

	not_counted.append( (hist_h0.Integral(int(xlim*binratio)+1, hist_h0.GetNbinsX(), int(ylim*binratio)+1, hist_h0.GetNbinsY()),
			     hist_h1.Integral(int(xlim*binratio)+1, hist_h1.GetNbinsX(), int(ylim*binratio)+1, hist_h1.GetNbinsY())) )
	mismatched_pt.append( (hist_h0.Integral(int(xlim*binratio)+1, hist_h0.GetNbinsX(), 0 , int(ylim*binratio)),
			       hist_h1.Integral(0,int(xlim*binratio), int(ylim*binratio)+1, hist_h1.GetNbinsY())) )
	matched.append( (hist_h0.Integral(0,int(xlim*binratio), int(ylim*binratio)+1, hist_h0.GetNbinsY()),
			 hist_h1.Integral(int(xlim*binratio)+1, hist_h1.GetNbinsX(), 0 , int(ylim*binratio))) )

	if mass in mass_plots:
            for i, cut in enumerate(cuts):

		hist = inp.Get(cut).Clone()
	        canv = ROOT.TCanvas(inputdir + "_" + outputname + str(normalization), "Efficinecy", 1000, 1000)

		outputroot.cd()
		hist.SetName("RSG" + "_" + str(mass) + cut.replace("/","_"))
		hist.Draw("colz")
		hist.Scale(1.0/hist.Integral())
		canv.cd()

		"""
		# draw the important numbers
		xnum, ynum = 0.7, 0.87       
 		n1 = ROOT.TLatex(xnum, ynum, "Double Counted: %.3f" % double_counted)
		n2 = ROOT.TLatex(xnum, ynum-.06, "Not Counted: %.3f" % not_counted)
		n3 = ROOT.TLatex(xnum, ynum-.06*2, "Mismatched Pt: %.3f" % mismatched_pt)
		n4 = ROOT.TLatex(xnum, ynum-.06*3, "Matched: %.3f" % matched)
		numbers = [n1, n2, n3, n4]
		for n in numbers:
		    n.SetTextAlign(22)
		    n.SetTextSize(0.04)
		    n.SetTextFont(42)
		    n.SetNDC()
		    n.Draw()
		"""

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
        	canv.SaveAs(outputdir + cut.split("/")[-1] + "_" + "M" + str(mass) + ".pdf")
        	canv.Close()

        inp.Close()
	
    # now plot the important numbers
    if True:
    	canv = ROOT.TCanvas(inputdir + "_" + outputname + str(normalization), "Efficinecy", 1000, 1000)

        # the lines that we'll plot
        lines = [ROOT.TGraph(len(mass_lst), array('d',mass_lst), array('d', [x[i][higgs_ind] for i in range(len(mass_lst))]) )
    		    for x in [double_counted, not_counted, mismatched_pt, matched]]


	# add legend
        xleg, yleg = 0.55, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
 
	graph = ROOT.TMultiGraph()
	strlist = ["Double Counted", "Not Counted", "Mismatched Pt", "Matched"]
	for j, (line, s) in enumerate(zip(lines,strlist)):
	    line.SetMarkerStyle(20+j)
	    line.SetMarkerColor(1+j)
	    line.SetMarkerSize(1)
	    graph.Add(line)
	    legend.AddEntry(line, s, "apl")

	graph.SetMaximum(1.2)       
	graph.Draw("apc")

	# set axes
	graph.GetXaxis().SetTitle("RSG Mass")
	graph.GetYaxis().SetTitle("Percentage")
	graph.SetTitle("Jet to truth %s-higgs Matching Statistics" % ("sublead" if higgs_ind else "lead"))
 
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

        canv.SaveAs(outputdir + "matching-h%i-dR%i.pdf" % (higgs_ind, dR*10 ) )
        canv.Close()

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
		temp_mc.GetXaxis().SetTitle( temp_mc.GetXaxis().GetTitle().replace("d","#Delta") )
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
            truth_mc.SetLineColor(1 + j)
            truth_mc.SetMarkerStyle(20 + j)
            truth_mc.SetMarkerColor(1 + j)
            truth_mc.SetMarkerSize(1)
            truth_mc.Scale(1/truth_mc.Integral())
            truth_mc.SetMaximum(maxbincontent * 1.5)
            truth_mc.SetMinimum(minbincontent)
            canv.cd()
            if j==0: 
                truth_mc.Draw("apc")
            else: 
                truth_mc.Draw("same apc")

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
