import ROOT, rootlogon
import argparse
import array
import copy
import glob
import helpers
import os
import sys
import time
import numpy

ROOT.gROOT.SetBatch(True)

var_names = [
"",
"FT_EFF_Eigen_B_0__1down",
"FT_EFF_Eigen_B_0__1up",
"FT_EFF_Eigen_B_1__1down",
"FT_EFF_Eigen_B_1__1up",
"FT_EFF_Eigen_B_2__1down",
"FT_EFF_Eigen_B_2__1up",
"FT_EFF_Eigen_B_3__1down",
"FT_EFF_Eigen_B_3__1up",
"FT_EFF_Eigen_B_4__1down",
"FT_EFF_Eigen_B_4__1up",
"FT_EFF_Eigen_C_0__1down",
"FT_EFF_Eigen_C_0__1up",
"FT_EFF_Eigen_C_1__1down",
"FT_EFF_Eigen_C_1__1up",
"FT_EFF_Eigen_C_2__1down",
"FT_EFF_Eigen_C_2__1up",
"FT_EFF_Eigen_C_3__1down",
"FT_EFF_Eigen_C_3__1up",
#"FT_EFF_Eigen_C_4__1down", #not in the new one
#"FT_EFF_Eigen_C_4__1up", #not in the new one
"FT_EFF_Eigen_Light_0__1down",
"FT_EFF_Eigen_Light_0__1up",
"FT_EFF_Eigen_Light_1__1down",
"FT_EFF_Eigen_Light_1__1up",
"FT_EFF_Eigen_Light_10__1down",
"FT_EFF_Eigen_Light_10__1up",
"FT_EFF_Eigen_Light_11__1down",
"FT_EFF_Eigen_Light_11__1up",
#"FT_EFF_Eigen_Light_12__1down", #not in the new one
#"FT_EFF_Eigen_Light_12__1up", #not in the new one
#"FT_EFF_Eigen_Light_13__1down", #not in the new one
#"FT_EFF_Eigen_Light_13__1up", #not in the new one
"FT_EFF_Eigen_Light_2__1down",
"FT_EFF_Eigen_Light_2__1up",
"FT_EFF_Eigen_Light_3__1down",
"FT_EFF_Eigen_Light_3__1up",
"FT_EFF_Eigen_Light_4__1down",
"FT_EFF_Eigen_Light_4__1up",
"FT_EFF_Eigen_Light_5__1down",
"FT_EFF_Eigen_Light_5__1up",
"FT_EFF_Eigen_Light_6__1down",
"FT_EFF_Eigen_Light_6__1up",
"FT_EFF_Eigen_Light_7__1down",
"FT_EFF_Eigen_Light_7__1up",
"FT_EFF_Eigen_Light_8__1down",
"FT_EFF_Eigen_Light_8__1up",
"FT_EFF_Eigen_Light_9__1down",
"FT_EFF_Eigen_Light_9__1up",
#"FT_EFF_extrapolation__1down", #not in the new one
#"FT_EFF_extrapolation__1up", #not in the new one
"FT_EFF_extrapolation from charm__1down",
"FT_EFF_extrapolation from charm__1up"]

def sum_variations(prefix, region, f):
    nominal = f.Get(prefix + "_0%s/mHH_l" % region).Clone()

    variations = [f.Get(prefix + ("_%d%s/mHH_l" % (i, region))).Clone() for i in xrange(1, len(var_names))]

    nom_bin_vals = numpy.array([nominal.GetBinContent(i) for i in xrange(nominal.GetXaxis().GetNbins() + 2)])

    tot_diff_up = numpy.array([0. for i in xrange(nominal.GetXaxis().GetNbins() + 2)])
    tot_diff_down = numpy.array([0. for i in xrange(nominal.GetXaxis().GetNbins() + 2)])
    for ct,v in enumerate(variations):
        var_vals = numpy.array([v.GetBinContent(i) for i in xrange(v.GetXaxis().GetNbins() + 2)])

        # if ct != 1:
        #    continue
        #print var_names[ct]
        #if ct % 2 == 0:
        #    diff = var_vals - nom_bin_vals
        #    if len(diff[diff < 0]) > 0:
        #        print var_names[ct]
        #    diff *= diff
        #    #print diff
        #    tot_diff_up += diff
        #    #print tot_diff_up
        #else:
        #    diff = nom_bin_vals - var_vals
        #    diff *= diff
        #    #print numpy.where(diff[diff < 0])
        #    tot_diff_down += diff

        diff = var_vals - nom_bin_vals
        diff_up = numpy.where(diff > 0)
        diff_down = numpy.where(diff < 0)
        diff *= diff
        tot_diff_up[diff_up] += diff[diff_up]
        tot_diff_down[diff_down] += diff[diff_down]
        
        

    #print tot_diff_up
    #print tot_diff_down
    tot_diff_up = numpy.sqrt(tot_diff_up)
    tot_diff_down = numpy.sqrt(tot_diff_down)

    #print tot_diff_up
    #print tot_diff_down

    ret_hist_up = nominal.Clone()
    ret_hist_down = nominal.Clone()
    ret_hist_up.SetName(prefix + "up")
    ret_hist_down.SetName(prefix + "down")
    ret_hist_up.SetTitle(prefix + "up")
    ret_hist_down.SetTitle(prefix + "down")

    for i in xrange(nominal.GetXaxis().GetNbins() + 2):
        ret_hist_up.SetBinContent(i, nom_bin_vals[i] + tot_diff_up[i])
        ret_hist_down.SetBinContent(i, nom_bin_vals[i] - tot_diff_down[i])

    ret_hist_up.Divide(nominal)
    ret_hist_down.Divide(nominal)

    for v in variations:
        v.Divide(nominal)

    nominal.Divide(nominal)

    return ret_hist_up, ret_hist_down, nominal, variations

    
def main():

    ops = options()
    f = ROOT.TFile("../mc-test/hist-Analysis.root", "READ")

    linestyles = [1, 2, 3, 4, 8]
    colortyles = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kOrange-3, ROOT.kViolet]
    prefs = ["all", "tj00", "tj01", "tj10", "tj11"]
    labels = ["Total syst.", "Lead, lead only", "Lead, sublead only", "Sublead, lead only", "Sublead, sublead only"]
    regions = ["FourTag_Signal", "ThreeTag_Signal", "tj0_j0_notag", "tj0_j1_notag", "tj1_j0_notag", "tj1_j1_notag"]
    #prefs = ["all"]
    hist_all = {}

    for r in regions:
        ct = 0

        canv = ROOT.TCanvas("canv" + r, "canv" + r, 600, 600)
        hists = {}
        for p in prefs:
            hist_up, hist_down, nom, varied = sum_variations("btag_syst_" + p, r, f)
            hists[p] = (hist_up, hist_down, nom, varied)
    

        hist_all[r] = hists
        xleg, yleg = 0.7, 0.73
        legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.2)
        for p in prefs:
            hist_up, hist_down, nom, v = hists[p]
            hist_up.SetLineColor(colortyles[ct])
            hist_down.SetLineColor(colortyles[ct])

            hist_up.GetXaxis().SetRangeUser(750., 1250.)
            hist_down.GetXaxis().SetRangeUser(750., 1250.)
            if p == "all":
                nom.GetXaxis().SetRangeUser(750., 1250.)
                nom.SetMarkerSize(1)
                nom.SetMarkerStyle(20)
                nom.SetLineWidth(2)
                nom.SetMarkerColor(ROOT.kBlack)
                nom.SetLineColor(ROOT.kBlack)
                
            hist_up.SetMarkerSize(1)
            hist_up.SetLineWidth(2)
            hist_down.SetMarkerSize(1)
            hist_down.SetLineWidth(2)
            hist_up.SetLineStyle(linestyles[ct])
            hist_down.SetLineStyle(linestyles[ct])
            hist_up.GetYaxis().SetRangeUser(0.0, 2.0)
            hist_up.GetYaxis().SetTitle("Ratio to nominal")

            if p == "all":
                legend.AddEntry(nom, "Nominal", "l p")
            legend.AddEntry(hist_up, labels[ct], "l")

            canv.cd()
            if p == "all":
                hist_up.Draw("hist")
                nom.Draw("ep same")
            else:
                hist_up.Draw("hist same")
            hist_down.Draw("hist same")

            ROOT.gPad.Update()
            canv.Update()
            ct += 1

        legend.Draw("same")
        canv.SaveAs("../Plot/btag_syst_" + r + ".pdf")
        #canv.SaveAs("../Plot/btag_syst_" + r + "_FT_EFF_Eigen_B_0__1down.pdf")

    canv2d = ROOT.TCanvas("canv2d", "canv2d", 600, 600)
    twod_vars_4b = ROOT.TH2F("2dvars4b", "2dvars4b", 100, 0.7, 1.3, 100, 0.7, 1.3)
    twod_vars_4b.GetXaxis().SetTitle("Leading track jet syst. fractional variation")
    twod_vars_4b.GetYaxis().SetTitle("Other track jet syst. fractional variation")
    #bhists = hist_all["tj0_j0_notag"]
    bhists = hist_all["FourTag_Signal"]
    bh1_up, bh1_down, bh1_nom, bh1_vars = bhists["tj00"]
    bh2_up, bh2_down, bh2_nom, bh2_vars = bhists["tj01"]
    bh3_up, bh3_down, bh3_nom, bh3_vars = bhists["tj10"]
    bh4_up, bh4_down, bh4_nom, bh4_vars = bhists["tj11"]

    for i in xrange(len(bh1_vars)):
        #print i
        hist1 = bh1_vars[i]
        hist2 = bh2_vars[i]
        hist3 = bh3_vars[i]
        hist4 = bh4_vars[i]
        #print hist1.GetXaxis().GetNbins()+2
        for bin_num in xrange(hist1.GetXaxis().FindBin(750), hist1.GetXaxis().FindBin(1250)+1):#hist1.GetXaxis().GetNbins()+2):
            #if i == 0:
            #    print hist1.GetBinContent(bin_num)
            #    print hist2.GetBinContent(bin_num)
            twod_vars_4b.Fill(hist1.GetBinContent(bin_num), hist2.GetBinContent(bin_num))
            twod_vars_4b.Fill(hist1.GetBinContent(bin_num), hist3.GetBinContent(bin_num))
            twod_vars_4b.Fill(hist1.GetBinContent(bin_num), hist4.GetBinContent(bin_num))

    canv2d.cd()
    canv2d.SetLogz(True)
    canv2d.SetRightMargin(0.13)
    twod_vars_4b.Draw("colz")
    canv2d.SaveAs("../Plot/2d_vars_4b.pdf")
    
        
    # stack legend
    
    #    
    #legend.SetBorderSize(0)
    #legend.SetFillColor(0)
    #legend.SetMargin(0.2)
    #legend.SetTextSize(0.025)
    #legend.Draw()
    #
    ## watermarks
    #xatlas, yatlas = 0.38, 0.87
    #atlas = ROOT.TLatex(xatlas,      yatlas, "ATLAS Internal")
    #hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "X #rightarrow HH #rightarrow 4b")
    #lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "#sqrt{s} = 13 TeV")
    #watermarks = [atlas, hh4b, lumi]
    #for wm in watermarks:
    #    wm.SetTextAlign(22)
    #    wm.SetTextSize(0.04)
    #    wm.SetTextFont(42)
    #    wm.SetNDC()
    #    wm.Draw()


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signal")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

if __name__ == "__main__":
    main()
        
