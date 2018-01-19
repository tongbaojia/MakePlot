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

ROOT.gROOT.SetBatch(True)
from ROOT import *    
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
SetAtlasStyle()

def main():

    ops = options()
    inputdir = ops.inputdir

    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "PaperPlot/SigEff/"
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    #set global draw options
    global mass_lst
    mass_lst = [700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    global lowmass
    lowmass = 650
    global highmass
    highmass = 3150

    # select the cuts
    # the list must start from the largest to the smallest!
    evtsel_lst = ["PassDiJetEta", "PassDetaHH", "PassBJetSkim", "PassSignal"]
    detail_lst = ["4trk_3tag_signal", "4trk_4tag_signal", "4trk_2tag_signal", \
    "4trk_2tag_split_signal", "3trk_3tag_signal", "3trk_2tag_signal", "3trk_2tag_split_signal", "2trk_2tag_split_signal"]
    region_lst = ["TwoTag_split_Signal", "ThreeTag_Signal", "FourTag_Signal"]
    global cut_dic
    cut_dic    = {"PassTrig":"Trigger", "PassDiJetEta":"large-R jets #geq 2", 
    "PassDetaHH":"|#Delta#eta_{hh}| < 1.7",  "PassBJetSkim":"b-tagged track-jets #geq 2", 
    "PassSignal":"X_{hh} < 1.6 ",
    "ThreeTag_Signal":"3 b-tagged track-jets", "FourTag_Signal":"4 b-tagged track-jets", "TwoTag_split_Signal":"2 b-tagged track-jets",
    }

    # Draw the efficiency plot relative to the all normalization
    DrawSignalEff(evtsel_lst, inputdir, "evtsel", "PreSel")
    DrawSignalEff(region_lst, inputdir, "region_lst", "PreSel", doint=True, dosum=True)
    DrawSignalEff(evtsel_lst, inputdir, "evtsel", "PreSel", signal="G_hh_c20")
    DrawSignalEff(region_lst, inputdir, "region_lst", "PreSel", doint=True, dosum=True, signal="G_hh_c20")
    DrawSignalEff(evtsel_lst, inputdir, "evtsel", "PreSel", signal="X_hh")
    DrawSignalEff(region_lst, inputdir, "region_lst", "PreSel", doint=True, dosum=True, signal="X_hh")


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
    return parser.parse_args()


def DrawSignalEff(cut_lst, inputdir="b77", outputname="", normalization="All", doint=False, donormint=False, dorel=False, dosum=False, signal="G_hh_c10"):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region
    afterscript = "_rel" if dorel else ""
    canv = ROOT.TCanvas(inputdir + "_" + "Efficiency" + "_" + normalization + afterscript, "Efficiency", 800, 800)
    xleg, yleg = 0.55, 0.73
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.18)
    # setup basic plot parameters
    # load input MC file
    eff_lst = []
    graph_lst = []
    maxbincontent = 0.001
    minbincontent = -0.001


    for i, cut in enumerate(cut_lst):
        eff_lst.append( ROOT.TH1F(inputdir + "_" + cut, "%s; Mass [GeV]; Acceptance x Efficiency" %cut, int((highmass-lowmass)/100), lowmass, highmass) )

        for mass in mass_lst:
            if signal == "G_hh_c20" and mass == 2750:
                continue
            #here could be changed to have more options
            input_mc = ROOT.TFile.Open(inputpath + "signal_" + signal + "_M%i/hist-MiniNTuple.root" % mass)
            cutflow_mc = input_mc.Get("CutFlowNoWeight").Clone() #notice here we use no weight for now!
            cutflow_mc_w = input_mc.Get("CutFlowWeight").Clone()
            if dorel:
                maxbincontent = 1.0
                if i > 0:
                    normalization = cut_lst[i - 1]
            totevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin(normalization))
            cutevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin(cut))
            #this is a really dirty temp fix
            scale_weight = (cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin("All")) * 1.0)\
                / (cutflow_mc_w.GetBinContent(cutflow_mc.GetXaxis().FindBin("All")) * 1.0)
            #for cuts that are defined in folders but not in the cutflow table...
            if doint:
                cuthist_temp = input_mc.Get(cut + "/mHH_l")
                cutevt_mc    = cuthist_temp.Integral(0, cuthist_temp.GetXaxis().GetNbins()+1) * scale_weight
            if donormint:
                cuthist_temp = input_mc.Get(normalization + "/mHH_l")
                totevt_mc    = cuthist_temp.Integral(0, cuthist_temp.GetXaxis().GetNbins()+1) * scale_weight

            eff_content = cutevt_mc/totevt_mc
            eff_lst[i].SetBinContent(eff_lst[i].GetXaxis().FindBin(mass), cutevt_mc/totevt_mc)
            eff_lst[i].SetBinError(eff_lst[i].GetXaxis().FindBin(mass), helpers.ratioerror(cutevt_mc, totevt_mc))

            if signal == "G_hh_c10":
                eff_lst[i].GetXaxis().SetTitle("m_{G*_{kk}} [GeV]")
            if signal == "G_hh_c20":
                eff_lst[i].GetXaxis().SetTitle("m_{G*_{kk}} [GeV]")
            if signal == "X_hh":
                eff_lst[i].GetXaxis().SetTitle("m_{S} [GeV]")
            
            maxbincontent = max(maxbincontent, eff_content)
            # print ratioerror(cutevt_mc, totevt_mc)
            input_mc.Close()

    if dosum:##add in a sum curve
        eff_lst.append( ROOT.TH1F(inputdir + "_" + "sum", "%s; Mass [GeV]; Acceptance x Efficiency" %cut, int((highmass-lowmass)/100), lowmass, highmass) )
        for i, cut in enumerate(cut_lst):
            eff_lst[-1].Add(eff_lst[i])
        maxbincontent =  eff_lst[-1].GetMaximum()

    for i, cut in enumerate(eff_lst):
        canv.cd()
        #maxbincontent = 0.15
        #convert it to a TGraph
        graph_lst.append(helpers.TH1toTAsym(eff_lst[i]))
        graph_lst[i].SetLineColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerStyle(CONF.mrk_lst[i])
        graph_lst[i].SetMarkerColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerSize(1)
        graph_lst[i].SetMaximum(maxbincontent * 1.6)
        graph_lst[i].SetMinimum(minbincontent)
        #print cut_dic[cut]
        if i < len(cut_lst):
            legend.AddEntry(graph_lst[i], cut_dic[cut_lst[i]], "apl")
        else: ##of corse this is do sum as well
            legend.AddEntry(graph_lst[i], "All of above", "apl")
        if i == 0: 
            graph_lst[i].Draw("APC")
            #gr.Draw("same L hist")
        else: 
            graph_lst[i].Draw("PC")
            #gr.Draw("same L hist")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.Draw()

    # draw reference lines
    yline05 = ROOT.TLine(1000, 0.0, 1000, maxbincontent)
    yline05.SetLineStyle(9)
    #yline05.Draw()
    yline10 = ROOT.TLine(2000, 0.0, 2000, maxbincontent)
    yline10.SetLineStyle(9)
    #yline10.Draw()
    # draw watermarks
    xatlas, yatlas = 0.2, 0.87
    #atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Preliminary")
    #ATLASLabel(xatlas, yatlas, "Preliminary")
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS")
    #atlas.SetTextAlign(22)
    atlas.SetTextSize(0.04)
    atlas.SetTextFont(72)
    atlas.SetNDC()
    atlas.Draw()
    status = ROOT.TLatex(xatlas + 0.14, yatlas, CONF.StatusLabel)
    #status.SetTextAlign(22)
    status.SetTextSize(0.04)
    status.SetTextFont(42)
    status.SetNDC()
    status.Draw()
    if signal == "G_hh_c10":
        signal_leg = "G*_{kk} k/#bar{M_{pl}} = 1,"
    if signal == "G_hh_c20":
        signal_leg = "G*_{kk} k/#bar{M_{pl}} = 2,"
    if signal == "X_hh":
        signal_leg = "S,"
    myText(xatlas, yatlas-0.05, 1, signal_leg + " #sqrt{s} = 13 TeV", CONF.paperlegsize - 2)
    myText(xatlas, yatlas-0.1, 1, "Boosted", CONF.paperlegsize - 2)
    # finish up
    canv.SaveAs(outputpath + signal + "_" + outputname + "_" + canv.GetName() + ".pdf")
    canv.SaveAs(outputpath + signal + "_" + outputname + "_" + canv.GetName() + ".eps")
    canv.SaveAs(outputpath + signal + "_" + outputname + "_" + canv.GetName() + ".png")
    canv.SaveAs(outputpath + signal + "_" + outputname + "_" + canv.GetName() + ".C")
    canv.Close()


if __name__ == "__main__":
    main()
