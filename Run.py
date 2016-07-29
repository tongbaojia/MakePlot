#Tony: this is designed to run over systmatics
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
    parser.add_argument("--Xhh",      action='store_true') #4times more time
    return parser.parse_args()

def main():
    start_time = time.time()
    global ops
    ops = options()

    #total 50 systematics
    bsyst = [
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

    print "total b syst: ", len(bsyst)
    inputtasks = []
    for i in range(1, len(bsyst)):
        inputtasks.append({"inputdir":"syst_b_" + str(i)})
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
    #for ttbar
    # inputtasks.append({"inputdir":"syst_tt_frag"})
    # inputtasks.append({"inputdir":"syst_tt_had"})
    # inputtasks.append({"inputdir":"syst_tt_ppcs"})
    # inputtasks.append({"inputdir":"syst_tt_mass_down"})
    # inputtasks.append({"inputdir":"syst_tt_mass_up"})
    # inputtasks.append({"inputdir":"syst_tt_rad_down"})
    # inputtasks.append({"inputdir":"syst_tt_rad_up"})

    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool  = mp.Pool(npool)
    pool.map(syst_pipeline, inputtasks)
    # for i in inputtasks:
    #     syst_pipeline(i)
    #syst_pipeline(inputtasks[49])
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

    #for ttbar, also need to link the MCs.
    if "syst_tt_" in t:
        for i, mass in enumerate(CONF.mass_lst):
            #print "creating links of signal samples", "signal_G_hh_c10_M" + str(mass)
            #this is a really bad practice and temp fix now! need to watch this very carfully...
            ori_link = CONF.inputpath + "b77/" + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root"
            #ori_link = inputpath.replace("TEST", "DS1_cb") + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root"
            dst_link = inputpath + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root"
            helpers.checkpath(inputpath + "signal_G_hh_c10_M" + str(mass))
            #print ori_link, dst_link
            if os.path.islink(dst_link):
                os.unlink(dst_link)
            os.symlink(ori_link, dst_link)

            #link the 2HDM samples if necessary
            if (ops.Xhh):
                ori_link = CONF.inputpath + "b77/" + "signal_X_hh_M" + str(mass) + "/hist-MiniNTuple.root"
                dst_link = inputpath + "signal_X_hh_M" + str(mass) + "/hist-MiniNTuple.root"
                helpers.checkpath(inputpath + "signal_X_hh_M" + str(mass))
                if os.path.islink(dst_link):
                    os.unlink(dst_link)
                print "linking: ", dst_link
                os.symlink(ori_link, dst_link)


    #start running programs
    os.system("python get_count.py --dosyst True " + " --inputdir " + t + (" --Xhh " if ops.Xhh else ""))
    os.system("python dump_hists.py " + " --inputdir " + t + (" --Xhh " if ops.Xhh else ""))


if __name__ == '__main__': 
    main()
