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
import numpy as np

ROOT.gROOT.SetBatch(True)
from ROOT import *    
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
SetAtlasStyle()


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
    parser.add_argument("--Xhh", action='store_true')
    return parser.parse_args()

def main():
    global ops
    ops = options()
    inputdir = ops.inputdir
    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "Plot/Other/"
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    ##paper plot
    Compare_Optimise(targetdir="AllTag_Signal", targetplot="hCandDeta")
    Compare_Optimise(targetdir="TwoTag_split_Signal", targetplot="hCandDeta", masslist=[2500, 2750, 3000])
    Compare_Optimise(targetdir="ThreeTag_Signal", targetplot="hCandDeta", masslist=[1600, 1800, 2000, 2500, 2750])
    Compare_Optimise(targetdir="FourTag_Signal", targetplot="hCandDeta", masslist=[1000, 1200, 1500, 1600, 1800])

def Compare_Optimise(targetdir="AllTag_Signal", targetplot="hCandDeta", masslist=[1000, 1200, 1500, 1800, 2000, 2500, 3000]):
    print targetdir, targetplot
    canv = ROOT.TCanvas(targetdir + "_" + targetplot, "Optimizer", 800, 800)
    xleg, yleg = 0.52, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    # load input MC file
    eff_lst = []
    graph_lst = []
    maxbincontent = 0.0001
    minbincontent = 0.00001

    for i, mass in enumerate(masslist):
        print mass, 
        eff_lst.append(Optimise("data_test/hist-MiniNTuple.root", ("signal_G_hh_c10_M" if not ops.Xhh else "signal_X_hh_M") + str(mass) + "/hist-MiniNTuple.root", "NoTag_Signal", targetdir, targetplot))
        maxbincontent = max(eff_lst[i].GetMaximum(), maxbincontent)

        canv.cd()
        #convert it to a TGraph
        graph_lst.append(helpers.TH1toTAsym(eff_lst[i]))
        graph_lst[i].SetLineColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerStyle(20 + i)
        graph_lst[i].SetMarkerColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerSize(1)
        graph_lst[i].SetMaximum(maxbincontent * 1.5)
        graph_lst[i].SetMinimum(minbincontent)
        legend.AddEntry(graph_lst[i], str(mass).replace("_", " "), "apl")
        if i == 0: 
            graph_lst[i].Draw("APC")
            #gr.Draw("same L hist")
        else: 
            graph_lst[i].Draw("PC")
            #gr.Draw("same L hist")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw reference lines
    yline05 = ROOT.TLine(1000, 0.0, 1000, maxbincontent)
    yline05.SetLineStyle(9)
    yline05.Draw()
    yline10 = ROOT.TLine(2000, 0.0, 2000, maxbincontent)
    yline10.SetLineStyle(9)
    yline10.Draw()
    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0" if not ops.Xhh else "2HDM")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    watermarks = [atlas, hh4b, lumi]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()
    # finish up
    # canv.SetLogy(1)
    canv.SaveAs(outputpath + ("G10_"if not ops.Xhh else "2HDM_") +  canv.GetName() + ".pdf")
    canv.Close()


def Optimise(bkgfile, sigfile, bkgpath, sigpath, plot="hCandDeta"):
    #print bkgpath, sigpath, plot
    bkginput = ROOT.TFile.Open(inputpath + bkgfile)
    siginput = ROOT.TFile.Open(inputpath + sigfile)

    bkghist = bkginput.Get(bkgpath + "/" + plot)
    sighist = siginput.Get(sigpath + "/" + plot)

    optimized_hist = BestCut(bkghist, sighist)
    optimized_hist.SetDirectory(0)

    bkginput.Close()
    siginput.Close()
    
    return optimized_hist


def BestCut(bkghist, sighist):
    cut = 0
    if (bkghist.GetXaxis().GetNbins() != sighist.GetXaxis().GetNbins()):
        print "wrong imput dimensions! Check inputs please!"
        return

    maxsig = 0
    maxcut = 0
    temp_hist = ROOT.TH1F(sighist.GetName(), "; %s; Signficance" % sighist.GetName(), bkghist.GetXaxis().GetNbins(), bkghist.GetXaxis().GetXmin(), bkghist.GetXaxis().GetXmax())
    for i in range(0, bkghist.GetXaxis().GetNbins()):
        bkgerr = ROOT.Double(0.)
        bkg = bkghist.IntegralAndError(0, i, bkgerr)
        sigerr = ROOT.Double(0.)
        sig = sighist.IntegralAndError(0, i, sigerr)
        temp_hist.SetBinContent(i, (sig/(1 + ROOT.TMath.Sqrt(bkg))))
        temp_hist.SetBinError(i, (sigerr/(1 + ROOT.TMath.Sqrt(bkg))))
        if ((sig/(1 + ROOT.TMath.Sqrt(bkg))) > maxsig):
            maxsig = (sig/(1 + ROOT.TMath.Sqrt(bkg)))
            maxcut = bkghist.GetXaxis().GetBinCenter(i)
        #print (sig/(1 + ROOT.TMath.Sqrt(bkg))), bkghist.GetXaxis().GetBinCenter(i)
    print ("%.3f, %.2f" % (maxsig, maxcut))
    
    return temp_hist

if __name__ == "__main__":
    main()
