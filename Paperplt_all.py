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

    global StatusLabel
    StatusLabel = "Internal" ##StatusLabel = "Preliminary"
    ops = options()
    inputdir = ops.inputdir
    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "PaperPlot/Other/"
    print "output direcotry is: ", outputpath
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    # # paper plot
    DrawPaper2D("data_test/hist-MiniNTuple.root", "NoTag_Incl", prename="NoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2DPrediction("data_test/hist-MiniNTuple.root", "NoTag_Incl", prename="TwoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    DrawPaper2D("signal_G_hh_c10_M2000/hist-MiniNTuple.root", "TwoTag_split_Incl", prename="Sig_TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2D("signal_G_hh_c10_M2000/hist-MiniNTuple.root", "ThreeTag_Incl", prename="Sig_ThreeTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2D("signal_G_hh_c10_M2000/hist-MiniNTuple.root", "FourTag_Incl", prename="Sig_FourTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    DrawPaper2D("ttbar_comb_test/hist-MiniNTuple.root", "NoTag_Incl", prename="Top_NoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2D("ttbar_comb_test/hist-MiniNTuple.root", "OneTag_Incl", prename="Top_OneTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    ## for muqcd study
    # outputpath = CONF.inputpath + inputdir + "/" + "Plot/Other/"
    # if not os.path.exists(outputpath):
    #     os.makedirs(outputpath)
    DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_Incl", prename="OneTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "OneTag_Incl", prename="TwoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_2Trk_split_Incl", prename="TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_3Trk_Incl", prename="ThreeTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_4Trk_Incl", prename="FourTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    ## only if QCD sample exists
    ##DrawPaper2DComparePrediction("../TEST/signal_QCD/hist-MiniNTuple.root", "NoTag_Incl", prename="QCD_OneTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    ##DrawPaper2DComparePrediction("../TEST/signal_QCD/hist-MiniNTuple.root", "OneTag_Incl", prename="QCD_TwoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

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

    temp_hist = inputroot.Get(inputdir + "/mH0H1").Clone()
    canv = ROOT.TCanvas(temp_hist.GetName(), temp_hist.GetTitle(), 1000, 800)
    if Xrange != [0, 0]:
        temp_hist.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
    if Yrange != [0, 0]:
        temp_hist.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
        temp_hist.GetYaxis().SetTitleOffset(1.5)

    #print Xrange, Yrange, temp_hist.GetXaxis().GetMinimum(), temp_hist.GetXaxis().GetMaximum()

    canv.SetLeftMargin(0.17)
    canv.SetRightMargin(0.23)
    # log scale
    #canv.SetLogz(1)
    temp_hist.Draw("colz")
    # Set Axis Labels
    temp_hist.GetXaxis().SetTitle("m_{J}^{lead} [GeV]")
    temp_hist.GetYaxis().SetTitle("m_{J}^{subl} [GeV]")
    temp_hist.GetZaxis().SetTitle("Events/10 GeV^{2}")
    temp_hist.GetZaxis().SetTitleOffset(1.8)
    temp_hist.GetZaxis().SetRangeUser(0, temp_hist.GetMaximum())
    # change divisions
    temp_hist.GetXaxis().SetNdivisions(505)
    temp_hist.GetYaxis().SetNdivisions(505)
    temp_hist.GetZaxis().SetNdivisions(505)

    # Draw Signal Region
    thetas = np.linspace(-np.pi, np.pi, 50)

    # get signal points:
    fSR = ROOT.TF2("SR",mySR,0.,Xrange[1],0.,Xrange[1])
    contorsSR = array.array("d", [1.6])
    fSR.SetContour(len(contorsSR),contorsSR)
    fSR.SetNpx(100)
    fSR.SetLineColor(ROOT.kRed)
    fSR.SetLineWidth(6)
    fSR.SetLineStyle(5)
    fSR.Draw("same, cont3")

    # get control:
    fCR = ROOT.TF2("CR", myCR,0,Xrange[1],0,Xrange[1])
    contoursCR = array.array("d", [32.8])
    fCR.SetContour(1, contoursCR)
    fCR.SetNpx(400)
    fCR.SetLineColor(ROOT.kOrange+7)
    fCR.SetLineWidth(6)
    fCR.Draw("same, cont3")

    # sideband:
    fSB = ROOT.TF2("SB", myCR,0,Xrange[1],0,Xrange[1])
    contoursSB = array.array("d", [63.0])
    fSB.SetContour(1, contoursSB)
    fSB.SetNpx(400)
    fSB.SetLineColor(ROOT.kYellow)
    fSB.SetLineWidth(6)
    fSB.Draw("same, cont3")

    # ttbar:
    fTT = ROOT.TF2("TT", myTop,0,Xrange[1],0,Xrange[1])
    contoursTT = array.array("d", [1.0])
    fTT.SetContour(1, contoursTT)
    fTT.SetNpx(50)
    fTT.SetLineColor(46)
    fTT.SetLineWidth(3)
    fTT.SetLineStyle(5)
    #fTT.Draw("same, cont3")
    # ttbar label:
    ttb_txt = ROOT.TLatex(0.65, 0.75, "#splitline{t#bar{t} enriched}{region}")
    ttb_txt.SetTextColor(46)
    ttb_txt.SetTextSize(0.03)
    #helpers.DrawWords(ttb_txt)

    # fill box
    fillbox = ROOT.TBox(110,202,230,240)
    fillbox.SetFillStyle(1001)
    fillbox.SetFillColor(0)
    # line box
    linebox = ROOT.TBox(110,202,230,240)
    linebox.SetFillStyle(0)
    linebox.SetLineWidth(2)
    linebox.SetLineStyle(1)
    linebox.SetLineColor(ROOT.kBlack)

    linebox.Draw("same")
    fillbox.Draw("same")

    # Draw Watermarks
    xatlas, yatlas = 0.37, 0.87
    ATLASLabel(xatlas, yatlas, StatusLabel)
    myText(xatlas, yatlas-0.05, 1, "#sqrt{s}=13 TeV, " + str(CONF.totlumi) + " fb^{-1}", CONF.paperlegsize)
    myText(xatlas, yatlas-0.1, 1, "Boosted", CONF.paperlegsize)

    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".png")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".eps")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".C")

    #shut it down
    canv.Close()
    inputroot.Close()

def DrawPaper2DPrediction(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0]):
    # functions for the different regions
    def myCR(x):
        return  ROOT.TMath.Sqrt( (x[0]-124)**2 + (x[1]-115)**2)

    def mySR(x):
        return  ROOT.TMath.Sqrt( ((x[0]-124)/(0.1*x[0]))**2 + ((x[1]-115)/(0.1*x[1]))**2)

    def myTop(x):
        return  ROOT.TMath.Sqrt( ((x[0]-175)/(0.1*x[0]))**2 + ((x[1]-164)/(0.1*x[1]))**2 )  


    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    inputroot_top = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist-MiniNTuple.root")
    #inputroot.cd(inputdir)
    temp_hist = inputroot.Get("NoTag_2Trk_split_Incl" + "/mH0H1").Clone()
    temp_hist_top = inputroot_top.Get("TwoTag_split_Incl" + "/mH0H1").Clone()

    #scale and add
    inputtex = CONF.inputpath + CONF.workdir + "/Plot/Tables/normfit.tex"
    f1 = open(inputtex, 'r')
    for line in f1: 
        #very stupid protection to distinguish 2b and 2bs
        if ("Nb=2s") in line:
            templine = line.split("&")
            tempqcd = templine[1].split(" ")
            muqcd = float(tempqcd[1])
            muqcd_err = float(tempqcd[3])
            temptop = templine[2].split(" ")
            mutop = float(temptop[1])
            mutop_err = float(temptop[3])
            #print " muqcd ", muqcd, " atop ", mutop
            temp_hist.Scale(muqcd)
            temp_hist_top.Scale(mutop)
            temp_hist.Add(temp_hist_top)
    
    #proceed
    canv = ROOT.TCanvas(temp_hist.GetName(), temp_hist.GetTitle(), 1000, 800)
    if Xrange != [0, 0]:
        temp_hist.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
    if Yrange != [0, 0]:
        temp_hist.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
        temp_hist.GetYaxis().SetTitleOffset(1.5)
    #print Xrange, Yrange, temp_hist.GetXaxis().GetMinimum(), temp_hist.GetXaxis().GetMaximum()
    canv.SetLeftMargin(0.17)
    canv.SetRightMargin(0.23)
    # log scale
    #canv.SetLogz(1)
    temp_hist.Draw("colz")
    # Set Axis Labels
    temp_hist.GetXaxis().SetTitle("m_{J}^{lead} [GeV]")
    temp_hist.GetYaxis().SetTitle("m_{J}^{subl} [GeV]")
    temp_hist.GetZaxis().SetTitle("Events/10 GeV^{2}")
    temp_hist.GetZaxis().SetTitleOffset(1.8)
    temp_hist.GetZaxis().SetRangeUser(0, temp_hist.GetMaximum())
    # change divisions
    temp_hist.GetXaxis().SetNdivisions(505)
    temp_hist.GetYaxis().SetNdivisions(505)
    temp_hist.GetZaxis().SetNdivisions(505)

    # Draw Signal Region
    thetas = np.linspace(-np.pi, np.pi, 50)

    # get signal points:
    fSR = ROOT.TF2("SR",mySR,0.,Xrange[1],0.,Xrange[1])
    contorsSR = array.array("d", [1.6])
    fSR.SetContour(len(contorsSR),contorsSR)
    fSR.SetNpx(100)
    fSR.SetLineColor(ROOT.kRed)
    fSR.SetLineWidth(6)
    fSR.SetLineStyle(5)
    fSR.Draw("same, cont3")

    # get control:
    fCR = ROOT.TF2("CR", myCR,0,Xrange[1],0,Xrange[1])
    contoursCR = array.array("d", [35.8])
    fCR.SetContour(1, contoursCR)
    fCR.SetNpx(400)
    fCR.SetLineColor(ROOT.kOrange+7)
    fCR.SetLineWidth(6)
    fCR.Draw("same, cont3")

    # sideband:
    fSB = ROOT.TF2("SB", myCR,0,Xrange[1],0,Xrange[1])
    contoursSB = array.array("d", [63.0])
    fSB.SetContour(1, contoursSB)
    fSB.SetNpx(400)
    fSB.SetLineColor(ROOT.kYellow)
    fSB.SetLineWidth(6)
    fSB.Draw("same, cont3")

    # ttbar:
    fTT = ROOT.TF2("TT", myTop,0,Xrange[1],0,Xrange[1])
    contoursTT = array.array("d", [1.0])
    fTT.SetContour(1, contoursTT)
    fTT.SetNpx(50)
    fTT.SetLineColor(46)
    fTT.SetLineWidth(3)
    fTT.SetLineStyle(5)
    #fTT.Draw("same, cont3")
    # ttbar label:
    ttb_txt = ROOT.TLatex(0.65, 0.75, "#splitline{t#bar{t} enriched}{region}")
    ttb_txt.SetTextColor(46)
    ttb_txt.SetTextSize(0.03)
    #helpers.DrawWords(ttb_txt)

    # fill box
    fillbox = ROOT.TBox(110,202,230,240)
    fillbox.SetFillStyle(1001)
    fillbox.SetFillColor(0)
    # line box
    linebox = ROOT.TBox(110,202,230,240)
    linebox.SetFillStyle(0)
    linebox.SetLineWidth(2)
    linebox.SetLineStyle(1)
    linebox.SetLineColor(ROOT.kBlack)

    linebox.Draw("same")
    fillbox.Draw("same")

    # Draw Watermarks
    xatlas, yatlas = 0.37, 0.87
    ATLASLabel(xatlas, yatlas, StatusLabel)
    myText(xatlas, yatlas-0.05, 1, "#sqrt{s}=13 TeV, " + str(CONF.totlumi) + " fb^{-1}", CONF.paperlegsize)
    myText(xatlas, yatlas-0.1, 1, "Boosted", CONF.paperlegsize)


    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".png")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".eps")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".C")

    #shut it down
    canv.Close()
    inputroot.Close()
    inputroot_top.Close()
    f1.close()

def DrawPaper2DComparePrediction(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0]):
    # functions for the different regions
    SB_rad = 53
    CR_rad = 33
    SR_rad = 1.6
    def mySB(x):
        #return  ROOT.TMath.Sqrt( (x[0]-124)**2 + (x[1]-115)**2)
        return  ROOT.TMath.Sqrt( (x[0]-134)**2 + (x[1]-125)**2)

    def myCR(x):
        return  ROOT.TMath.Sqrt( (x[0]-124)**2 + (x[1]-115)**2)

    def mySR(x):
        return  ROOT.TMath.Sqrt( ((x[0]-124)/(0.1*x[0]))**2 + ((x[1]-115)/(0.1*x[1]))**2)

    def myTop(x):
        return  ROOT.TMath.Sqrt( ((x[0]-175)/(0.1*x[0]))**2 + ((x[1]-164)/(0.1*x[1]))**2 )  


    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    inputroot_top = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist-MiniNTuple.root")
    #inputroot.cd(inputdir)
    #zero tag background estiamte string
    temp_hist      = inputroot.Get(inputdir + "/mH0H1").Clone()
    temp_hist_top_b= inputroot_top.Get(inputdir + "/mH0H1").Clone()
    temp_hist_top  = inputroot_top.Get(prename + "/mH0H1").Clone()
    temp_hist_data = inputroot.Get(prename + "/mH0H1").Clone()

    #rebin
    rebin_factor = 1 #default 5
    temp_hist.Rebin2D(rebin_factor, rebin_factor)
    temp_hist_top.Rebin2D(rebin_factor, rebin_factor)
    temp_hist_top_b.Rebin2D(rebin_factor, rebin_factor)
    temp_hist_data.Rebin2D(rebin_factor, rebin_factor)

    #add
    temp_hist.Add(temp_hist_top_b, -1)#substract original top
    #load fitted muqcd information
    inputtex = CONF.inputpath + CONF.workdir + "/Plot/Tables/normfit.tex"
    f1 = open(inputtex, 'r')
    ##if scale
    # for line in f1: 
    #     #very stupid protection to distinguish 2b and 2bs
    #     tempdic={"TwoTag_split_Incl":"Nb=2s", "ThreeTag_Incl":"Nb=3", "FourTag_Incl":"Nb=4"}
    #     if (tempdic[prename] in line):
    #         templine = line.split("&")
    #         tempqcd = templine[1].split(" ")
    #         muqcd = float(tempqcd[1])
    #         muqcd_err = float(tempqcd[3])
    #         temptop = templine[2].split(" ")
    #         mutop = float(temptop[1])
    #         mutop_err = float(temptop[3])
    #         #print "before scale!! ", "estint: ", temp_hist.Integral(), " data: ", temp_hist_data.Integral()
    #         #print " muqcd ", muqcd, " atop ", mutop
    #         temp_hist.Scale(muqcd)
    #         temp_hist_top.Scale(mutop)
    #         temp_hist.Add(temp_hist_top)
    #         #print "post scale!! ", "estint: ", temp_hist.Integral(), " data: ", temp_hist_data.Integral()
    ##if not scale--direct muqcd values;
    ##in this case, substract top from the data
    temp_hist_data_copy  = temp_hist_data.Clone("copy")
    temp_hist_data.Add(temp_hist_top, -1)

    #scale down by data
    print "divide!! ", "estint: ", temp_hist.Integral(), " data: ", temp_hist_data.Integral()
    #temp_hist_data.Add(temp_hist, -1)
    #ROOT.gStyle.SetPaintTextFormat(".0f")
    #temp_hist_data.Add(temp_hist, -1)
    temp_hist_data.Divide(temp_hist)
    ##check the maximum bin information
    max_x = ROOT.Long(0)
    max_y = ROOT.Long(0)
    max_z = ROOT.Long(0)
    temp_hist_data.GetMaximumBin(max_x, max_y, max_z)
    print "maxbin: ", max_x, max_y, " content: ", temp_hist_data.GetBinContent(max_x, max_y), inputroot.Get(prename + "/mH0H1").GetBinContent(max_x * rebin_factor, max_y * rebin_factor), inputroot.Get(inputdir + "/mH0H1").GetBinContent(max_x * rebin_factor, max_y * rebin_factor)
    ##proceed
    canv = ROOT.TCanvas(temp_hist_data.GetName(), temp_hist_data.GetTitle(), 1000, 800)
    if Xrange != [0, 0]:
        temp_hist_data.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
    if Yrange != [0, 0]:
        temp_hist_data.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
        temp_hist_data.GetYaxis().SetTitleOffset(1.5)
    #print Xrange, Yrange, temp_hist.GetXaxis().GetMinimum(), temp_hist.GetXaxis().GetMaximum()
    canv.SetLeftMargin(0.17)
    canv.SetRightMargin(0.23)
    # log scale
    #canv.SetLogz(1)
    ##fill the pull plots:
    pull_hist_OT = ROOT.TH1F("pull_OT", "OT; #mu_{qcd}; Counts", 30, 0.2, 0.4)
    pull_hist_SB = ROOT.TH1F("pull_SB", "SB; #mu_{qcd}; Counts", 30, 0.2, 0.4)
    pull_hist_CR = ROOT.TH1F("pull_CR", "CR; #mu_{qcd}; Counts", 30, 0.2, 0.4)
    pull_hist_SR = ROOT.TH1F("pull_SR", "SR; #mu_{qcd}; Counts", 30, 0.2, 0.4)
    ##blind SR and CR; notice it is exclusive!
    for x_bin in range(temp_hist_data.GetXaxis().GetNbins()):
        for y_bin in range(temp_hist_data.GetYaxis().GetNbins()):
            #pull_hist_OT.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
            if mySR((temp_hist_data.GetXaxis().GetBinCenter(x_bin), temp_hist_data.GetYaxis().GetBinCenter(y_bin))) < SR_rad:
                if CONF.blind is True and ("ThreeTag_" in prename or "TwoTag_split_" in prename or "FourTag_" in prename ):
                    temp_hist_data.SetBinContent(x_bin, y_bin, 0)
                else:
                    pull_hist_SR.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
            elif myCR((temp_hist_data.GetXaxis().GetBinCenter(x_bin), temp_hist_data.GetYaxis().GetBinCenter(y_bin))) < CR_rad:
                if CONF.blind is True and ("ThreeTag_" in prename or "TwoTag_split_" in prename or "FourTag_" in prename ):
                    temp_hist_data.SetBinContent(x_bin, y_bin, 0)
                else:
                    pull_hist_CR.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
            elif mySB((temp_hist_data.GetXaxis().GetBinCenter(x_bin), temp_hist_data.GetYaxis().GetBinCenter(y_bin))) < SB_rad:
                pull_hist_SB.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
            else:
                pull_hist_OT.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
    temp_hist_data.Draw("colz")
    # Set Axis Labels
    temp_hist_data.GetXaxis().SetTitle("m_{J}^{lead} [GeV]")
    temp_hist_data.GetYaxis().SetTitle("m_{J}^{subl} [GeV]")
    temp_hist_data.GetZaxis().SetTitle("#mu qcd")
    temp_hist_data.GetZaxis().SetTitleOffset(1.8)
    temp_hist_max = max(temp_hist_data.GetMaximum(), abs(temp_hist_data.GetMinimum()))
    temp_hist_data.GetZaxis().SetRangeUser(0, temp_hist_max)
    #temp_hist_data.GetZaxis().SetRangeUser(0.2, 0.3)
    # change divisions
    temp_hist_data.GetXaxis().SetNdivisions(505)
    temp_hist_data.GetYaxis().SetNdivisions(505)
    temp_hist_data.GetZaxis().SetNdivisions(505)

    # Draw Signal Region
    thetas = np.linspace(-np.pi, np.pi, 50)

    # get signal points:
    fSR = ROOT.TF2("SR",mySR,0.,Xrange[1],0.,Xrange[1])
    contorsSR = array.array("d", [SR_rad])
    fSR.SetContour(len(contorsSR),contorsSR)
    fSR.SetNpx(400)
    fSR.SetLineColor(ROOT.kRed)
    fSR.SetLineWidth(6)
    fSR.Draw("same, cont3")

    # get control:
    fCR = ROOT.TF2("CR", myCR,0,Xrange[1],0,Xrange[1])
    contoursCR = array.array("d", [CR_rad])
    fCR.SetContour(1, contoursCR)
    fCR.SetNpx(400)
    fCR.SetLineColor(ROOT.kOrange+7)
    fCR.SetLineWidth(6)
    fCR.Draw("same, cont3")

    # sideband:
    fSB = ROOT.TF2("SB", mySB,0,Xrange[1],0,Xrange[1])
    contoursSB = array.array("d", [SB_rad])
    fSB.SetContour(1, contoursSB)
    fSB.SetNpx(400)
    fSB.SetLineColor(ROOT.kBlue)
    fSB.SetLineWidth(6)
    fSB.Draw("same, cont3")

    # ttbar:
    fTT = ROOT.TF2("TT", myTop,0,Xrange[1],0,Xrange[1])
    contoursTT = array.array("d", [1.0])
    fTT.SetContour(1, contoursTT)
    fTT.SetNpx(50)
    fTT.SetLineColor(46)
    fTT.SetLineWidth(3)
    fTT.SetLineStyle(5)
    #fTT.Draw("same, cont3")
    # ttbar label:
    ttb_txt = ROOT.TLatex(0.65, 0.75, "#splitline{t#bar{t} enriched}{region}")
    ttb_txt.SetTextColor(46)
    ttb_txt.SetTextSize(0.03)
    #helpers.DrawWords(ttb_txt)

    # fill box
    fillbox = ROOT.TBox(110,202,210,240)
    fillbox.SetFillStyle(1001)
    fillbox.SetFillColor(0)
    # line box
    linebox = ROOT.TBox(110,202,210,240)
    linebox.SetFillStyle(0)
    linebox.SetLineWidth(2)
    linebox.SetLineStyle(1)
    linebox.SetLineColor(ROOT.kBlack)

    #linebox.Draw("same")
    #fillbox.Draw("same")

    # Draw Watermarks
    xatlas, yatlas = 0.37, 0.87
    ATLASLabel(xatlas, yatlas, StatusLabel)
    myText(xatlas, yatlas-0.05, 1, "#sqrt{s}=13 TeV, " + str(CONF.totlumi) + " fb^{-1}", CONF.paperlegsize)
    myText(xatlas, yatlas-0.1, 1, "Boosted", CONF.paperlegsize)


    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".png")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".eps")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".C")

    ##draw the stacked pull
    canv.Clear()
    #canv.SetLogy(1)
    canv.SetRightMargin(0.13)
    pull_hs = ROOT.THStack("pull_hs","; #mu_{qcd}; Counts")
    pull_hist_OT.SetFillColor(CONF.clr_lst[0])
    pull_hist_SB.SetFillColor(CONF.clr_lst[1])
    pull_hist_CR.SetFillColor(CONF.clr_lst[2])
    pull_hist_SR.SetFillColor(CONF.clr_lst[3])
    pull_hs.SetMinimum(0.1)
    pull_hs.SetMaximum(pull_hist_SB.GetMaximum()*2.5)
    # pull_hist_OT.SetMinimum(0.1)
    # pull_hist_SB.SetMinimum(0.1)
    # pull_hist_CR.SetMinimum(0.1)
    # pull_hist_SR.SetMinimum(0.1)
    # pull_hist_OT.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    # pull_hist_SB.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    # pull_hist_CR.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    # pull_hist_SR.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    pull_hist_OT.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*2.5)
    pull_hist_SB.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*2.5)
    pull_hist_CR.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*2.5)
    pull_hist_SR.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*2.5)
    #pull_hs.Add(pull_hist_OT)
    pull_hs.Add(pull_hist_SB)
    pull_hs.Add(pull_hist_CR)
    pull_hs.Add(pull_hist_SR)
    #pull_hist_OT.Draw("hist")
    pull_hs.Draw("hist")
    #pull_hist_OT.Draw("same")
    leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
    #leg.AddEntry(pull_hist_OT, "OT mean: %.3f" % pull_hist_OT.GetMean())
    leg.AddEntry(pull_hist_SB, "SB mean: %.3f" % pull_hist_SB.GetMean())
    leg.AddEntry(pull_hist_CR, "CR mean: %.3f" % pull_hist_CR.GetMean())
    leg.AddEntry(pull_hist_SR, "SR mean: %.3f" % pull_hist_SR.GetMean())
    leg.SetTextFont(43)
    leg.SetTextSize(CONF.legsize)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.Draw()
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_pull.pdf")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_pull.root")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_pull.C")

    #shut it down
    canv.Close()
    inputroot.Close()
    inputroot_top.Close()
    f1.close()

if __name__ == "__main__":
    main()
