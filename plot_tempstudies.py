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
import numpy as np

ROOT.gROOT.SetBatch(True)
from ROOT import *    
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
SetAtlasStyle()


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
    return parser.parse_args()

def main():

    ops = options()
    inputdir = ops.inputdir
    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" + "Plot/Other/"

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    ##starndard plots
    ##for 1D shape comparison
    for histname in ["mHH_l"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_split_Incl" + "/" + histname, "leg":"2bs SB"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Incl" + "/" + histname, "leg":"2bs prediction"},
            ], keyword=histname, norm=True, Xrange=[500, 3500], Rebin=10, Logy=1, prename="2bs_")
    # for histname in ["leadHCand_Mass", "sublHCand_Mass"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_split_Incl" + "/" + histname, "leg":"2bs SB"},
    #         ], keyword=histname, norm=True, prename="2bs_")
    for histname in ["leadHCand_Pt_m", "sublHCand_Pt_m"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_split_Incl" + "/" + histname, "leg":"2bs SB"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Incl" + "/" + histname, "leg":"2bs prediction"},
            ], keyword=histname, Xrange=[500, 1200], norm=True, prename="2bs_")
    for histname in ["leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_split_Incl" + "/" + histname, "leg":"2bs SB"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"NoTag_2Trk_split_Incl" + "/" + histname, "leg":"2bs prediction"},
            ], keyword=histname, Xrange=[0, 1000], norm=True, prename="2bs_", Rebin=4, Logy=1)
    # for histname in ["leadHCand_trk_dr", "sublHCand_trk_dr"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_split_Incl" + "/" + histname, "leg":"2bs SB"},
    #         ], keyword=histname, Xrange=[0, 1], norm=True, prename="2bs_")

    for histname in ["mHH_l"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_lead_Incl" + "/" + histname, "leg":"3b SB, 2tag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_subl_Incl" + "/" + histname, "leg":"3b SB, 2tag on subl"},
            ], keyword=histname, norm=True, Xrange=[500, 3500], Rebin=10, Logy=1, prename="3b_")
    # for histname in ["leadHCand_Mass", "sublHCand_Mass"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_lead_Incl" + "/" + histname, "leg":"3b SB, 2tag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_subl_Incl" + "/" + histname, "leg":"3b SB, 2tag on subl"},
    #         ], keyword=histname, norm=True, prename="3b_")
    for histname in ["leadHCand_Pt_m", "sublHCand_Pt_m"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_lead_Incl" + "/" + histname, "leg":"3b SB, 2tag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_subl_Incl" + "/" + histname, "leg":"3b SB, 2tag on subl"},
            ], keyword=histname, Xrange=[500, 1200], norm=True, prename="3b_")
    for histname in ["leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_lead_Incl" + "/" + histname, "leg":"3b SB, 2tag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_subl_Incl" + "/" + histname, "leg":"3b SB, 2tag on subl"},
            ], keyword=histname, Xrange=[0, 500], norm=True, prename="3b_")
    # for histname in ["leadHCand_trk_dr", "sublHCand_trk_dr"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_lead_Incl" + "/" + histname, "leg":"3b SB, 2tag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"ThreeTag_subl_Incl" + "/" + histname, "leg":"3b SB, 2tag on subl"},
    #         ], keyword=histname, Xrange=[0, 1], norm=True, prename="3b_")

    for histname in ["mHH_l"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"FourTag_Incl" + "/" + histname, "leg":"4b incl"},
            ], keyword=histname, norm=True, Xrange=[500, 3500], Rebin=10, Logy=1, prename="4b_")
    # for histname in ["leadHCand_Mass", "sublHCand_Mass"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"FourTag_Incl" + "/" + histname, "leg":"4b incl"},
    #         ], keyword=histname, norm=True, prename="4b_")
    for histname in ["leadHCand_Pt_m", "sublHCand_Pt_m"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"FourTag_Incl" + "/" + histname, "leg":"4b incl"},
            ], keyword=histname, Xrange=[500, 1200], norm=True, prename="4b_")
    for histname in ["leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt"]:
        DrawMulti1Dcomparison([
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
            {"file":"data_test/hist-MiniNTuple.root", "path":"FourTag_Incl" + "/" + histname, "leg":"4b incl"},
            ], keyword=histname, Xrange=[0, 500], norm=True, prename="4b_")
    # for histname in ["leadHCand_trk_dr", "sublHCand_trk_dr"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         {"file":"data_test/hist-MiniNTuple.root", "path":"FourTag_Incl" + "/" + histname, "leg":"4b incl"},
    #         ], keyword=histname, Xrange=[0, 1], norm=True, prename="4b_")
    
    ##others
    # DrawMulti1Dcomparison([
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + "leadHCand_trk_dr", "leg":"lead: OneTag on lead"},
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + "leadHCand_trk_dr", "leg":"lead: OneTag on subl"},
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + "sublHCand_trk_dr", "leg":"subl: OneTag on lead"},
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + "sublHCand_trk_dr", "leg":"subl: OneTag on subl"},
    #     ], keyword=histname, Xrange=[0, 1.5], norm=True, prename="OneTag")
    # DrawMulti1Dcomparison([
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + "leadHCand_trk_dr", "leg":"lead: TwoTag on lead"},
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + "leadHCand_trk_dr", "leg":"lead: TwoTag on subl"},
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + "sublHCand_trk_dr", "leg":"subl: TwoTag on lead"},
    #     {"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + "sublHCand_trk_dr", "leg":"subl: TwoTag on subl"},
    #     ], keyword=histname, Xrange=[0, 1.5], norm=True, prename="TwoTag")


    # for histname in ["mHH_l"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         ], keyword=histname, norm=True, Xrange=[500, 3500], Rebin=10, Logy=1, prename="qcd_")
    # for histname in ["leadHCand_Mass", "sublHCand_Mass"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         ], keyword=histname, norm=True, prename="qcd_")
    # for histname in ["leadHCand_Pt_m", "sublHCand_Pt_m"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         ], keyword=histname, Xrange=[500, 1200], norm=True, prename="qcd_")
    # for histname in ["leadHCand_trks_Pt", "sublHCand_trks_Pt"]:
    #     DrawMulti1Dcomparison([
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag on subl"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag on lead"},
    #         {"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag on subl"},
    #         ], keyword=histname, Xrange=[0, 500], norm=True, prename="qcd_")
    ##for 2D shape comparison
    # for histname in ["mH0H1"]:
    #     Draw2Dcomparison({"base":{"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag Lead"},
    #                       "comp":{"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag Subl"}}, RebinX=2, RebinY=2)
    #     Draw2Dcomparison({"base":{"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag Lead"},
    #                       "comp":{"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag Subl"}}, RebinX=2, RebinY=2)
    # for histname in ["dRH0H1"]:
    #     Draw2Dcomparison({"base":{"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag Lead"},
    #                       "comp":{"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag Subl"}}, RebinX=2, RebinY=2)
    #     Draw2Dcomparison({"base":{"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag Lead"},
    #                       "comp":{"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag Subl"}}, RebinX=2, RebinY=2)
    # for histname in ["trkfracH0H1"]:
    #     Draw2Dcomparison({"base":{"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag Lead"},
    #                       "comp":{"file":"data_test/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag Subl"}}, RebinX=1, RebinY=1)
    #     Draw2Dcomparison({"base":{"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag Lead"},
    #                       "comp":{"file":"data_test/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag Subl"}}, RebinX=1, RebinY=1)
    # for histname in ["mH0H1"]:
    #     Draw2Dcomparison({"base":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag Lead"},
    #                       "comp":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag Subl"}}, RebinX=2, RebinY=2,prename="qcd_",  SubTop=False)
    #     Draw2Dcomparison({"base":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag Lead"},
    #                       "comp":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag Subl"}}, RebinX=2, RebinY=2,prename="qcd_",  SubTop=False)
    # for histname in ["dRH0H1"]:
    #     Draw2Dcomparison({"base":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag Lead"},
    #                       "comp":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag Subl"}}, RebinX=2, RebinY=2,prename="qcd_",  SubTop=False)
    #     Draw2Dcomparison({"base":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag Lead"},
    #                       "comp":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag Subl"}}, RebinX=2, RebinY=2,prename="qcd_",  SubTop=False)
    # for histname in ["trkfracH0H1"]:
    #     Draw2Dcomparison({"base":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_lead_Incl" + "/" + histname, "leg":"OneTag Lead"},
    #                       "comp":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"OneTag_subl_Incl" + "/" + histname, "leg":"OneTag Subl"}}, RebinX=1, RebinY=1,prename="qcd_",  SubTop=False)
    #     Draw2Dcomparison({"base":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_lead_Incl" + "/" + histname, "leg":"TwoTag Lead"},
    #                       "comp":{"file":"signal_QCD/hist-MiniNTuple.root", "path":"TwoTag_subl_Incl" + "/" + histname, "leg":"TwoTag Subl"}}, RebinX=1, RebinY=1,prename="qcd_",  SubTop=False)
    

def DrawMulti1Dcomparison(inputlst, keyword="", prename="", Xrange=[0, 0], Yrange=[0, 0], norm=True, Logy=0, Rebin=1):
    #print inputdir
    tempname = "directcompare" + "_" + keyword + ("" if Logy == 0 else "_" + str(Logy))
    canv = ROOT.TCanvas(tempname, tempname, 800, 800)
    # two pad
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


    #top pad
    canv.cd()
    pad0.SetLogy(Logy)
    pad0.Draw()
    pad0.cd()

    xleg, yleg = 0.58, 0.73
    legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.2)
    counter = 0
    maxbincontent = (0.05 if (norm) else 10)
    minbincontent = (0.001 if (norm) else 0.001)
    temphst_lst = []
    graph_lst   = []
    tempratio_lst = []

    for i, dic in enumerate(inputlst):
        refroot = ROOT.TFile.Open(inputpath + dic["file"])
        temphst_lst.append(refroot.Get(dic["path"]).Clone())
        tempratio_lst.append(refroot.Get(dic["path"]).Clone(dic["path"] + "_ratio"))
        temphst_lst[i].SetDirectory(0) #otherwise the hist lives in the current open file
        tempratio_lst[i].SetDirectory(0) #otherwise the hist lives in the current open file

        #print dic["file"], dic["path"], temphst_lst[i].Integral()
        if Rebin != 1:
            temphst_lst[i].Rebin(Rebin)
            tempratio_lst[i].Rebin(Rebin)

        if norm:
            NormFactor = 1/temphst_lst[i].Integral(0, temphst_lst[i].GetXaxis().GetNbins()+1)
            temphst_lst[i].Scale(NormFactor)

        for j in range(1, temphst_lst[0].GetNbinsX()+1):
            if norm:
                try:
                    temphst_lst[i].SetBinError(j, tempratio_lst[i].GetBinError(j)*(NormFactor))
                    #print tempratio_lst[i].GetBinError(j), NormFactor
                except ZeroDivisionError:
                    pass
            try:
                tempratio_lst[i].SetBinContent(j, temphst_lst[i].GetBinContent(j) / temphst_lst[0].GetBinContent(j))
                tempratio_lst[i].SetBinError(j, helpers.ratioerror(\
                    temphst_lst[i].GetBinContent(j), temphst_lst[0].GetBinContent(j), \
                    temphst_lst[i].GetBinError(j), temphst_lst[0].GetBinError(j)))
            except ZeroDivisionError:
                pass
                #print "Divide by zero! Check bin content in", canv.GetName()



        maxbincontent = max(maxbincontent, temphst_lst[i].GetMaximum())
        minbincontent = max(minbincontent, temphst_lst[i].GetMinimum())
        #graph_lst.append(helpers.TH1toTAsym(temphst_lst[i], efficiency=False))
        temphst_lst[i].SetLineColor(1 if i == 0 else CONF.clr_lst[i])
        #temphst_lst[i].SetLineStyle(1 + i)
        temphst_lst[i].SetMarkerStyle(20 + i)
        temphst_lst[i].SetMarkerColor(1 if i == 0 else CONF.clr_lst[i])
        temphst_lst[i].SetMarkerSize(1)
        temphst_lst[i].SetMaximum(maxbincontent * (1.5 if (Logy == 0 or norm) else 150))
        temphst_lst[i].SetMinimum(0.001 if Logy == 0 else minbincontent)
        if Xrange != [0, 0]:
            temphst_lst[i].GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
        legend.AddEntry(temphst_lst[i], dic["leg"], "pl")
        temphst_lst[i].Draw("EP" if i==0 else "hist same")
        refroot.Close()
    
    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw watermarks
    xatlas, yatlas = 0.4, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "Simulations")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    info  = ROOT.TLatex(xatlas, yatlas-0.06, keyword.replace("data_est_", "").replace("_mHH_l", "").replace("_", " "))
    watermarks = [atlas, info]
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
    for i, dic in enumerate(inputlst):
        tempratio_lst[i].SetLineColor(1 if i == 0 else CONF.clr_lst[i])
        #tempratio_lst[i].SetLineStyle(1 + i)
        tempratio_lst[i].SetMarkerStyle(20 + i)
        tempratio_lst[i].SetMarkerColor(1 if i == 0 else CONF.clr_lst[i])
        tempratio_lst[i].SetMarkerSize(1)
        tempratio_lst[i].GetYaxis().SetTitleFont(43)
        tempratio_lst[i].GetYaxis().SetTitleSize(28)
        tempratio_lst[i].GetYaxis().SetLabelFont(43)
        tempratio_lst[i].GetYaxis().SetLabelSize(28)
        tempratio_lst[i].GetYaxis().SetTitle("ratio to ref")
        tempratio_lst[i].GetYaxis().SetRangeUser(0.6, 1.5) #set range for ratio plot
        tempratio_lst[i].GetYaxis().SetNdivisions(405)
        tempratio_lst[i].GetXaxis().SetTitleFont(43)
        tempratio_lst[i].GetXaxis().SetTitleOffset(3.5)
        tempratio_lst[i].GetXaxis().SetTitleSize(28)
        tempratio_lst[i].GetXaxis().SetLabelFont(43)
        tempratio_lst[i].GetXaxis().SetLabelSize(28)
        if Xrange != [0, 0]:
            tempratio_lst[i].GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
        if i > 0:
            tempratio_lst[i].Draw("ep" if i == 1 else "ep same")
    # draw the ratio 1 line
    line = ROOT.TLine(Xrange[0], 1.0, Xrange[1], 1.0)
    line.SetLineStyle(1)
    line.Draw()

    #save and clean up
    canv.SaveAs(outputpath + prename + canv.GetName() + ".pdf")
    pad0.Close()
    pad1.Close()
    canv.Close()
    del(tempratio_lst)
    del(temphst_lst)
    del(graph_lst)

def Draw2Dcomparison(inputlst, keyword="_", prename="comp", Xrange=[0, 0], Yrange=[0, 0], RebinX=1, RebinY=1, SubTop=True):
    # functions for the different regions

    #print inputdir
    inputroot_base = ROOT.TFile.Open(inputpath + inputlst["base"]["file"])
    if inputlst["base"]["file"] != inputlst["comp"]["file"]:
        inputroot_comp = ROOT.TFile.Open(inputpath + inputlst["comp"]["file"])
    else:
        inputroot_comp = inputroot_base
    #inputroot.cd(inputdir)
    temp_hist_base = inputroot_base.Get(inputlst["base"]["path"]).Clone()
    temp_hist_comp = inputroot_comp.Get(inputlst["comp"]["path"]).Clone()
    temp_hist_base.SetDirectory(0)
    temp_hist_comp.SetDirectory(0)
    inputroot_top_base = ROOT.TFile.Open(inputpath + inputlst["base"]["file"].replace("data", "ttbar_comb"))
    inputroot_top_comp = inputroot_top_base
    if SubTop:
        if inputlst["base"]["file"] != inputlst["comp"]["file"]:
            inputroot_top_comp = ROOT.TFile.Open(inputpath + inputlst["comp"]["file"].replace("data", "ttbar_comb"))
        else:
            inputroot_top_comp = inputroot_top_base
        temp_hist_top_base = inputroot_top_base.Get(inputlst["base"]["path"]).Clone()
        temp_hist_top_comp = inputroot_top_comp.Get(inputlst["comp"]["path"]).Clone()
        temp_hist_top_base.SetDirectory(0)
        temp_hist_top_comp.SetDirectory(0)
        temp_hist_base.Add(temp_hist_top_base, -1)
        temp_hist_comp.Add(temp_hist_top_comp, -1)

    #rebin
    temp_hist_base.Rebin2D(RebinX, RebinY)
    temp_hist_comp.Rebin2D(RebinX, RebinY)
    #normalize
    temp_hist_comp.Scale(temp_hist_base.Integral()/temp_hist_comp.Integral())
    #sub/ratio
    temp_hist_base.Add(temp_hist_comp, -1)#substract original top
    #temp_hist_base.Divide(temp_hist_comp)
    #load fitted muqcd information
    #inputtex = CONF.inputpath + CONF.workdir + "/Plot/Tables/normfit.tex"
    #f1 = open(inputtex, 'r')

    ##check the maximum bin information
    ##proceed
    canv = ROOT.TCanvas(inputlst["base"]["path"].replace("/", "_"), temp_hist_base.GetTitle(), 1000, 800)
    canv.SetLeftMargin(0.17)
    canv.SetRightMargin(0.23)
    ##set plot range
    if Xrange != [0, 0]:
        temp_hist_base.GetXaxis().SetRangeUser(Xrange[0], Xrange[1])
    if Yrange != [0, 0]:
        temp_hist_base.GetYaxis().SetRangeUser(Yrange[0], Yrange[1])
        temp_hist_base.GetYaxis().SetTitleOffset(1.5)

    ##blind SR and CR
    # Set Axis Labels
    #temp_hist_base.GetXaxis().SetTitle("m_{J}^{lead} [GeV]")
    #temp_hist_base.GetYaxis().SetTitle("m_{J}^{subl} [GeV]")
    temp_hist_base.GetZaxis().SetTitle(inputlst["base"]["leg"] + "-" + inputlst["comp"]["leg"] + "(norm)")
    temp_hist_base.GetZaxis().SetTitleOffset(1.8)
    #temp_hist_base = max(temp_hist_base.GetMaximum(), abs(temp_hist_base.GetMinimum()))
    #temp_hist_base.GetZaxis().SetRangeUser(-temp_hist_max, temp_hist_max)
    # change divisions
    temp_hist_base.GetXaxis().SetNdivisions(505)
    temp_hist_base.GetYaxis().SetNdivisions(505)
    temp_hist_base.GetZaxis().SetNdivisions(505)

    ##finally draw
    temp_hist_base.Draw("colz")
    # fill box
    # Draw Watermarks
    xatlas, yatlas = 0.37, 0.87
    ATLASLabel(xatlas, yatlas, CONF.StatusLabel)
    myText(xatlas, yatlas-0.05, 1, "#sqrt{s}=13 TeV, " + str(CONF.totlumi) + " fb^{-1}", CONF.paperlegsize)
    myText(xatlas, yatlas-0.1, 1, "Boosted", CONF.paperlegsize)


    canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".pdf")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".png")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".eps")
    #canv.SaveAs(outputpath + prename + "_" +  canv.GetName() + ".C")

    #shut it down
    canv.Close()
    inputroot_base.Close()
    if(inputroot_comp):
        inputroot_comp.Close()
    if(inputroot_top_base):
        inputroot_top_base.Close()
    if(inputroot_top_comp):
        inputroot_top_comp.Close()



if __name__ == "__main__":
    main()
