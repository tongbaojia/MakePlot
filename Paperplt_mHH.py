# Tony Tong, baojia.tong@cern.ch
## plot signal region, control region
import os, argparse
import sys
import math
import ROOT
import time
import help_table
import help_plot as h_plt
from ROOT import *
import rootlogon  
import config as CONF
try:
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    SetAtlasStyle()
except:
    print "Passing on AtlasStyle.C"
    pass
from array import array
TH1.AddDirectory(False)
ROOT.gROOT.SetBatch(True)

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir",  default=CONF.workdir)
    parser.add_argument("--inputroot", default="sum")
    parser.add_argument("--hist",      default="pole")
    return parser.parse_args()

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
    gBkg.SetName("bkg_g")
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
    for i in range(1, data.GetN()):
        gRatioBand.SetPoint(i, data.GetX()[i]/1000, 1.0)
        if bkg.GetY()[i] > 0.02:
            gRatioBand.SetPointEYhigh(i, bkg.GetErrorYhigh(i) / bkg.GetY()[i]) 
            gRatioBand.SetPointEYlow(i, bkg.GetErrorYlow(i) / bkg.GetY()[i])             
            gRatioBand.SetPointEXhigh(i, bkg.GetErrorXhigh(i)/1000) 
            gRatioBand.SetPointEXlow(i, bkg.GetErrorXlow(i)/1000)             
    # ratio set to data/bkg with data stat errors only
    gRatioDataBkg = data.Clone("gRatioDataBkg")
    for i in range(1, data.GetN()):
        if data.GetY()[i]>0 and bkg.GetY()[i] > 0.02:
            gRatioDataBkg.SetPoint(i, data.GetX()[i]/1000, data.GetY()[i] / bkg.GetY()[i])
            gRatioDataBkg.SetPointEYhigh(i, data.GetErrorYhigh(i) / bkg.GetY()[i])
            gRatioDataBkg.SetPointEYlow(i, data.GetErrorYlow(i) / bkg.GetY()[i])
            gRatioDataBkg.SetPointEXhigh(i, 0) 
            gRatioDataBkg.SetPointEXlow(i, 0)             
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

def plotRegion(config, cut, xTitle, yTitle="Events / 0.1 TeV", Logy=0, rebin=None, rebinarry=None, outputFolder=""):
    #load configurations from config file
    filepath = config["root"] 
    filename = config["inputdir"] 
    outputFolder= config["outputdir"]
    blinded  = config["blind"]
    #print blinded, " blinded!", config["blind"]
    #print config, filepath, filename
    #print cut
    gStyle.SetErrorX(0)
    gStyle.SetHatchesSpacing(0.7)
    gStyle.SetHatchesLineWidth(1)

    # input file: this part is different!!
    ifile = ROOT.TFile(filepath)
    data = ifile.Get("totalbkg_hh" ).Clone()
    if not blinded:
        data = ifile.Get("data_hh").Clone()
    data_est = ifile.Get("totalbkg_hh").Clone()
    qcd = ifile.Get("qcd_hh").Clone()

    #get all the systematics
    syst_up = []
    syst_down = []
    ifile.cd()
    for key in ROOT.gDirectory.GetListOfKeys():
        kname = key.GetName()
        # if "QCDShape" in kname:
        #     continue
        if "totalbkg_hh" in kname and "up" in kname:
            syst_up.append(ifile.Get(kname).Clone(kname.replace(".", "") + "_cp"))
            #print kname
        elif "totalbkg_hh" in kname and "down" in kname:
            syst_down.append(ifile.Get(kname).Clone(kname.replace(".", "")  + "_cp"))
        elif "totalbkg_hh" in kname:
            syst_up.append(ifile.Get(kname).Clone(kname.replace(".", "")  + "_cp"))
            syst_down.append(ifile.Get(kname).Clone(kname.replace(".", "")  + "_cp"))
    #print len(syst_up), len(syst_down)
    #qcd_origin = ifile.Get("qcd_" + cut )
    #print "factor is ", qcd.Integral()/qcd_origin.Integral()
    ttbar = ifile.Get("ttbar_hh").Clone()
    zjet  = ifile.Get("zjet_hh").Clone()
    RSG1_1000 = ifile.Get("signal_RSG_c10_hh_m1000").Clone()
    RSG1_1500 = ifile.Get("signal_RSG_c10_hh_m1500").Clone()
    RSG1_2000 = ifile.Get("signal_RSG_c10_hh_m2000").Clone()
    Xhh_2000  = ifile.Get("signal_2HDM_hh_m2000").Clone()
    RSG1_1500.Scale(10)
    RSG1_2000.Scale(30 * 1.61) ##stupid
    Xhh_2000.Scale(5)

    if not rebin == None:
        data.Rebin(rebin)
        data_est.Rebin(rebin)
        qcd.Rebin(rebin)
        ttbar.Rebin(rebin)
        #zjet.Rebin(rebin)
        RSG1_1000.Rebin(rebin)
        RSG1_1500.Rebin(rebin)
        RSG1_2000.Rebin(rebin)
        Xhh_2000.Rebin(rebin)

    #use array to rebin histgrams
    if not rebinarry == None:
        data      = data.Rebin(len(rebinarry) - 1, data.GetName()+"_rebinned", rebinarry)
        data_est  = data_est.Rebin(len(rebinarry) - 1, data_est.GetName()+"_rebinned", rebinarry)
        qcd       = qcd.Rebin(len(rebinarry) - 1, qcd.GetName()+"_rebinned", rebinarry)
        ttbar     = ttbar.Rebin(len(rebinarry) - 1, ttbar.GetName()+"_rebinned", rebinarry)
        #zjet      = zjet.Rebin(len(rebinarry) - 1, zjet.GetName()+"_rebinned", rebinarry)
        RSG1_1000 = RSG1_1000.Rebin(len(rebinarry) - 1, RSG1_1000.GetName()+"_rebinned", rebinarry)
        RSG1_1500 = RSG1_1500.Rebin(len(rebinarry) - 1, RSG1_1500.GetName()+"_rebinned", rebinarry)
        RSG1_2000 = RSG1_2000.Rebin(len(rebinarry) - 1, RSG1_2000.GetName()+"_rebinned", rebinarry)
        Xhh_2000  = Xhh_2000.Rebin(len(rebinarry) - 1, Xhh_2000.GetName()+"_rebinned", rebinarry)   

    #get QS scores
    if "Signal" in cut and blinded:
        ks = 0
    else:
        ks   = data.KolmogorovTest(data_est, "QU")
    int_data = data.Integral(0, data.GetXaxis().GetNbins()+1)
    int_data_est = data_est.Integral(0, data_est.GetXaxis().GetNbins()+1)
    percentdiff   = (int_data_est - int_data)/int_data * 100.0
    #chi2 =        data.Chi2Test(data_est, "QU CHI2")
    #ndf  = chi2 / data.Chi2Test(data_est, "QU CHI2/NDF") if chi2 else 0.0

    xMin = data.GetXaxis().GetBinLowEdge(1)
    xMax = data.GetXaxis().GetBinUpEdge(data.GetXaxis().GetNbins())
    yMax = data.GetMaximum() * 1.8
    if ("FourTag" in cut):
        yMax = data.GetMaximum() * 2
    if Logy==1:
        yMax = yMax * 20
    #qcd_fit = ifile.Get("qcd_fit")
    #qcd_fitUp = ifile.Get("qcd_fitUp")
    #qcd_fitDown = ifile.Get("qcd_fitDown")

    #make the total backgroudn with sytematics
    data = makeTotBkg([data])[1]
    #bkg = makeTotBkg([ttbar,qcd])
    bkg = makeTotBkg([data_est], syst_up, syst_down)
    #bkg = makeTotBkg([ttbar,qcd,zjet])
    # bkg/data ratios: [0] band for stat errors, [1] bkg/data with syst errors
    ratios = makeDataRatio(data, bkg[1])

    # stack signal on background
    #RSG1_1000.Add(bkg[0]) 
    #RSG1_1500.Add(bkg[0]) 
    #RSG1_2000.Add(bkg[0]) 

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

    pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.0, 1., 0.30)
    pad1.SetRightMargin(0.05)
    pad1.SetBottomMargin(0.38)
    pad1.SetTopMargin(0.05)
    pad1.SetFrameFillColor(0)
    pad1.SetFillStyle(0) # transparent
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(0)

    c0.cd()
    pad0.SetLogy(Logy)
    pad0.Draw()
    pad0.cd()


    bkg[0].SetTitle("")
    bkg[0].SetStats(0)
    bkg[0].SetLineColor(ROOT.kBlack)
    bkg[0].SetLineWidth(1)
    bkg[0].GetYaxis().SetTitleFont(43)
    bkg[0].GetYaxis().SetTitleSize(33)
    bkg[0].GetYaxis().SetLabelFont(43)
    bkg[0].GetYaxis().SetLabelSize(28)
    bkg[0].GetYaxis().SetTitle(yTitle)
    bkg[0].GetYaxis().SetTitleOffset(1.25)
    bkg[0].GetYaxis().SetRangeUser(0.02, yMax)
    bkg[0].SetFillColor(ROOT.kYellow)
    bkg[0].Draw("HISTO")

    # RSG1_1000.SetLineWidth(2)
    # RSG1_1000.SetLineStyle(2)
    # RSG1_1000.SetLineColor(ROOT.kViolet+7)
    # RSG1_1000.Draw("HISTO SAME")

    #RSG1_1500.SetLineWidth(2)
    #RSG1_1500.SetLineStyle(2)
    #RSG1_1500.SetLineColor(ROOT.kGreen+4)
    #RSG1_1500.Draw("HISTO SAME")


    bkg[1].SetFillColor(CONF.col_dic["syst"])
    bkg[1].SetLineColor(0)
    bkg[1].SetFillStyle(3345)
    bkg[1].SetMarkerSize(0)
    bkg[1].Draw("E2 SAME")


    #print config, filepath, filename, cut, ttbar.Integral()
    ttbar.SetLineWidth(1)
    ttbar.SetLineColor(ROOT.kBlack)
    ttbar.SetFillColor(ROOT.kAzure-9)
    ttbar.Draw("HISTO SAME")

    RSG1_2000.SetLineWidth(2)
    RSG1_2000.SetLineStyle(7)
    RSG1_2000.SetLineColor(ROOT.kViolet)
    RSG1_2000.Draw("HISTO SAME")

    Xhh_2000.SetLineWidth(2)
    Xhh_2000.SetLineStyle(2)
    Xhh_2000.SetLineColor(ROOT.kRed)
    Xhh_2000.Draw("HISTO SAME")

    ## add extra line
    line0 = ROOT.TLine(xMin, 0.02, xMax, 0.02)
    line0.SetLineWidth(2)
    line0.Draw()

    #zjet.SetLineWidth(2)
    #zjet.SetLineColor(ROOT.kBlack)
    #zjet.SetFillColor(ROOT.kGreen+4)
    #zjet.Draw("HISTO SAME")

    zeroXerror(data)
    data.SetMarkerStyle(20)
    data.SetMarkerSize(1)
    data.SetLineWidth(2)
    data.GetXaxis().SetLabelSize(0)
    data.GetXaxis().SetLabelOffset(999)
    if not ("Signal" in cut and blinded):
        data.Draw("EPZ SAME")

    # bottom pad
    c0.cd()
    pad1.Draw()
    pad1.cd()

    hratio = ROOT.TH1F("hratio","",1, xMin/1000, xMax/1000)
    hratio.SetStats(0)
    
    hratio.GetYaxis().SetTitleFont(43)
    hratio.GetYaxis().SetTitleSize(33)
    hratio.GetYaxis().SetLabelFont(43)
    hratio.GetYaxis().SetLabelSize(28)
    hratio.GetYaxis().SetTitleOffset(1.25)
    hratio.GetYaxis().SetTitle("Data / Bkgd")
    hratio.GetYaxis().SetRangeUser(0.5, 1.5) #set range for ratio plot
    hratio.GetYaxis().SetNdivisions(503)

    hratio.GetXaxis().SetTitleFont(43)
    hratio.GetXaxis().SetTitleOffset(2.8)
    hratio.GetXaxis().SetTitleSize(33)
    hratio.GetXaxis().SetLabelFont(43)
    hratio.GetXaxis().SetLabelSize(28)
    hratio.GetXaxis().SetTitle(xTitle)
    hratio.Draw()


    #
    # Add stat uncertianty
    #
    ratios[0].SetFillColor(CONF.col_dic["syst"])
    ratios[0].SetFillStyle(3345)
    ratios[0].SetLineColor(0)
    ratios[0].Draw("E2")

    #zeroXerror(ratios[1])
    ratios[1].SetMarkerStyle(20)
    ratios[1].SetMarkerSize(1)
    ratios[1].SetLineWidth(2)
    h_plt.drawarrow(ratios[1], 0.5, 1.5)
    if not ("Signal" in cut and blinded):
        ratios[1].Draw("E0PZ SAME")



    # TeV_axis = ROOT.TGaxis(0, 0, 4000, 0, 0, 4, 510, "");
    # TeV_axis.SetTitle(xTitle);
    # TeV_axis.SetTitleFont(43)
    # TeV_axis.SetTitleOffset(3.5)
    # TeV_axis.SetTitleSize(33)
    # TeV_axis.SetLabelFont(43)
    # TeV_axis.SetLabelSize(28)
    # TeV_axis.SetTitle(xTitle)
    # TeV_axis.Draw()
    # qcd_fit.SetLineColor(kRed)
    # qcd_fitUp.SetLineColor(kRed)
    # qcd_fitUp.SetLineStyle(2)
    # qcd_fitDown.SetLineColor(kRed)
    # qcd_fitDown.SetLineStyle(2)
    # qcd_fit.Draw("SAME")
    # qcd_fitUp.Draw("SAME")
    # qcd_fitDown.Draw("SAME")

    # Fit the ratio with a TF1
    # if not ("Signal" in cut and blinded):
    #     testfit = ROOT.TF1("testfit", "pol2", xMin, xMax)
    #     testfit.SetParameters(1, 0, 0)
    #     ratios[1].Fit("testfit")
    #     testfit.SetLineColor(kRed)
    #     testfit.Draw("SAME")
    #     fitresult = testfit.GetParameters()
    #     myText(0.2, 0.17, 1, "y=%s x^2 + %s x + %s" % (str('%.2g' % fitresult[0]), \
    #         str('%.2g' % fitresult[1]),str('%.2g' % fitresult[2])), CONF.paperlegsize)

    # draw the ratio 1 line
    line = ROOT.TLine(xMin/1000, 1.0, xMax/1000, 1.0)
    line.SetLineStyle(1)
    line.SetLineWidth(1)
    line.Draw()

    c0.cd()
    #
    # Add ks score
    #
    #myText(0.15, 0.97, 1, "KS = %s" % str(('%.3g' % ks)), CONF.paperlegsize)
    #myText(0.4, 0.97, 1, "(Est-Obs)/Obs = %s; E=%s; O=%s" % (str(('%.1f' % percentdiff)), str(('%.1f' % int_data_est)), str(('%.1f' % int_data))), CONF.paperlegsize)
    #myText(0.15, 0.92, 1, "#chi^{2} / ndf = %s / %s" % (str(chi2), str(ndf)), CONF.paperlegsize)

    # labels
    legHunit=0.045
    legH=legHunit*6 # retuned below based on number of entries to 0.05*num_entries
    legW=0.4
    leg = ROOT.TLegend(0.57, 0.83, 0.93, 0.93)
    # top right, a bit left
    ATLASLabel(0.19, 0.91, CONF.StatusLabel)
    if "15" in filepath:
        myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 2015, 3.2 fb^{-1}", CONF.paperlegsize)
    elif "16" in filepath:
        myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 2016, 2.6 fb^{-1}", CONF.paperlegsize)
    else:
        myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, " + str(CONF.totlumi) + " fb^{-1}", CONF.paperlegsize)

    if cut.find("Signal") > -1:
        tag = "Boosted Signal Region"
    elif cut.find("Control") > -1:
        tag = "Boosted Control Region"
    elif cut.find("Sideband") > -1:
        tag = "Boosted Sideband Region"
    if cut.find("FourTag") > -1:
        tag += ", 4-tag"
    elif cut.find("ThreeTag") > -1:
        tag += ", 3-tag"
    elif cut.find("TwoTag") > -1:
        tag += ", 2-tag"
    myText(0.19, 0.83, 1, tag, CONF.paperlegsize)
    ##### legend
    #leg.SetNColumns(2)
    leg.SetTextFont(43)
    leg.SetTextSize(CONF.paperlegsize)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(data, "Data", "PE")
    leg.AddEntry(bkg[0], "Multijet", "F")
    leg.AddEntry(ttbar, "t#bar{t}","F")
    #leg.AddEntry(zjet, "Z+jets","F")
    #leg.AddEntry(RSG1_1000, "RSG1, 1TeV", "F")
    #leg.AddEntry(RSG1_1500, "G1.5TeV*10", "F")
    leg.AddEntry(Xhh_2000,  "Scalar (2 TeV)", "l") ## times 5
    leg.AddEntry(RSG1_2000, "G_{KK} (2 TeV k/#bar{M}_{Pl}=1) #times 30", "l")
    leg.AddEntry(bkg[1], "Stat+Syst Uncertainties", "FF")
    #leg.AddEntry(qcd_fit, "Fit to Ratio", "L")
    #leg.AddEntry(qcd_fitUp, "#pm 1#sigma Uncertainty", "L")
    leg.SetY1(leg.GetY2()-leg.GetNRows()*legHunit)
    leg.Draw()
    c0.Update() 
    pad0.Update()
    pad1.Update()

    # save
    postname = ("" if Logy == 0 else "_" + str(Logy)) + ("" if not ("Signal" in cut and blinded) else "_blind")
    #c0.SaveAs(outputFolder+"/"+filename.replace(".root", ".pdf"))
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".root")
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".C")
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".png")
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".pdf")
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".eps")

    pad0.Close()
    pad1.Close()
    c0.Close()
    del(data)
    del(data_est)
    del(qcd)
    del(ttbar)
    del(zjet)
    del(RSG1_1000)
    del(RSG1_1500)
    del(RSG1_2000)
    del(syst_up)
    del(syst_down)

def dumpRegion(config):
    #setup the rebin arrays
    rebin_dic = {}
    #different rebin for each catagory
    if "TwoTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 4000, 100))
        rebin_dic["mHH_pole"]   = array('d', range(0, 4000, 100))
        rebin_dic["j0_Pt"]      = array('d', [400, 450] + range(450, 600, 30) + range(600, 800, 40) + [800, 850, 900, 1000, 1200, 2000])
        rebin_dic["j1_Pt"]      = array('d', range(250, 600, 50) + [600, 700, 1000, 2000])
        rebin_dic["trk0_Pt"]    = array('d', [0, 60] + range(60, 300, 30) + [300, 330, 360, 400, 450, 500, 600, 800, 1300, 2000])
        rebin_dic["trk1_Pt"]    = array('d', range(0, 200, 20) + [200, 250, 400])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10)] + [1, 1.5, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 30, 60, 90, 120, 160, 200, 250, 300, 350, 400, 450, 500, 600, 800])
        rebin_dic["trks_Pt"]    = array('d', range(0, 400, 40) + [400, 450, 500, 550, 600, 800, 900, 1000, 1300, 1600, 2000])
    if "ThreeTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 4000, 100))
        rebin_dic["mHH_pole"]   = array('d', range(0, 4000, 100))
        rebin_dic["j0_Pt"]      = array('d', [400, 450, 480, 520, 560, 600, 640, 690, 750, 820, 1000, 2000])
        rebin_dic["j1_Pt"]      = array('d', range(250, 600, 50) + [600, 700, 800, 1000, 1300, 2000])
        rebin_dic["trk0_Pt"]    = array('d', [0, 70] + range(70, 310, 40) + [310, 360, 430, 500, 600, 800, 2000])
        rebin_dic["trk1_Pt"]    = array('d', range(0, 180, 30) + [180, 400])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10)] + [1, 1.5, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 30, 70] + range(70, 310, 40) + [310, 360, 430, 500, 600, 800, 2000])
        rebin_dic["trks_Pt"]    = array('d', [0, 30, 70] + range(70, 310, 40) + [310, 360, 430, 500, 600, 800, 2000])
    if "FourTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 4000, 100))
        rebin_dic["mHH_pole"]   = array('d', range(0, 4000, 100))
        rebin_dic["j0_Pt"]      = array('d', [450, 500, 570, 650, 800, 1000, 2000])
        rebin_dic["j1_Pt"]      = array('d', [250, 320, 390, 460, 550, 2000])
        rebin_dic["trk0_Pt"]    = array('d', [0, 70, 140, 210, 280, 360, 500, 2000])
        rebin_dic["trk1_Pt"]    = array('d', range(0, 180, 30) + [180, 400])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10, 2)] + [1, 1.5, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 70, 140, 210, 280, 350, 500, 2000])
        rebin_dic["trks_Pt"]    = array('d', [0, 70, 140, 210, 280, 350, 500, 2000])
    #all the kinematic plots that needs to be plotted; set the axis and name, rebin information 1 by 1
    if "pole" in config["hist"]:
        plotRegion(config, cut=config["cut"] + "mHH_pole",        xTitle="m_{2J} [TeV]", rebinarry=rebin_dic["mHH_pole"])
        plotRegion(config, cut=config["cut"] + "mHH_pole",        xTitle="m_{2J} [TeV]", Logy=1, rebinarry=rebin_dic["mHH_pole"])
    else:
        plotRegion(config, cut=config["cut"] + "mHH_l",           xTitle="m_{2J} [TeV]", rebinarry=rebin_dic["mHH_l"])
        plotRegion(config, cut=config["cut"] + "mHH_l",           xTitle="m_{2J} [TeV]", Logy=1, rebinarry=rebin_dic["mHH_l"])

    print config["outputdir"], "done!"

##################################################################################################
# Main

def main():

    start_time = time.time()
    ops = options()
    #setup basics
    inputdir = ops.inputdir
    inputroot = ops.inputroot
    inputpath = CONF.inputpath + inputdir + "/"

    global figuresFolder

    global finaldis
    #finaldis = "pole"
    finaldis = ops.hist

    # plot in the control region #
    # figuresFolder = inputpath + inputroot + "Plot/" + "Sideband"
    # plotRegion(rootinputpath, inputdir, cut="FourTag" + "_" + "Sideband" + "_" + "mHH_l", xTitle="m_{2J} [GeV]")
    # plotRegion(rootinputpath, inputdir, cut="FourTag" + "_" + "Sideband" + "_" + "mHH_l", xTitle="m_{2J} [GeV]", Logy=1)
    region_lst = ["Signal", "Control"]
    cut_lst = ["TwoTag_split", "ThreeTag", "FourTag"]
    #create master list
    inputtasks = []
    #fill the task list
    for i, region in enumerate(region_lst):
        if inputroot == "sum":
            inputroot = ""
        outputFolder = inputpath + inputroot + "PaperPlot/" + region
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        for j, cut in enumerate(cut_lst):
            rootinputpath = inputpath + "Limitinput/"  + inputdir + "_limit_" + cut + "_fullsys" + ("" if "pole" not in finaldis else "_pole") +".root"
            config = {}
            config["hist"] = "pole"            
            if region == "Control":
                config["hist"]  = "l"  
                rootinputpath = inputpath + "Limitinput/"  + inputdir + "_limit_" + cut + "_fullsys" + "_CR.root"
            config["root"] = rootinputpath
            config["inputdir"] = inputdir
            config["outputdir"] = outputFolder
            config["cut"] = cut + "_" + region + "_"
            config["blind"] = False
            inputtasks.append(config)

   
    #dumpRegion(inputtasks[0])
    for i in inputtasks:
        dumpRegion(i)
    print("--- %s seconds ---" % (time.time() - start_time))

    
#####################################
if __name__ == '__main__':
    main()
