import ROOT, rootlogon
import argparse, array, copy, glob, os, sys, time
import helpers
import config as CONF

ROOT.gROOT.SetBatch(True)

def main():

    ops = options()
    inputdir = ops.inputdir
    inputroot = ops.inputroot

    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "Plot/SigEff/"
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    # select the cuts
    # cut_sig_lst = ["2Trk_OneTag_Signal_Significance", "2Trk_TwoTag_split_Signal_Significance",\
    # "3Trk_OneTag_Signal_Significance", "3Trk_TwoTag_Signal_Significance", "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance",\
    # "4Trk_OneTag_Signal_Significance", "4Trk_TwoTag_Signal_Significance", "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]
    # cut_sig_lst = ["2Trk_OneTag_Signal_Significance", "2Trk_TwoTag_split_Signal_Significance",\
    # "3Trk_OneTag_Signal_Significance", "3Trk_TwoTag_Signal_Significance", "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance",\
    # "4Trk_OneTag_Signal_Significance", "4Trk_TwoTag_Signal_Significance", "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]
    # cut_sig_lst = ["2Trk_TwoTag_split_Signal_Significance",\
    # "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance",\
    # "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]
    

    # cut_sig_lst = ["OneTag_Signal_Significance", "TwoTag_split_Signal_Significance",\
    # "TwoTag_Signal_Significance", "ThreeTag_Signal_Significance",\
    # "FourTag_Signal_Significance", "ThreeTag_1loose_Signal_Significance", "TwoTag_split_1loose_Signal_Significance", "TwoTag_split_2loose_Signal_Significance"]
    # cut_sig_lst = ["2Trk_in1_OneTag_Signal_Significance", "2Trk_in1_TwoTag_Signal_Significance", \
    #     "2Trk_OneTag_Signal_Significance", "2Trk_TwoTag_split_Signal_Significance", \
    #     "3Trk_OneTag_Signal_Significance", "3Trk_TwoTag_Signal_Significance", "3Trk_TwoTag_split_Signal_Significance", "3Trk_ThreeTag_Signal_Significance", \
    #     "4Trk_OneTag_Signal_Significance", "4Trk_TwoTag_Signal_Significance", "4Trk_TwoTag_split_Signal_Significance", "4Trk_ThreeTag_Signal_Significance", "4Trk_FourTag_Signal_Significance"]

    # Draw the efficiency plot relative to the all normalization
    #DrawSignalEff(cut_sig_lst, "TEST_b77", "Significance", 100)
    # b_tag = [70, 77, 80, 85, 90]
    cut_all_lst = ["OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
    outputname = inputdir + "_allsig"
    DrawSignalEff(cut_all_lst, inputdir, inputroot, outputname, 0.005, (2400, 3100))
    DrawSignalEff(cut_all_lst, inputdir, inputroot, outputname, 0.06, (1750, 2450))
    DrawSignalEff(cut_all_lst, inputdir, inputroot, outputname, 0.2, (1450, 2450))
    DrawSignalEff(cut_all_lst, inputdir, inputroot, outputname, 1.5)
    DrawSignalEff(cut_all_lst, inputdir, inputroot, outputname, 300, logy=1)


    cut_rel_lst = ["TwoTag_split", "ThreeTag", "FourTag"]
    outputname = inputdir + "_relsig"
    DrawSignalEff(cut_rel_lst, inputdir, inputroot, outputname, 0.005, (2400, 3100))
    DrawSignalEff(cut_rel_lst, inputdir, inputroot, outputname, 0.06, (1750, 2450))
    DrawSignalEff(cut_rel_lst, inputdir, inputroot, outputname, 0.2, (1450, 2450))
    DrawSignalEff(cut_rel_lst, inputdir, inputroot, outputname, 1.5)
    DrawSignalEff(cut_rel_lst, inputdir, inputroot, outputname, 300, logy=1)

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    parser.add_argument("--inputroot", default="sum")
    return parser.parse_args()

def DrawSignalEff(cut_lst, inputdir="b77", inputroot="sum", outputname="", normalization=1.0, plotrange=(0, 3100), logy=0):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region
    histname = "_Signal_Significance"

    canv = ROOT.TCanvas(outputname + "_" + str(plotrange[0]) + "_" +  str(plotrange[1]), "Efficiency", 800, 800)
    xleg, yleg = 0.65, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.2)

    # two pad
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

    #top pad
    canv.cd()
    pad0.SetLogy(logy)
    pad0.Draw()
    pad0.cd()
    # setup basic plot parameters
    lowmass = -50
    highmass = 3150
    # load input MC file
    input_mc = ROOT.TFile.Open(CONF.inputpath + inputdir + "/" + inputroot + "_" + inputdir + ".root")
    maxbincontent = normalization
    minbincontent = 0.00001
    temp_all = input_mc.Get(cut_lst[0] + histname).Clone()
    temp_all.SetName("Combined")

    input_mc_ref = ROOT.TFile.Open(CONF.inputpath +"f_fin-cb-newSR-ref/" + "sum_f_fin-cb-newSR-ref" + ".root")
    temp_ref = input_mc_ref.Get(cut_lst[0] + histname).Clone()
    temp_ref.SetName("Run2-ref")

    temp_ratio = input_mc.Get(cut_lst[0] + histname).Clone()
    temp_ratio.SetName("Ratio")

    for j in range(1, temp_all.GetNbinsX()+1):
            temp_all.SetBinContent(j, 0)
            temp_all.SetBinError(j, 0)
            temp_ref.SetBinContent(j, 0)
            temp_ref.SetBinError(j, 0)
            temp_all.SetMinimum(minbincontent)
            temp_ref.SetMinimum(minbincontent)

    graph_lst = []
    
    for i, cut in enumerate(cut_lst):
        #print cut
        sig_mc = input_mc.Get(cut + histname) #get the input histogram
        sig_mc_ref = input_mc_ref.Get(cut + histname) #get the input histogram
        for j in range(1, temp_all.GetNbinsX()+1):
            #temp_all.SetBinContent(j, ROOT.TMath.Sqrt(temp_all.GetBinContent(j) * temp_all.GetBinContent(j) + sig_mc.GetBinContent(j) * sig_mc.GetBinContent(j)))
            temp_ref.SetBinContent(j, ROOT.TMath.Sqrt(temp_ref.GetBinContent(j) * temp_ref.GetBinContent(j) + sig_mc_ref.GetBinContent(j) * sig_mc_ref.GetBinContent(j)))
            temp_all.SetBinContent(j, ROOT.TMath.Sqrt(temp_all.GetBinContent(j) * temp_all.GetBinContent(j) + sig_mc.GetBinContent(j) * sig_mc.GetBinContent(j)))
            temp_ref.SetBinError(j, ROOT.TMath.Sqrt(temp_ref.GetBinError(j) * temp_ref.GetBinError(j) + sig_mc_ref.GetBinError(j) * sig_mc_ref.GetBinError(j)))
            temp_all.SetBinError(j, ROOT.TMath.Sqrt(temp_all.GetBinError(j) * temp_all.GetBinError(j) + sig_mc.GetBinError(j) * sig_mc.GetBinError(j)))
        del(sig_mc_ref)


        graph_lst.append(helpers.TH1toTAsym(sig_mc, pltrange=plotrange))
        graph_lst[i].SetMaximum(maxbincontent * 1.5)
        graph_lst[i].SetMinimum(minbincontent)
        graph_lst[i].SetLineColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerStyle(20 + i)
        graph_lst[i].SetMarkerColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerSize(1)
        legend.AddEntry(graph_lst[i], cut.replace("_", " "), "APL")
        
        if cut==cut_lst[0]: 
            graph_lst[i].Draw("APC")
        else: 
            graph_lst[i].Draw("PC")
        del(sig_mc)

    graph_all = helpers.TH1toTAsym(temp_all)
    graph_all.SetLineColor(2)
    graph_all.SetLineStyle(2)
    graph_all.SetMarkerStyle(5)
    graph_all.SetMarkerColor(2)
    graph_all.SetMarkerSize(1)
    graph_all.GetXaxis().SetRangeUser(plotrange[0], plotrange[1])
    legend.AddEntry(graph_all, graph_all.GetName().replace("_", " "), "APL")
    graph_all.Draw("PC")

    graph_ref = helpers.TH1toTAsym(temp_ref)
    graph_ref.SetLineColor(1)
    graph_ref.SetLineStyle(3)
    graph_ref.SetMarkerStyle(4)
    graph_ref.SetMarkerColor(1)
    graph_ref.SetMarkerSize(1)
    graph_ref.GetXaxis().SetRangeUser(plotrange[0], plotrange[1])
    legend.AddEntry(graph_ref, graph_ref.GetName().replace("_", " "), "APL")
    graph_ref.Draw("PC")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.02)
    legend.Draw()

    # draw reference lines
    xline05 = ROOT.TLine(lowmass, 0.05, highmass, 0.05)
    xline05.SetLineStyle(3)
    xline05.Draw()
    xline10 = ROOT.TLine(lowmass, 0.1, highmass, 0.1)
    xline10.SetLineStyle(4)
    xline10.Draw()
    yline05 = ROOT.TLine(1000, 0.0, 1000, maxbincontent)
    yline05.SetLineStyle(9)
    yline05.Draw()
    yline10 = ROOT.TLine(2000, 0.0, 2000, maxbincontent)
    yline10.SetLineStyle(9)
    yline10.Draw()
    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    watermarks = [atlas, hh4b, lumi]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()

    #bottom pad
    canv.cd()
    pad1.Draw()
    pad1.cd()
    for j in range(1, temp_ratio.GetNbinsX()+1):
        try:
            temp_ratio.SetBinContent(j, temp_all.GetBinContent(j) / temp_ref.GetBinContent(j))
            temp_ratio.SetBinError(j, helpers.ratioerror(\
                temp_all.GetBinContent(j), temp_ref.GetBinContent(j), \
                temp_all.GetBinError(j), temp_ref.GetBinError(j)))
        except ZeroDivisionError:
            pass
            #print "Divide by zero! Check bin content in", canv.GetName()

    temp_ratio.SetMarkerStyle(20)
    temp_ratio.SetMarkerColor(1)
    temp_ratio.SetMarkerSize(1)
    temp_ratio.GetYaxis().SetTitleFont(43)
    temp_ratio.GetYaxis().SetTitleSize(28)
    temp_ratio.GetYaxis().SetLabelFont(43)
    temp_ratio.GetYaxis().SetLabelSize(28)
    temp_ratio.GetYaxis().SetTitle(" %s/ ref" % inputdir)
    temp_ratio.GetYaxis().SetRangeUser(0.8, 1.2) #set range for ratio plot
    temp_ratio.GetYaxis().SetNdivisions(405)

    temp_ratio.GetXaxis().SetTitleFont(43)
    temp_ratio.GetXaxis().SetTitleOffset(3.5)
    temp_ratio.GetXaxis().SetTitleSize(28)
    temp_ratio.GetXaxis().SetLabelFont(43)
    temp_ratio.GetXaxis().SetLabelSize(28)
    temp_ratio.GetXaxis().SetRangeUser(plotrange[0], plotrange[1])
    temp_ratio.GetXaxis().SetTitle("mass, GeV")

    temp_ratio.Draw("ep")
    # draw the ratio 1 line
    line = ROOT.TLine(plotrange[0], 1.0, plotrange[1], 1.0)
    line.SetLineStyle(1)
    line.Draw()

    # finish up
    if logy != 0:
        canv.SetName(canv.GetName() + "_1")
    canv.SaveAs(outputpath + canv.GetName() + ".pdf")

    pad0.Close()
    pad1.Close()
    canv.Close()
    input_mc.Close()
    input_mc_ref.Close()
    #clean up all the pointers...
    del(temp_all)
    del(temp_ref)
    del(temp_ratio)
    del(graph_all)
    del(graph_ref)
    del(graph_lst)


if __name__ == "__main__":
    main()
