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

    # create output file
    output = ROOT.TFile.Open("/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Plot/sig_eff.root", "recreate")
    # select the cuts
    cut_lst = ["PassTrig", "PassDiJetPt", "PassDiJetEta", "PassDetaHH",  "PassBJetSkim", "PassSignal"]
    cut_sig_lst = ["2trk_0tag_signal", "3trk_0tag_signal", "4trk_0tag_signal", "2trk_1tag_signal", "3trk_1tag_signal", "4trk_1tag_signal"]
    #cut_sig_lst = ["2trk_2tag_split_signal", "3trk_2tag_split_signal", "3trk_2tag_signal", "3trk_3tag_signal", "4trk_2tag_split_signal", "4trk_2tag_signal", "4trk_3tag_signal", "4trk_4tag_signal"]

    # # Draw the efficiency plot relative to the all normalization
    # DrawSignalEff(cut_lst, "b70", "pre_")
    DrawSignalEff(cut_lst, "b77", "pre_")
    # DrawSignalEff(cut_lst, "b80", "pre_")
    # DrawSignalEff(cut_lst, "b85", "pre_")
    # DrawSignalEff(cut_lst, "b90", "pre_")
    # # Draw the efficiency plot relative to the all normalization
    # DrawSignalEff(cut_sig_lst, "b70", "")
    DrawSignalEff(cut_sig_lst, "b77", "")
    # DrawSignalEff(cut_sig_lst, "b80", "")
    # DrawSignalEff(cut_sig_lst, "b85", "")
    # DrawSignalEff(cut_sig_lst, "b90", "")
    # # Draw the efficiency plot relative to the signal region
    # DrawSignalEff(cut_sig_lst, "b70", "", 1)
    DrawSignalEff(cut_sig_lst, "b77", "", 1)
    # DrawSignalEff(cut_sig_lst, "b80", "", 1)
    # DrawSignalEff(cut_sig_lst, "b85", "", 1)
    # DrawSignalEff(cut_sig_lst, "b90", "", 1)

    output.Close()

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

def DrawSignalEff(cut_lst, inputdir, outputname="", normalization=0):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region

    canv = ROOT.TCanvas(inputdir + "_" + outputname + str(normalization) + "_" + "Efficiency", "Efficiency", 800, 800)
    xleg, yleg = 0.55, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    lowmass = -50
    highmass = 3150
    # load input MC file
    mass_lst = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    eff_lst = []
    maxbincontent = 1
    minbincontent = -0.01
    for i, cut in enumerate(cut_lst):
        eff_lst.append( ROOT.TH1F(inputdir + "_" + cut, "%s; Mass, GeV; Efficiency" %cut, 32, lowmass, highmass) )
        eff_lst[i].SetLineColor(1 + i)
        eff_lst[i].SetMarkerStyle(20 + i)
        eff_lst[i].SetMarkerColor(1 + i)
        eff_lst[i].SetMarkerSize(1)

        for mass in mass_lst:
            #here could be changed to have more options
            input_mc = ROOT.TFile.Open("/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/" + inputdir + "/signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass)
            cutflow_mc = input_mc.Get("CutFlowNoWeight") #notice here we use no weight for now!
            totevt_mc = 0
            if (normalization == 0): 
                totevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin("PreSel"))
                maxbincontent = 0.05
            if (normalization == 1): 
                totevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin("PassSignal"))
                maxbincontent = 0.6
            cutevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin(cut))
            eff_lst[i].SetBinContent(eff_lst[i].GetXaxis().FindBin(mass), cutevt_mc/totevt_mc)
            eff_lst[i].SetBinError(eff_lst[i].GetXaxis().FindBin(mass), ratioerror(cutevt_mc, totevt_mc))
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

    # finish up
    canv.SaveAs(outputdir + outputname + canv.GetName() + ".pdf")
    canv.Clear()



if __name__ == "__main__":
    main()
