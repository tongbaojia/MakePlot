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
#ROOT.gROOT.Macro("../../XhhCommon/post_processing/helpers.C")
#ROOT.gROOT.Macro("../../XhhCommon/post_processing/cross_sections.C")

def main():

    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "Trig_eff.root", "recreate")
    outputdir = CONF.outplotpath
    # setup canvas
    canv = ROOT.TCanvas("Trig", "Trig", 800, 800)
    # load input MC file
    #input_mc = ROOT.TFile.Open("../../test_ttbarnonhad/hist-hh4b-00-06-03q.root")
    eff_lst = ["j_Pt_t", "j_Eta", "j_Phi"]
    for plot_name in eff_lst:

        input_mc = ROOT.TFile.Open(CONF.inputpath + "trig_ttbarnonhad/hist-MiniNTuple.root ")
        allevt_mc = input_mc.Get("PassLep_%s" % plot_name)
        passevt_mc = input_mc.Get("PassTrig_%s" % plot_name)
        eff_mc = ROOT.TEfficiency(passevt_mc, allevt_mc)
        eff_mc.SetLineColor(ROOT.kRed)
        eff_mc.SetMarkerColor(ROOT.kRed)
        hst_eff_mc = eff_mc.GetCopyTotalHisto()
        hst_eff_mc.GetYaxis().SetTitle("HLT_j360_a10r Trigger Efficiency")
        hst_eff_mc.SetMaximum(1.5)
        hst_eff_mc.SetMinimum(0)
        hst_eff_mc.Draw("")
        eff_mc.Draw("same")
        ROOT.gPad.Update();
        eff_mc.GetPaintedGraph().SetMaximum(1.5)
        eff_mc.GetPaintedGraph().SetMinimum(0)
        # load input data file
        input_data = ROOT.TFile.Open(CONF.inputpath + "trig_data/hist-MiniNTuple.root")
        allevt_data = input_data.Get("PassLep_%s" % plot_name)
        passevt_data = input_data.Get("PassTrig_%s" % plot_name)
        eff_data = ROOT.TEfficiency(passevt_data, allevt_data)
        eff_data.SetMarkerStyle(20)
        eff_data.SetMarkerSize(1)
        eff_data.SetLineColor(ROOT.kBlack)
        eff_data.SetMarkerColor(ROOT.kBlack)
        eff_data.Draw("same")
        ROOT.gPad.Update();
        eff_data.GetPaintedGraph().SetMaximum(1.5)
        eff_data.GetPaintedGraph().SetMinimum(0)
        # hst_eff_data.SetMaximum(1.5)
        # hst_eff_data.SetMinimum(0)
        # hst_eff_data.Draw("same")

        # stack legend
        xleg, yleg = 0.6, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.2)
        legend.AddEntry(eff_mc, "t#bar{t} MC", "apl")
        legend.AddEntry(eff_data, "data", "apl")
        legend.SetBorderSize(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.04)
        legend.Draw()


        # watermarks
        xatlas, yatlas = 0.38, 0.87
        atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
        hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "Semi-leptonic t#bar{t}")
        lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "#sqrt{s} = 13 TeV")
        watermarks = [atlas, hh4b, lumi]

        # draw watermarks
        for wm in watermarks:
            wm.SetTextAlign(22)
            wm.SetTextSize(0.04)
            wm.SetTextFont(42)
            wm.SetNDC()
            wm.Draw()

        # draw data/MC ratio
        ratioMin = 0
        ratioMax = 2

        # for i in range(eff_data.GetPaintedGraph().GetGlobalBin()):
        #     print eff_data.GetName(), " ", eff_data.GetEfficiency(i)
        #passevt_data.Divide(allevt_data)    
        #passevt_mc.Divide(allevt_mc)
        for i in range(0, passevt_data.GetNbinsX() + 2):
            passevt_data.SetBinContent(i, eff_data.GetEfficiency(i))
            passevt_mc.SetBinContent(i, eff_mc.GetEfficiency(i))
            passevt_data.SetBinError(i, max(eff_data.GetEfficiencyErrorLow(i), eff_data.GetEfficiencyErrorUp(i)))
            passevt_mc.SetBinError(i, max(eff_mc.GetEfficiencyErrorLow(i), eff_mc.GetEfficiencyErrorUp(i)))
    
        passevt_data.SetMarkerStyle(20)
        passevt_data.SetMarkerSize(1)
        passevt_data.SetLineColor(ROOT.kBlack)
        passevt_data.SetMarkerColor(ROOT.kBlack)


        ratio = helpers.ratio(name   = canv.GetName()+"_ratio",
                                 numer  = passevt_data,   # AHH KILL ME
                                 denom  = passevt_mc,
                                 min    = ratioMin,
                                 max    = ratioMax,
                                 ytitle = "Data / pred."
                                )
        share,top,bot = helpers.same_xaxis(name          = canv.GetName()+"_share",
                                   top_canvas    = canv,
                                   bottom_canvas = ratio,
                                   )
        canv.SetName(canv.GetName()+"_noratio")
        share.SetName(share.GetName().replace("_share", ""))
        canv = share

        # finish up
        output.cd()
        canv.SaveAs(outputdir + eff_mc.GetName() + ".pdf")


    canv.Clear()
    #check basic distributions in mc makes sense
    plot_lst = ["j_Pt", "j_Eta", "j_Phi", "j_M", "mu_Pt", "mu_Eta", "mu_Phi",\
     "met", "met_Phi", "bj_Pt", "bj_Eta", "bj_Phi", "bj_M", "bj_MV2", \
     "w_MT", "l_dPhi_mu_met", "l_dEta_mu_bj", "l_dPhi_mu_bj", "l_dR_mu_bj", \
     "l_Pt", "l_Eta", "l_Phi", "l_M", "l_MT", \
     "leptop_dR", "leptop_deta", "leptop_dphi", "leptop_m", "leptop_mT"]

    plot_2d_lst = ["mu_Pt_met", "l_Pt_met", "l_Pt_mu_pt", "l_Pt_j_pt", "l_Pt_bj_pt", "l_Pt_dR_mu_bj"]

    ## validate in MC
    # for plot_name in plot_lst:
    #     plt_before = input_mc.Get("AllLep_%s" % plot_name)
    #     plt_after  = input_mc.Get("PassLep_%s" % plot_name)
    #     plt_before.SetLineColor(ROOT.kRed)
    #     plt_after.SetLineColor(ROOT.kBlue)
    #     maxvalue = max(plt_before.GetMaximum(), plt_after.GetMaximum())
    #     plt_before.SetMaximum(1.5 * maxvalue)
    #     plt_after.SetMaximum(1.5 * maxvalue)
    #     plt_before.Draw()
    #     plt_after.Draw("same")

    #     xatlas, yatlas = 0.4, 0.9
    #     atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    #     hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "Semi-leptonic t#bar{t} MC")
    #     lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "#sqrt{s} = 13 TeV")
    #     watermarks = [atlas, hh4b, lumi]

    #     xleg, yleg = 0.6, 0.7
    #     legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.2)
    #     legend.AddEntry(plt_before, "before selection", "apl")
    #     legend.AddEntry(plt_after,  "after selection", "apl")
    #     legend.SetBorderSize(0)
    #     legend.SetMargin(0.3)
    #     legend.SetTextSize(0.04)
    #     legend.Draw()
    #      # draw watermarks
    #     for wm in watermarks:
    #         wm.SetTextAlign(22)
    #         wm.SetTextSize(0.04)
    #         wm.SetTextFont(42)
    #         wm.SetNDC()
    #         wm.Draw()

    #     output.cd()
    #     canv.SaveAs(outputdir + plt_before.GetName()+".pdf")
    #     canv.Clear()

    # ## validate in data
    for plot_name in plot_lst:
        plt_before = input_mc.Get("PassLep_%s" % plot_name)
        plt_after  = input_data.Get("PassLep_%s" % plot_name)
        plt_before.SetLineColor(ROOT.kRed)
        plt_after.SetLineColor(ROOT.kBlack)
        plt_after.SetMarkerStyle(20)
        plt_after.SetMarkerSize(1)
        plt_after.GetYaxis().SetTitleOffset(1.5)
        plt_before.GetYaxis().SetTitleOffset(1.5)
        maxvalue = max(plt_before.GetMaximum(), plt_after.GetMaximum())
        plt_before.SetMaximum(1.5 * maxvalue)
        plt_after.SetMaximum(1.5 * maxvalue)
        plt_before.SetMinimum(0)
        plt_after.SetMinimum(0)
        plt_after.Draw("ep")
        plt_before.Draw("hist same")

        xatlas, yatlas = 0.38, 0.87
        atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
        hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "Semi-leptonic t#bar{t} MC")
        lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "#sqrt{s} = 13 TeV")
        watermarks = [atlas, hh4b, lumi]

        xleg, yleg = 0.6, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.2)
        legend.AddEntry(plt_before, "MC", "apl")
        legend.AddEntry(plt_after,  "data", "apl")
        legend.SetBorderSize(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.04)
        legend.Draw()
         # draw watermarks
        for wm in watermarks:
            wm.SetTextAlign(22)
            wm.SetTextSize(0.04)
            wm.SetTextFont(42)
            wm.SetNDC()
            wm.Draw()


        # draw data/MC ratio
        ratioMin = 0
        ratioMax = 2 
        ratio = helpers.ratio(name   = canv.GetName()+"_ratio",
                              numer  = plt_after,   # AHH KILL ME
                              denom  = plt_before,
                              min    = ratioMin,
                              max    = ratioMax,
                              ytitle = "Data / pred."
                              )
        share,top,bot = helpers.same_xaxis(name          = canv.GetName()+"_share",
                                   top_canvas    = canv,
                                   bottom_canvas = ratio,
                                   )
        canv.SetName(canv.GetName()+"_noratio")
        share.SetName(share.GetName().replace("_share", ""))
        canv = share

        output.cd()
        canv.SaveAs(outputdir + plt_before.GetName()+".pdf")
        plt_before.Write()
        plt_after.Write()
        canv.Clear()


    # for plot_name in plot_2d_lst:
    #     plt_after  = input_mc.Get("PassLep_%s" % plot_name)
    #     plt_after.Draw("colz")

    #     xatlas, yatlas = 0.4, 0.9
    #     atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    #     hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "Semi-leptonic t#bar{t} MC")
    #     lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "#sqrt{s} = 13 TeV")
    #     watermarks = [atlas, hh4b, lumi]

    #     # draw watermarks
    #     for wm in watermarks:
    #         wm.SetTextAlign(22)
    #         wm.SetTextSize(0.04)
    #         wm.SetTextFont(42)
    #         wm.SetNDC()
    #         wm.Draw()

    #     output.cd()
    #     canv.SaveAs(outputdir + plt_after.GetName()+".pdf")
    #     canv.Clear()

    eff_mc.Write()
    eff_data.Write()
    output.Close()

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def warn(message):
    print
    print "Warning in %s: %s" % (__file__, message)
    print

if __name__ == "__main__":
    main()
