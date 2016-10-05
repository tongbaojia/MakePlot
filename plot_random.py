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

    ##paper plot
    DrawPaper2D("data_test/hist-MiniNTuple.root", "NoTag_Incl", prename="NoTag_Incl_paper", Xrange=[10, 300], Yrange=[10, 350])  

    #region shape comparisons
    #side band shapes
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_Sideband", keyword="mH0H1", prename="Sideband", Xrange=[40, 250], Yrange=[40, 250])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_Control", keyword="mH0H1", prename="Control", Xrange=[40, 250], Yrange=[40, 250])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_ZZ", keyword="mH0H1", prename="ZZ", Xrange=[40, 250], Yrange=[40, 250])
    #DrawRegionPlot("data_test/hist-MiniNTuple.root", "NoTag", keyword="mH0H1", prename="Compare", Xrange=[40, 250], Yrange=[40, 250])
    #correlations of the jet mass and jet pT
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_Incl", keyword="leadHCand_trk0_pt_v_j_m", prename="NoTag_Incl", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_Incl", keyword="leadHCand_trk1_pt_v_j_m", prename="NoTag_Incl", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_Incl", keyword="sublHCand_trk0_pt_v_j_m", prename="NoTag_Incl", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_Incl", keyword="sublHCand_trk1_pt_v_j_m", prename="NoTag_Incl", Xrange=[10, 300], Yrange=[50, 200])
    
    #for study only, not in the main production
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "TwoTag_split_Sideband", keyword="leadHCand_trk0_pt_v_j_m", prename="TwoTag_split_Sideband", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "TwoTag_split_Sideband", keyword="leadHCand_trk1_pt_v_j_m", prename="TwoTag_split_Sideband", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "ThreeTag_Sideband", keyword="leadHCand_trk0_pt_v_j_m", prename="ThreeTag_Sideband", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("data_test/hist-MiniNTuple.root", "ThreeTag_Sideband", keyword="leadHCand_trk1_pt_v_j_m", prename="ThreeTag_Sideband", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("signal_G_hh_c10_M1500/hist-MiniNTuple.root", "AllTag_Incl", keyword="leadHCand_trk0_pt_v_j_m", prename="RSG1500_All_Incl", Xrange=[10, 300], Yrange=[50, 200])
    #DrawSignalPlot("signal_G_hh_c10_M1500/hist-MiniNTuple.root", "AllTag_Incl", keyword="leadHCand_trk1_pt_v_j_m", prename="RSG1500_All_Incl", Xrange=[10, 300], Yrange=[50, 200])
    
    #for MV2 studies
    #DrawBTaggingPlot("signal_G_hh_c10_M1500/hist-MiniNTuple.root", "AllTag_Signal", keyword="MV2H0", prename="RSG1500_All_Incl", Xrange=[-2, 2], Yrange=[-2, 2])
    DrawBTaggingPlot("signal_G_hh_c10_M1500/hist-MiniNTuple.root", "AllTag_Signal", keyword="MV2H1", prename="RSG1500_All_Incl", Xrange=[-2, 2], Yrange=[-2, 2])
    DrawBTaggingPlot("signal_G_hh_c10_M1500/hist-MiniNTuple.root", "AllTag_Signal", keyword="MV2H0H1", prename="RSG1500_All_Incl", Xrange=[-2, 2], Yrange=[-2, 2], dodouble=2)
    DrawBTaggingPlot("signal_G_hh_c10_M2500/hist-MiniNTuple.root", "AllTag_Signal", keyword="MV2H1", prename="RSG2500_All_Incl", Xrange=[-2, 2], Yrange=[-2, 2])
    DrawBTaggingPlot("signal_G_hh_c10_M2500/hist-MiniNTuple.root", "AllTag_Signal", keyword="MV2H0H1", prename="RSG2500_All_Incl", Xrange=[-2, 2], Yrange=[-2, 2], dodouble=2)
    #DrawBTaggingPlot("data_test/hist-MiniNTuple.root",             "AllTag_Signal", keyword="MV2H0", prename="Data_AllTag_Signal", Xrange=[-2, 2], Yrange=[-2, 2])
    DrawBTaggingPlot("data_test/hist-MiniNTuple.root",             "AllTag_Signal", keyword="MV2H1", prename="Data_AllTag_Signal", Xrange=[-2, 2], Yrange=[-2, 2])
    DrawBTaggingPlot("data_test/hist-MiniNTuple.root",             "AllTag_Signal", keyword="MV2H0H1", prename="Data_AllTag_Signal", Xrange=[-2, 2], Yrange=[-2, 2], dodouble=2)



    # # # #signalregion shape comparison
    # inputroot = "sum_" + inputdir + ".root"
    # DrawSRcomparison(inputroot, inputdata="ttbar")
    # DrawSRcomparison(inputroot, inputdata="ttbar", Logy=1)
    # DrawSRcomparison(inputroot, inputdata="qcd_est")
    # DrawSRcomparison(inputroot, inputdata="qcd_est", Logy=1)

    # # # #draw the mhh before and after scale
    # DrawScalecomparison(inputroot, norm=False)
    # DrawScalecomparison(inputroot, norm=True, Logy=1)

    ###draw the reweighted 2D distributions; works conditionally!
    # inputpath = CONF.inputpath + "DS1_cb_j0pT-leadtrk-fin_19" + "/"
    # outputpath = CONF.inputpath + "DS1_cb_j0pT-leadtrk-fin_19" + "/" + "Plot/Other/"
    # if not os.path.exists(outputpath):
    #     os.makedirs(outputpath)
    # for i in ["2Trk_split", "3Trk", "4Trk"]:
    #     DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Sideband", keyword="mHH_l_weight", prename=i, Xrange=[0, 4000], Yrange=[0.5, 1.5])
    #     DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Sideband", keyword="leadHCand_trk0_Pt_weight", prename=i, Xrange=[0, 2000], Yrange=[0.5, 1.5])
    #     DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Sideband", keyword="sublHCand_trk1_Pt_weight", prename=i, Xrange=[0, 400], Yrange=[0.5, 1.5])
    #     DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Sideband", keyword="leadHCand_Pt_m_weight", prename=i, Xrange=[0, 2000], Yrange=[0.5, 1.5])
    #     #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Signal", keyword="mHH_l_weight", prename=i, Xrange=[0, 4000], Yrange=[0.5, 1.5])
    #     #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Signal", keyword="leadHCand_trk0_Pt_weight", prename=i, Xrange=[0, 2000], Yrange=[0.5, 1.5])
    #     #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Signal", keyword="leadHCand_trk1_Pt_weight", prename=i, Xrange=[0, 400], Yrange=[0.5, 1.5])
    #     #DrawSignalPlot("data_test/hist-MiniNTuple.root", "NoTag_" + i + "_Signal", keyword="leadHCand_Pt_m_weight", prename=i, Xrange=[0, 2000], Yrange=[0.5, 1.5])

    ##draw the reweighted 1D distributions; for study only, not in the main production
    #DrawSRcomparison(inputroot, inputdata="qcd_est", keyword = "leadHCand_Mass")
    #DrawSRcomparison(inputroot, inputdata="qcd_est", keyword = "leadHCand_Mass", Logy=1)


    ##testing two plots from two different files
    #for 2HMD deta comparison study
    # for histname in ["hCandDeta", "mHH_l", "hCandDr",
    #     "leadHCand_Mass_s", "leadHCand_Pt_m", "leadHCand_trk0_Pt", "leadHCand_trk1_Pt",
    #     "sublHCand_Mass_s", "sublHCand_Pt_m", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt"]:
    #     DrawMulticomparison([
    #         {"file":"signal_G_hh_c10_M1500/hist-MiniNTuple.root", "path":"AllTag_Signal/" + histname, "leg":"Graviton"}, 
    #         {"file":"signal_X_hh_M1500/hist-MiniNTuple.root", "path":"AllTag_Signal/" + histname, "leg":"2HDM"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"NoTag_Signal/" + histname, "leg":"NoTagData"},
    #         ], keyword=histname, norm=True)

def DrawRegionPlot(inputname, inputdir, keyword="_", prename="Compare", Xrange=[0, 0], Yrange=[0, 0]):
    region_lst = ["Signal", "Control", "Sideband"]
    region_dic = {"Sideband":1, "Control":2, "Signal":3}
    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)

    canv = ROOT.TCanvas(inputdir + "_" +  keyword, " ", 800, 800)
    temp_hist_lst = []
    for i, region in enumerate(region_lst):
        #print inputdir + "_" + region + "/" + keyword
        temp_hist_lst.append(inputroot.Get(inputdir + "_" + region + "/" + keyword).Clone())
        if Xrange != [0, 0]:
            temp_hist_lst[i].GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
        if Yrange != [0, 0]:
            temp_hist_lst[i].GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
            temp_hist_lst[i].GetYaxis().SetTitleOffset(1.4)
        for xbin in range(0, temp_hist_lst[i].GetXaxis().GetNbins()+1):
            for ybin in range(0, temp_hist_lst[i].GetYaxis().GetNbins()+1):
                if temp_hist_lst[i].GetBinContent(xbin, ybin) > 0:
                    temp_hist_lst[i].SetBinContent(xbin, ybin, region_dic[region])

        temp_hist_lst[i].GetZaxis().Set(3, 0.5, 3.5)
        temp_hist_lst[i].GetZaxis().SetRangeUser(0.5, 3.5)
        temp_hist_lst[i].GetZaxis().SetLabelSize(0.07)
        temp_hist_lst[i].GetZaxis().SetLabelOffset(-0.03)
        temp_hist_lst[i].GetZaxis().SetBinLabel(1, "SB")
        temp_hist_lst[i].GetZaxis().SetBinLabel(2, "CR")
        temp_hist_lst[i].GetZaxis().SetBinLabel(3, "SR")

        #ROOT.gStyle.SetPadRightMargin(0.15)
        temp_hist_lst[i].Draw("colz " + ("" if i == 0 else " same "))

    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "Data #sqrt{s} = 13 TeV")
    watermarks = [atlas, hh4b, lumi]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()

    canv.cd()
    ROOT.gStyle.SetPadRightMargin(0.1)
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")

    #done
    del(temp_hist_lst)
    inputroot.Close()

def DrawSignalPlot(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0]):
    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    inputroot.cd(inputdir)
    for key in ROOT.gDirectory.GetListOfKeys():
        kname = key.GetName()
        if keyword in kname:
            print "find:", kname
            temp_hist = ROOT.gDirectory.Get(kname).Clone()
            canv = ROOT.TCanvas(temp_hist.GetName(), temp_hist.GetTitle(), 800, 800)
            if Xrange != [0, 0]:
                temp_hist.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
            if Yrange != [0, 0]:
                temp_hist.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
                temp_hist.GetYaxis().SetTitleOffset(1.4)

            temp_hist.Draw("colz")

            xatlas, yatlas = 0.35, 0.89
            atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
            lumi  = ROOT.TLatex(xatlas, yatlas-0.04, "#sqrt{s} = 13 TeV")
            hh4b  = ROOT.TLatex(xatlas, yatlas-0.08, "RSG c=1.0")
            if "data" in inputname:
                watermarks = [atlas, lumi]
            else:
                watermarks = [atlas, hh4b, lumi]
            for wm in watermarks:
                wm.SetTextAlign(22)
                wm.SetTextSize(0.025)
                wm.SetTextFont(42)
                wm.SetNDC()
                wm.Draw()

            #draw the correlation factor
            if temp_hist.InheritsFrom("TH2"):
                ROOT.gStyle.SetPadRightMargin(0.15)
                myText(0.2, 0.97, 1, "Coor = %s" % str(('%.2g' % temp_hist.GetCorrelationFactor())), CONF.legsize)

            canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")
            print "save: ", outputpath + prename + "_" +  canv.GetName() + ".pdf"

            #produce profile plot if 2D
            if temp_hist.InheritsFrom("TH2"):
                #profile x
                canv.Clear()
                temp_prox = temp_hist.ProfileX()
                temp_prox.GetYaxis().SetTitle(temp_hist.GetYaxis().GetTitle())
                temp_prox.SetMaximum(temp_prox.GetMaximum() * 1.5)
                canv.Clear()
                temp_prox.Draw()
                for wm in watermarks:
                    wm.Draw()
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_profx.pdf")
                #profile y
                canv.Clear()
                temp_proy = temp_hist.ProfileY()
                temp_proy.GetYaxis().SetTitle(temp_hist.GetXaxis().GetTitle())
                temp_proy.SetMaximum(temp_proy.GetMaximum() * 1.5)
                temp_proy.Draw()
                for wm in watermarks:
                    wm.Draw()
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_profy.pdf")
                #profile x
                canv.Clear()
                temp_projx = temp_hist.ProjectionX()
                temp_projx.GetYaxis().SetTitle("NEvents")
                temp_projx.SetMaximum(temp_projx.GetMaximum() * 1.5)
                canv.Clear()
                temp_projx.Draw()
                for wm in watermarks:
                    wm.Draw()
                myText(0.2, 0.97, 1, "Mean=%s, RMS=%s" % (str(('%.2g' % temp_projx.GetMean())), str(('%.2g' % temp_projx.GetRMS()))), CONF.legsize)
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_projx.pdf")
                #profile y
                canv.Clear()
                temp_projy = temp_hist.ProjectionY()
                temp_projy.GetYaxis().SetTitle("NEvents")
                temp_projy.SetMaximum(temp_projy.GetMaximum() * 1.5)
                temp_projy.Draw()
                for wm in watermarks:
                    wm.Draw()
                myText(0.2, 0.97, 1, "Mean=%s, RMS=%s" % (str(('%.2g' % temp_projy.GetMean())), str(('%.2g' % temp_projy.GetRMS()))), CONF.legsize)
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_projy.pdf")
            canv.Close()
            #done
    inputroot.Close()

def DrawPaper2D(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0]):
    # functions for the different regions
    def myCR(x):
	return  ROOT.TMath.Sqrt( (x[0]-124)**2 + (x[1]-115)**2)

    def mySR(x):
	return  ROOT.TMath.Sqrt( ((x[0]-124)/(0.1*x[0]))**2 + ((x[1]-115)/(0.1*x[1]))**2)

    def myTop(x):
	return  ROOT.TMath.Sqrt( ((x[0]-175)/(0.1*x[0]))**2 + ((x[1]-164)/(0.1*x[1]))**2 )	


    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    #inputroot.cd(inputdir)
    ROOT.gStyle.SetPadRightMargin(0.15)

    temp_hist = inputroot.Get(inputdir + "/mH0H1").Clone()
    canv = ROOT.TCanvas(temp_hist.GetName(), temp_hist.GetTitle(), 800, 800)
    if Xrange != [0, 0]:
        temp_hist.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
    if Yrange != [0, 0]:
        temp_hist.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
        temp_hist.GetYaxis().SetTitleOffset(1.8)

    canv.SetLeftMargin(0.2)

    # log scale
    canv.SetLogz(1)

    temp_hist.Draw("colz")
    # Set Axis Labels
    temp_hist.GetXaxis().SetTitle("Leading Higgs Mass [GeV]")
    temp_hist.GetYaxis().SetTitle("Subleading Higgs Mass [GeV]")

    # Draw Signal Region
    thetas = np.linspace(-np.pi, np.pi, 50)

    # get signal points:
    fSR = ROOT.TF2("SR",mySR,0.,Xrange[1],0.,Xrange[1])
    contorsSR = array.array("d", [1.6])
    fSR.SetContour(len(contorsSR),contorsSR)
    fSR.SetNpx(50)
    fSR.SetLineWidth(2)
    fSR.SetLineStyle(5)
    fSR.Draw("same, cont3")

    # get control:
    fCR = ROOT.TF2("CR", myCR,0,Xrange[1],0,Xrange[1])
    contoursCR = array.array("d", [35.8])
    fCR.SetContour(1, contoursCR)
    fCR.SetNpx(200)
    fCR.SetLineWidth(2)
    fCR.Draw("same, cont3")

    # sideband:
    fSB = ROOT.TF2("SB", myCR,0,Xrange[1],0,Xrange[1])
    contoursSB = array.array("d", [63.0])
    fSB.SetContour(1, contoursSB)
    fSB.SetNpx(200)
    fSB.SetLineWidth(2)
    fSB.Draw("same, cont3")

    # ttbar:
    fTT = ROOT.TF2("TT", myTop,0,Xrange[1],0,Xrange[1])
    contoursTT = array.array("d", [1.0])
    fTT.SetContour(1, contoursTT)
    fTT.SetNpx(50)
    fTT.SetLineColor(46)
    fTT.SetLineWidth(3)
    fTT.SetLineStyle(5)
    fTT.Draw("same, cont3")
    # ttbar label:
    ttb_txt = ROOT.TLatex(0.72, 0.52, "#splitline{t#bar{t} enriched}{region}")
    ttb_txt.SetTextColor(46)
    helpers.DrawWords(ttb_txt)

    # fill box
    fillbox = ROOT.TBox(Xrange[0]+1, Yrange[1]-51, Xrange[1]-1, Yrange[1]-1)
    fillbox.SetFillStyle(1001)
    fillbox.SetFillColor(0)
    # line box
    linebox = ROOT.TBox(Xrange[0]+1, Yrange[1]-51, Xrange[1]-1, Yrange[1]-1)
    linebox.SetFillStyle(0)
    linebox.SetLineWidth(4)
    linebox.SetLineStyle(1)
    linebox.SetLineColor(ROOT.kBlack)

    linebox.Draw("same")
    fillbox.Draw("same")

    # Draw Watermarks
    wm = helpers.DrawWatermarks(0.35, 0.875, deltax=[0.3,], 
		watermarks=["ATLAS Internal", "#sqrt{s} = 13 TeV"])

    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")

    #shut it down
    canv.Close()
    inputroot.Close()

def DrawSRcomparison(inputname, inputdata="ttbar", inputtype=["TwoTag_split_Signal", "ThreeTag_Signal", "FourTag_Signal"], keyword="mHH_l", prename="", Xrange=[0, 0], Yrange=[0, 0], norm=True, Logy=0):
    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    tempname = inputdata + "_" + "compare" + "_" + keyword + ("" if Logy == 0 else "_" + str(Logy))
    canv = ROOT.TCanvas(tempname, tempname, 800, 800)
    canv.SetLogy(Logy)
    xleg, yleg = 0.5, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.15, yleg+0.2)
    counter = 0
    maxbincontent = (0.2 if Logy ==0 else 10)

    for key in ROOT.gDirectory.GetListOfKeys():
        kname = key.GetName()
        for i, region in enumerate(inputtype):
            if inputdata + "_" + region  + "_" + keyword in kname:

                temp_hist = ROOT.gDirectory.Get(kname)
                #print temp_hist.GetName()
                if "mHH_l" in keyword:
                    temp_hist.Rebin(10) #since the binning is changed!!!
                temp_hist.SetLineColor(2 + i)
                temp_hist.SetMarkerStyle(20 + i)
                temp_hist.SetMarkerColor(2 + i)
                temp_hist.SetMarkerSize(1)
                if norm:
                    temp_hist.Scale(1/temp_hist.Integral(0, temp_hist.GetXaxis().GetNbins()+1))

                if Xrange != [0, 0]:
                    temp_hist.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
                if Yrange != [0, 0]:
                    temp_hist.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])


                maxbincontent = max(maxbincontent, temp_hist.GetMaximum())
                temp_hist.SetMaximum(maxbincontent * 1.5)
                legend.AddEntry(temp_hist, region.replace("_", " "), "apl")

                if counter==0:
                    temp_hist.Draw("")
                else:
                    temp_hist.Draw("same")
                counter += 1

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    watermarks = [atlas]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()

    canv.SaveAs(outputpath + canv.GetName() + ".pdf")
    canv.Close()

    inputroot.Close()

def DrawScalecomparison(inputname, inputtype=["TwoTag_split_Signal", "ThreeTag_Signal", "FourTag_Signal"], prename="", Xrange=[0, 3000], Yrange=[0, 0], norm=True, Logy=0):
    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    inputdata= ["data_est", "RSG1_1500", "RSG1_2500"]
    for i, region in enumerate(inputtype):

        tempname = region + "_" + "compare_scale" + "_mHH" + ("" if Logy == 0 else "_" + str(Logy))
        canv = ROOT.TCanvas(tempname, tempname, 800, 800)
        canv.SetLogy(Logy)
        xleg, yleg = 0.52, 0.73
        legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
        counter = 0
        maxbincontent = (0.3 if Logy ==0 else 10)

        for j, data in enumerate(inputdata):
            for key in ROOT.gDirectory.GetListOfKeys():
                kname = key.GetName()
                if (data + "_" + region  + "_" + "mHH_l"  in kname) or (data + "_" + region  + "_" + "mHH_pole" in kname):
                    #print kname
                    temp_hist = ROOT.gDirectory.Get(kname)
                    #print temp_hist.GetName()
                    temp_hist.Rebin(10)
                    temp_hist.SetLineColor(2 + j)
                    temp_hist.SetMarkerStyle(20 + j)
                    if "pole" in kname: temp_hist.SetMarkerStyle(20 + j + len(inputdata))
                    temp_hist.SetMarkerColor(2 + j)
                    temp_hist.SetMarkerSize(1)
                    if norm:
                        temp_hist.Scale(1/temp_hist.Integral(0, temp_hist.GetXaxis().GetNbins()+1))

                    if Xrange != [0, 0]:
                        temp_hist.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
                    if Yrange != [0, 0]:
                        temp_hist.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])

                    maxbincontent = max(maxbincontent, temp_hist.GetMaximum())
                    
                    temp_hist.SetMaximum(maxbincontent * 1.5)
                    legend.AddEntry(temp_hist, data.replace("_", " ") + ("" if "pole" not in kname else " scaled"), "apl")

                    if counter==0:
                        temp_hist.Draw("")
                    else:
                        temp_hist.Draw("same")

                    counter += 1

        legend.SetBorderSize(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.03)
        legend.Draw()

        # draw watermarks
        xatlas, yatlas = 0.35, 0.87
        atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
        hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0")
        lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
        watermarks = [atlas]
        for wm in watermarks:
            wm.SetTextAlign(22)
            wm.SetTextSize(0.04)
            wm.SetTextFont(42)
            wm.SetNDC()
            wm.Draw()

        canv.SaveAs(outputpath + canv.GetName() + ".pdf")
        canv.Close()

    inputroot.Close()

def DrawMulticomparison(inputlst, keyword="", prename="", Xrange=[0, 0], Yrange=[0, 0], norm=True, Logy=0):
    #print inputdir
    tempname = "directcompare" + "_" + keyword + ("" if Logy == 0 else "_" + str(Logy))
    canv = ROOT.TCanvas(tempname, tempname, 800, 800)
    canv.SetLogy(Logy)
    xleg, yleg = 0.5, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.15, yleg+0.2)
    counter = 0
    maxbincontent = (0.05 if Logy ==0 else 10)
    temphst_lst = []

    for i, dic in enumerate(inputlst):
        refroot = ROOT.TFile.Open(inputpath + dic["file"])
        temphst_lst.append(refroot.Get(dic["path"]).Clone())
        temphst_lst[i].SetDirectory(0) #otherwise the hist lives in the current open file

        temphst_lst[i].SetLineColor(2 + i)
        temphst_lst[i].SetMarkerStyle(20 + i)
        temphst_lst[i].SetMarkerColor(2 + i)
        temphst_lst[i].SetMarkerSize(1)
        if norm:
            temphst_lst[i].Scale(1/temphst_lst[i].Integral(0, temphst_lst[i].GetXaxis().GetNbins()+1))

        maxbincontent = max(maxbincontent, temphst_lst[i].GetMaximum())
        temphst_lst[i].SetMaximum(maxbincontent * 1.5)
        legend.AddEntry(temphst_lst[i], dic["leg"], "apl")
        temphst_lst[i].Draw("" if i==0 else "same")
        refroot.Close()
    
    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "Simulations")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    watermarks = [atlas]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()

    canv.SaveAs(outputpath + canv.GetName() + ".pdf")
    canv.Close()

def DrawBTaggingPlot(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0], dodouble=1):
    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    inputroot.cd(inputdir)
    for key in ROOT.gDirectory.GetListOfKeys():
        kname = key.GetName()
        if keyword in kname:
            print "find:", kname
            temp_hist = ROOT.gDirectory.Get(kname).Clone()
            #if rebin
            temp_hist.RebinX(10)
            temp_hist.RebinY(10)
            canv = ROOT.TCanvas(temp_hist.GetName(), temp_hist.GetTitle(), 800, 800)
            if Xrange != [0, 0]:
                temp_hist.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
            if Yrange != [0, 0]:
                temp_hist.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
                temp_hist.GetYaxis().SetTitleOffset(1.4)

            temp_hist.Draw("colz")

            xatlas, yatlas = 0.35, 0.89
            atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
            lumi  = ROOT.TLatex(xatlas, yatlas-0.04, "#sqrt{s} = 13 TeV")
            hh4b  = ROOT.TLatex(xatlas, yatlas-0.08, "RSG c=1.0")
            if "data" in inputname:
                watermarks = [atlas, lumi]
            else:
                watermarks = [atlas, hh4b, lumi]
            for wm in watermarks:
                wm.SetTextAlign(22)
                wm.SetTextSize(0.025)
                wm.SetTextFont(42)
                wm.SetNDC()
                wm.Draw()

            #draw the b-tagging lines
            xlines = []
            ylines = []
            xnotes = []
            ynotes = []
            btag_lst = [[30, 0.9951 * dodouble], [50, 0.9452 * dodouble], [60, 0.8529 * dodouble], [70, 0.6455 * dodouble], [77, 0.370 * dodouble], [85, -0.1416 * dodouble]]
            for j, btag_wp in enumerate(btag_lst):
                print dodouble, btag_wp[1]
                xlines.append(ROOT.TLine(btag_wp[1], btag_wp[1], 2, btag_wp[1]))
                xlines[-1].SetLineStyle(9)
                xlines[-1].Draw()
                ylines.append(ROOT.TLine(btag_wp[1], btag_wp[1], btag_wp[1], 2))
                ylines[-1].SetLineStyle(9)
                ylines[-1].Draw()
                xnotes.append(ROOT.TLatex(btag_wp[1], 1 + 0.08, str(btag_wp[0])))
                xnotes[-1].SetTextSize(0.015)
                xnotes[-1].Draw()
                #compute the percentage of tags inside the cuts
                evt_cut    = temp_hist.Integral(temp_hist.GetXaxis().FindBin(btag_wp[1]), temp_hist.GetXaxis().FindBin(2), temp_hist.GetYaxis().FindBin(btag_wp[1]), temp_hist.GetYaxis().FindBin(2))
                evt_total  = temp_hist.Integral(temp_hist.GetXaxis().FindBin(-2), temp_hist.GetXaxis().FindBin(2), temp_hist.GetYaxis().FindBin(-2), temp_hist.GetYaxis().FindBin(2))
                #print evt_cut, evt_total
                ynotes.append(ROOT.TLatex(1 + 0.12, btag_wp[1], ("%.4f " % (100 * evt_cut/evt_total))))
                ynotes[-1].SetTextSize(0.015)
                ynotes[-1].Draw()
            #draw the correlation factor
            if temp_hist.InheritsFrom("TH2"):
                ROOT.gStyle.SetPadRightMargin(0.15)
                myText(0.2, 0.97, 1, "Coor = %s" % str(('%.2g' % temp_hist.GetCorrelationFactor())), CONF.legsize)

            canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")
            print "save: ", outputpath + prename + "_" +  canv.GetName() + ".pdf"

            #produce profile plot if 2D
            if temp_hist.InheritsFrom("TH2"):
                #profile x
                canv.Clear()
                temp_prox = temp_hist.ProfileX()
                temp_prox.GetYaxis().SetTitle(temp_hist.GetYaxis().GetTitle())
                temp_prox.SetMaximum(temp_prox.GetMaximum() * 1.5)
                canv.Clear()
                temp_prox.Draw()
                for wm in watermarks:
                    wm.Draw()
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_profx.pdf")
                #profile y
                canv.Clear()
                temp_proy = temp_hist.ProfileY()
                temp_proy.GetYaxis().SetTitle(temp_hist.GetXaxis().GetTitle())
                temp_proy.SetMaximum(temp_proy.GetMaximum() * 1.5)
                temp_proy.Draw()
                for wm in watermarks:
                    wm.Draw()
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_profy.pdf")
                #profile x
                canv.Clear()
                temp_projx = temp_hist.ProjectionX()
                temp_projx.GetYaxis().SetTitle("NEvents")
                temp_projx.SetMaximum(temp_projx.GetMaximum() * 1.5)
                canv.Clear()
                temp_projx.Draw()
                for wm in watermarks:
                    wm.Draw()
                myText(0.2, 0.97, 1, "Mean=%s, RMS=%s" % (str(('%.2g' % temp_projx.GetMean())), str(('%.2g' % temp_projx.GetRMS()))), CONF.legsize)
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_projx.pdf")
                #profile y
                canv.Clear()
                temp_projy = temp_hist.ProjectionY()
                temp_projy.GetYaxis().SetTitle("NEvents")
                temp_projy.SetMaximum(temp_projy.GetMaximum() * 1.5)
                temp_projy.Draw()
                for wm in watermarks:
                    wm.Draw()
                myText(0.2, 0.97, 1, "Mean=%s, RMS=%s" % (str(('%.2g' % temp_projy.GetMean())), str(('%.2g' % temp_projy.GetRMS()))), CONF.legsize)
                canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_projy.pdf")
            canv.Close()
            #done
    inputroot.Close()


if __name__ == "__main__":
    main()
