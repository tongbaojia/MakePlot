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
    return parser.parse_args()

def main():

    ops = options()
    inputdir = ops.inputdir
    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "Plot/Other/"

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    ##starndard plots
    # ##paper plot

    # check reweighting in QCD MC
    for histname in ["leadHCand_trk0_Pt", "sublHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk1_Pt"]:
        DrawMulticomparison([
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"OneTag_Incl/" + histname, "leg":"1b;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_split_Incl/" + histname, "leg":"2bs;"}, 
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Incl/" + histname, "leg":"1b reweighted bkg;"},
            {"file":"../Moriond_bkgtrk_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Incl/" + histname, "leg":"1b reweighted bkgtrk;"},
            {"file":"../Moriond_j0pT-alltrk-fin_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Incl/" + histname, "leg":"1b reweighted alltrk;"},
            ], keyword=histname, norm=True, Xrange=[0, 1000], Rebin=5, Logy=1)

    for histname in ["mHH_l"]:
        DrawMulticomparison([
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"OneTag_Signal/" + histname, "leg":"1b;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_split_Signal/" + histname, "leg":"2bs;"}, 
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Signal/" + histname, "leg":"1b reweighted bkg;"},
            {"file":"../Moriond_bkgtrk_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Signal/" + histname, "leg":"1b reweighted bkgtrk;"},
            {"file":"../Moriond_j0pT-alltrk-fin_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Signal/" + histname, "leg":"1b reweighted alltrk;"},
            ], keyword=histname, norm=True, Xrange=[500, 3500], prename="SR", Rebin=10, Logy=1)
    
    for histname in ["mHH_l"]:
        DrawMulticomparison([
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"OneTag_Sideband/" + histname, "leg":"1b;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_split_Sideband/" + histname, "leg":"2bs;"}, 
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Sideband/" + histname, "leg":"1b reweighted bkg;"},
            {"file":"../Moriond_bkgtrk_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Sideband/" + histname, "leg":"1b reweighted bkgtrk;"},
            {"file":"../Moriond_j0pT-alltrk-fin_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Sideband/" + histname, "leg":"1b reweighted alltrk;"},
            ], keyword=histname, norm=True, Xrange=[500, 3500], prename="SB", Rebin=10, Logy=1)

    ##for QCD mHH shape study
    for histname in ["mHH_l"]:
        DrawMulticomparison([ 
            {"file":"../Moriond/sum_Moriond.root", "path":"qcd_TwoTag_split_Sideband_mHH_l", "leg":"Data;"},
            {"file":"../Moriond/sum_Moriond.root", "path":"qcd_est_TwoTag_split_Sideband_mHH_l", "leg":"DataEst;"},
            {"file":"../Moriond_bkg_5/sum_Moriond_bkg_5.root", "path":"qcd_est_TwoTag_split_Sideband_mHH_l", "leg":"New DataEst;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_split_Sideband/" + histname, "leg":"DijetMC;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"OneTag_Sideband/" + histname, "leg":"1bDijetMC noreweight;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Sideband/" + histname, "leg":"1bDijetMC reweighted;"},
            ], keyword=histname, norm=True, Xrange=[500, 3500], prename="SB", Rebin=10, Logy=1)

    # ##for QCD mHH shape study
    for histname in ["mHH_l"]:
        DrawMulticomparison([ 
            #{"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_Sideband/" + histname, "leg":"0b;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"OneTag_Sideband/" + histname, "leg":"1b;"},
            #{"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_Sideband/" + histname, "leg":"2b;"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Sideband/" + histname, "leg":"1b; reweighted bkg"},
            {"file":"../Moriond_j0pT-alltrk-fin_5/signal_QCD/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Sideband/" + histname, "leg":"1b; reweighted alltrk"},
            {"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_split_Sideband/" + histname, "leg":"2bs;"},
            #{"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"ThreeTag_Sideband/" + histname, "leg":"3b;"},
            #{"file":"../Moriond_bkg_5/signal_QCD/hist-MiniNTuple.root", "path":"FourTag_Sideband/" + histname, "leg":"4b;"},
            ], keyword=histname, prename="MC", norm=True, Xrange=[500, 3500], Rebin=10, Logy=1)
    for histname in ["mHH_l"]:
        DrawMulticomparison([ 
            #{"file":"../Moriond/sum_Moriond.root", "path":"qcd_NoTag_Sideband_" + histname, "leg":"0b;"},
            {"file":"../Moriond/sum_Moriond.root", "path":"qcd_OneTag_Sideband_" + histname, "leg":"1b;"},
            {"file":"../Moriond/sum_Moriond.root", "path":"qcd_TwoTag_Sideband_" + histname, "leg":"2b;"},
            {"file":"../Moriond/sum_Moriond.root", "path":"qcd_TwoTag_split_Sideband_" + histname, "leg":"2bs;"},
            #{"file":"../Moriond/sum_Moriond.root", "path":"qcd_ThreeTag_Sideband_" + histname, "leg":"3b;"},
            #{"file":"../Moriond/sum_Moriond.root", "path":"qcd_FourTag_Sideband_" + histname, "leg":"4b;"},
            ], keyword=histname, prename="Data",  norm=True, Xrange=[500, 3500], Rebin=10, Logy=1)


def DrawMulticomparison(inputlst, keyword="", prename="", Xrange=[0, 0], Yrange=[0, 0], norm=True, Logy=0, Rebin=1):
    #print inputdir
    tempname = "directcompare" + "_" + keyword + ("" if Logy == 0 else "_" + str(Logy))
    canv = ROOT.TCanvas(tempname, tempname, 800, 800)
    # two pad
    pad0 = ROOT.TPad("pad0", "pad0", 0.0, 0.31, 1., 1.)
    pad0.SetRightMargin(0.05)
    pad0.SetBottomMargin(0.0001)
    pad0.SetFrameFillColor(0)
    pad0.SetFrameBorderMode(0)
    pad0.SetFrameFillColor(0)
    pad0.SetBorderMode(0)
    pad0.SetBorderSize(0)

    pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.0, 1., 0.30)
    pad1.SetRightMargin(0.05)
    pad1.SetBottomMargin(0.38)
    pad1.SetTopMargin(0.0001)
    pad1.SetFrameFillColor(0)
    pad1.SetFillStyle(0) # transparent
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(0)


    #top pad
    canv.cd()
    pad0.SetLogy(Logy)
    pad0.Draw()
    pad0.cd()

    xleg, yleg = 0.5, 0.6
    legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.3)
    counter = 0
    maxbincontent = (0.05 if Logy ==0 else 10)
    temphst_lst = []
    graph_lst   = []
    tempratio_lst = []

    for i, dic in enumerate(inputlst):
        #print dic["file"], dic["path"] ##?????
        refroot = ROOT.TFile.Open(inputpath + dic["file"])
        temphst_lst.append(refroot.Get(dic["path"]).Clone())
        tempratio_lst.append(refroot.Get(dic["path"]).Clone(dic["path"] + "_ratio"))
        temphst_lst[i].SetDirectory(0) #otherwise the hist lives in the current open file
        tempratio_lst[i].SetDirectory(0) #otherwise the hist lives in the current open file

        if Rebin != 1:
            temphst_lst[i].Rebin(Rebin)
            tempratio_lst[i].Rebin(Rebin)
        
        if norm:
            temphst_lst[i].Scale(temphst_lst[0].Integral(0, temphst_lst[0].GetXaxis().GetNbins()+1)/temphst_lst[i].Integral(0, temphst_lst[i].GetXaxis().GetNbins()+1))

        for j in range(1, temphst_lst[0].GetNbinsX()+1):
            try:
                tempratio_lst[i].SetBinContent(j, temphst_lst[i].GetBinContent(j) / temphst_lst[0].GetBinContent(j))
                tempratio_lst[i].SetBinError(j, helpers.ratioerror(\
                    temphst_lst[i].GetBinContent(j), temphst_lst[0].GetBinContent(j), \
                    temphst_lst[i].GetBinError(j), temphst_lst[0].GetBinError(j)))
            except ZeroDivisionError:
                pass
                #print "Divide by zero! Check bin content in", canv.GetName()


        maxbincontent = max(maxbincontent, temphst_lst[i].GetMaximum())
        #graph_lst.append(helpers.TH1toTAsym(temphst_lst[i], efficiency=False))
        temphst_lst[i].SetLineColor(1 if i == 0 else CONF.clr_lst[i])
        #temphst_lst[i].SetLineStyle(1 + i)
        temphst_lst[i].SetMarkerStyle(20 + i)
        temphst_lst[i].SetMarkerColor(1 if i == 0 else CONF.clr_lst[i])
        temphst_lst[i].SetMarkerSize(1)
        temphst_lst[i].SetMaximum(maxbincontent * (1.5 if Logy == 0 else 150))
        temphst_lst[i].SetMinimum(0.001 if Logy == 0 else 0.2)
        if Xrange != [0, 0]:
            temphst_lst[i].GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
        legend.AddEntry(temphst_lst[i], dic["leg"] + " KS: " + str(('%.3g' % temphst_lst[i].KolmogorovTest(temphst_lst[0], "QU"))), "pl")
        temphst_lst[i].Draw("EP" if i==0 else "hist same")
        refroot.Close()
    
    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw watermarks
    xatlas, yatlas = 0.28, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "Simulations")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    info  = ROOT.TLatex(xatlas, yatlas-0.06, keyword.replace("data_est_", "").replace("_mHH_l", "").replace("_", " "))
    watermarks = [atlas, info]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()

    #bottom pad
    canv.cd()
    pad1.Draw()
    pad1.cd()
    for i, dic in enumerate(inputlst):
        tempratio_lst[i].SetLineColor(1 if i == 0 else CONF.clr_lst[i])
        #tempratio_lst[i].SetLineStyle(1 + i)
        tempratio_lst[i].SetMarkerStyle(20 + i)
        tempratio_lst[i].SetMarkerColor(1 if i == 0 else CONF.clr_lst[i])
        tempratio_lst[i].SetMarkerSize(1)
        tempratio_lst[i].GetYaxis().SetTitleFont(43)
        tempratio_lst[i].GetYaxis().SetTitleSize(28)
        tempratio_lst[i].GetYaxis().SetLabelFont(43)
        tempratio_lst[i].GetYaxis().SetLabelSize(28)
        tempratio_lst[i].GetYaxis().SetTitle("ratio to ref")
        tempratio_lst[i].GetYaxis().SetRangeUser(0.6, 1.5) #set range for ratio plot
        tempratio_lst[i].GetYaxis().SetNdivisions(405)
        tempratio_lst[i].GetXaxis().SetTitleFont(43)
        tempratio_lst[i].GetXaxis().SetTitleOffset(3.5)
        tempratio_lst[i].GetXaxis().SetTitleSize(28)
        tempratio_lst[i].GetXaxis().SetLabelFont(43)
        tempratio_lst[i].GetXaxis().SetLabelSize(28)
        if Xrange != [0, 0]:
            tempratio_lst[i].GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
        if i > 0:
            tempratio_lst[i].Draw("ep" if i == 1 else "ep same")
    # draw the ratio 1 line
    line = ROOT.TLine(Xrange[0], 1.0, Xrange[1], 1.0)
    line.SetLineStyle(1)
    line.Draw()

    #save and clean up
    canv.SaveAs(outputpath + canv.GetName() + ("_" + prename + "_" if prename is not "" else "") + ".pdf")
    pad0.Close()
    pad1.Close()
    canv.Close()
    del(tempratio_lst)
    del(temphst_lst)
    del(graph_lst)

if __name__ == "__main__":
    main()
