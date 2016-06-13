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
mass_lst = [700, 800, 900, 1000, 1100, 1200, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]


def main():

    ops = options()
    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")

    print output

    # set up to draw
    cut = "truth_2j_2trk/h0h1_jet_match"
    single_channel = ["h%d no match  ", "h%d match     ", "h%d mismatch ", "h%d 2 match  "]

    # cut = "truth_2j_2trk/b0b1_tj_match"
    # single_channel = ["b%s no match ", "b%s match ", "b%s mismatch ", "b%s 2 match ", "b%s miss "]

    p0_channel = [s % 0 for s in single_channel]
    p1_channel = [s % 1 for s in single_channel]
    channel_strs = [x+y for y in p1_channel for x in p0_channel]
    channel_strs = ["bad h matching"] + channel_strs

    DrawMatchingStats(output, "TEST", cut, channel_strs, "higgs-matching.pdf")
    output.Close()


def DrawMatchingStats(outputroot, inputdir, cut, channel_strs, outputfile, normalization=0):
    channels = np.zeros( [len(mass_lst), len(channel_strs)] )

    canv = ROOT.TCanvas(inputdir + "_" + str(normalization), "Efficinecy", 1000, 1000)

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
	if np.any(data[3:] > .02):
	    lines.append( ROOT.TGraph(len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
	    strlist.append(channel_strs[i])

    # add legend
    xleg, yleg = 0.55, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
 
    graph = ROOT.TMultiGraph()
    for j, (line, s) in enumerate(zip(lines,strlist)):
	line.SetMarkerStyle(20+j)
	# line.SetMarkerColor(1+j)
	line.SetMarkerColor(CONF.clr_lst[j])
	line.SetMarkerSize(1)
	graph.Add(line)
	legend.AddEntry(line, s, "apl")

    graph.SetMaximum(1.2) 
    graph.Draw("apc")

    # set axes
    graph.GetXaxis().SetTitle("RSG Mass [GeV]")
    graph.GetYaxis().SetTitle("Percentage")
    # graph.SetTitle("Jet to truth higgs Matching Statistics")
 
    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.02)
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

    canv.SaveAs(outputdir + outputfile)
    canv.Close()

def DrawJetTruthComp(outputroot, inputdir, outputname, normalization=0):
    # parameters for function
    # what higgs to plot, what size to make the dR jets, whether to make a plot of the important numbers
    plot_num = True
    dR = 1
    higgs_ind = 0

    # set up the canvas
    cuts = ["truth_2j_2trk/" + data for data in ["h0_2comp_dR", "h1_2comp_dR", "b0_2comp_dR", "b1_2comp_dR", "b2_2comp_dR", "b3_2comp_dR"] ]
    mass_plots = []

    double_counted = []
    not_counted = []
    mismatched_pt = []
    matched = []


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
    if plot_num:
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
	    line.SetMarkerColor(CONF.clr_lst[j])
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
        graph_array = []
        graph = ROOT.TMultiGraph()

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

            outputroot.cd()
            temp_mc.SetName("RSG" + "_" + str(mass) + "_" + cut.replace("/", "_"))
            temp_mc.Write()
            truth_mc = outputroot.Get(temp_mc.GetName())
            truth_mc.Scale(1/truth_mc.Integral())

	    graph_array.append( helpers.TH1toTAsym(truth_mc) )

            graph_array[-1].SetLineColor(CONF.clr_lst[j])
            graph_array[-1].SetMarkerStyle(20 + j)
            graph_array[-1].SetMarkerColor(CONF.clr_lst[j])
            graph_array[-1].SetMarkerSize(1)
            canv.cd()

	    graph.Add(graph_array[-1])
            legend.AddEntry(graph_array[-1], str(mass) + " GeV", "apl")

	    if j == 0:
	        Xaxis_str = graph_array[0].GetXaxis().GetTitle()
		Yaxis_str = graph_array[0].GetYaxis().GetTitle()

            input_mc.Close()

	graph.Draw("apc")

	# rebin the hist for pt
	# set other options
	graph.GetYaxis().SetTitle( Yaxis_str )
	graph.GetXaxis().SetNdivisions(505)
	if cut.split("_")[-1] == "pt":
	    graph.GetXaxis().SetTitle( Xaxis_str + " [GeV]")
	else:
	    graph.GetXaxis().SetTitle( Xaxis_str.replace("d","#Delta") )
	    dR_type = cut.split("/")[1][0:4]
	    if dR_type != "h0h1":
		graph.GetXaxis().SetRangeUser(0, 3)
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

        graph.SetMaximum(maxbincontent * 1.5)
        graph.SetMinimum(minbincontent)
        

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
