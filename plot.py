# plot.py
#  main():
#   -> plotCR(...)
#   -> plotSR(...)
#
#
import os
import sys
import math
import ROOT
from ROOT import *
import AtlasStyle
gROOT.LoadMacro("AtlasLabels.C")
from array import array
TH1.AddDirectory(False)

StatusLabel="Internal"

ROOT.gROOT.SetBatch(True)
# zero the x-errors
def zeroXerror(g):
    for i in range(0,g.GetN()):
        g.SetPointEXlow(i,  0.0)
        g.SetPointEXhigh(i, 0.0) 

# function to build total background in histograma and graph format
def makeTotBkg(bkgs=[], bkgsUp=[], bkgsDown=[]):
    # total bkg histogram
    hBkg = bkgs[0].Clone("bkg")
    if len(bkgs)>1:
        hBkg.Reset()
        for h in bkgs:
            hBkg.Add(h)
    # total bkg graph with errors
    gBkg = ROOT.TGraphAsymmErrors(bkgs[0].GetNbinsX())
    # add stat errors
    for i in range(0, gBkg.GetN()):
        gBkg.SetPoint(i,       hBkg.GetBinCenter(i+1), hBkg.GetBinContent(i+1))
        gBkg.SetPointEXlow(i,  hBkg.GetBinWidth(i+1) / 2.)
        gBkg.SetPointEXhigh(i, hBkg.GetBinWidth(i+1) / 2.)
        gBkg.SetPointEYlow(i,  hBkg.GetBinError(i+1))
        gBkg.SetPointEYhigh(i, hBkg.GetBinError(i+1))
    # add syst errors (if provided)
    if len(bkgsUp)>0:
        # loop over points
        for i in range(0, gBkg.GetN()):
            ### error up
            err = math.pow(gBkg.GetErrorYhigh(i),2)
            # loop over backgrounds
            for ih in range(0, len(bkgs)):
                err += math.pow(math.fabs( bkgs[ih].GetBinContent(i+1) - bkgsUp[ih].GetBinContent(i+1) ), 2)
            gBkg.SetPointEYhigh(i, math.sqrt(err))
            ### error down
            err = math.pow(gBkg.GetErrorYlow(i),2)
            # loop over backgrounds
            for ih in range(0, len(bkgs)):
                err += math.pow(math.fabs( bkgs[ih].GetBinContent(i+1) - bkgsDown[ih].GetBinContent(i+1) ), 2)
            gBkg.SetPointEYlow(i, math.sqrt(err))

    return [hBkg, gBkg]

# function to build data/bkgd ratios
def makeDataRatio(data, bkg):
    # ratio set to one with error band 
    gRatioBand = data.Clone("gRatioBand")
    for i in range(0, data.GetN()):
        gRatioBand.SetPoint(i, data.GetX()[i], 1.0)
        if bkg.GetY()[i] > 0:
            gRatioBand.SetPointEYhigh(i, bkg.GetErrorYhigh(i) / bkg.GetY()[i]) 
            gRatioBand.SetPointEYlow(i, bkg.GetErrorYlow(i) / bkg.GetY()[i])             
            gRatioBand.SetPointEXhigh(i, bkg.GetErrorXhigh(i)) 
            gRatioBand.SetPointEXlow(i, bkg.GetErrorXlow(i))             
    # ratio set to data/bkg with data stat errors only
    gRatioDataBkg = data.Clone("gRatioDataBkg")
    for i in range(0, data.GetN()):
        if data.GetY()[i]>0 and bkg.GetY()[i]>0:
            gRatioDataBkg.SetPoint(i, data.GetX()[i], data.GetY()[i] / bkg.GetY()[i])
            gRatioDataBkg.SetPointEYhigh(i, data.GetErrorYhigh(i) / bkg.GetY()[i])
            gRatioDataBkg.SetPointEYlow(i, data.GetErrorYlow(i) / bkg.GetY()[i])
            gRatioDataBkg.SetPointEXhigh(i, data.GetErrorXhigh(i)) 
            gRatioDataBkg.SetPointEXlow(i, data.GetErrorXlow(i))             
        else:
            gRatioDataBkg.SetPoint(i, 0.0, -1000)

    return [gRatioBand,gRatioDataBkg]

def do_variable_rebinning(hist,bins, scale=1.0):
    a=hist.GetXaxis()
    newhist=ROOT.TH1F(hist.GetName()+"_rebinned",
                      hist.GetTitle()+";"+hist.GetXaxis().GetTitle()+";"+hist.GetYaxis().GetTitle(),
                      len(bins)-1,
                      array('d',bins))

    newhist.Sumw2()
    newa=newhist.GetXaxis()

    for b in range(1, hist.GetNbinsX()+1):
        newb             = newa.FindBin(a.GetBinCenter(b))

        # Get existing new content (if any)                                                                                                              
        val              = newhist.GetBinContent(newb)
        err              = newhist.GetBinError(newb)

        # Get content to add
        ratio_bin_widths = scale*newa.GetBinWidth(newb)/a.GetBinWidth(b)
        #print "ratio_bin_widths",ratio_bin_widths
        val              = val+hist.GetBinContent(b)/ratio_bin_widths
        err              = math.sqrt(err*err+hist.GetBinError(b)/ratio_bin_widths*hist.GetBinError(b)/ratio_bin_widths)
        newhist.SetBinContent(newb,val)
        newhist.SetBinError(newb,err)

    return newhist

def graphFromHist(hist):
    hist.SetBinErrorOption(1)

    nBins = hist.GetNbinsX()

    dataGr = ROOT.TGraphAsymmErrors(nBins)
    dataGr.SetName("data_hh")
    for i in range(nBins):
        thisX        = hist.GetBinCenter(i+1)
        thisY        = hist.GetBinContent(i+1)
        if thisY:
            thisYErrLow  = hist.GetBinErrorLow(i+1)
            thisYErrUp   = hist.GetBinErrorUp(i+1)
            binWidthOver2  = thisX - hist.GetBinLowEdge(i+1)
        else:
            thisYErrLow = 0
            thisYErrUp  = 0
            binWidthOver2  = thisX - hist.GetBinLowEdge(i+1)
        #print i, thisX, thisY, thisYErrLow, thisYErrUp                                                                                                  
        dataGr.SetPoint(i,thisX, thisY)
        dataGr.SetPointError(i, binWidthOver2, binWidthOver2, thisYErrLow, thisYErrUp)
    return dataGr

def rebinData(ifile, rebin, scale=1.0):
    dataHist = ifile.Get("data_hh_hist")    
    dataHistNew = do_variable_rebinning(dataHist, rebin, scale)
    return graphFromHist(dataHistNew)

####################################################################################
#plot

def plotRegion(filename, cut, xTitle, yTitle, xMin, xMax, yMax, rMin, rMax, labelPos, rebin=None, inputBinWidth=25, finalBinUnits=25):

    gStyle.SetErrorX(0)
    gStyle.SetHatchesSpacing(0.7)
    gStyle.SetHatchesLineWidth(1)

    # input file
    ifile = ROOT.TFile(filename)

    # read stuff
    data = ifile.Get("data_" + cut )
    qcd = ifile.Get("qcd_est_" + cut )
    qcd_origin = ifile.Get("qcd_" + cut )
    print "factor is ", qcd.Integral()/qcd_origin.Integral()
    ttbar = ifile.Get("ttbar_" + cut )
    zjet = ifile.Get("zjet_" + cut )
    RSG1_1000 = ifile.Get("RSG1_1000_" + cut )
    RSG1_1500 = ifile.Get("RSG1_1500_" + cut )
    RSG1_2000 = ifile.Get("RSG1_2000_" + cut )
    yMax = data.GetMaximum() * 1.5
    #qcd_fit = ifile.Get("qcd_fit")
    #qcd_fitUp = ifile.Get("qcd_fitUp")
    #qcd_fitDown = ifile.Get("qcd_fitDown")

    if not rebin == None:
        if isinstance(rebin,list):
            binScale = float(inputBinWidth)/finalBinUnits

            data  = do_variable_rebinning(data, rebin, binScale)
            qcd   = do_variable_rebinning(qcd, rebin, binScale)
            ttbar = do_variable_rebinning(ttbar, rebin, binScale)
            zjet = do_variable_rebinning(zjet, rebin, binScale)
        else:
            print "rebin has to be a list"
            import sys
            sys.exit(-1)

    # total background: [0] histogram, [1] graph for the bkg errors
    if filename.find("boosted")>-1:
        totalbkg_hh = ifile.Get("totalbkg_hh")
        if isinstance(rebin,list):
            binScale = float(inputBinWidth)/finalBinUnits
            totalbkg_hh = do_variable_rebinning(totalbkg_hh, rebin,binScale)
        bkg = makeTotBkg([totalbkg_hh])
    else:
        data = makeTotBkg([data])[1]
        bkg = makeTotBkg([ttbar,qcd,zjet])

    # bkg/data ratios: [0] band for bkg errors, [1] bkg/data with stat errors only
    ratios = makeDataRatio(data,bkg[1])

    # canvas
    c0 = ROOT.TCanvas("c0"+filename+cut, "Insert hilarious TCanvas name here", 800, 600)
    c0.SetRightMargin(0.05)

    # top pad
    pad0 = ROOT.TPad("pad0", "pad0", 0.0, 0.31, 1., 1.)
    pad0.SetRightMargin(0.05)
    pad0.SetBottomMargin(0.0001)
    pad0.SetFrameFillColor(0)
    pad0.SetFrameBorderMode(0)
    pad0.SetFrameFillColor(0)
    pad0.SetBorderMode(0)
    pad0.SetBorderSize(0)

    pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.0, 1., 0.29)
    pad1.SetRightMargin(0.05)
    pad1.SetBottomMargin(0.38)
    pad1.SetTopMargin(0.0001)
    pad1.SetFrameFillColor(0)
    pad1.SetFillStyle(0) # transparent
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(0)

    c0.cd()
    pad0.Draw()
    pad0.cd()

    bkg[0].SetTitle("")
    bkg[0].SetStats(0)
    bkg[0].SetLineColor(ROOT.kBlack)
    bkg[0].SetLineWidth(2)
    bkg[0].GetYaxis().SetTitleFont(43)
    bkg[0].GetYaxis().SetTitleSize(28)
    bkg[0].GetYaxis().SetLabelFont(43)
    bkg[0].GetYaxis().SetLabelSize(28)
    bkg[0].GetYaxis().SetTitle(yTitle)
    bkg[0].GetYaxis().SetRangeUser(0.001, yMax)
    #bkg[0].GetYaxis().SetRangeUser(0, yMax)
    bkg[0].GetXaxis().SetRangeUser(xMin, xMax)
    bkg[0].SetFillColor(ROOT.kYellow)
    bkg[0].Draw("HISTO")

    bkg[1].SetFillColor(ROOT.kBlue)
    bkg[1].SetLineColor(ROOT.kBlue)
    bkg[1].SetFillStyle(3345)
    bkg[1].SetMarkerSize(0)
    bkg[1].Draw("E2 SAME")

    ttbar.SetLineWidth(2)
    ttbar.SetLineColor(ROOT.kBlack)
    ttbar.SetFillColor(ROOT.kAzure-9)
    ttbar.Draw("HISTO SAME")

    zjet.SetLineWidth(2)
    zjet.SetLineColor(ROOT.kBlack)
    zjet.SetFillColor(ROOT.kGreen+4)
    zjet.Draw("HISTO SAME")

    # RSG1_1000.SetLineWidth(2)
    # RSG1_1000.SetLineStyle(2)
    # RSG1_1000.SetLineColor(ROOT.kViolet+7)
    # RSG1_1000.Draw("HISTO SAME")

    RSG1_1500.Scale(25)
    RSG1_1500.SetLineWidth(2)
    RSG1_1500.SetLineStyle(2)
    RSG1_1500.SetLineColor(ROOT.kPink+7)
    RSG1_1500.Draw("HISTO SAME")


    RSG1_2000.Scale(100)
    RSG1_2000.SetLineWidth(2)
    RSG1_2000.SetLineStyle(2)
    RSG1_2000.SetLineColor(ROOT.kGreen+4)
    RSG1_2000.Draw("HISTO SAME")

    zeroXerror(data)
    data.SetMarkerStyle(20)
    data.SetMarkerSize(1)
    data.SetLineWidth(2)
    data.Draw("EPZ SAME")

    # bottom pad
    c0.cd()
    pad1.Draw()
    pad1.cd()

    hratio = ROOT.TH1F("hratio","",1,xMin,xMax)
    hratio.SetStats(0)
    
    hratio.GetYaxis().SetTitleFont(43)
    hratio.GetYaxis().SetTitleSize(28)
    hratio.GetYaxis().SetLabelFont(43)
    hratio.GetYaxis().SetLabelSize(28)
    hratio.GetYaxis().SetTitle("Data / Bkgd")
    hratio.GetYaxis().SetRangeUser(rMin, rMax)
    hratio.GetYaxis().SetNdivisions(405)

    hratio.GetXaxis().SetTitleFont(43)
    hratio.GetXaxis().SetTitleOffset(3.5)
    hratio.GetXaxis().SetTitleSize(28)
    hratio.GetXaxis().SetLabelFont(43)
    hratio.GetXaxis().SetLabelSize(28)
    hratio.GetXaxis().SetTitle(xTitle)

    hratio.Draw()
    
    #zeroXerror(ratios[1])
    ratios[1].SetMarkerStyle(20)
    ratios[1].SetMarkerSize(1)
    ratios[1].SetLineWidth(2)
    ratios[1].Draw("E0PZ SAME")
    # qcd_fit.SetLineColor(kRed)
    # qcd_fitUp.SetLineColor(kRed)
    # qcd_fitUp.SetLineStyle(2)
    # qcd_fitDown.SetLineColor(kRed)
    # qcd_fitDown.SetLineStyle(2)
    # qcd_fit.Draw("SAME")
    # qcd_fitUp.Draw("SAME")
    # qcd_fitDown.Draw("SAME")


    #
    # Add stat uncertianty
    #
    ratios[0].SetFillColor(kBlue)
    ratios[0].SetFillStyle(3345)
    ratios[0].Draw("E2 same")


    line = ROOT.TLine(xMin, 1.0, xMax, 1.0)
    line.SetLineStyle(1)
    line.Draw()

    c0.cd()

    # labels
    legHunit=0.05
    legH=legHunit*6 # retuned below based on number of entries to 0.05*num_entries
    legW=0.4
    if labelPos==1:
        leg = ROOT.TLegend(0.6, 0.702-legH, 0.6+legW, 0.702)
        # top right
        ATLASLabel(0.61,0.85, StatusLabel);
        myText(0.61,0.80, 1, "#sqrt{s}=13 TeV, 3.2 fb^{-1}", 22);
        myText(0.61,0.75, 1, ' ' + cut.replace("_", "; "), 22);
    elif labelPos==11:
        leg = ROOT.TLegend(0.6, 0.72-legH, 0.6+legW, 0.72)
        # top right, a bit left
        ATLASLabel(0.57,0.85,StatusLabel);
        myText(0.57,0.80, 1, "#sqrt{s}=13 TeV, 3.2 fb^{-1}", 22);
        myText(0.57,0.75, 1, ' ' + cut.replace("_", "; "), 22);
    elif labelPos==2:
        leg = ROOT.TLegend(0.6, 0.905-legH, 0.6+legW, 0.905)
        # top
        ATLASLabel(0.26,0.86,StatusLabel);
        myText(0.26,0.81, 1, "#sqrt{s}=13 TeV, 3.2 fb^{-1}", 22);
        myText(0.26,0.76, 1, ' ' + cut.replace("_", "; "), 22);
    else:
        leg = ROOT.TLegend(0.6, 0.905-legH, 0.6+legW, 0.905)

    ##### legend
    leg.SetTextFont(43)
    leg.SetTextSize(22)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(data, "Data", "PE")
    leg.AddEntry(bkg[0], "Multijet", "F")
    leg.AddEntry(ttbar, "t#bar{t}","F")
    leg.AddEntry(zjet, "Z+jets","F")
    leg.AddEntry(bkg[1], "Stat Uncertainty", "F")
    #leg.AddEntry(RSG1_1000, "RSG1, 1TeV", "F")
    leg.AddEntry(RSG1_1500, "RSG1, 1.5TeV * 25", "F")
    leg.AddEntry(RSG1_2000, "RSG1, 2TeV * 100", "F")
    #leg.AddEntry(qcd_fit, "Fit to Ratio", "L")
    #leg.AddEntry(qcd_fitUp, "#pm 1#sigma Uncertainty", "L")
    leg.SetY1(leg.GetY2()-leg.GetNRows()*legHunit)
    leg.Draw()

    # save
    #c0.SaveAs("../"+figuresFolder+"/"+filename.replace(".root", ".pdf"))
    c0.SaveAs("../"+figuresFolder+"/"+ cut + ".png")
    #c0.SaveAs("../"+figuresFolder+"/"+ cut + ".pdf")
    #c0.SaveAs("../"+figuresFolder+"/"+ cut + ".eps")



##################################################################################################
# Main

def main():

    global StatusLabel
    StatusLabel = "Internal" ##StatusLabel = "Preliminary"
    
    global figuresFolder
    figuresFolder = "Plot"
    
    # plot in the control region #
    # plotRegion("../Plot/TEST_b77.root", cut="4Trk_FourTag_Signal_mHH_l",xTitle="m_{2J} [GeV]",yTitle="Number of Events",xMin=500,xMax=3000,yMax=20,rMin=0.001,rMax=2.5,labelPos=11,rebin=None)
    
    # cut_lst = ["2Trk_in1_NoTag", "2Trk_in1_OneTag", "2Trk_in1_TwoTag", \
    #     "2Trk_NoTag", "2Trk_OneTag", "2Trk_TwoTag_split", \
    #     "3Trk_NoTag", "3Trk_OneTag", "3Trk_TwoTag", "3Trk_TwoTag_split", "3Trk_ThreeTag", \
    #     "4Trk_NoTag", "4Trk_OneTag", "4Trk_TwoTag", "4Trk_TwoTag_split", "4Trk_ThreeTag", "4Trk_FourTag",\
    #     "OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]

    cut_lst = ["ThreeTag", "FourTag"]
    for i, cut in enumerate(cut_lst):
        if "NoTag" not in cut:
            plotRegion("../Plot/TEST_b77.root", cut=cut + "_Control_mHH_l", xTitle="m_{2J} [GeV]",yTitle="Number of Events",xMin=500,xMax=3000,yMax=20,rMin=0.001,rMax=2.5,labelPos=11,rebin=None)
    


#####################################
if __name__ == '__main__':
    main()
