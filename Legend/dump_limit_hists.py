"""
qcd.py: a script to convert ntuples into a multijet ntuple.
$ python qcd.py --wp=77
"""
import argparse
import array
import copy
import os
import sys
import ROOT
import glob
from math import sqrt
from Xhh4bUtils.BkgFit.BackgroundFit_MultiChannel import BackgroundFit
from Xhh4bUtils.BkgFit.HistoTools import BlindData2bSR
import config as CONF

treename  = "XhhMiniNtuple"

ROOT.gROOT.SetBatch()
def main():

    ops = options()

    if ops.data is None:
        fatal("Please specify the data histogram files with --data")

    if ops.mc is None:
        fatal("Please specify the ttbar histogram files with --mc")

    if ops.zjets is None:
        fatal("Please specify the zjets histogram files with --mc")

    #if ops.signal is None:
    #    fatal("Please specify the signal histogram directory with --signal")

    suffix = ""

    if not ops.suffix is None:
        suffix = ops.suffix

    n_btag = ["4", "3"]

    #actual fit part
    results = BackgroundFit(ops.data, ops.mc, ops.zjets, distributionName = "leadHCand_Mass", n_btag = n_btag, whichFunc = "XhhBoosted", output = ops.output)

    print results
    mu_qcd = results["muqcd"]
    tt_scale = results["topscale"]

    data_file = ROOT.TFile(ops.data, "READ")

    mc_file = None
    if not ops.mc is None:
        mc_file = ROOT.TFile(ops.mc, "READ")

    for i in range(len(n_btag)):
        if not ops.data is None:
            outfile_sub = ROOT.TFile("%s/qcd_sub_%s_%stag.root" % (ops.output, suffix, n_btag[i]), "RECREATE")

            keys = data_file.GetListOfKeys()

            for k in keys:
                c_dir = data_file.Get(k.GetName())
                if not "TwoTag_" in k.GetName():
                    continue
                outfile_sub.cd()
                new_dir = ROOT.TDirectoryFile(c_dir.GetName(), c_dir.GetTitle())

                hists = None
                try:
                    hists = c_dir.GetListOfKeys()
                except:
                    continue
            
                for h in hists:
                    curr_hist = c_dir.Get(h.GetName()).Clone()
                    #print k.GetName()+"/"+h.GetName()
                    curr_hist.Add(mc_file.Get(k.GetName()+"/"+h.GetName()), -tt_scale[i])
                    curr_hist.Scale(mu_qcd[i])
                    new_dir.cd()
                    curr_hist.Write()

                outfile_sub.cd()
                new_dir.Write()
    
            outfile_sub.Close()

    for i in range(len(n_btag)):
        if not ops.mc is None:
            outfile_sub = ROOT.TFile("%s/tt_sub_%s_%stag.root" % (ops.output, suffix, n_btag[i]), "RECREATE")

            keys = mc_file.GetListOfKeys()

            for k in keys:
                c_dir = mc_file.Get(k.GetName())
                
                if not "ThreeTag_" in k.GetName():
                    continue

                outfile_sub.cd()
                new_dir = ROOT.TDirectoryFile(c_dir.GetName(), c_dir.GetTitle())

                hists = None
                try:
                    hists = c_dir.GetListOfKeys()
                except:
                    continue
            
                for h in hists:
                    curr_hist = c_dir.Get(h.GetName()).Clone()
                    #print "btag ", i, " ", tt_scale[i]
                    #print "4 entries", mc_file.Get(k.GetName().replace("Three", "Four")+"/"+h.GetName()).GetEntries()
                    n_3tag = curr_hist.GetEntries()
                    curr_hist.Scale(tt_scale[i])
                    if n_btag[i] == "4":
                        #print "btag ", i, " ", tt_scale[i]
                        n_4tag = mc_file.Get(k.GetName().replace("Three", "Four")+"/"+h.GetName()).GetEntries()
                        if curr_hist.GetEntries() != 0:
                            curr_hist.Scale(n_4tag / n_3tag)
                    
                    new_dir.cd()
                    curr_hist.Write()

                outfile_sub.cd()
                new_dir.Write()
    
            outfile_sub.Close()
            

    signal_2tag = data_file.Get("TwoTag_Signal/mHH_l")
    #signal_2tag = BlindData2bSR(signal_2tag)
    print "# of events, 2tag signal: %f" % signal_2tag.Integral(0, signal_2tag.GetXaxis().GetNbins()+1)
    print signal_2tag
    bg_pred_4tag = signal_2tag.Clone()
    bg_pred_4tag.Scale(mu_qcd[0])

    bg_pred_3tag = signal_2tag.Clone()
    bg_pred_3tag.Scale(mu_qcd[1])

    outfile = ROOT.TFile("%s/4b_region_boosted_%s.root" % (ops.output, suffix), "RECREATE")
    outfile_3b = ROOT.TFile("%s/3b_region_boosted_%s.root" % (ops.output, suffix), "RECREATE")

    outfile.cd()
    bg_pred_4tag.SetName("qcd_hh")
    bg_pred_4tag.SetTitle("qcd_hh")
    bg_pred_4tag.Write()

    outfile_3b.cd()
    bg_pred_3tag.SetName("qcd_hh")
    bg_pred_3tag.SetTitle("qcd_hh")
    bg_pred_3tag.Write()

    if not ops.mc is None:
        outfile.cd()
        ttbar_4tag = mc_file.Get("FourTag_Signal/mHH_l").Clone()
        ttbar_4tag.Scale(tt_scale[0])
        ttbar_4tag.SetName("ttbar_hh")
        ttbar_4tag.SetTitle("ttbar_hh")
        ttbar_4tag.Write()

        outfile_3b.cd()
        ttbar_3tag = mc_file.Get("ThreeTag_Signal/mHH_l").Clone()
        ttbar_3tag.Scale(tt_scale[1])
        ttbar_3tag.SetName("ttbar_hh")
        ttbar_3tag.SetTitle("ttbar_hh")
        ttbar_3tag.Write()


    if not ops.signal is None:
        signal_files = glob.glob(ops.signal + "/hist-*c10*.root")

        for file in signal_files:
            curr_file = ROOT.TFile(file, "READ")
            out_hist = curr_file.Get("FourTag_Signal/mHH_l")
            out_hist_3b = curr_file.Get("ThreeTag_Signal/mHH_l")
    
            str_pos = file.find("c10_M")
    
            if str_pos == -1:
                print "Couldn't parse mass of " + file
                continue

            substr = file[str_pos+5:]
            mass_str = substr.split(".")[0]
            print mass_str

            out_hist.SetName("g_hh_m" + mass_str)
            out_hist.SetTitle("g_hh_m" + mass_str)
            out_hist.Scale(0.333) # H->bb BR ^2

            out_hist_3b.SetName("g_hh_m" + mass_str)
            out_hist_3b.SetTitle("g_hh_m" + mass_str)
            out_hist_3b.Scale(0.333) # H->bb BR ^2

            outfile.cd()
            out_hist.Write()

            outfile_3b.cd()
            out_hist_3b.Write()

            curr_file.Close()

    
    outfile.Close()
    outfile_3b.Close()
            
    

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data")
    parser.add_argument("--signal")
    parser.add_argument("--mc")
    parser.add_argument("--zjets")
    parser.add_argument("--suffix")
    parser.add_argument("--output", default=CONF.inputpath)

    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

if __name__ == '__main__': 
    main()
