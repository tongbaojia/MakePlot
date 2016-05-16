import ROOT, rootlogon
import argparse
import array
import copy
import glob
import helpers
import os
import sys
import time

ROOT.gROOT.SetBatch(True)
#set output directory
outputdir = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Plot/"

def main():

    ops = options()
    inputdir = ops.inputdir
    inputroot = ops.inputroot
    # create output file
    output = ROOT.TFile.Open("/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Plot/sig_prediction.root", "recreate")
    # select the cuts
    # cut_sig_lst = ["2Trk_OneTag_Signal_Significance", "2Trk_TwoTag_split_Signal_Significance",\
    # "3Trk_OneTag_Signal_Significance", "3Trk_TwoTag_Signal_Significance", "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance",\
    # "4Trk_OneTag_Signal_Significance", "4Trk_TwoTag_Signal_Significance", "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]
    # cut_sig_lst = ["2Trk_OneTag_Signal_Significance", "2Trk_TwoTag_split_Signal_Significance",\
    # "3Trk_OneTag_Signal_Significance", "3Trk_TwoTag_Signal_Significance", "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance",\
    # "4Trk_OneTag_Signal_Significance", "4Trk_TwoTag_Signal_Significance", "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]
    # cut_sig_lst = ["2Trk_TwoTag_split_Signal_Significance",\
    # "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance",\
    # "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]
    
    cut_sig_lst = ["OneTag_Signal_Significance", "TwoTag_split_Signal_Significance",\
    "TwoTag_Signal_Significance", "ThreeTag_Signal_Significance",\
    "FourTag_Signal_Significance", "ThreeTag_1loose_Signal_Significance", "TwoTag_split_1loose_Signal_Significance", "TwoTag_split_2loose_Signal_Significance"]

    # cut_sig_lst = ["2Trk_in1_OneTag_Signal_Significance", "2Trk_in1_TwoTag_Signal_Significance", \
    #     "2Trk_OneTag_Signal_Significance", "2Trk_TwoTag_split_Signal_Significance", \
    #     "3Trk_OneTag_Signal_Significance", "3Trk_TwoTag_Signal_Significance", "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance", \
    #     "4Trk_OneTag_Signal_Significance", "4Trk_TwoTag_Signal_Significance", "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]

    # Draw the efficiency plot relative to the all normalization
    #DrawSignalEff(cut_sig_lst, "TEST_b77", "Significance", 100)
    # b_tag = [70, 77, 80, 85, 90]
    
    DrawSignalEff(cut_sig_lst, inputdir, inputroot, "bag", 0.005, (2400, 3100))
    DrawSignalEff(cut_sig_lst, inputdir, inputroot, "bag", 0.05, (1750, 2450))
    DrawSignalEff(cut_sig_lst, inputdir, inputroot, "bag", 0.2, (1450, 2450))
    DrawSignalEff(cut_sig_lst, inputdir, inputroot, "bag", 1.5)
    #DrawSignalEff(cut_sig_lst, "TEST_b%i" % i, "Significance", 0.2, (400, 850))
    # Draw the efficiency plot relative to the signal region

    output.Close()

def ratioerror(a, b):
    if a > 0:
        return a / b * ROOT.TMath.Sqrt(1.0/a + 1.0/b)
    else:
        return 0

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    parser.add_argument("--inputroot", default="sum")
    return parser.parse_args()

def DrawSignalEff(cut_lst, inputdir="b77", inputroot="sum", outputname="", normalization=1.0, plotrange=(0, 3100)):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region

    canv = ROOT.TCanvas(inputroot + "_" + str(normalization), "Efficiency", 800, 800)
    xleg, yleg = 0.55, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    lowmass = -50
    highmass = 3150
    # load input MC file
    input_mc = ROOT.TFile.Open("/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/" + inputdir + "/" + inputroot + "_" + inputdir + ".root")
    maxbincontent = normalization
    minbincontent = 0.00001
    temp_all = input_mc.Get(cut_lst[0]).Clone()
    temp_all.SetName("Combined")

    input_mc_b77 = ROOT.TFile.Open("/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/b77/" + "sum_b77" + ".root")
    temp_current = input_mc_b77.Get(cut_lst[0]).Clone()
    temp_current.SetName("Run2-b77")

    for j in range(1, temp_all.GetNbinsX()+1):
            temp_all.SetBinContent(j, 0)
            temp_all.SetBinError(j, 0)
            temp_current.SetBinContent(j, 0)
            temp_current.SetBinError(j, 0)
            temp_all.SetMinimum(minbincontent)
            temp_current.SetMinimum(minbincontent)

    for i, cut in enumerate(cut_lst):
        #print cut
        cutflow_mc = input_mc.Get(cut) #get the input histogram
        cutflow_mc_b77 = input_mc_b77.Get(cut) #get the input histogram
        for j in range(1, temp_all.GetNbinsX()+1):
            #temp_all.SetBinContent(j, ROOT.TMath.Sqrt(temp_all.GetBinContent(j) * temp_all.GetBinContent(j) + cutflow_mc.GetBinContent(j) * cutflow_mc.GetBinContent(j)))
            if ("4Trk_ThreeTag_Signal" in cut) or ("4Trk_FourTag_Signal" in cut):
                temp_current.SetBinContent(j, ROOT.TMath.Sqrt(temp_current.GetBinContent(j) * temp_current.GetBinContent(j) + cutflow_mc_b77.GetBinContent(j) * cutflow_mc_b77.GetBinContent(j)))
            else:
                temp_all.SetBinContent(j, ROOT.TMath.Sqrt(temp_all.GetBinContent(j) * temp_all.GetBinContent(j) + cutflow_mc.GetBinContent(j) * cutflow_mc.GetBinContent(j)))

        cutflow_mc.SetMaximum(maxbincontent * 1.5)
        cutflow_mc.SetMinimum(minbincontent)
        cutflow_mc.SetLineColor(i%7 + 1)
        cutflow_mc.SetMarkerStyle(20 + i)
        cutflow_mc.SetMarkerColor(i%7 + 1)
        cutflow_mc.SetMarkerSize(1)
        cutflow_mc.GetXaxis().SetRangeUser(plotrange[0], plotrange[1])
        legend.AddEntry(cutflow_mc, cut.replace("_", " "), "apl")
        canv.cd()
        if cut==cut_lst[0]: 
            cutflow_mc.Draw("epl")
        else: 
            cutflow_mc.Draw("same epl")

    temp_all.SetLineColor(2)
    temp_all.SetMarkerStyle(5)
    temp_all.SetMarkerColor(2)
    temp_all.SetMarkerSize(1)
    temp_all.GetXaxis().SetRangeUser(plotrange[0], plotrange[1])
    legend.AddEntry(temp_all, temp_all.GetName(), "apl")
    temp_all.Draw("same ep")

    temp_current.SetLineColor(1)
    temp_current.SetMarkerStyle(4)
    temp_current.SetMarkerColor(1)
    temp_current.SetMarkerSize(1)
    temp_current.GetXaxis().SetRangeUser(plotrange[0], plotrange[1])
    legend.AddEntry(temp_current, temp_current.GetName(), "apl")
    temp_current.Draw("same ep")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.02)
    legend.Draw()

    # draw reference lines
    xline05 = ROOT.TLine(lowmass, 0.05, highmass, 0.05)
    xline05.SetLineStyle(3)
    xline05.Draw()
    xline10 = ROOT.TLine(lowmass, 0.1, highmass, 0.1)
    xline10.SetLineStyle(4)
    xline10.Draw()
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

    #canv.SetLogy()
    # finish up
    canv.SaveAs(outputdir + outputname + "_" + canv.GetName() + "_" + str(plotrange[0]) + "_" +  str(plotrange[1]) + ".pdf")
    canv.Clear()
    input_mc.Close()
    input_mc_b77.Close()



if __name__ == "__main__":
    main()
