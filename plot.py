# Tony Tong; baojia.tong@cern.ch
import os, argparse, sys, math, time
import config as CONF
from array import array
import ROOT as ROOT
import help_plot as h_plt
import help_table as h_table
import helpers
import rootlogon
#for parallel processing!
import multiprocessing as mp
try:
    import simplejson as json                 
except ImportError:
    import json
#other setups
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()
ROOT.TH1.AddDirectory(False)
ROOT.gROOT.SetBatch(True)

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",  default=CONF.workdir)
    parser.add_argument("--inputroot", default="sum")
    parser.add_argument("--detail",    default=True)
    return parser.parse_args()

#plot
def plotRegion(config, cut, xTitle, yTitle="N Events", Logy=0, rebin=None, rebinarry=None, outputFolder="", doZjet=False):
    #load configurations from config file
    filepath = config["root"] 
    filename = config["inputdir"]
    outputFolder= config["outputdir"]
    blinded = config["blind"]
    #print config, filepath, filename, cut
    ROOT.gStyle.SetErrorX(0)
    ROOT.gStyle.SetHatchesSpacing(0.7)
    ROOT.gStyle.SetHatchesLineWidth(1)

    # input file
    ifile = ROOT.TFile(filepath + filename + ".root")
    # read stuff
    data = ifile.Get("data_" + cut )
    if "Signal" in cut and blinded:
        data = ifile.Get("data_est_" + cut )
    data_est = ifile.Get("data_est_" + cut )
    qcd = ifile.Get("qcd_est_" + cut )
    #qcd_origin = ifile.Get("qcd_" + cut )
    #print "factor is ", qcd.Integral()/qcd_origin.Integral()
    ttbar = ifile.Get("ttbar_est_" + cut )
    if (doZjet):
        zjet = ifile.Get("zjet_" + cut )
    RSG1_1000 = ifile.Get("RSG1_1000_" + cut )
    RSG1_1500 = ifile.Get("RSG1_1500_" + cut )
    RSG1_1500.Scale(10)
    RSG1_2000 = ifile.Get("RSG1_2000_" + cut )
    RSG1_2000.Scale(30)
    RSG1_2500 = ifile.Get("RSG1_2500_" + cut )
    RSG1_2500.Scale(100)

    #do simple rebin as rebin values
    if not rebin == None:
        data.Rebin(rebin)
        data_est.Rebin(rebin)
        qcd.Rebin(rebin)
        ttbar.Rebin(rebin) 
        if (doZjet):
            zjet.Rebin(rebin)
        RSG1_1000.Rebin(rebin)
        RSG1_1500.Rebin(rebin)
        RSG1_2000.Rebin(rebin)
        RSG1_2500.Rebin(rebin)
    #use array to rebin histgrams
    if not rebinarry == None:
        data      = data.Rebin(len(rebinarry) - 1, data.GetName()+"_rebinned", rebinarry)
        data_est  = data_est.Rebin(len(rebinarry) - 1, data_est.GetName()+"_rebinned", rebinarry)
        qcd       = qcd.Rebin(len(rebinarry) - 1, qcd.GetName()+"_rebinned", rebinarry)
        ttbar     = ttbar.Rebin(len(rebinarry) - 1, ttbar.GetName()+"_rebinned", rebinarry)
        if (doZjet):
            zjet      = zjet.Rebin(len(rebinarry) - 1, zjet.GetName()+"_rebinned", rebinarry)
        RSG1_1000 = RSG1_1000.Rebin(len(rebinarry) - 1, RSG1_1000.GetName()+"_rebinned", rebinarry)
        RSG1_1500 = RSG1_1500.Rebin(len(rebinarry) - 1, RSG1_1500.GetName()+"_rebinned", rebinarry)
        RSG1_2000 = RSG1_2000.Rebin(len(rebinarry) - 1, RSG1_2000.GetName()+"_rebinned", rebinarry)
        RSG1_2500 = RSG1_2500.Rebin(len(rebinarry) - 1, RSG1_2500.GetName()+"_rebinned", rebinarry)

    #get QS scores
    if "Signal" in cut and blinded:
        ks = 0
    else:
        ks   = data.KolmogorovTest(data_est, "QU")
    int_data = data.Integral(0, data.GetXaxis().GetNbins()+1)
    int_data_est = data_est.Integral(0, data_est.GetXaxis().GetNbins()+1)
    percent_ratio  = (int_data)/int_data_est
    #chi2 =        data.Chi2Test(data_est, "QU CHI2")
    #ndf  = chi2 / data.Chi2Test(data_est, "QU CHI2/NDF") if chi2 else 0.0

    #load basic information
    xMin = data.GetXaxis().GetBinLowEdge(1)
    xMax = data.GetXaxis().GetBinUpEdge(data.GetXaxis().GetNbins())
    yMax = data.GetMaximum() * 1.6
    if ("FourTag" in cut):
        yMax = data.GetMaximum() * 2.0
    if Logy==1:
        yMax = yMax * 100
    #qcd_fit = ifile.Get("qcd_fit")
    #qcd_fitUp = ifile.Get("qcd_fitUp")
    #qcd_fitDown = ifile.Get("qcd_fitDown")

    ##add in normalization error at least
    syst_up = []
    syst_down = []
    f1 = open(filepath + filename + ".txt")
    masterdic = json.load(f1)

    ##find the systmatics from the fit
    cut_temp = cut.split("_")
    if cut_temp[1] == "split":
        cut_temp.remove("split")
        cut_temp[0] = "TwoTag_split"
    #for key_temp, value_temp in masterdic["data_est_nofit"][cut_temp[0]].iteritems():
        #print key_temp, value_temp, cut_temp[1]
        #print key_temp, value_temp, 
    ##this is the total error in the region from the fit
    #print masterdic["data_est_nofit"][cut_temp[0]][cut_temp[1] + "_err"]
    temp_syst_up = data_est.Clone(data_est.GetName() + "_syst_up")
    temp_syst_up.Scale((data_est.Integral() + masterdic["data_est_nofit"][cut_temp[0]][cut_temp[1] + "_err"])/data_est.Integral())
    #print "here", (data_est.Integral() + masterdic["data_est_nofit"][cut_temp[0]][cut_temp[1] + "_err"])/data_est.Integral()
    temp_syst_down = data_est.Clone(data_est.GetName() + "_syst_down")
    temp_syst_down.Scale((data_est.Integral() - masterdic["data_est_nofit"][cut_temp[0]][cut_temp[1] + "_err"])/data_est.Integral())
    syst_up.append(temp_syst_up)
    syst_down.append(temp_syst_down)

    #setup data and bkg estiamtes
    data = h_plt.makeTotBkg([data])[1]
    bkg = h_plt.makeTotBkg([ttbar,qcd])
    if (doZjet):
        bkg = h_plt.makeTotBkg([ttbar,qcd,zjet])
    #bkg = h_plt.makeTotBkg([ttbar,qcd], syst_up, syst_down)
    #bkg = h_plt.makeTotBkg([ttbar,qcd,zjet], syst_up, syst_down)
    # bkg/data ratios: [0] band for stat errors, [1] bkg/data with syst errors
    ratios = h_plt.makeDataRatio(data, bkg[1])

    # stack signal on background
    RSG1_1000.Add(bkg[0]) 
    RSG1_1500.Add(bkg[0]) 
    RSG1_2000.Add(bkg[0]) 
    RSG1_2500.Add(bkg[0]) 

    # canvas
    c0 = ROOT.TCanvas("c0"+filename+cut, "Insert hilarious TCanvas name here", 600, 600)
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
    pad1.SetTopMargin(0.0001)
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
    bkg[0].SetLineWidth(2)
    bkg[0].GetYaxis().SetTitleFont(43)
    bkg[0].GetYaxis().SetTitleSize(28)
    bkg[0].GetYaxis().SetLabelFont(43)
    bkg[0].GetYaxis().SetLabelSize(28)
    bkg[0].GetYaxis().SetTitle(yTitle)
    bkg[0].GetYaxis().SetRangeUser(0.02, yMax)
    bkg[0].SetFillColor(ROOT.kYellow)
    bkg[0].Draw("HISTO")

    # RSG1_1000.SetLineWidth(2)
    # RSG1_1000.SetLineStyle(2)
    # RSG1_1000.SetLineColor(ROOT.kViolet+7)
    # RSG1_1000.Draw("HISTO SAME")

    RSG1_1500.SetLineWidth(2)
    RSG1_1500.SetLineStyle(2)
    RSG1_1500.SetLineColor(ROOT.kPink+7)
    #RSG1_1500.Draw("HISTO SAME")


    RSG1_2000.SetLineWidth(2)
    RSG1_2000.SetLineStyle(2)
    RSG1_2000.SetLineColor(ROOT.kPink+7)
    RSG1_2000.Draw("HISTO SAME")

    RSG1_2500.SetLineWidth(2)
    RSG1_2500.SetLineStyle(2)
    RSG1_2500.SetLineColor(ROOT.kGreen+4)
    #RSG1_2500.Draw("HISTO SAME")

    bkg[1].SetFillColor(CONF.col_dic["syst"])
    bkg[1].SetLineColor(CONF.col_dic["syst"])
    bkg[1].SetFillStyle(3345)
    bkg[1].SetMarkerSize(0)
    bkg[1].Draw("E2 SAME")

    ttbar.SetLineWidth(2)
    ttbar.SetLineColor(ROOT.kBlack)
    ttbar.SetFillColor(ROOT.kAzure-9)
    ttbar.Draw("HISTO SAME")

    if (doZjet):
        zjet.SetLineWidth(2)
        zjet.SetLineColor(ROOT.kBlack)
        zjet.SetFillColor(ROOT.kGreen+4)
        zjet.Draw("HISTO SAME")

    h_plt.zeroXerror(data)
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

    hratio = ROOT.TH1F("hratio","",1, xMin, xMax)
    hratio.SetStats(0)
    
    hratio.GetYaxis().SetTitleFont(43)
    hratio.GetYaxis().SetTitleSize(28)
    hratio.GetYaxis().SetLabelFont(43)
    hratio.GetYaxis().SetLabelSize(28)
    hratio.GetYaxis().SetTitle("Data / Bkgd")
    hratio.GetYaxis().SetRangeUser(0.4, 1.8) #set range for ratio plot
    hratio.GetYaxis().SetNdivisions(405)

    hratio.GetXaxis().SetTitleFont(43)
    hratio.GetXaxis().SetTitleOffset(3.5)
    hratio.GetXaxis().SetTitleSize(28)
    hratio.GetXaxis().SetLabelFont(43)
    hratio.GetXaxis().SetLabelSize(28)
    hratio.GetXaxis().SetTitle(xTitle)

    hratio.Draw()

    #
    # Add stat uncertianty
    #
    ratios[0].SetFillColor(CONF.col_dic["syst"])
    ratios[0].SetFillStyle(3345)
    ratios[0].Draw("E2")

    #h_plt.zeroXerror(ratios[1])
    ratios[1].SetMarkerStyle(20)
    ratios[1].SetMarkerSize(1)
    ratios[1].SetLineWidth(2)
    if not ("Signal" in cut and blinded):
        ratios[1].Draw("E0PZ SAME")
    ##add arrows; call this function
    h_plt.drawarrow(ratios[1], 0.4, 1.8)
    # qcd_fit.SetLineColor(kRed)
    # qcd_fitUp.SetLineColor(kRed)
    # qcd_fitUp.SetLineStyle(2)
    # qcd_fitDown.SetLineColor(kRed)
    # qcd_fitDown.SetLineStyle(2)
    # qcd_fit.Draw("SAME")
    # qcd_fitUp.Draw("SAME")
    # qcd_fitDown.Draw("SAME")

    ## Fit the ratio with a TF1
    if("mHH" in cut and not blinded):
        testfit = ROOT.TF1("testfit", "pol1", xMin, xMax)
        testfit.SetParameters(1, 0)
        ratios[1].Fit("testfit", "QLWW0IBF", "")
        testfit.SetLineColor(ROOT.kRed)
        testfit.SetLineStyle(9)
        testfit.Draw("SAME")
        fitresult = testfit.GetParameters()
        ROOT.myText(0.15, 0.12, 1, "y=%s x + %s, prob:%s" % (str('%.2g' % fitresult[0]), \
            str('%.2g' % fitresult[1]), str('%.2g' % float(testfit.GetProb()))), CONF.legsize)

    # draw the ratio 1 line
    line = ROOT.TLine(xMin, 1.0, xMax, 1.0)
    line.SetLineStyle(1)
    line.Draw()
    c0.cd()

    #
    # Add ks score
    #
    if (ops.detail):
        ROOT.myText(0.15, 0.97, 1, "KS = %s" % str(('%.3g' % ks)), CONF.legsize)
        ROOT.myText(0.4, 0.97, 1, "Obs/Est = %s/%s = %s" % 
            (str(('%.1f' % int_data)), str(('%.1f' % int_data_est)), str(('%.3f' % percent_ratio))), CONF.legsize)
        #myText(0.15, 0.92, 1, "#chi^{2} / ndf = %s / %s" % (str(chi2), str(ndf)), CONF.legsize)

    # labels
    legHunit=0.05
    legH=legHunit*6 # retuned below based on number of entries to 0.05*num_entries
    legW=0.4
    leg = ROOT.TLegend(0.65, 0.75, 0.95, 0.95)
    # top right, a bit left
    if not CONF.thesis:
        ROOT.ATLASLabel(0.19, 0.91, CONF.StatusLabel)
    if "15" in filepath:
        ROOT.myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 2015, 3.2 fb^{-1}", CONF.legsize)
    elif "16" in filepath:
        ROOT.myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 2016, 2.6 fb^{-1}", CONF.legsize)
    else:
        ROOT.myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 15+16, " + str(CONF.totlumi) + " fb^{-1}", CONF.legsize)

    #clean up the info string
    infostr = cut
    infostr = infostr.replace("_", ";")
    infostr = infostr.replace("Sideband", "SB") if "Sideband" in infostr else infostr
    infostr = infostr.replace("Control", "CR") if "Sideband" in infostr else infostr
    infostr = infostr.replace("Signal", "SR") if "Sideband" in infostr else infostr
    infostr = infostr.replace("FourTag", "4b") if "FourTag" in infostr else infostr
    infostr = infostr.replace("ThreeTag", "3b") if "ThreeTag" in infostr else infostr
    infostr = infostr.replace("TwoTag;split", "2bs") if "TwoTag;split" in infostr else infostr
    ROOT.myText(0.19, 0.83, 1, ' ' + infostr, CONF.legsize)

    ##### legend
    #leg.SetNColumns(2)
    leg.SetTextFont(43)
    leg.SetTextSize(CONF.legsize)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(data, "Data", "PE")
    leg.AddEntry(bkg[0], "Multijet", "F")
    leg.AddEntry(ttbar, "t#bar{t}","F")
    if (doZjet):
        leg.AddEntry(zjet, "Z+jets","F")
    leg.AddEntry(bkg[1], "Stat Uncer.", "F")
    #leg.AddEntry(RSG1_1000, "RSG1, 1TeV", "F")
    #leg.AddEntry(RSG1_1500, "RSG 1.5TeV * 10", "F")
    leg.AddEntry(RSG1_2000, "G(2000)#times30", "F")
    #leg.AddEntry(RSG1_2500, "RSG 2.5TeV * 100", "F")
    #leg.AddEntry(qcd_fit, "Fit to Ratio", "L")
    #leg.AddEntry(qcd_fitUp, "#pm 1#sigma Uncertainty", "L")
    leg.SetY1(leg.GetY2()-leg.GetNRows()*legHunit)
    leg.Draw()





    # save
    postname = ("" if Logy == 0 else "_" + str(Logy)) + ("" if not ("Signal" in cut and blinded) else "_blind")
    #c0.SaveAs(outputFolder+"/"+filename.replace(".root", ".pdf"))
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".png")
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".pdf")
    #c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".eps")
    #c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".C")

    #close and quit
    pad0.Close()
    pad1.Close()
    c0.Close()
    f1.close()
    del(leg)

def dumpRegion(config):
    #setup the rebin arrays
    rebin_dic = {}
    #different rebin for each catagory
    if "TwoTag" or "OneTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 4000, 100))
        rebin_dic["mHH_pole"]   = array('d', range(0, 4000, 100))
        rebin_dic["j0_Pt"]      = array('d', [400, 450] + range(450, 600, 30) + range(600, 800, 40) + [800, 850, 900, 970, 1060, 1250, 2000])
        rebin_dic["j1_Pt"]      = array('d', range(250, 900, 50) + [900, 960, 1030, 1110, 1300, 2000])
        rebin_dic["trk0_Pt"]    = array('d', [0, 60] + range(60, 300, 30) + [300, 330, 360, 400, 450, 500, 570, 660, 800, 1250, 2000])
        rebin_dic["trk1_Pt"]    = array('d', range(0, 200, 20) + [200, 250, 400])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10)] + [1, 1.2, 1.5, 1.7, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 30, 60, 90, 120, 160, 200, 250, 300, 350, 400, 450, 500, 600, 800])
        rebin_dic["trks_Pt"]    = array('d', range(0, 400, 40) + [400, 450, 500, 550, 600, 800, 900, 1000, 1300, 1600, 2000])
    if "ThreeTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 4000, 100))
        rebin_dic["mHH_pole"]   = array('d', range(0, 4000, 100))
        rebin_dic["j0_Pt"]      = array('d', [400, 450, 480, 520, 560, 600, 640, 680, 730, 790, 860, 940, 1030, 1150, 1350, 2000])
        rebin_dic["j1_Pt"]      = array('d', range(250, 850, 50) + [850, 910, 980, 1060, 1150, 1250, 2000])
        rebin_dic["trk0_Pt"]    = array('d', range(0, 80, 80) + range(80, 320, 40) + [320, 370, 430, 490, 580, 700, 1000, 2000])
        rebin_dic["trk1_Pt"]    = array('d', range(0, 160, 20) + [160, 190, 250, 400])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10)] + [1, 1.2, 1.5, 1.7, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 30, 70] + range(70, 310, 40) + [310, 360, 430, 500, 600, 800, 2000])
        rebin_dic["trks_Pt"]    = array('d', [0, 30, 70] + range(70, 310, 40) + [310, 360, 430, 500, 600, 800, 2000])
    if "FourTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 4000, 100))
        rebin_dic["mHH_pole"]   = array('d', range(0, 4000, 100))
        rebin_dic["j0_Pt"]      = array('d', [450, 490, 530, 570, 610, 650, 700, 750, 800, 870, 950, 1100, 2000])
        rebin_dic["j1_Pt"]      = array('d', [250, 300, 350, 400, 450, 510, 580, 650, 800, 2000])
        rebin_dic["trk0_Pt"]    = array('d', [0, 70, 130, 190, 250, 320, 390, 480, 1000, 2000])
        rebin_dic["trk1_Pt"]    = array('d', range(0, 180, 30) + [180, 400])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10, 2)] + [1, 1.2, 1.5, 1.7, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 70, 140, 210, 280, 350, 500, 2000])
        rebin_dic["trks_Pt"]    = array('d', [0, 70, 140, 210, 280, 350, 500, 2000])
    #all the kinematic plots that needs to be plotted; set the axis and name, rebin information 1 by 1
    plotRegion(config, cut=config["cut"] + "mHH_l",              xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_l"])
    plotRegion(config, cut=config["cut"] + "mHH_l",              xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_l"], Logy=1)
    plotRegion(config, cut=config["cut"] + "mHH_pole",           xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_pole"])
    plotRegion(config, cut=config["cut"] + "mHH_pole",           xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_pole"], Logy=1)
    plotRegion(config, cut=config["cut"] + "leadHCand_trk0_Pt",  xTitle="J0 leadtrk p_{T} [GeV]", rebinarry=rebin_dic["trk0_Pt"])
    plotRegion(config, cut=config["cut"] + "leadHCand_trk1_Pt",  xTitle="J0 subltrk p_{T} [GeV]", rebinarry=rebin_dic["trk1_Pt"])
    plotRegion(config, cut=config["cut"] + "sublHCand_trk0_Pt",  xTitle="J1 leadtrk p_{T} [GeV]", rebinarry=rebin_dic["trk0_Pt"])
    plotRegion(config, cut=config["cut"] + "sublHCand_trk1_Pt",  xTitle="J1 subltrk p_{T} [GeV]", rebinarry=rebin_dic["trk1_Pt"])
    plotRegion(config, cut=config["cut"] + "leadHCand_Pt_m",     xTitle="J0 p_{T} [GeV]", rebinarry=rebin_dic["j0_Pt"])
    plotRegion(config, cut=config["cut"] + "leadHCand_Pt_m",     xTitle="J0 p_{T} [GeV]", rebinarry=rebin_dic["j0_Pt"], Logy=1)
    plotRegion(config, cut=config["cut"] + "sublHCand_Pt_m",     xTitle="J1 p_{T} [GeV]", rebinarry=rebin_dic["j1_Pt"])
    plotRegion(config, cut=config["cut"] + "sublHCand_Pt_m",     xTitle="J1 p_{T} [GeV]", rebinarry=rebin_dic["j1_Pt"], Logy=1)
    
    if CONF.fullstudy:
        plotRegion(config, cut=config["cut"] + "hCandDr",            xTitle="#Delta R",    rebin=2)
        plotRegion(config, cut=config["cut"] + "hCandDeta",          xTitle="#Delta #eta", rebin=2)
        plotRegion(config, cut=config["cut"] + "hCandDphi",          xTitle="#Delta #phi", rebin=2)
        plotRegion(config, cut=config["cut"] + "leadHCand_Eta",      xTitle="J0 #eta",     rebin=2)
        plotRegion(config, cut=config["cut"] + "leadHCand_Phi",      xTitle="J0 #phi",     rebin=2)
        plotRegion(config, cut=config["cut"] + "leadHCand_Mass_s",   xTitle="J0 m [GeV]",  rebin=1)
        plotRegion(config, cut=config["cut"] + "leadHCand_trk_dr",   xTitle="J0 #Delta_{trk}",    rebinarry=rebin_dic["trk_dr"])
        plotRegion(config, cut=config["cut"] + "sublHCand_Eta",      xTitle="J1 #eta",     rebin=2)
        plotRegion(config, cut=config["cut"] + "sublHCand_Phi",      xTitle="J1 #phi",     rebin=2)
        plotRegion(config, cut=config["cut"] + "sublHCand_Mass_s",   xTitle="J1 m [GeV]",  rebin=1)
        plotRegion(config, cut=config["cut"] + "sublHCand_trk_dr",   xTitle="J1 #DeltaR_{trk}",    rebinarry=rebin_dic["trk_dr"])
        plotRegion(config, cut=config["cut"] + "leadHCand_ntrk",     xTitle="J0 Ntrk")
        plotRegion(config, cut=config["cut"] + "sublHCand_ntrk",     xTitle="J1 Ntrk")
        plotRegion(config, cut=config["cut"] + "leadHCand_trk_pt_diff_frac", xTitle="J0 pt diff", rebin=4)
        plotRegion(config, cut=config["cut"] + "sublHCand_trk_pt_diff_frac", xTitle="J1 pt diff", rebin=4)


    print config["outputdir"], "done!"


##################################################################################################
# Main
def main():
    #start time
    start_time = time.time()
    global ops
    ops = options()
    #setup basics
    inputdir  = ops.inputdir
    inputroot = ops.inputroot
    inputpath = CONF.inputpath + inputdir + "/"
    rootinputpath = inputpath + inputroot + "_"
    print "input root file is: ", rootinputpath
    # plot in the control region #
    # outputFolder = inputpath + inputroot + "Plot/" + "Sideband"
    # plotRegion(rootinputpath, inputdir, cut="FourTag" + "_" + "Sideband" + "_" + "mHH_l", xTitle="m_{2J} [GeV]")
    # plotRegion(rootinputpath, inputdir, cut="FourTag" + "_" + "Sideband" + "_" + "mHH_l", xTitle="m_{2J} [GeV]", Logy=1)
    region_lst = ["Sideband", "Control", "Signal"]
    cut_lst    = ["TwoTag_split", "ThreeTag", "FourTag"]
    #cut_lst = ["OneTag"]
    #create master list
    inputtasks = []
    #fill the task list
    for i, region in enumerate(region_lst):
        outputFolder = inputpath + "Plot/" + region
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        for j, cut in enumerate(cut_lst):
            config = {}
            config["root"] = rootinputpath
            config["inputdir"] = inputdir
            config["outputdir"] = outputFolder
            config["cut"] = cut + "_" + region + "_"
            config["blind"] = CONF.blind
            inputtasks.append(config)

        # for j, cut in enumerate(cut_lst):
        #     config = {}
        #     config["root"] = rootinputpath
        #     config["inputdir"] = inputdir
        #     config["outputdir"] = outputFolder
        #     config["cut"] = cut + "_" + region + "_"
        #     if "Signal" in region:
        #         config["blind"] = False
        #         inputtasks.append(config)

    #parallel compute!
    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool = mp.Pool(npool)
    pool.map(dumpRegion, inputtasks)
    # for i in inputtasks:
    #     dumpRegion(i)
    #dumpRegion(inputtasks[0])
    print("--- %s seconds ---" % (time.time() - start_time))

    
#####################################
if __name__ == '__main__':
    main()