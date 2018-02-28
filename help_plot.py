import copy
import math
import ROOT
import os, sys
from array import array
import time
import glob

ROOT.gROOT.SetBatch(True)
canv = None

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
    # total bkg histogram, with error settings
    hBkg_err = hBkg.Clone("bkg_err")
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
            for ih in range(0, len(bkgsUp)):
                err += math.pow(math.fabs( hBkg.GetBinContent(i+1) - bkgsUp[ih].GetBinContent(i+1) ), 2)
            gBkg.SetPointEYhigh(i, math.sqrt(err))
            ### error down
            err = math.pow(gBkg.GetErrorYlow(i),2)
            # loop over backgrounds
            for ih in range(0, len(bkgsDown)):
                err += math.pow(math.fabs( hBkg.GetBinContent(i+1) - bkgsDown[ih].GetBinContent(i+1) ), 2)
            gBkg.SetPointEYlow(i, math.sqrt(err))
        # loop over points, for hBkg
        for i in range(0, gBkg.GetN()):
            maxbinerr = max(gBkg.GetErrorYhigh(i), gBkg.GetErrorYlow(i))
            hBkg_err.SetBinError(i, maxbinerr)
    return [hBkg, gBkg, hBkg_err]

# function to build data/bkgd ratios
def makeDataRatio(data, bkg):
    # ratio set to one with error band 
    gRatioBand = data.Clone("gRatioBand")
    for i in range(0, data.GetN()):
        gRatioBand.SetPoint(i, data.GetX()[i], 1.0)
        if bkg.GetY()[i] > 0.02:
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
            pass
            #gRatioDataBkg.SetPoint(i, 0.0, -1000)

    return [gRatioBand, gRatioDataBkg]

def do_variable_rebinning(hist,bins, scale=1):
    a=hist.GetXaxis()

    newhist=ROOT.TH1F(hist.GetName()+"_rebinned",
                      hist.GetTitle()+";"+hist.GetXaxis().GetTitle()+";"+hist.GetYaxis().GetTitle(),
                      len(bins)-1,
                      array('d',bins))

    newhist.Sumw2()
    newa=newhist.GetXaxis()
    #print "check size ", hist.GetNbinsX(), newhist.GetNbinsX()
    for b in range(0, hist.GetNbinsX()+2):
        newb             = newa.FindBin(a.GetBinCenter(b))

        # Get existing new content (if any)                                                                                                              
        val              = newhist.GetBinContent(newb)
        err              = newhist.GetBinError(newb)
        # Get content to add
        ratio_bin_widths = scale*newa.GetBinWidth(newb)/a.GetBinWidth(b)
        #print "ratio_bin_widths",ratio_bin_widths
        #val              = val+hist.GetBinContent(b)/ratio_bin_widths
        #err              = math.sqrt(err*err+hist.GetBinError(b)/ratio_bin_widths*hist.GetBinError(b)/ratio_bin_widths)
        val              = val+hist.GetBinContent(b)
        err              = math.sqrt(err*err+hist.GetBinError(b)*hist.GetBinError(b))
        #print "bin", newb, " new value ", val, " change ", hist.GetBinContent(b)
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

def rebinData(ifile, rebin, scale=1):
    dataHist = ifile.Get("data_hh_hist")    
    dataHistNew = do_variable_rebinning(dataHist, rebin, scale)
    return graphFromHist(dataHistNew)

def drawarrow(graph, ratio_ylow=0.5, ratio_yhigh=1.5):
    '''this function adds arrows on overflow/underflow bins'''
    ratio_arrow = ROOT.TArrow(0, 0, 0, 0, 0.01, "|>")
    ratio_arrow.SetLineWidth(2)
    ratio_arrow.SetLineColor(ROOT.kBlack)
    ratio_arrow.SetFillColor(ROOT.kBlack)

    for pt in xrange(graph.GetN()):
        y = graph.GetY()[pt]
        x = graph.GetX()[pt]
        if y <= 0 : ##pass the empty bins
            continue
        y_low  = y + graph.GetEYhigh()[pt]
        y_high = y - graph.GetEYlow()[pt]
        if y_low < ratio_ylow * 1.1:
            ratio_arrow.DrawArrow(x, 1 - abs(1 - ratio_ylow)*2./3., x, ratio_ylow + 0.03)
            #print y, y_low
        elif y_high > ratio_yhigh * 0.9:
            ratio_arrow.DrawArrow(x, 1 + abs(1 - ratio_yhigh)*2./3., x, ratio_yhigh - 0.03)
####################################################################################
