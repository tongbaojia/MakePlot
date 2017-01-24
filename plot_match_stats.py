#Tony: made by Gray Putnam for truth matching studies
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

# whether to use PlotAll() or main()
plotall = False

# names for the legend
# bsingle_channel = ["b%s no match ", "b%s match ", "b%s mismatch ", "b%s 2 match ", "b%s miss "]
# bsingle_channel = ["b%s no match ", "b%s match 0 ", "b%s match 1 ", "b%s match 0,1 ", "b%s match 2 ", "b%s match 0,2 ", "b%s match 1,2 ", "b%s match 0,1,2 ", "b%s miss "]
bsingle_channel = ["b%s no match ", "b%s match-n ", "b%s match-b ", "b%s miss "]
hsingle_channel = ["h%d no match  ", "h%d match     ", "h%d mismatch ", "h%d 2 match  "]

inpsubdir = "TEST"

def main():

    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")

    print output

    # set up to draw
    # cut = "truth_general_data/h0h1_jet_match"
    cut = "truth_general_data/b2b3_tj_match"

    p0_channel = [s % 0 for s in hsingle_channel]
    p1_channel = [s % 1 for s in hsingle_channel]
    channel_strs = [x+y for y in p1_channel for x in p0_channel]
    # channel_strs = ["bad h matching"] + channel_strs

    DrawMatchingStats(output, inpsubdir, cut, channel_strs, "b-matching-all-sublead.pdf", cutoff=.01)
    output.Close()

# plots matching stats for h's and both pairs's of bs
def PlotAll():
    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")
    print output

    # first the higgs
    hcut = "truth_general_data/h0h1_jet_match"

    h0_channel = [s % 0 for s in hsingle_channel]
    h1_channel = [s % 1 for s in hsingle_channel]
    hchannel_strs = [x+y for y in h1_channel for x in h0_channel]
    DrawMatchingStats(output, inpsubdir, hcut, hchannel_strs, "higgs-matching.pdf")

    # now do the pairs of b's
    bpairs = [("truth_general_data/b0b1_tj_match", "hlead-b-matching-btag.pdf", 0.01) 
	     ,("truth_general_data/b2b3_tj_match", "hsublead-b-matching-btag.pdf", 0.03)]

    for bcut, sfile, cutoff in bpairs:
        p0_channel = [s % "hi" for s in bsingle_channel]
        p1_channel = [s % "lo" for s in bsingle_channel]
        channel_strs = [x+y for y in p1_channel for x in p0_channel]
        channel_strs = ["bad h matching"] + channel_strs

        DrawMatchingStats(output, inpsubdir, bcut, channel_strs, sfile, cutoff)
        
    output.Close()


def DrawMatchingStats(outputroot, inputdir, cut, channel_strs, outputfile, cutoff = 0.001, normalization=0):
    channels = np.zeros( [len(mass_lst), 26] )

    canv = ROOT.TCanvas(inputdir + "_" + str(normalization), "Efficinecy", 1000, 1000)

    for i,mass in enumerate(mass_lst):
	inp = ROOT.TFile.Open(CONF.inputpath + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass)
	try:
	    hist = inp.Get(cut).Clone()
	except:
	    if inp is None:
		print mass
	    print CONF.inputpath + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass
	    print cut
	    raise

	# normalize
	hist.Scale(1/hist.Integral())

	for j in range(1,len(channel_strs)):
	    channels[i,j-1] = hist.GetBinContent(j)

	inp.Close()
		     
    # now generate the lines
    lines = []
    strlist = []
    """
    for i in range(len(channel_strs)):
	data = np.copy(channels[:,i]).astype("float64")
	if np.any(data[3:] > cutoff):
	    lines.append( ROOT.TGraph(len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
	    strlist.append(channel_strs[i])
    # bsingle_channel = ["b%s no match ", "b%s match ", "b%s mismatch ", "b%s 2 match ", "b%s miss "]
    # bsingle channel = ["b no match", " bno b-tag", " b btag", "b miss"]
    bdata = np.zeros([3, channels.shape[0] ])
    bdata[0,:] = (channels[:,6]).astype("float64") 
    bdata[1,:] = (channels[:,7] + channels[:,10]).astype("float64") 
    bdata[2,:] =  (channels[:,11]).astype("float64") 
    norm = np.sum(bdata, axis=0)
    print bdata
    bdata = bdata/norm

    print norm

    data = bdata[0,:]
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "Neither b b-tagged" )

    data = bdata[1,:]
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "One b b-tagged" )

    data = bdata[2,:]
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "Both b's b-tagged" )

    """
    data = (channels[:,0]).astype("float64")
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "Bad Higgs Matching" ) 
    
    data = (channels[:,7] + channels[:,13]).astype("float64") 
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "Each b Matched to Unique Jet" )

    data = (channels[:,12] + channels[:,8]).astype("float64")
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "Both b's Matched to Same Jet" )

    data = (channels[:,9] + channels[:,14] + channels[:,17] + channels[:,18]).astype("float64")
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "One b Matched to 2 Jets. One Matched to 1" ) 

    data = (channels[:,2] + channels[:,3] + channels[:,6] + channels[:,11]).astype("float64")
    lines.append( ROOT.TGraph( len(mass_lst), np.array(mass_lst, dtype="float64"), data) )
    strlist.append( "One b Matched to 1 Jet. One Not Matched." )

    print (channels[:,1] + channels[:,4] + channels[:,5], channels[:,10] + channels[:,15] + channels[:,16] + np.sum(channels[:,19:-1], axis=1))

    # add legend
    xleg, yleg = 0.49, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
 
    graph = ROOT.TMultiGraph()
    for j, (line, s) in enumerate(zip(lines,strlist)):
	line.SetMarkerStyle(20+j)
	# line.SetMarkerColor(1+j)
	line.SetMarkerColor(CONF.clr_lst[j])
	line.SetLineColor(CONF.clr_lst[j])
	line.SetMarkerSize(1)
	graph.Add(line)
	legend.AddEntry(line, s, "apl")

    graph.SetMaximum(1.3) 
    graph.Draw("apc")

    # set axes
    graph.GetXaxis().SetTitle("RSG Mass [GeV]")
    graph.GetYaxis().SetTitle("Percentage")
    # graph.SetTitle("Jet to truth higgs Matching Statistics")
 
    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.02)
    legend.Draw()

    wm = helpers.DrawWatermarks()

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

		wm = helpers.DrawWatermarks()

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

	wm2 = helpers.DrawWatermarks()
        canv.SaveAs(outputdir + "matching-h%i-dR%i.pdf" % (higgs_ind, dR*10 ) )
        canv.Close()

if __name__ == "__main__":
    if plotall:
	PlotAll()
    else:
        main()
