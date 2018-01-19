### This is the 2D distributions

import ROOT, rootlogon
import argparse
import array
import copy
import glob, helpers, os, sys, time
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
    '''run this to produce 2D MJ0-J1 plots for paper'''
    start_time = time.time()
    global StatusLabel
    StatusLabel = CONF.StatusLabel
    ops = options()
    inputdir = ops.inputdir
    global inputpath
    inputpath = CONF.inputpath + "TEST" + "/" ##have to change this to TEST to have full mHH region plots!!!
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "PaperPlot/Other/"
    print "output direcotry is: ", outputpath
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    # # paper plot
    DrawPaper2D("data_test/hist-MiniNTuple.root", "NoTag_Incl", prename="NoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2D("signal_G_hh_c10_M1200/hist-MiniNTuple.root", "AllTag_Incl", prename="Sig_1200_AllTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2D("signal_G_hh_c10_M2000/hist-MiniNTuple.root", "AllTag_Incl", prename="Sig_2000_AllTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    DrawPaper2DPrediction("data_test/hist-MiniNTuple.root", "NoTag_Incl", prename="TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250])

    # DrawPaper2D("signal_G_hh_c10_M2000/hist-MiniNTuple.root", "TwoTag_split_Incl", prename="Sig_2000_TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M2000/hist-MiniNTuple.root", "ThreeTag_Incl", prename="Sig_2000_ThreeTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M2000/hist-MiniNTuple.root", "FourTag_Incl", prename="Sig_2000_FourTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M1000/hist-MiniNTuple.root", "TwoTag_split_Incl", prename="Sig_1000_TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M1000/hist-MiniNTuple.root", "ThreeTag_Incl", prename="Sig_1000_ThreeTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M1000/hist-MiniNTuple.root", "FourTag_Incl", prename="Sig_1000_FourTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M3000/hist-MiniNTuple.root", "TwoTag_split_Incl", prename="Sig_3000_TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M3000/hist-MiniNTuple.root", "ThreeTag_Incl", prename="Sig_3000_ThreeTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("signal_G_hh_c10_M3000/hist-MiniNTuple.root", "FourTag_Incl", prename="Sig_3000_FourTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    # DrawPaper2D("ttbar_comb_test/hist-MiniNTuple.root", "NoTag_Incl", prename="Top_NoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2D("ttbar_comb_test/hist-MiniNTuple.root", "OneTag_Incl", prename="Top_OneTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    #special 2D optimization study

    # # for muqcd study
    # # outputpath = CONF.inputpath + inputdir + "/" + "Plot/Other/"
    # # if not os.path.exists(outputpath):
    # #     os.makedirs(outputpath)
    # DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_Incl",            prename="OneTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "OneTag_Incl",           prename="TwoTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_2Trk_split_Incl", prename="TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_3Trk_Incl",       prename="ThreeTag_Incl", Xrange=[50, 250], Yrange=[50, 250])
    # DrawPaper2DComparePrediction("data_test/hist-MiniNTuple.root", "NoTag_4Trk_Incl",       prename="FourTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    # # ## only if QCD sample exists
    # DrawPaper2DComparePrediction("signal_QCD/hist-MiniNTuple.root", "NoTag_Incl", prename="OneTag_Incl", Xrange=[50, 250], Yrange=[50, 250], subTop=False, extra="QCD_")
    # DrawPaper2DComparePrediction("signal_QCD/hist-MiniNTuple.root", "OneTag_Incl", prename="TwoTag_Incl", Xrange=[50, 250], Yrange=[50, 250], subTop=False, extra="QCD_")
    # DrawPaper2DComparePrediction("signal_QCD/hist-MiniNTuple.root",  "NoTag_2Trk_split_Incl", prename="TwoTag_split_Incl", Xrange=[50, 250], Yrange=[50, 250], subTop=False, extra="QCD_")
    # DrawPaper2DComparePrediction("signal_QCD/hist-MiniNTuple.root",  "NoTag_3Trk_Incl",       prename="ThreeTag_Incl", Xrange=[50, 250], Yrange=[50, 250], subTop=False, extra="QCD_")
    # DrawPaper2DComparePrediction("signal_QCD/hist-MiniNTuple.root",  "NoTag_4Trk_Incl",       prename="FourTag_Incl", Xrange=[50, 250], Yrange=[50, 250], subTop=False, extra="QCD_")

    # DrawPaper2DOptimzie("data_test/hist-MiniNTuple.root", "OneTag_Incl", prename="AllTag_Incl", Xrange=[50, 250], Yrange=[50, 250])

    print("--- %s seconds ---" % (time.time() - start_time))
# functions for the different regions
def mySB(x):
    #return  ROOT.TMath.Sqrt( (x[0]-124)**2 + (x[1]-115)**2)
    return  ROOT.TMath.Sqrt( (x[0]-134)**2 + (x[1]-125)**2)

def myCR(x):
    return  ROOT.TMath.Sqrt( (x[0]-124)**2 + (x[1]-115)**2)
    #return  ROOT.TMath.Sqrt( ((x[0]-124)/(0.1*x[0]))**2 + ((x[1]-115)/(0.1*x[1]))**2)

def mySR(x, leadC=124, sublC=115, leadW=0.085, tilt=1.4, tilt2=1.8):
    # value = 0
    # if (x[1] >= sublC):
    #     value = ROOT.TMath.Sqrt( ((x[0]-leadC)/(leadW*x[0]))**2 + ((x[1]-sublC)/(tilt * leadW*x[1]))**2)
    # if (x[1] < sublC):
    #     value = ROOT.TMath.Sqrt( ((x[0]-leadC)/(leadW*x[0]))**2 + ((x[1]-sublC)/(tilt2 * leadW*x[1]))**2)
    # return value
    # return  ROOT.TMath.Sqrt( ((x[0]-124)/(0.085*x[0]))**2 + ((x[1]-115)/(0.12*x[1]))**2)
    return  ROOT.TMath.Sqrt( ((x[0]-124)/(0.1*x[0]))**2 + ((x[1]-115)/(0.1*x[1]))**2)

def myTop(x):
    return  ROOT.TMath.Sqrt( ((x[0]-175)/(0.1*x[0]))**2 + ((x[1]-164)/(0.1*x[1]))**2 ) 
  

def DrawPaper2D(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0]):

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
    rebin_factor = 5 #default 5
    temp_hist.Rebin2D(rebin_factor, rebin_factor)
    #canv.SetLogz(1)
    temp_hist.Draw("colz")
    # Set Axis Labels
    temp_hist.GetXaxis().SetTitle("m_{J}^{lead} [GeV]")
    temp_hist.GetYaxis().SetTitle("m_{J}^{subl} [GeV]")
    temp_hist.GetZaxis().SetTitle("Events/10 GeV^{2}")
    temp_hist.GetZaxis().SetTitleOffset(1.6)
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
    fSR.SetLineWidth(3)
    fSR.SetLineStyle(5)
    fSR.Draw("same, cont3")

    # get control:
    fCR = ROOT.TF2("CR", myCR,0,Xrange[1],0,Xrange[1])
    contoursCR = array.array("d", [33.0])
    fCR.SetContour(1, contoursCR)
    fCR.SetNpx(600)
    fCR.SetLineColor(ROOT.kOrange+7)
    fCR.SetLineWidth(3)
    fCR.Draw("same, cont3")

    # sideband:
    fSB = ROOT.TF2("SB", mySB,0,Xrange[1],0,Xrange[1])
    contoursSB = array.array("d", [58.0])
    fSB.SetContour(1, contoursSB)
    fSB.SetNpx(600)
    fSB.SetLineColor(ROOT.kYellow)
    fSB.SetLineWidth(3)
    fSB.Draw("same, cont3")

    # # ttbar:
    # fTT = ROOT.TF2("TT", myTop,0,Xrange[1],0,Xrange[1])
    # contoursTT = array.array("d", [1.0])
    # fTT.SetContour(1, contoursTT)
    # fTT.SetNpx(50)
    # fTT.SetLineColor(46)
    # fTT.SetLineWidth(3)
    # fTT.SetLineStyle(5)
    # fTT.Draw("same, cont3")
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

    #print inputdir
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    inputroot_top = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist-MiniNTuple.root")
    #inputroot.cd(inputdir)
    temp_hist = inputroot.Get("NoTag_2Trk_split_Incl" + "/mH0H1").Clone()
    temp_hist_top = inputroot_top.Get("TwoTag_split_Incl" + "/mH0H1").Clone()

    #scale and add
    inputtex = CONF.inputpath + CONF.workdir + "/Plot/Tables/normfit.tex"
    f1 = open(inputtex, 'r')
    rebin_factor = 5 #default 5
    temp_hist.Rebin2D(rebin_factor, rebin_factor)
    temp_hist_top.Rebin2D(rebin_factor, rebin_factor)
    for line in f1: 
        #very stupid protection to distinguish 2b and 2bs
        if ("TwoTag") in line:
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
    contoursCR = array.array("d", [33.0])
    fCR.SetContour(1, contoursCR)
    fCR.SetNpx(400)
    fCR.SetLineColor(ROOT.kOrange+7)
    fCR.SetLineWidth(6)
    fCR.Draw("same, cont3")

    # sideband:
    fSB = ROOT.TF2("SB", mySB,0,Xrange[1],0,Xrange[1])
    contoursSB = array.array("d", [58.0])
    fSB.SetContour(1, contoursSB)
    fSB.SetNpx(400)
    fSB.SetLineColor(ROOT.kYellow)
    fSB.SetLineWidth(6)
    fSB.Draw("same, cont3")

    # # ttbar:
    # fTT = ROOT.TF2("TT", myTop,0,Xrange[1],0,Xrange[1])
    # contoursTT = array.array("d", [1.0])
    # fTT.SetContour(1, contoursTT)
    # fTT.SetNpx(50)
    # fTT.SetLineColor(46)
    # fTT.SetLineWidth(3)
    # fTT.SetLineStyle(5)
    # fTT.Draw("same, cont3")
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

def DrawPaper2DComparePrediction(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0], subTop=True, extra=""):
    ## functions for the different regions; specifcally for muqcd studies
    SB_rad = 58
    CR_rad = 33
    SR_rad = 1.6
 
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
    rebin_factor = 4 #default 5
    temp_hist.Rebin2D(rebin_factor, rebin_factor)
    temp_hist_top.Rebin2D(rebin_factor, rebin_factor)
    temp_hist_top_b.Rebin2D(rebin_factor, rebin_factor)
    temp_hist_data.Rebin2D(rebin_factor, rebin_factor)

    #add
    if (subTop):
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
    if (subTop):
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
    min_x = ROOT.Long(0)
    min_y = ROOT.Long(0)
    min_z = ROOT.Long(0)
    temp_hist_data.GetMaximumBin(max_x, max_y, max_z)
    temp_hist_data.GetMinimumBin(min_x, min_y, min_z)
    print "maxbin: ", max_x, max_y, " content: ", temp_hist_data.GetBinContent(max_x, max_y), " value: ",  inputroot.Get(prename + "/mH0H1").GetBinContent(max_x * rebin_factor, max_y * rebin_factor), inputroot.Get(inputdir + "/mH0H1").GetBinContent(max_x * rebin_factor, max_y * rebin_factor)
    #print "average muqcd: ", temp_hist_data.GetMean(3)
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
    local_min = temp_hist_data.GetBinContent(min_x, min_y)
    local_max = temp_hist_data.GetBinContent(max_x, max_y)
    ##this is a temp plot contains everything; to get mean value
    pull_hist_All = ROOT.TH1F("pull_All", "All; #mu_{qcd}; Counts", 50, local_min, local_max)
    for x_bin in range(temp_hist_data.GetXaxis().GetNbins()):
        for y_bin in range(temp_hist_data.GetYaxis().GetNbins()):
            pull_hist_All.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
    local_mean = pull_hist_All.GetMean()
    local_RMS  = pull_hist_All.GetRMS()
    local_scale = 3.5
    local_fill_min = max(local_mean - local_scale * 0.5 * local_RMS, 0)
    local_fill_max = max(local_mean + local_scale * 0.5 * local_RMS, 0)
    pull_hist_OT = ROOT.TH1F("pull_OT", "OT; #mu_{qcd}; Weighted Counts", 40, local_fill_min, local_fill_max)
    pull_hist_SB = ROOT.TH1F("pull_SB", "SB; #mu_{qcd}; Weighted Counts", 40, local_fill_min, local_fill_max)
    pull_hist_CR = ROOT.TH1F("pull_CR", "CR; #mu_{qcd}; Weighted Counts", 40, local_fill_min, local_fill_max)
    pull_hist_SR = ROOT.TH1F("pull_SR", "SR; #mu_{qcd}; Weighted Counts", 40, local_fill_min, local_fill_max)
    ##blind SR and CR; notice it is exclusive!
    for x_bin in range(temp_hist_data.GetXaxis().GetNbins()):
        for y_bin in range(temp_hist_data.GetYaxis().GetNbins()):
            #pull_hist_OT.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
            if mySR((temp_hist_data.GetXaxis().GetBinCenter(x_bin), temp_hist_data.GetYaxis().GetBinCenter(y_bin))) < SR_rad:
                if (CONF.blind is True and "QCD" not in extra) and ("ThreeTag_" in prename or "TwoTag_split_" in prename or "FourTag_" in prename ):
                    temp_hist_data.SetBinContent(x_bin, y_bin, 0)
                else:
                    pull_hist_SR.Fill(temp_hist_data.GetBinContent(x_bin, y_bin), temp_hist_data_copy.GetBinContent(x_bin, y_bin))
            elif myCR((temp_hist_data.GetXaxis().GetBinCenter(x_bin), temp_hist_data.GetYaxis().GetBinCenter(y_bin))) < CR_rad:
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
    temp_hist_data.GetZaxis().SetRangeUser(local_fill_min, local_fill_max)
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


    canv.SaveAs(outputpath + extra + prename + "_" +  canv.GetName() + ".pdf")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".png")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".eps")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".C")

    ##draw the stacked pull
    canv.Clear()
    #canv.SetLogy(1)
    canv.SetRightMargin(0.13)
    pull_hs = ROOT.THStack("pull_hs","; #mu_{qcd}; Counts")
    pull_hist_OT.SetFillColor(CONF.clr_lst[3])
    pull_hist_SB.SetFillColor(CONF.clr_lst[1])
    pull_hist_CR.SetFillColor(CONF.clr_lst[2])
    pull_hist_SR.SetFillColor(CONF.clr_lst[0])
    pull_hist_OT.SetLineColor(CONF.clr_lst[3])
    pull_hist_SB.SetLineColor(CONF.clr_lst[1])
    pull_hist_CR.SetLineColor(CONF.clr_lst[2])
    pull_hist_SR.SetLineColor(CONF.clr_lst[0])
    pull_hist_OT.SetMarkerColor(CONF.clr_lst[3])
    pull_hist_SB.SetMarkerColor(CONF.clr_lst[1])
    pull_hist_CR.SetMarkerColor(CONF.clr_lst[2])
    pull_hist_SR.SetMarkerColor(CONF.clr_lst[0])
    pull_hist_OT.SetMarkerStyle(CONF.mrk_lst[3])
    pull_hist_SB.SetMarkerStyle(CONF.mrk_lst[1])
    pull_hist_CR.SetMarkerStyle(CONF.mrk_lst[2])
    pull_hist_SR.SetMarkerStyle(CONF.mrk_lst[0])
    f_gaus_OT = ROOT.TF1("f_gaus_OT", "gaus", local_fill_min, local_fill_max)
    f_gaus_SB = ROOT.TF1("f_gaus_SB", "gaus", local_fill_min, local_fill_max)
    f_gaus_CR = ROOT.TF1("f_gaus_CR", "gaus", local_fill_min, local_fill_max)
    f_gaus_SR = ROOT.TF1("f_gaus_SR", "gaus", local_fill_min, local_fill_max)
    #f_gaus_OT.SetLineColor(CONF.clr_lst[3])
    f_gaus_SB.SetLineColor(CONF.clr_lst[1])
    f_gaus_CR.SetLineColor(CONF.clr_lst[2])
    f_gaus_SR.SetLineColor(CONF.clr_lst[0])
    pull_hs.SetMinimum(0.1)
    pull_hs.SetMaximum(pull_hist_SB.GetMaximum()*2.5)
    # pull_hist_OT.SetMinimum(0.1)
    # pull_hist_SB.SetMinimum(0.1)
    # pull_hist_CR.SetMinimum(0.1)
    # pull_hist_SR.SetMinimum(0.1)
    pull_hist_OT.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    pull_hist_SB.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    pull_hist_CR.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    pull_hist_SR.SetMaximum(pull_hist_SB.GetMaximum()*1.5)
    # pull_hist_OT.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*1.5)
    # pull_hist_SB.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*1.5)
    # pull_hist_CR.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*1.5)
    # pull_hist_SR.GetYaxis().SetRangeUser(0.1, pull_hist_SB.GetMaximum()*1.5)
    #pull_hs.Add(pull_hist_OT)
    #pull_hs.Add(pull_hist_SB)
    #pull_hs.Add(pull_hist_CR)
    #pull_hs.Add(pull_hist_SR)
    #pull_hist_OT.Draw("hist")
    #pull_hs.Draw("hist")
    #pull_hist_OT.Draw()
    pull_hist_SB.Draw("")
    pull_hist_CR.Draw("same")
    pull_hist_SR.Draw("same")
    ### do the guassian fit
    pull_hist_SB.Fit(f_gaus_SB, "QL")
    f_gaus_SB.Draw("same")
    pull_hist_CR.Fit(f_gaus_CR, "QL")
    f_gaus_SB.Draw("same")
    pull_hist_SR.Fit(f_gaus_SR, "QL")
    f_gaus_SB.Draw("same")
    ### do the outside ring
    #pull_hist_OT.Fit(f_gaus_OT, "QL")
    #f_gaus_OT.Draw("same")

    #pull_hist_OT.Draw("same")
    leg = ROOT.TLegend(0.2,0.75,0.8,0.92)
    #leg.AddEntry(pull_hist_OT, "OT mean: %.3f" % pull_hist_OT.GetMean())
    leg.AddEntry(pull_hist_SB, "SB mean: %.3f #pm %.3f; Gaus mean: %.3f width: %.3f" % (pull_hist_SB.GetMean(), pull_hist_SB.GetMeanError(), f_gaus_SB.GetParameter(1), f_gaus_SB.GetParameter(2) ))
    leg.AddEntry(pull_hist_CR, "CR mean: %.3f #pm %.3f; Gaus mean: %.3f width: %.3f" % (pull_hist_CR.GetMean(), pull_hist_CR.GetMeanError(), f_gaus_CR.GetParameter(1), f_gaus_CR.GetParameter(2) ))
    leg.AddEntry(pull_hist_SR, "SR mean: %.3f #pm %.3f; Gaus mean: %.3f width: %.3f" % (pull_hist_SR.GetMean(), pull_hist_SR.GetMeanError(), f_gaus_SR.GetParameter(1), f_gaus_SR.GetParameter(2) ))
    print prename
    print "SB mean: %.3f #pm %.3f; Gaus mean: %.3f width: %.3f" % (pull_hist_SB.GetMean(), pull_hist_SB.GetMeanError(), f_gaus_SB.GetParameter(1), f_gaus_SB.GetParameter(2) )
    print "CR mean: %.3f #pm %.3f; Gaus mean: %.3f width: %.3f" % (pull_hist_CR.GetMean(), pull_hist_CR.GetMeanError(), f_gaus_CR.GetParameter(1), f_gaus_CR.GetParameter(2) )
    print "SR mean: %.3f #pm %.3f; Gaus mean: %.3f width: %.3f" % (pull_hist_SR.GetMean(), pull_hist_SR.GetMeanError(), f_gaus_SR.GetParameter(1), f_gaus_SR.GetParameter(2) )
    #leg.AddEntry(pull_hist_OT, "OT mean: %.3f #pm %.3f; Gaus mean: %.3f width: %.3f" % (pull_hist_OT.GetMean(), pull_hist_OT.GetMeanError(), f_gaus_OT.GetParameter(1), f_gaus_OT.GetParameter(2) ))
    leg.SetTextFont(43)
    leg.SetTextSize(CONF.legsize)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.Draw()
    canv.SaveAs(outputpath + extra + prename + "_" +  canv.GetName() + "_pull.pdf")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_pull.root")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + "_pull.C")

    #shut it down
    canv.Close()
    inputroot.Close()
    inputroot_top.Close()
    f1.close()

def DrawPaper2DOptimzie(inputname, inputdir, keyword="_", prename="", Xrange=[0, 0], Yrange=[0, 0], subTop=True, extra=""):
    ## functions for the different regions; specifcally for muqcd studies
    SB_rad = 53
    CR_rad = 33
    SR_rad = 1.6

    rebin_factor = 1 #default 5
    inputroot = ROOT.TFile.Open(inputpath + inputname)
    temp_hist      = inputroot.Get(inputdir + "/mH0H1").Clone()
    temp_hist.Rebin2D(rebin_factor, rebin_factor)
    outputroot = ROOT.TFile.Open(outputpath + "Optimize_cut.root", "recreate")

    hist_cuts_Xhh   = ROOT.TH1F("cuts_Xhh_G", ";mass; Xhh", 23, 750, 3050)
    hist_cuts_leadC = ROOT.TH1F("cuts_leadC_G", ";mass;  leadH Center, GeV;", 23, 750, 3050)
    hist_cuts_sublC = ROOT.TH1F("cuts_sublC_G", ";mass;  sublH Center, GeV;", 23, 750, 3050)
    hist_cuts_leadW = ROOT.TH1F("cuts_leadW_G", ";mass;  leadH Width ratio;", 23, 750, 3050)
    hist_cuts_tilt  = ROOT.TH1F("cuts_tilt_G",  ";mass;  sublH/leadH Width ratio;", 23, 750, 3050)
    hist_cuts_tilt2 = ROOT.TH1F("cuts_tilt2_G",  ";mass;  sublH/leadH Width ratio;", 23, 750, 3050)
    
    hist_cuts_dict = {
        0:hist_cuts_Xhh, 
        1:hist_cuts_leadC, 
        2:hist_cuts_sublC, 
        3:hist_cuts_leadW, 
        4:hist_cuts_tilt,  
        5:hist_cuts_tilt2, 
        }

    for mass in [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]:
    #for mass in [2000]:
        #print inputdir
        #print inputdir
        inputroot_sig = ROOT.TFile.Open(inputpath + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root")
        #zero tag background estiamte string
        temp_hist_sig  = inputroot_sig.Get(prename + "/mH0H1").Clone("mH0H1_" + str(mass))
        #rebin
        temp_hist_sig.Rebin2D(rebin_factor, rebin_factor)

        #add    ##blind SR and CR; notice it is exclusive!
        hist_sens_Xhh   = ROOT.TH1F("sens_Xhh_G"+str(mass), "; Xhh; Sensitivity;", 40, 1.3, 2.1)
        hist_sens_leadC = ROOT.TH1F("sens_leadC_G"+str(mass), "; leadH Center, GeV; Sensitivity;", 40, 115, 135)
        hist_sens_sublC = ROOT.TH1F("sens_sublC_G"+str(mass), "; sublH Center, GeV; Sensitivity;", 40, 108, 128)
        hist_sens_leadW = ROOT.TH1F("sens_leadW_G"+str(mass), "; leadH Width ratio, GeV; Sensitivity;", 40, 0.06, 0.1)
        hist_sens_tilt  = ROOT.TH1F("sens_tilt_G"+str(mass),  "; sublH/leadH Width ratio; Sensitivity;", 40, 1.2, 2.0)
        hist_sens_tilt2 = ROOT.TH1F("sens_tilt2_G"+str(mass),  "; sublH/leadH Width ratio2; Sensitivity;", 40, 1.4, 2.2)
        
        hist_sens_dict = {
            0:hist_sens_Xhh, 
            1:hist_sens_leadC, 
            2:hist_sens_sublC, 
            3:hist_sens_leadW, 
            4:hist_sens_tilt,  
            5:hist_sens_tilt2, 
            }

        maxj = 0
        maxsensitivity = 0
        def update_SB(x_bin, y_bin, S, B, S_err, B_err):
            B += temp_hist.GetBinContent(x_bin, y_bin)
            S += temp_hist_sig.GetBinContent(x_bin, y_bin)
            S_err = ROOT.TMath.Sqrt(S_err * S_err + temp_hist_sig.GetBinError(x_bin, y_bin) ** 2)
            B_err = ROOT.TMath.Sqrt(B_err * B_err + temp_hist.GetBinError(x_bin, y_bin) ** 2)
            return S, B, S_err, B_err

        for j in range(40):
            S = [0, 0, 0, 0, 0, 0]
            B = [0, 0, 0, 0, 0, 0]
            S_err = [0, 0, 0, 0, 0, 0]
            B_err = [0, 0, 0, 0, 0, 0]
            for x_bin in range(temp_hist.GetXaxis().FindBin(100), temp_hist.GetXaxis().FindBin(160)):
                for y_bin in range(temp_hist.GetYaxis().FindBin(80), temp_hist.GetYaxis().FindBin(150)):
                    if mySR((temp_hist.GetXaxis().GetBinCenter(x_bin), temp_hist.GetYaxis().GetBinCenter(y_bin))) < 1.3 + j * 0.02:
                        S[0], B[0], S_err[0], B_err[0] = update_SB( x_bin, y_bin, S[0], B[0], S_err[0], B_err[0])
                    if mySR((temp_hist.GetXaxis().GetBinCenter(x_bin), temp_hist.GetYaxis().GetBinCenter(y_bin)), leadC=115 +  j*0.5) < SR_rad:
                        S[1], B[1], S_err[1], B_err[1] = update_SB( x_bin, y_bin, S[1], B[1], S_err[1], B_err[1])
                    if mySR((temp_hist.GetXaxis().GetBinCenter(x_bin), temp_hist.GetYaxis().GetBinCenter(y_bin)), sublC=108 +  j*0.5) < SR_rad:
                        S[2], B[2], S_err[2], B_err[2] = update_SB( x_bin, y_bin, S[2], B[2], S_err[2], B_err[2])
                    if mySR((temp_hist.GetXaxis().GetBinCenter(x_bin), temp_hist.GetYaxis().GetBinCenter(y_bin)), leadW=0.06 +  j*0.001) < SR_rad:
                        S[3], B[3], S_err[3], B_err[3] = update_SB( x_bin, y_bin, S[3], B[3], S_err[3], B_err[3])
                    if mySR((temp_hist.GetXaxis().GetBinCenter(x_bin), temp_hist.GetYaxis().GetBinCenter(y_bin)), tilt=1.2 + j*0.02) < SR_rad:
                        S[4], B[4], S_err[4], B_err[4] = update_SB( x_bin, y_bin, S[4], B[4], S_err[4], B_err[4])
                    if mySR((temp_hist.GetXaxis().GetBinCenter(x_bin), temp_hist.GetYaxis().GetBinCenter(y_bin)), tilt2=1.4 + j*0.02) < SR_rad:
                        S[5], B[5], S_err[5], B_err[5] = update_SB( x_bin, y_bin, S[5], B[5], S_err[5], B_err[5])

                    #if mySR((temp_hist.GetXaxis().GetBinCenter(x_bin), temp_hist.GetYaxis().GetBinCenter(y_bin)), tilt= 1 - 0.2 + j * 0.02) < 1.6:
            for i in range(6):
                sensitivity = (1.0*S[i])/(1 + ROOT.TMath.Sqrt(B[i]))
                try:
                    sensitivity_err = sensitivity * ROOT.TMath.Sqrt((1.0*S_err[i]/S[i])**2 + (1./(4*B[i]))*((1.0*B_err[i]/(1+ROOT.TMath.Sqrt(B[i])))**2))
                except ZeroDivisionError:
                    sensitivity_err = 0

                hist_sens_dict[i].SetBinContent(j, sensitivity)
                hist_sens_dict[i].SetBinError(j, sensitivity_err)
            #print "quick estimate ", j, " sens ", sensitivity - 0.163538536032, " pm ", sensitivity_err
            #print "quick estimate ", j, " sens ", sensitivity, " pm ", sensitivity_err
            if sensitivity > maxsensitivity:
                maxsensitivity = sensitivity
                maxj = j

        for i in range(6):
            print i, hist_sens_dict[i].GetName(), hist_sens_dict[i].GetMaximum(), " bin: ", hist_sens_dict[i].GetBinCenter(hist_sens_dict[i].GetMaximumBin())
            hist_cuts_dict[i].Fill(mass, hist_sens_dict[i].GetBinCenter(hist_sens_dict[i].GetMaximumBin()))##only fill the maximum here
            bin_error = 0
            for j in range(40):
                #print abs(hist_sens_dict[i].GetBinContent(j) -  hist_sens_dict[i].GetMaximum()), hist_sens_dict[i].GetBinError(hist_sens_dict[i].GetMaximumBin())
                if abs(hist_sens_dict[i].GetBinContent(j) -  hist_sens_dict[i].GetMaximum()) < hist_sens_dict[i].GetBinError(hist_sens_dict[i].GetMaximumBin()):
                    bin_error = hist_sens_dict[i].GetBinCenter(hist_sens_dict[i].GetMaximumBin()) - hist_sens_dict[i].GetBinCenter(j) 
                    print hist_sens_dict[i].GetBinContent(j),  hist_sens_dict[i].GetMaximum(), j, bin_error
                    break
            hist_cuts_dict[i].SetBinError(hist_cuts_dict[i].GetXaxis().FindBin(mass), bin_error)##only set the maximum error here

        outputroot.cd()
        canv = ROOT.TCanvas(temp_hist.GetName(), temp_hist.GetTitle(), 1000, 800)
        for i in range(6):
            hist_sens_dict[i].GetYaxis().SetRangeUser(hist_sens_dict[i].GetMaximum() * 0.8, hist_sens_dict[i].GetMaximum() * 1.1)
            hist_sens_dict[i].Draw()
            hist_sens_dict[i].Write()
            canv.SaveAs(outputpath + hist_sens_dict[i].GetName() + ".pdf")
            canv.Clear()
        
        #del temp_hist_sig
        inputroot_sig.Close()
    
    #shut it down
    outputroot.cd()
    for i in range(6):
        average_value = hist_cuts_dict[i].Integral()/(15.0)
        print i, hist_cuts_dict[i].GetName(), average_value
        hist_cuts_dict[i].GetYaxis().SetRangeUser(average_value * 0.8, average_value * 1.2)
        hist_cuts_dict[i].Draw()
        hist_cuts_dict[i].Write()
        canv.SaveAs(outputpath + hist_cuts_dict[i].GetName() + ".pdf")
        canv.Clear()
    outputroot.Close()
    inputroot.Close()


if __name__ == "__main__":
    main()
