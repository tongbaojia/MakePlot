import ROOT, rootlogon, helpers
import config as CONF
import argparse, copy, glob, os, sys, time
from Xhh4bUtils.BkgFit.BackgroundFit_Ultimate import BackgroundFit
import Xhh4bUtils.BkgFit.smoothfit as smoothfit
#for parallel processing!
import multiprocessing as mp
#end of import for now
ROOT.gROOT.SetBatch(True)
import getcount 

#set global variables
# cut_lst = ["2Trk_in1_NoTag", "2Trk_in1_OneTag", "2Trk_in1_TwoTag", \
#     "2Trk_NoTag", "2Trk_OneTag", "2Trk_TwoTag_split", \
#     "3Trk_NoTag", "3Trk_OneTag", "3Trk_TwoTag", "3Trk_TwoTag_split", "3Trk_ThreeTag", \
#     "4Trk_NoTag", "4Trk_OneTag", "4Trk_TwoTag", "4Trk_TwoTag_split", "4Trk_ThreeTag", "4Trk_FourTag",
#     "NoTag", "OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
# input are exclusive trkjets
dump_lst = ["NoTag", "OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"] #"ThreeTag_1loose", "TwoTag_split_1loose", "TwoTag_split_2loose"]
cut_lst = ["NoTag", "NoTag_2Trk_split", "NoTag_3Trk", "NoTag_4Trk", \
"OneTag_2Trk_split", "OneTag_3Trk", "OneTag_4Trk", "OneTag", \
"TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
#"ThreeTag_1loose", "TwoTag_split_1loose", "TwoTag_split_2loose"]
word_dict = {"FourTag":0, "ThreeTag":1, "TwoTag":3,"TwoTag_split":2, "OneTag":4, "NoTag":5}
numb_dict = {4:"FourTag", 3:"ThreeTag", 2:"TwoTag", 1:"OneTag", 0:"NoTag"}
region_lst = ["Sideband", "Control", "ZZ", "Signal"]
blind=True
#set list of dumping yields
yield_lst = ["qcd_est", "ttbar_est", "zjet", "data_est", "data", "RSG1_1000", "RSG1_2000", "RSG1_3000"]
yield_dic = {"qcd_est":"QCD Est", "ttbar_est":"$t\\bar{t}$ Est. ", "zjet":"$Z+jets$", "data_est":"Total Bkg Est",\
 "data":"Data", "RSG1_1000":"$c=1.0$,$m=1.0TeV$", "RSG1_2000":"$c=1.0$,$m=2.0TeV$", "RSG1_3000":"$c=1.0$,$m=3.0TeV$"}
yield_tag_lst = ["TwoTag_split", "ThreeTag", "FourTag"]
yield_region_lst = ["Sideband", "Control", "Signal"]

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    parser.add_argument("--full", default=False) #4times more time
    return parser.parse_args()

#do everything in one main?
def main():
    print "DONE"
### end

if __name__ == "__main__":
    main()
