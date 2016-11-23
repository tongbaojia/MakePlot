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

def main():

    global ops
    ops = options()
    inputdir = ops.inputdir

    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "Plot/SigEff/"

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    #set global draw options
    global mass_lst
    #mass_lst = [700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000, 3500, 4000, 4500, 5000, 6000]
    mass_lst = [700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    global lowmass
    lowmass = min(mass_lst) - 50
    global highmass
    highmass = max(mass_lst) + 150
    # create output file
    #output = ROOT.TFile.Open(outuputpath + "sigeff.root", "recreate")
    #output.Close()

    # select the cuts
    # the list must start from the largest to the smallest!
    evtsel_lst = ["PassTrig", "PassFatJetMass", "PassDiJetEta", "PassDetaHH",  "PassBJetSkim", "PassSignal"]
    detail_lst = ["4trk_3tag_signal", "4trk_4tag_signal", "4trk_2tag_signal", \
    "4trk_2tag_split_signal", "3trk_3tag_signal", "3trk_2tag_signal", "3trk_2tag_split_signal", "2trk_2tag_split_signal"]
    region_lst = ["ThreeTag_Signal", "FourTag_Signal", "TwoTag_Signal", "TwoTag_split_Signal", "OneTag_Signal", "NoTag_Signal"]

    # Draw the efficiency plot relative to the all normalization
    DrawSignalEff(evtsel_lst, inputdir, "evtsel", "PreSel")
    DrawSignalEff(evtsel_lst, inputdir, "evtsel", "PreSel", dorel=True)
    #DrawSignalEff(evtsel_lst, inputdir, "evtsel", "All", dorelfcomp=True) #for signal selection efficiency comparison; i.e. trig combination
    #DrawSignalEff(evtsel_lst, inputdir, "evtsel", "All", dorel=True, dorelfcomp=True) #for signal selection efficiency comparison; i.e. trig combination
    DrawSignalEff(evtsel_lst, inputdir, "evtsel", "All")
    DrawSignalEff(evtsel_lst, inputdir, "evtsel", "All", dorel=True)
    DrawSignalEff(region_lst, inputdir, "region_lst", "PreSel", doint=True)
    DrawSignalEff(region_lst, inputdir, "region_lst", "PassDetaHH", doint=True)
    # For cuts that don't exist in the cutflow plot; only run this on original sample!
    #DrawSignalEff(detail_lst, inputdir, "detail_lst", "AllTag_Signal", donormint=True)
    #DrawSignalEff(region_lst, inputdir, "region_lst", "AllTag_Signal", doint=True, donormint=True)
    #DrawSignalEff(detail_lst, inputdir, "detail_lst", "PreSel")
    #DrawSignalEff(detail_lst, inputdir, "detail_lst", "PassDetaHH")


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
    parser.add_argument("--Xhh", action='store_true')
    return parser.parse_args()


def DrawSignalEff(cut_lst, inputdir="b77", outputname="", normalization="All", doint=False, donormint=False, dorel=False, dorelfcomp=False):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region
    afterscript = ("_rel" if dorel else "") + ("_ref" if dorelfcomp else "") 
    canv = ROOT.TCanvas(inputdir + "_" + "Efficiency" + "_" + normalization + afterscript, "Efficiency", 800, 800)
    xleg, yleg = 0.52, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    # load input MC file
    eff_lst = []
    graph_lst = []
    maxbincontent = 0.001
    minbincontent = -0.001

    for i, cut in enumerate(cut_lst):
        eff_lst.append( ROOT.TH1F(inputdir + "_" + cut, "%s; Mass, GeV; Efficiency" %cut, int((highmass-lowmass)/100), lowmass, highmass) )

        for mass in mass_lst:
            #here could be changed to have more options
            input_mc_type= "signal_G_hh_c10_M" if not ops.Xhh else "signal_X_hh_M"
            input_mc     = ROOT.TFile.Open(inputpath + input_mc_type + "%i/hist-MiniNTuple.root" % mass)
            cutflow_mc   = input_mc.Get("CutFlowNoWeight").Clone("CutFlowNoWeight") #notice here we use no weight for now!
            cutflow_mc_w = input_mc.Get("CutFlowWeight").Clone("CutFlowWeight")
            if dorel:
                maxbincontent = 1.0
                if i > 0:
                    normalization = cut_lst[i - 1]
            totevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin(normalization))
            cutevt_mc = cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin(cut))
            #this is a really dirty temp fix
            scale_weight = (cutflow_mc.GetBinContent(cutflow_mc.GetXaxis().FindBin("All")) * 1.0)\
                / (cutflow_mc_w.GetBinContent(cutflow_mc_w.GetXaxis().FindBin("All")) * 1.0)
                
            #this is really only for doing reference comparison only!
            input_mc_ref = ROOT.TFile.Open(CONF.inputpath + "ref" + "/" + "signal_G_hh_c10_M" + "%i/hist-MiniNTuple.root" % mass)
            cutflow_mc_ref   = input_mc_ref.Get("CutFlowNoWeight").Clone("CutFlowNoWeight_ref") #notice here we use no weight for now!
            cutflow_mc_w_ref = input_mc_ref.Get("CutFlowWeight").Clone("CutFlowWeight_ref")
            totevt_mc_ref = cutflow_mc_ref.GetBinContent(cutflow_mc_ref.GetXaxis().FindBin(normalization))
            cutevt_mc_ref = cutflow_mc_ref.GetBinContent(cutflow_mc_ref.GetXaxis().FindBin(cut))
            scale_weight_ref = (cutflow_mc_ref.GetBinContent(cutflow_mc_ref.GetXaxis().FindBin("All")) * 1.0)\
                / (cutflow_mc_w_ref.GetBinContent(cutflow_mc_w_ref.GetXaxis().FindBin("All")) * 1.0)

            #print cut, mass, cutevt_mc, totevt_mc, cutevt_mc_ref, totevt_mc_ref
            #for cuts that are defined in folders but not in the cutflow table...
            if doint:
                cuthist_temp     = input_mc.Get(cut + "/mHH_l")
                cutevt_mc        = cuthist_temp.Integral(0, cuthist_temp.GetXaxis().GetNbins()+1) * scale_weight
                cuthist_temp_ref = input_mc_ref.Get(cut + "/mHH_l")
                cutevt_mc_ref    = cuthist_temp_ref.Integral(0, cuthist_temp_ref.GetXaxis().GetNbins()+1) * scale_weight_ref
            if donormint:
                cuthist_temp     = input_mc.Get(normalization + "/mHH_l")
                totevt_mc        = cuthist_temp.Integral(0, cuthist_temp.GetXaxis().GetNbins()+1) * scale_weight
                cuthist_temp_ref = input_mc_ref.Get(normalization + "/mHH_l")
                totevt_mc_ref    = cuthist_temp_ref.Integral(0, cuthist_temp_ref.GetXaxis().GetNbins()+1) * scale_weight_ref

            #for ref comparison
            if dorel and dorelfcomp:
                totevt_mc = totevt_mc * (cutevt_mc_ref / totevt_mc_ref) * 1.0
            elif dorelfcomp:
                totevt_mc = cutevt_mc_ref * 1.0
                minbincontent = 0.5
            
            # if mass == 2500:
            #     print "m:{:>5} c:{:>24} evt:{:>8};".format(mass, cut, cutevt_mc)

            #continue as usual
            eff_content = cutevt_mc/totevt_mc
            eff_lst[i].SetBinContent(eff_lst[i].GetXaxis().FindBin(mass), cutevt_mc/totevt_mc)
            eff_lst[i].SetBinError(eff_lst[i].GetXaxis().FindBin(mass), helpers.ratioerror(cutevt_mc, totevt_mc))
            maxbincontent = max(maxbincontent, eff_content)
            # print ratioerror(cutevt_mc, totevt_mc)
            input_mc.Close()
            input_mc_ref.Close()

        canv.cd()
        #convert it to a TGraph
        graph_lst.append(helpers.TH1toTAsym(eff_lst[i]))
        graph_lst[i].SetLineColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerStyle(20 + i)
        graph_lst[i].SetMarkerColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerSize(1)
        graph_lst[i].SetMaximum(maxbincontent * 1.5)
        graph_lst[i].SetMinimum(minbincontent)
        legend.AddEntry(graph_lst[i], cut.replace("_", " "), "apl")
        if cut==cut_lst[0]: 
            graph_lst[i].Draw("APC")
            #gr.Draw("same L hist")
        else: 
            graph_lst[i].Draw("PC")
            #gr.Draw("same L hist")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw reference lines
    yline05 = ROOT.TLine(1000, 0.0, 1000, maxbincontent)
    yline05.SetLineStyle(9)
    yline05.Draw()
    yline10 = ROOT.TLine(2000, 0.0, 2000, maxbincontent)
    yline10.SetLineStyle(9)
    yline10.Draw()
    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0" if not ops.Xhh else "2HDM")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    watermarks = [atlas, hh4b, lumi]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()
    # finish up
    canv.SaveAs(outputpath + outputname + ("_" if not ops.Xhh else "_2HDM_" ) + canv.GetName() + ".pdf")
    canv.Close()




if __name__ == "__main__":
    main()
