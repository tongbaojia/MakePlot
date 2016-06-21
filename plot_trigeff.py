import ROOT, rootlogon
import argparse
import array
import copy
import glob
import helpers
import os
import sys
import time
import config as CONF

ROOT.gROOT.SetBatch(True)

def main():

    ops = options()
    inputdir = ops.inputdir

    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "Plot/Trigger/"

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    #set global draw options
    global mass_lst
    mass_lst = [700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    global lowmass
    lowmass = 650
    global highmass
    highmass = 3150
    # create output file
    #output = ROOT.TFile.Open(outuputpath + "sigeff.root", "recreate")
    # select the cuts
    cut_lst = ["PassTrig"]

    # Draw the efficiency plot relative to the all normalization
    DrawTrigEff(cut_lst, inputdir, outputname="trig", normalization="PreSel")
    DrawTrigEff(cut_lst, inputdir, outputname="trig", normalization="All")
    # Draw pT dependent trig efficiency; needs fix...
    #DrawPtEff(inputdir, outputname="trig")
    #output.Close()

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

def DrawTrigEff(cut_lst, inputdir, outputname="", normalization="All"):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region

    canv = ROOT.TCanvas(inputdir + "_" + "Efficiency" + "_" + normalization, "Efficiency", 800, 800)
    xleg, yleg = 0.55, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    # load input MC file
    eff_lst = []
    maxbincontent = 1
    minbincontent = -0.01
    for i, cut in enumerate(cut_lst):
        eff_lst.append( ROOT.TH1F(inputdir + "_" + cut, "%s; Mass, GeV; Efficiency" %cut, int((highmass-lowmass)/100), lowmass, highmass) )
        eff_lst[i].SetLineColor(2 + i)
        eff_lst[i].SetMarkerStyle(20 + i)
        eff_lst[i].SetMarkerColor(2 + i)
        eff_lst[i].SetMarkerSize(1)

        for mass in mass_lst:
            #here could be changed to have more options
            input_mc = ROOT.TFile.Open(inputpath + "signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass)
            cutflow_mc = input_mc.Get("CutFlowNoWeight") #notice here we use no weight for now!
            totevt_mc = 0
            totevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin(normalization))
            maxbincontent = 1
            cutevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin(cut))
            eff_lst[i].SetBinContent(eff_lst[i].GetXaxis().FindBin(mass), cutevt_mc/totevt_mc)
            eff_lst[i].SetBinError(eff_lst[i].GetXaxis().FindBin(mass), helpers.ratioerror(cutevt_mc, totevt_mc))
            # print ratioerror(cutevt_mc, totevt_mc)
            input_mc.Close()

        eff_lst[i].SetMaximum(maxbincontent * 1.5)
        eff_lst[i].SetMinimum(minbincontent)
        legend.AddEntry(eff_lst[i], cut.replace("_", " "), "apl")
        canv.cd()
        if cut==cut_lst[0]: 
            eff_lst[i].Draw("epl")
        else: 
            eff_lst[i].Draw("same epl")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw reference lines
    xline90 = ROOT.TLine(lowmass, 0.9, highmass, 0.9)
    xline90.SetLineStyle(3)
    xline90.Draw()
    xline95 = ROOT.TLine(lowmass, 0.95, highmass, 0.95)
    xline95.SetLineStyle(4)
    xline95.Draw()
    xline98 = ROOT.TLine(lowmass, 0.98, highmass, 0.98)
    xline98.SetLineStyle(5)
    xline98.Draw()
    yline05 = ROOT.TLine(1000, 0.0, 1000, maxbincontent)
    yline05.SetLineStyle(9)
    yline05.Draw()
    yline10 = ROOT.TLine(2000, 0.0, 2000, maxbincontent)
    yline10.SetLineStyle(9)
    yline10.Draw()
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
    canv.SaveAs(outputpath + outputname + "_" + canv.GetName() + ".pdf")
    canv.Close()
    

def DrawPtEff(inputdir, outputname=""):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region

    canv = ROOT.TCanvas(inputdir + "_pT_" + "Efficiency", "Efficiency", 800, 800)
    xleg, yleg = 0.55, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    # load input MC file
    eff_lst = []
    graph_lst = []
    maxbincontent = 1
    minbincontent = -0.01
    file_lst = ["data_test", "signal_G_hh_c10_M1000", "signal_G_hh_c10_M1100", "signal_G_hh_c10_M1200"]
    leg_lst  = ["Data16",    "RSG 1TeV", "RSG 1.1TeV", "RSG 1.2TeV"]
    for i, file in enumerate(file_lst):

        input_mc  = ROOT.TFile.Open(inputpath + file + "/hist-MiniNTuple.root")
        hist_tag  = input_mc.Get("h_leadHCand_pT_pre_trig").Clone() #hist before trigger
        hist_prob = input_mc.Get("h_leadHCand_pT_aft_trig").Clone() #hist after trigger

        xMin = hist_tag.GetXaxis().GetXmin()
        xMax = hist_tag.GetXaxis().GetXmax()
        #print xMin, xMax
        eff_lst.append(ROOT.TH1F(file + "_pT_eff", ";p_{T} [GeV]; Efficiency", hist_tag.GetXaxis().GetNbins(), xMin, xMax))

        for j in range(hist_tag.GetXaxis().GetNbins() + 1):
            #print j, hist_prob.GetBinContent(j), hist_prob.GetBinCenter(j)
            if hist_prob.GetBinContent(j) > 0:
                eff_lst[i].SetBinContent(j, hist_prob.GetBinContent(j)/hist_tag.GetBinContent(j))
                eff_lst[i].SetBinError(j, helpers.ratioerror(hist_prob.GetBinContent(j), hist_tag.GetBinContent(j), hist_prob.GetBinError(j), hist_tag.GetBinError(j)))
        
        graph_lst.append(helpers.TH1toTAsym(eff_lst[i]))
        graph_lst[i].SetLineColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerStyle(20 + i)
        graph_lst[i].SetMarkerColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerSize(1)
        graph_lst[i].SetMaximum(maxbincontent * 1.5)
        graph_lst[i].SetMinimum(minbincontent)
        legend.AddEntry(graph_lst[i], leg_lst[i].replace("_", " "), "apl")
        canv.cd()
        if i == 0: 
            graph_lst[i].Draw("APC")
        else: 
            graph_lst[i].Draw("PC")
        input_mc.Close()

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw reference lines
    xline90 = ROOT.TLine(xMin, 0.9, xMax, 0.9)
    xline90.SetLineStyle(3)
    xline90.Draw()
    xline95 = ROOT.TLine(xMin, 0.95, xMax, 0.95)
    xline95.SetLineStyle(4)
    xline95.Draw()
    xline98 = ROOT.TLine(xMin, 0.98, xMax, 0.98)
    xline98.SetLineStyle(5)
    xline98.Draw()
    
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
    canv.SaveAs(outputpath + outputname + "_" + canv.GetName() + ".pdf")
    canv.Close()
    

if __name__ == "__main__":
    main()
