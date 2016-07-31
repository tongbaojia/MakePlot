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
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

def main():

    ops = options()
    inputdir = ops.inputdir
    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "PaperPlot/Other/"

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    # # paper plot
    DrawPaper2D("data_test/hist-MiniNTuple.root", "NoTag_Incl", prename="NoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

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
    fSR.SetNpx(50)
    fSR.SetLineWidth(6)
    fSR.SetLineStyle(5)
    fSR.Draw("same, cont3")

    # get control:
    fCR = ROOT.TF2("CR", myCR,0,Xrange[1],0,Xrange[1])
    contoursCR = array.array("d", [35.8])
    fCR.SetContour(1, contoursCR)
    fCR.SetNpx(200)
    fCR.SetLineWidth(6)
    fCR.Draw("same, cont3")

    # sideband:
    fSB = ROOT.TF2("SB", myCR,0,Xrange[1],0,Xrange[1])
    contoursSB = array.array("d", [63.0])
    fSB.SetContour(1, contoursSB)
    fSB.SetNpx(200)
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
    fillbox = ROOT.TBox(Xrange[0], Yrange[1]-21, Xrange[1], Yrange[1])
    fillbox.SetFillStyle(1001)
    fillbox.SetFillColor(0)
    # line box
    linebox = ROOT.TBox(Xrange[0], Yrange[1]-21, Xrange[1], Yrange[1])
    linebox.SetFillStyle(0)
    linebox.SetLineWidth(2)
    linebox.SetLineStyle(1)
    linebox.SetLineColor(ROOT.kBlack)

    linebox.Draw("same")
    fillbox.Draw("same")

    # Draw Watermarks
    xatlas, yatlas = 0.3, 0.9
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas+0.3, yatlas, "#sqrt{s}=13 TeV, " + str(CONF.totlumi) + " fb^{-1}")
    watermarks = [atlas, hh4b]
    for wm in watermarks:
        wm.SetTextAlign(24)
        wm.SetTextSize(0.035)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()

    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".png")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".eps")
    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".C")

    #shut it down
    canv.Close()
    inputroot.Close()


if __name__ == "__main__":
    main()
