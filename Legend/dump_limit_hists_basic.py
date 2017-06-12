"""
qcd.py: a script to convert ntuples into a multijet ntuple.
$ python qcd.py --wp=70
"""
import argparse
import array
import copy
import os
import sys
import ROOT
import glob
from math import sqrt

treename  = "XhhMiniNtuple"

ROOT.gROOT.SetBatch()
def main():

    ops = options()

    if ops.data is None:
        fatal("Please specify the data histogram files with --data")

    if ops.signal is None:
        fatal("Please specify the signal histogram directory with --signal")

    suffix = ""

    if not ops.suffix is None:
        suffix = ops.suffix


    data_file = ROOT.TFile(ops.data, "READ")
    #signal_file = ROOT.TFile(ops.signal, "READ")

    sideband_2tag = data_file.Get("TwoTag_Sideband/mHH_l")
    sideband_3tag = data_file.Get("ThreeTag_Sideband/mHH_l")
    sideband_4tag = data_file.Get("FourTag_Sideband/mHH_l")

    mc_file = None
    if not ops.mc is None:
        mc_file = ROOT.TFile(ops.mc, "READ")
        sideband_2tag.Add(mc_file.Get("TwoTag_Sideband/mHH_l"), -1.0)
        sideband_3tag.Add(mc_file.Get("ThreeTag_Sideband/mHH_l"), -1.0)
        sideband_4tag.Add(mc_file.Get("FourTag_Sideband/mHH_l"), -1.0)

    error_2tag = ROOT.Double()
    error_3tag = ROOT.Double()
    error_4tag = ROOT.Double()
    n_events_2tag = sideband_2tag.IntegralAndError(0, sideband_2tag.GetXaxis().GetNbins()+1, error_2tag)
    n_events_3tag = sideband_3tag.IntegralAndError(0, sideband_3tag.GetXaxis().GetNbins()+1, error_3tag)
    n_events_4tag = sideband_4tag.IntegralAndError(0, sideband_4tag.GetXaxis().GetNbins()+1, error_4tag)

    print "# of events, 2tag sideband: %f +- %f" % (n_events_2tag, error_2tag)
    print "# of events, 3tag sideband: %f +- %f" % (n_events_3tag, error_3tag)
    print "# of events, 4tag sideband: %f +- %f" % (n_events_4tag, error_4tag)
    mu_qcd = n_events_4tag / n_events_2tag
    mu_qcd_3tag = n_events_3tag / n_events_2tag
    mu_err = mu_qcd*sqrt((error_2tag/n_events_2tag)**2 + (error_4tag/n_events_4tag)**2)
    mu_err_3tag = mu_qcd_3tag*sqrt((error_2tag/n_events_2tag)**2 + (error_3tag/n_events_3tag)**2)
    print "mu_qcd: %f +- %f" % (mu_qcd, mu_err)
    print "mu_qcd_3tag: %f +- %f" % (mu_qcd_3tag, mu_err_3tag)

    if not ops.mc is None:
        outfile_sub = ROOT.TFile("qcd_mc_sub_%s.root" % suffix, "RECREATE")

        keys = data_file.GetListOfKeys()

        for k in keys:
            c_dir = data_file.Get(k.GetName())
            if not "TwoTag" in k.GetName():
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
                curr_hist.Add(mc_file.Get(k.GetName()+"/"+h.GetName()), -1.0)
                curr_hist.Scale(mu_qcd)
                new_dir.cd()
                curr_hist.Write()

            outfile_sub.cd()
            new_dir.Write()

        outfile_sub.Close()
            

    signal_2tag = data_file.Get("TwoTag_Signal/mHH_l")
    print "# of events, 2tag signal: %f" % signal_2tag.Integral(0, signal_2tag.GetXaxis().GetNbins()+1)
    print signal_2tag
    bg_pred_4tag = signal_2tag.Clone()
    bg_pred_4tag.Scale(mu_qcd)

    bg_pred_3tag = signal_2tag.Clone()
    bg_pred_3tag.Scale(mu_qcd_3tag)

    outfile = ROOT.TFile("4b_region_boosted_%s.root" % suffix, "RECREATE")
    outfile_3b = ROOT.TFile("3b_region_boosted_%s.root" % suffix, "RECREATE")

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
        ttbar_4tag = mc_file.Get("FourTag_Signal/mHH_l")
        ttbar_4tag.SetName("ttbar_hh")
        ttbar_4tag.SetTitle("ttbar_hh")
        ttbar_4tag.Write()

        outfile_3b.cd()
        ttbar_3tag = mc_file.Get("ThreeTag_Signal/mHH_l")
        ttbar_3tag.SetName("ttbar_hh")
        ttbar_3tag.SetTitle("ttbar_hh")
        ttbar_3tag.Write()

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
            
    

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data")
    parser.add_argument("--signal")
    parser.add_argument("--mc")
    parser.add_argument("--suffix")

    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

if __name__ == '__main__': 
    main()
