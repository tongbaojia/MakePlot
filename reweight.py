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
#other setups
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()
ROOT.TH1.AddDirectory(False)
StatusLabel="Internal"
ROOT.gROOT.SetBatch(True)

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default=CONF.workdir)
    parser.add_argument("--inputroot", default="sum")
    parser.add_argument("--iter", default=0)
    return parser.parse_args()

####################################################################################
#plot

def plotRegion(config, cut, xTitle, yTitle="N Events", Logy=0, labelPos=11, rebin=None, rebinarry=[], fitrange=[0, 0]):
    #load configurations from config file
    filepath = config["root"] 
    filename = config["inputdir"] 
    outputFolder= config["outputdir"]
    ##print config, filepath, filename
    #debug
    #print filepath, filename, cut
    ROOT.gStyle.SetErrorX(0)
    ROOT.gStyle.SetHatchesSpacing(0.7)
    ROOT.gStyle.SetHatchesLineWidth(1)

    # input file
    ifile = ROOT.TFile(filepath + filename + ".root")

    # read stuff
    #print "data_" + cut
    if config["compcut"] is not "": ## this means qcd estimate is something special now; NOTICE: things are inverted here!!!
        #print config, filepath, filename, config["compcut"]
        data = ifile.Get("data_" + cut.replace(config["cut"], config["compcut"]) )
        ttbar = ifile.Get("ttbar_" + cut.replace(config["cut"], config["compcut"]) )
        qcd = ifile.Get("data_" + cut) #note these are the compcut plots
        ttbar_est = ifile.Get("ttbar_" + cut)
        #zjet = ifile.Get("zjet_" + cut )
        data.Add(ttbar, -1)
        qcd.Add(ttbar_est, -1) ##special treatment here; directly subtracting the MC component

    else: ##default method
        data = ifile.Get("data_" + cut )
        qcd = ifile.Get("qcd_est_" + cut )
        ttbar = ifile.Get("ttbar_est_" + cut )
        #zjet = ifile.Get("zjet_" + cut )
        #modify data
        data.Add(ttbar, -1)
        #data.Add(zjet, -1)

    #qcd_origin = ifile.Get("qcd_" + cut )
    #print "factor is ", qcd.Integral()/qcd_origin.Integral()
    #RSG1_1000 = ifile.Get("RSG1_1000_" + cut )
    #RSG1_1500 = ifile.Get("RSG1_1500_" + cut )
    #RSG1_2500 = ifile.Get("RSG1_2500_" + cut )

    #clear factioned binns; only for reweighting purpose
    # for b in range(1, data.GetNbinsX()+1): 
    #     if  data.GetBinContent(b) < 1:
    #         data.SetBinContent(b, 0)
    #         data.SetBinError(b, 0)

    #swap data if blinded
    if "Signal" in cut and blinded:
        data = qcd.Clone()
    #do rebin
    if not rebin == None:
        data.Rebin(rebin)
        qcd.Rebin(rebin)
        ttbar.Rebin(rebin)
        #zjet.Rebin(rebin)
        #RSG1_1000.Rebin(rebin)
        #RSG1_1500.Rebin(rebin)
        #RSG1_2500.Rebin(rebin)
    if rebinarry != []:
        data      = h_plt.do_variable_rebinning(data, rebinarry)
        qcd       = h_plt.do_variable_rebinning(qcd, rebinarry)
        ttbar     = h_plt.do_variable_rebinning(ttbar, rebinarry)
        #zjet      = h_plt.do_variable_rebinning(zjet, rebinarry)
        #RSG1_1000 = h_plt.do_variable_rebinning(RSG1_1000, rebinarry)
        #RSG1_1500 = h_plt.do_variable_rebinning(RSG1_1500, rebinarry)
        #RSG1_2500 = h_plt.do_variable_rebinning(RSG1_2500, rebinarry)

    #get QS scores
    if "Signal" in cut and blinded:
        ks = 0
    else:
        ks   = data.KolmogorovTest(qcd, "QU")

    int_data = data.Integral(0, data.GetXaxis().GetNbins()+1)
    int_qcd = qcd.Integral(0, qcd.GetXaxis().GetNbins()+1)
    percentdiff   = (int_qcd - int_data)/int_data * 100.0
    #chi2 =        data.Chi2Test(qcd, "QU CHI2")
    #ndf  = chi2 / data.Chi2Test(qcd, "QU CHI2/NDF") if chi2 else 0.0
    if config["compcut"] is not "": 
        ##special treatment here: for comps, rescale the original distributions
        ##thus the number of events is kept the same!
        data.Scale(int_qcd/int_data)


    xMin = data.GetXaxis().GetBinLowEdge(1)
    xMax = data.GetXaxis().GetBinUpEdge(data.GetXaxis().GetNbins())
    yMax = data.GetMaximum() * 1.5
    if Logy==1:
        yMax = yMax * 100
    #qcd_fit = ifile.Get("qcd_fit")
    #qcd_fitUp = ifile.Get("qcd_fitUp")
    #qcd_fitDown = ifile.Get("qcd_fitDown")

    #this is the important part...where the backgrounds are set
    data = h_plt.makeTotBkg([data])[1]
    bkg  = h_plt.makeTotBkg([qcd])
    #bkg = h_plt.makeTotBkg([ttbar,qcd,zjet]) #original
    # bkg/data ratios: [0] band for bkg errors, [1] bkg/data with stat errors only
    ratios = h_plt.makeDataRatio(data, bkg[1])
    # canvas
    c0 = ROOT.TCanvas("c0"+filename+cut, "Insert hilarious TCanvas name here", 800, 800)
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
    bkg[0].GetYaxis().SetRangeUser(0.001, yMax)
    bkg[0].SetFillColor(ROOT.kYellow)
    bkg[0].Draw("HISTO")

    bkg[1].SetFillColor(CONF.col_dic["syst"])
    bkg[1].SetLineColor(CONF.col_dic["syst"])
    bkg[1].SetFillStyle(3345)
    bkg[1].SetMarkerSize(0)
    bkg[1].Draw("E2 SAME")

    #ttbar.SetLineWidth(2)
    #ttbar.SetLineColor(ROOT.kBlack)
    #ttbar.SetFillColor(ROOT.kAzure-9)
    #ttbar.Draw("HISTO SAME")

    #zjet.SetLineWidth(2)
    #zjet.SetLineColor(ROOT.kBlack)
    #zjet.SetFillColor(ROOT.kGreen+4)
    #zjet.Draw("HISTO SAME")

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

    hratio = ROOT.TH1F("hratio","", 1, xMin, xMax)
    hratio.SetStats(0)
    
    hratio.GetYaxis().SetTitleFont(43)
    hratio.GetYaxis().SetTitleSize(28)
    hratio.GetYaxis().SetLabelFont(43)
    hratio.GetYaxis().SetLabelSize(28)
    hratio.GetYaxis().SetTitle("Data / Bkgd")
    hratio.GetYaxis().SetRangeUser(0.5, 1.5) #set range for ratio plot
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

    #zeroXerror(ratios[1])
    ratios[1].SetMarkerStyle(20)
    ratios[1].SetMarkerSize(1)
    ratios[1].SetLineWidth(2)
    if not ("Signal" in cut and blinded):
        ratios[1].Draw("E0PZ SAME")
    # qcd_fit.SetLineColor(ROOT.kRed)
    # qcd_fitUp.SetLineColor(ROOT.kRed)
    # qcd_fitUp.SetLineStyle(2)
    # qcd_fitDown.SetLineColor(ROOT.kRed)
    # qcd_fitDown.SetLineStyle(2)
    # qcd_fit.Draw("SAME")
    # qcd_fitUp.Draw("SAME")
    # qcd_fitDown.Draw("SAME")

    testfit={}
    # Fit the ratio with a TF1
    if not ("Signal" in cut and blinded):
        if fitrange == [0, 0]:
            fitMin = xMin
            fitMax = xMax
        else:
            fitMin = fitrange[0]
            fitMax = fitrange[1]

        #enable smart fit~! will pick the highest prob fit
        #no 0 order polynomial!!!
        for iter_fit in range(1, 4):
            testfit[iter_fit] = ROOT.TF1("testfit" + str(iter_fit), "pol" + str(iter_fit), xMin, xMax)
        #initialization of parameters
        if ("trk0_Pt" in cut): #for the leading track jet fit
            #testfit[3].SetParameters(1, 0.006, -2E-5, +2E-8)
            testfit[3].SetParameters(0.76, 0.009, -5E-5, +9E-8)
            #testfit[3].SetParameters(0.6, 0.007, -3E-5, +3E-8); testing version
        elif ("trk1_Pt" in cut): #for the subleading track jet fit
            testfit[2].SetParameters(0.82, 0.004, -1E-5)
        elif ("trks_Pt" in cut): #for the subleading track jet fit
            testfit[3].SetParameters(0.82, 0.004, -2E-5, -2E-8)
        elif ("trk_pt_diff" in cut): #for the subleading track jet fit
            testfit[3].SetParameters(1, 0.001, -0.000001, -0.00000001)
        elif ("Pt_m" in cut): #for the subleading track jet fit
            testfit[1].SetParameters(0.9, 0.0005)
        elif ("Rhh" in cut): #for the subleading track jet fit
            testfit[1].SetParameters(1, 0.7)
        #for the other distributions
        testfit[1].SetParameters(0.9, 0.001)
        #testfit[1].SetParLimits(1, 0.8, 1.2)
        testfit[2].SetParameters(1.0, 0.0, 0.0)
        #testfit[2].SetParLimits(0, 0.8, 1.2)
        testfit[3].SetParameters(1.0, 0.0, 0.0, 0.0)

        #do the 3 fits and save the output
        testfitprob = [0]
        for iter_fit in range(1, 4):
            ratios[1].Fit("testfit" + str(iter_fit), "QWLR0IBF", "", fitMin, fitMax)
            testfitprob.append(float(testfit[iter_fit].GetProb()))
        #pick the best iteration; try to avoid higher order function as much as possible
        best_iter = 1
        if testfitprob[2]/(testfitprob[best_iter] + 1E-8) > 1.1:
            best_iter = 2
        if testfitprob[3]/(testfitprob[best_iter] + 1E-8) > 1.1:
            best_iter = 3
        
        #proceed with saving parameters
        fitprob = testfitprob[best_iter]
        fitresult = testfit[best_iter].GetParameters()
        if len(fitresult) < 4:#fill in 0 if there are less than 3 paramters
            fitresult += [int(0)] * (4 - len(fitresult))
        testfit[best_iter].SetLineColor(ROOT.kRed)
        testfit[best_iter].SetLineStyle(9)
        testfit[best_iter].Draw("SAME")
        ROOT.myText(0.02, 0.17, 1, "y=%s + %s x + %sx^2 + %sx^3, prob:%s" % 
            (str('%.2g' % fitresult[0]),
            str('%.2g' % fitresult[1]), 
            str('%.2g' % fitresult[2]), 
            str('%.2g' % fitresult[3]), 
            str('%.2g' % fitprob))
            , CONF.legsize)
        #draw the line for stat and end of the fit
        ystart = ROOT.TLine(fitMin, 0.60, fitMin, 1.40)
        ystart.SetLineStyle(5)
        ystart.Draw()
        yend = ROOT.TLine(fitMax, 0.60, fitMax, 1.40)
        yend.SetLineStyle(5)
        yend.Draw()

        #write out the reweighting parameteres; for things in the sideband only
        f_reweight = open(reweightfolder + "r" + str(iter_reweight) + "_" + cut +".txt", "w")
        f_reweight.write("reweighting function of: " + cut + "; prob is: " + str('%.2g' % fitprob) + "\n")
        f_reweight.write("par0: " + str('%.3g' % fitresult[0]) + " \n")
        f_reweight.write("par1: " + str('%.3g' % fitresult[1]) + " \n")
        f_reweight.write("par2: " + str('%.3g' % fitresult[2]) + " \n")
        f_reweight.write("par3: " + str('%.3g' % fitresult[3]) + " \n")
        f_reweight.write("low:  " + str('%.3g' % fitMin) + " \n")
        f_reweight.write("high: " + str('%.3g' % fitMax) + " \n")
        f_reweight.close()

        #done with the fit!!
        #try spline interpolation: CSPLINE, LINEAR, POLYNOMIAL, CSPLINE_PERIODIC, AKIMA, AKIMA_PERIODIC
        inter = ROOT.Math.Interpolator(0, ROOT.Math.Interpolation.kCSPLINE)
        ni = ratios[1].GetN()
        xi = ROOT.vector('double')(ni + 2)
        yi = ROOT.vector('double')(ni + 2)
        #deal with the beginning
        for k in range(0, ni):
            xk = ROOT.Double()
            yk = ROOT.Double()
            ratios[1].GetPoint(k, xk, yk)
            xi[k + 1] = xk
            yi[k + 1] = yk
        #for edge effects
        xi[0] = xi[1] - abs(xi[1] - xi[2])
        yi[0] = yi[1]
        xi[ni + 1] = xi[ni] + abs(xi[ni] - xi[ni - 1])
        yi[ni + 1] = yi[ni]
        inter.SetData(xi, yi)
        temp_graph = ROOT.TGraph(ni + 2)
        for k in range(0, ni + 2):
            temp_graph.SetPoint(k, xi[k], yi[k])
        spline = ROOT.TSpline3(cut, temp_graph)
        spline.SaveAs(reweightfolder + "rs" + str(iter_reweight) + "_" + cut +".cxx")

        inter_step = 5
        xf = ROOT.vector('double')(ni * inter_step)
        yf = ROOT.vector('double')(ni * inter_step)
        inter_graph = ROOT.TGraph(ratios[1].GetN() * inter_step)
        spline_graph = ROOT.TGraph(ratios[1].GetN() * inter_step)
        for k in range(0, (ni * inter_step)):
            xf[k] = xi[0] + (xi[ni + 1] - xi[0])/(ni * inter_step * 1.0) * k
            #print k, xf[k], inter.Eval(xf[k])
            inter_graph.SetPoint(k, xf[k], inter.Eval(xf[k]))
            spline_graph.SetPoint(k, xf[k], spline.Eval(xf[k]))

        inter_graph.SetLineColor(ROOT.kBlue)
        inter_graph.SetLineWidth(2)
        inter_graph.Draw("SAME L")
        spline_graph.SetLineColor(ROOT.kGreen)
        spline_graph.SetLineWidth(2)
        spline_graph.Draw("SAME L")

    # draw the ratio 1 line
    line = ROOT.TLine(xMin, 1.0, xMax, 1.0)
    line.SetLineStyle(1)
    line.Draw()

    c0.cd()
    #
    # Add ks score
    #
    ROOT.myText(0.15, 0.97, 1, "KS = %s" % str(('%.3g' % ks)), CONF.legsize)
    ROOT.myText(0.4, 0.97, 1, "(Est-Obs)/Obs = %s; E=%s; O=%s" % (str(('%.1f' % percentdiff)), str(('%.1f' % int_qcd)), str(('%.1f' % int_data))), CONF.legsize)
    #myText(0.15, 0.92, 1, "#chi^{2} / ndf = %s / %s" % (str(chi2), str(ndf)), CONF.legsize)

    # labels
    legHunit=0.05
    legH=legHunit*6 # retuned below based on number of entries to 0.05*num_entries
    legW=0.4
    leg = ROOT.TLegend(0.65, 0.75, 0.95, 0.95)
    # top right, a bit left
    ROOT.ATLASLabel(0.19, 0.91, StatusLabel)
    if "15" in filepath:
        ROOT.myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 2015, 3.2 fb^{-1}", CONF.legsize)
    elif "16" in filepath:
        ROOT.myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 2016, 2.6 fb^{-1}", CONF.legsize)
    elif "cb" in filepath:
        ROOT.myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 15+16, " + str(CONF.totlumi) + " fb^{-1}", CONF.legsize)
    else:
        ROOT.myText(0.19, 0.87, 1, "#sqrt{s}=13 TeV, 15+16, " + str(CONF.totlumi) + " fb^{-1}", CONF.legsize)
    ##### legend
    leg.SetNColumns(1)
    leg.SetTextFont(43)
    leg.SetTextSize(12)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    if config["compcut"] is not "": 
        #inverted here as well!!!
        leg.AddEntry(data, config["compcut"].replace("_", " "), "PE")
        leg.AddEntry(bkg[0], config["cut"].replace("_", " "), "F")
    else:
        leg.AddEntry(data, "Data", "PE")
        leg.AddEntry(bkg[0], "Multijet Est", "F")
    #leg.AddEntry(ttbar, "t#bar{t}","F")
    #leg.AddEntry(zjet, "Z+jets","F")
    leg.AddEntry(bkg[1], "Stat Uncertainty", "F")
    #leg.AddEntry(RSG1_1000, "RSG1, 1TeV", "F")
    #leg.AddEntry(RSG1_1500, "RSG1, 1.5TeV * 25", "F")
    #leg.AddEntry(RSG1_2500, "RSG1, 2.5TeV * 1000", "F")
    #leg.AddEntry(qcd_fit, "Fit to Ratio", "L")
    #leg.AddEntry(qcd_fitUp, "#pm 1#sigma Uncertainty", "L")
    leg.SetY1(leg.GetY2()-leg.GetNRows()*legHunit)
    leg.Draw()

    # save
    postname = ("" if Logy == 0 else "_" + str(Logy)) + ("" if not ("Signal" in cut and blinded) else "_blind")
    #c0.SaveAs(outputFolder+"/"+filename.replace(".root", ".pdf"))
    c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".png")
    #c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + postname + ".pdf")
    #c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + ".pdf")
    #c0.SaveAs(outputFolder+ "/" + filename + "_" + cut + ".eps")

    pad0.Close()
    pad1.Close()
    c0.Close()
    del(data)
    del(qcd)
    del(ttbar)
    #del(zjet)
    #del(RSG1_1000)
    #del(RSG1_1500)
    #del(RSG1_2500)
    del(testfit)

    ##rename the spline function generated
    with open(reweightfolder + "rs" + str(iter_reweight) + "_" + cut +".cxx","r") as f:
        newlines = []
        for line in f.readlines():
            newlines.append(line.replace("/afs/cern", "rs" + str(iter_reweight) + "_" + cut))
        with open(reweightfolder + "rs" + str(iter_reweight) + "_" + cut +".cxx", "w") as f:
            for line in newlines:
                f.write(line)

    ##should only be run non-parellel.
    if ("Sideband" in cut and False):
        outputroot.cd()
        ratios[1].SetName(cut)
        ratios[1].Write()




def dumpRegion(config):
    rebin_dic = {}
    #different rebin for each catagory
    if "TwoTag" in config["cut"] or "OneTag" in config["cut"] or "Trk" in config["cut"]:
        rebin_dic["mHH_l"]       = array('d', range(0, 2000, 100) + range(2000, 3000, 200) + [3000, 3500, 4000])
        rebin_dic["mHH_pole"]    = array('d', range(0, 2000, 100) + range(2000, 3000, 200) + [3000, 3500, 4000])
        #rebin_dic["j0_Pt"]      = array('d', [400, 450] + range(450, 600, 30) + range(600, 800, 40) + [800, 850, 900, 1000, 1200, 2000])
        rebin_dic["j0_Pt"]       = array('d', range(450, 600, 30) + range(600, 800, 40) + [800, 850, 910, 980, 1100, 2000]) #9.5 version
        rebin_dic["j1_Pt"]       = array('d', range(250, 650, 40) + [650, 700, 750, 800, 870, 960, 2000])
        #rebin_dic["trk0_Pt"]    = array('d', [0, 60] + range(60, 300, 40) + [300, 340, 390, 450, 520, 600, 800, 1300, 2000])
        rebin_dic["j0_trk0_Pt"]  = array('d', [0, 60, 100, 140, 180, 220, 260, 300, 350, 400, 460, 520, 620, 820, 1200, 2000]) #9.5 version
        rebin_dic["j1_trk0_Pt"]  = array('d', [0, 60, 100, 140, 180, 220, 260, 300, 350, 400, 460, 520, 620, 820, 1200, 2000]) #9.5 version
        rebin_dic["trk1_Pt"]     = array('d', range(0, 150, 15) + [150, 170, 190, 220, 250, 600]) #tuned
        rebin_dic["trk_dr"]      = array('d', [0, 0.2] + [x * 0.1 for x in range(2, 10)] + [1, 1.5, 2])
        rebin_dic["trk_pT_diff"] = array('d', [0, 30, 60, 90, 120, 160, 200, 250, 300, 350, 400, 450, 500, 600, 800])
        rebin_dic["trks_Pt"]     = array('d', range(0, 400, 40) + [400, 450, 500, 550, 600, 800, 900, 1000, 1300, 1600, 2000])
    if "ThreeTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 2000, 100) + range(2000, 3000, 200) + [3000, 3500, 4000])
        rebin_dic["mHH_pole"]   = array('d', range(0, 2000, 100) + range(2000, 3000, 200) + [3000, 3500, 4000])
        #rebin_dic["j0_Pt"]      = array('d', [400, 450, 480, 520, 560, 600, 640, 690, 750, 820, 1000, 2000])
        rebin_dic["j0_Pt"]      = array('d', range(450, 690, 40) + range(690, 840, 50) + [840, 900, 1000, 2000])#9.5 version
        rebin_dic["j1_Pt"]      = array('d', range(250, 650, 40) + [650, 700, 800, 900, 1000, 2000])
        rebin_dic["j0_trk0_Pt"]    = array('d', range(0, 80, 80) + range(80, 320, 40) + [320, 370, 430, 490, 560, 640, 820, 2000])
        rebin_dic["j1_trk0_Pt"]    = array('d', range(0, 80, 80) + range(80, 320, 40) + [320, 370, 430, 490, 560, 640, 820, 2000])
        rebin_dic["trk1_Pt"]    = array('d',range(0, 200, 20) + [200, 500])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10)] + [1, 1.5, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 30, 70] + range(70, 310, 40) + [310, 360, 430, 500, 600, 800, 2000])
        rebin_dic["trks_Pt"]    = array('d', [0, 30, 70] + range(70, 310, 40) + [310, 360, 430, 500, 600, 800, 2000])
    if "FourTag" in config["cut"]:
        rebin_dic["mHH_l"]      = array('d', range(0, 2000, 100) + range(2000, 3000, 200) + [3000, 3500, 4000])
        rebin_dic["mHH_pole"]   = array('d', range(0, 2000, 100) + range(2000, 3000, 200) + [3000, 3500, 4000])
        #rebin_dic["j0_Pt"]      = array('d', [450, 500, 570, 650, 800, 1000, 2000])
        rebin_dic["j0_Pt"]      = array('d', [450, 550, 650, 750, 850, 2000]) #9.5 version
        rebin_dic["j1_Pt"]      = array('d', [250, 320, 390, 460, 550, 2000])
        #rebin_dic["trk0_Pt"]    = array('d', [0, 70, 140, 210, 280, 360, 500, 2000])
        rebin_dic["j0_trk0_Pt"]    = array('d', [0, 100, 150, 200, 250, 300, 380, 500, 2000]) #9.5 version
        rebin_dic["j1_trk0_Pt"]    = array('d', [0, 100, 150, 200, 250, 300, 380, 500, 2000]) #9.5 version
        rebin_dic["trk1_Pt"]    = array('d', range(0, 150, 30) + [150, 500])
        rebin_dic["trk_dr"]     = array('d', [x * 0.1 for x in range(0, 10, 2)] + [1, 1.5, 2])
        rebin_dic["trk_pT_diff"]= array('d', [0, 70, 140, 210, 280, 350, 500, 2000])
        rebin_dic["trks_Pt"]    = array('d', [0, 70, 140, 210, 280, 350, 500, 2000])
    #all the kinematic plots that needs to be plotted; set the axis and name, rebin information 1 by 1
    plotRegion(config, cut=config["cut"] + "mHH_l",              xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_l"], fitrange=[800, 3000])
    plotRegion(config, cut=config["cut"] + "mHH_l",              xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_l"], Logy=1, fitrange=[800, 3000])
    #plotRegion(config, cut=config["cut"] + "mHH_pole",           xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_pole"], fitrange=[800, 3000])
    #plotRegion(config, cut=config["cut"] + "mHH_pole",           xTitle="m_{2J} [GeV]", rebinarry=rebin_dic["mHH_pole"], Logy=1, fitrange=[800, 3000])
    plotRegion(config, cut=config["cut"] + "leadHCand_trk0_Pt",  xTitle="J0 leadtrk p_{T} [GeV]", rebinarry=rebin_dic["j0_trk0_Pt"], fitrange=[0, 2000])
    plotRegion(config, cut=config["cut"] + "sublHCand_trk0_Pt",  xTitle="J1 leadtrk p_{T} [GeV]", rebinarry=rebin_dic["j1_trk0_Pt"], fitrange=[0, 2000])
    plotRegion(config, cut=config["cut"] + "leadHCand_trk1_Pt",  xTitle="J0 subltrk p_{T} [GeV]", rebinarry=rebin_dic["trk1_Pt"], fitrange=[0, 600])
    plotRegion(config, cut=config["cut"] + "sublHCand_trk1_Pt",  xTitle="J1 subltrk p_{T} [GeV]", rebinarry=rebin_dic["trk1_Pt"], fitrange=[0, 600])
    plotRegion(config, cut=config["cut"] + "leadHCand_Pt_m",     xTitle="J0 p_{T} [GeV]", rebinarry=rebin_dic["j0_Pt"], fitrange=[450, 2000])
    plotRegion(config, cut=config["cut"] + "leadHCand_Pt_m",     xTitle="J0 p_{T} [GeV]", rebinarry=rebin_dic["j0_Pt"], Logy=1, fitrange=[450, 2000])
    plotRegion(config, cut=config["cut"] + "sublHCand_Pt_m",     xTitle="J1 p_{T} [GeV]", rebinarry=rebin_dic["j1_Pt"], fitrange=[250, 2000])
    plotRegion(config, cut=config["cut"] + "sublHCand_Pt_m",     xTitle="J1 p_{T} [GeV]", rebinarry=rebin_dic["j1_Pt"], Logy=1, fitrange=[250, 2000])
    
    if CONF.fullstudy:
        #plotRegion(config, cut=config["cut"] + "Rhh",                xTitle="Rhh", rebin=2)
        plotRegion(config, cut=config["cut"] + "leadHCand_Mass",     xTitle="J0 m [GeV]", rebin=2, fitrange=[60, 200])
        plotRegion(config, cut=config["cut"] + "sublHCand_Mass",     xTitle="J1 m [GeV]", rebin=2, fitrange=[60, 200])
        plotRegion(config, cut=config["cut"] + "hCandDr",            xTitle="#Delta R", rebin=2, fitrange=[2, 3.6])
        plotRegion(config, cut=config["cut"] + "hCandDeta",          xTitle="#Delta #eta", rebin=2, fitrange=[0, 1.7])
        plotRegion(config, cut=config["cut"] + "hCandDphi",          xTitle="#Delta #phi", rebin=2)
        plotRegion(config, cut=config["cut"] + "leadHCand_Eta",      xTitle="J0 #eta", rebin=3, fitrange=[-2, 2])
        plotRegion(config, cut=config["cut"] + "leadHCand_Phi",      xTitle="J0 #phi", rebin=4, fitrange=[-3, 3])
        plotRegion(config, cut=config["cut"] + "leadHCand_trk_dr",   xTitle="J0 dRtrk", rebin=2, rebinarry=rebin_dic["trk_dr"], fitrange=[0.2, 1.2])
        plotRegion(config, cut=config["cut"] + "sublHCand_Eta",      xTitle="J1 #eta", rebin=3, fitrange=[-2, 2])
        plotRegion(config, cut=config["cut"] + "sublHCand_Phi",      xTitle="J1 #phi", rebin=4, fitrange=[-3, 3])
        plotRegion(config, cut=config["cut"] + "sublHCand_trk_dr",   xTitle="J1 dRtrk", rebin=2, rebinarry=rebin_dic["trk_dr"], fitrange=[0.2, 1.2])
        plotRegion(config, cut=config["cut"] + "leadHCand_ntrk",     xTitle="J0 Ntrk", fitrange=([1, 6] if "TwoTag" in config["cut"] else [2, 4]))
        plotRegion(config, cut=config["cut"] + "sublHCand_ntrk",     xTitle="J1 Ntrk", fitrange=([1, 6] if "TwoTag" in config["cut"] else [2, 4]))
        plotRegion(config, cut=config["cut"] + "leadHCand_trk_pt_diff_frac", xTitle="J0 pt diff", rebinarry=rebin_dic["trk_pT_diff"], fitrange=[0, 600])
        plotRegion(config, cut=config["cut"] + "sublHCand_trk_pt_diff_frac", xTitle="J1 pt diff", rebinarry=rebin_dic["trk_pT_diff"], fitrange=[0, 600])
        #plotRegion(config, cut=config["cut"] + "leadHCand_trk0_Eta",      xTitle="J0 #eta", rebin=2)
        #plotRegion(config, cut=config["cut"] + "leadHCand_trk0_Phi",      xTitle="J0 #phi", rebin=4)
        #plotRegion(config, cut=config["cut"] + "sublHCand_trk0_Eta",      xTitle="J1 #eta", rebin=2)
        #plotRegion(config, cut=config["cut"] + "sublHCand_trk0_Phi",      xTitle="J1 #phi", rebin=4)
        #plotRegion(config, cut=config["cut"] + "leadHCand_trks_Pt",  xTitle="J0 trks p_{T} [GeV]", rebinarry=rebin_dic["trks_Pt"], fitrange=[0, 1000])
        #plotRegion(config, cut=config["cut"] + "sublHCand_trks_Pt",  xTitle="J1 trks p_{T} [GeV]", rebinarry=rebin_dic["trks_Pt"], fitrange=[0, 1000])
        #plotRegion(config, cut=config["cut"] + "trks_Pt",            xTitle="Jets trks p_{T} [GeV]", rebinarry=rebin_dic["trks_Pt"], fitrange=[0, 1000])
        #plotRegion(config, cut=config["cut"] + "hCand_Pt_assy",      xTitle="pT assy", fitrange=[0, 0.5])
    print config["outputdir"], "done!"


##################################################################################################
# Main

def main():

    start_time = time.time()
    ops = options()
    global blinded
    blinded = True
    global iter_reweight
    iter_reweight = int(ops.iter)
    #setup basics
    inputdir = ops.inputdir
    inputroot = ops.inputroot
    inputpath = CONF.inputpath + inputdir + "/"
    rootinputpath = inputpath + inputroot + "_"
    print "input root file is: ", rootinputpath

    global StatusLabel
    StatusLabel = "Internal" ##StatusLabel = "Preliminary"

    global reweightfolder
    reweightfolder = inputpath + "Reweight/"
    helpers.checkpath(reweightfolder)

    global outputroot
    outputroot = ROOT.TFile(reweightfolder + "reweights.root", "recreate")
    # plot in the control region #
    # outputFolder = inputpath + inputroot + "Plot/" + "Sideband"
    # plotRegion(rootinputpath, inputdir, cut="FourTag" + "_" + "Sideband" + "_" + "mHH_l", xTitle="m_{2J} [GeV]")
    # plotRegion(rootinputpath, inputdir, cut="FourTag" + "_" + "Sideband" + "_" + "mHH_l", xTitle="m_{2J} [GeV]", Logy=1)

    #region_lst = ["Sideband"]
    #cut_lst    = ["TwoTag_split", "ThreeTag", "FourTag"]
    region_lst  = ["Incl"]
    ##these are the distributios we want to look like 
    ##these are the disbrituions we are changing
    cut_lst     = ["NoTag_2Trk_split_lead", "NoTag_2Trk_split_subl", "NoTag_3Trk_lead", "NoTag_3Trk_subl", "NoTag_4Trk_lead", "NoTag_4Trk_subl"] 
    comp_lst    = ["OneTag_subl", "OneTag_lead", "TwoTag_subl", "TwoTag_lead", "TwoTag_subl", "TwoTag_lead"]
    #comp_lst   = ["NoTag_2Trk_split_subl", "NoTag_2Trk_split_lead", "NoTag_3Trk_subl", "NoTag_3Trk_lead", "NoTag_4Trk_subl", "NoTag_4Trk_lead"]

    #create master list
    inputtasks = []
    #fill the task list
    for i, region in enumerate(region_lst):
        if inputroot == "sum":
            inputroot = ""
        outputFolder = inputpath + inputroot + "Plot_r" + str(iter_reweight) + "/" + region
        helpers.checkpath(outputFolder)

        for j, cut in enumerate(cut_lst):
            config = {}
            config["root"] = rootinputpath
            config["inputdir"] = inputdir
            config["outputdir"] = outputFolder
            config["cut"] = cut + "_" + region + "_"
            if comp_lst[j]:
                config["compcut"] = comp_lst[j] + "_" + region + "_"
            else:
                config["compcut"] = "" ##by default this is disabled
            inputtasks.append(config)
    #parallel compute!
    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool = mp.Pool(npool)
    pool.map(dumpRegion, inputtasks)
    ##for debug
    # for task in inputtasks:
    #     dumpRegion(task)
    # dumpRegion(inputtasks[0])
    outputroot.Close()
    print("--- %s seconds ---" % (time.time() - start_time))

    
#####################################
if __name__ == '__main__':
    main()
