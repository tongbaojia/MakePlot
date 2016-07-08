import ROOT, helpers
import config as CONF
import argparse, copy, glob, os, sys, time
try:
    import simplejson as json                 
except ImportError:
    import json        
from Xhh4bUtils.BkgFit.BackgroundFit_Ultimate import BackgroundFit
import Xhh4bUtils.BkgFit.smoothfit as smoothfit
#for parallel processing!
import multiprocessing as mp


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

def main():
    start_time = time.time()
    ops = options()

    #total 50 systematics
    bsyst = [
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
        "FT_EFF_Eigen_Light_0__1down",
        "FT_EFF_Eigen_Light_0__1up",
        "FT_EFF_Eigen_Light_1__1down",
        "FT_EFF_Eigen_Light_1__1up",
        "FT_EFF_Eigen_Light_10__1down",
        "FT_EFF_Eigen_Light_10__1up",
        "FT_EFF_Eigen_Light_11__1down",
        "FT_EFF_Eigen_Light_11__1up",
        "FT_EFF_Eigen_Light_12__1down",
        "FT_EFF_Eigen_Light_12__1up",
        "FT_EFF_Eigen_Light_13__1down",
        "FT_EFF_Eigen_Light_13__1up",
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
        "FT_EFF_extrapolation__1down",
        "FT_EFF_extrapolation__1up",
        "FT_EFF_extrapolation_from_charm__1down",
        "FT_EFF_extrapolation_from_charm__1up",
    ]

    print len(bsyst)
    inputtasks = []
    inputtasks.append({"inputdir":"syst_JET_JER"})
    inputtasks.append({"inputdir":"syst_JET_JMR"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Baseline_All__1down"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Baseline_All__1up"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Modelling_All__1down"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Modelling_All__1up"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_TotalStat_All__1down"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_TotalStat_All__1up"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Tracking_All__1down"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Tracking_All__1up"})
    for i in range(0, 50):
        inputtasks.append({"inputdir":"syst_b_" + str(i)})

    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool  = mp.Pool(npool)
    pool.map(syst_pipeline, inputtasks)
    #for i in inputtasks:
        #syst_pipeline(i)
    print("--- %s seconds ---" % (time.time() - start_time))

def syst_pipeline(config):
    t = config["inputdir"]
    print "the directory is: ", t
    inputpath = CONF.inputpath + t + "/"
    #check if for syst, the data file is there
    helpers.checkpath(inputpath + "data_test")
    #this is a really bad practice and temp fix now! need to watch this very carfully...
    ori_link = CONF.inputpath + "b77/data_test/hist-MiniNTuple.root"
    dst_link = inputpath + "data_test/hist-MiniNTuple.root"
    #print ori_link, dst_link
    if os.path.islink(dst_link):
        os.unlink(dst_link)
    os.symlink(ori_link, dst_link)

    #start running programs
    #os.system("python get_count.py --dosyst True --full False " + " --inputdir " + t)
    #os.system("python dump_hists.py " + " --inputdir " + t)


if __name__ == '__main__': 
    main()