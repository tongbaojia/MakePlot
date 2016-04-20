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

from math import sqrt

treename  = "XhhMiniNtuple"

ROOT.gROOT.SetBatch()
def main():

    ops = options()

    if ops.data is None:
        fatal("Please specify the histogram files with --data and --mc")

    if ops.mc is None:
        print "WARNING: running without MC subtraction"


    data_file = ROOT.TFile(ops.data, "READ")

    sideband_2tag = data_file.Get("TwoTag_Sideband/mHH")
    sideband_4tag = data_file.Get("FourTag_Sideband/mHH")

    if not ops.mc is None:
        mc_file = ROOT.TFile(ops.mc, "READ")
        sideband_2tag = sideband_2tag.Add(mc_file.Get("TwoTag_Sideband/mHH", -1.0))
        sideband_4tag = sideband_4tag.Add(mc_file.Get("FourTag_Sideband/mHH", -1.0))

    error_2tag = ROOT.Double()
    error_4tag = ROOT.Double()
    n_events_2tag = sideband_2tag.IntegralAndError(0, sideband_2tag.GetXaxis().GetNbins()+1, error_2tag)
    n_events_4tag = sideband_4tag.IntegralAndError(0, sideband_4tag.GetXaxis().GetNbins()+1, error_4tag)

    print "# of events, 2tag sideband: %f +- %f" % (n_events_2tag, error_2tag)
    print "# of events, 4tag sideband: %f +- %f" % (n_events_4tag, error_4tag)
    mu_qcd = n_events_4tag / n_events_2tag
    mu_err = mu_qcd*sqrt((error_2tag/n_events_2tag)**2 + (error_4tag/n_events_4tag)**2)
    print "mu_qcd: %f +- %f" % (mu_qcd, mu_err)

    control_2tag = data_file.Get("TwoTag_Control/mHH")
    control_4tag = data_file.Get("FourTag_Control/mHH")
    print "# of events, 2tag control: %f" % control_2tag.Integral(0, control_2tag.GetXaxis().GetNbins()+1)
    print "# of events, 4tag control: %f" % control_4tag.Integral(0, control_4tag.GetXaxis().GetNbins()+1)

    signal_2tag = data_file.Get("TwoTag_Signal/mHH")
    print "# of events, 2tag signal: %f" % signal_2tag.Integral(0, signal_2tag.GetXaxis().GetNbins()+1)
    

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data")
    parser.add_argument("--mc")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

if __name__ == '__main__': 
    main()
