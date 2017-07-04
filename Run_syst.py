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
    parser.add_argument("--inputdir", default=CONF.workdir + "_" + CONF.reweightdir)
    parser.add_argument("--Xhh",      default=CONF.doallsig) #4times more time, be aware
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
        "FT_EFF_Eigen_Light_14__1down",
        "FT_EFF_Eigen_Light_14__1up",
        "FT_EFF_Eigen_Light_15__1down",
        "FT_EFF_Eigen_Light_15__1up",
        "FT_EFF_Eigen_Light_16__1down",
        "FT_EFF_Eigen_Light_16__1up",
        "FT_EFF_Eigen_Light_17__1down",
        "FT_EFF_Eigen_Light_17__1up",
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

    print "total b syst: ", len(bsyst) ##the total is 58 now...
    inputtasks = []
    for i in range(1, len(bsyst)):
        inputtasks.append({"inputdir":"syst_b_" + str(i)})
    inputtasks.append({"inputdir":"syst_JET_JER"}) #
    inputtasks.append({"inputdir":"syst_JET_JMR"}) #
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Baseline_All__1down"}) #
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Baseline_All__1up"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Modelling_All__1down"}) #
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Modelling_All__1up"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_TotalStat_All__1down"}) #
    inputtasks.append({"inputdir":"syst_JET_Rtrk_TotalStat_All__1up"})
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Tracking_All__1down"}) #
    inputtasks.append({"inputdir":"syst_JET_Rtrk_Tracking_All__1up"})
    ##for ttbar MC variations
    ##see: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/TopSystematics2015
    inputtasks.append({"inputdir":"syst_tt_frag"}) #
    inputtasks.append({"inputdir":"syst_tt_had"})
    inputtasks.append({"inputdir":"syst_tt_ppcs"}) #
    inputtasks.append({"inputdir":"syst_tt_mass_down"})
    inputtasks.append({"inputdir":"syst_tt_mass_up"}) #
    inputtasks.append({"inputdir":"syst_tt_rad_down"})
    inputtasks.append({"inputdir":"syst_tt_rad_up"}) #

    ### for parallel computing
    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool  = mp.Pool(npool)
    pool.map(syst_pipeline, inputtasks)

    # for i in inputtasks:
    #     syst_pipeline(i)
    #syst_pipeline({"inputdir":"syst_b_0_copy"})
    #syst_pipeline({"inputdir":"syst_JET_JER_copy"})
    #syst_pipeline({"inputdir":"Moriond_ZZ"}) ##see if this helps ZZ...

    print("--- %s seconds ---" % (time.time() - start_time))

def syst_pipeline(config):
    t = config["inputdir"]
    print "the directory is: ", t
    inputpath = CONF.inputpath + t + "/"

    #check if for syst, the data file is there
    helpers.checkpath(inputpath + "data_test")
    #this is a really bad practice and temp fix now! need to watch this very carfully...
    ori_link = CONF.inputpath + ops.inputdir + "/data_test/hist-MiniNTuple.root"
    dst_link = inputpath + "data_test/hist-MiniNTuple.root"
    #print ori_link, dst_link
    if os.path.islink(dst_link):
        os.unlink(dst_link)
    os.symlink(ori_link, dst_link)

    #for ttbar, also need to link the MCs.
    if "syst_tt_" in t:
        ##copy zjets as well
        helpers.checkpath(inputpath + "zjets_test")
        ori_link = CONF.inputpath + ops.inputdir + "/zjets_test/hist-MiniNTuple.root"
        dst_link = inputpath + "zjets_test/hist-MiniNTuple.root"
        if os.path.islink(dst_link):
            os.unlink(dst_link)
        os.symlink(ori_link, dst_link)
        ##copy other MC signals
        sigMClist = ["signal_G_hh_c10_M"]
        if (ops.Xhh):
            sigMClist = ["signal_G_hh_c10_M", "signal_G_hh_c20_M", "signal_X_hh_M"]
        for sigMC in sigMClist:
            for i, mass in enumerate(CONF.mass_lst):
                if mass == 2750 and sigMC == "signal_G_hh_c20_M": ##no 2750 c20 sample
                    continue
                #print "creating links of signal samples", "signal_G_hh_c10_M" + str(mass)
                #this is a really bad practice and temp fix now! need to watch this very carfully...
                ori_link = CONF.inputpath + ops.inputdir + "/" + sigMC + str(mass) + "/hist-MiniNTuple.root"
                #ori_link = inputpath.replace("TEST", "DS1_cb") + "signal_G_hh_c10_M" + str(mass) + "/hist-MiniNTuple.root"
                dst_link = inputpath + sigMC + str(mass) + "/hist-MiniNTuple.root"
                helpers.checkpath(inputpath + sigMC + str(mass))
                #print ori_link, dst_link
                if os.path.islink(dst_link):
                    os.unlink(dst_link)
                os.symlink(ori_link, dst_link)

    #start running programs
    #print (inputpath)
    os.system("rm " + inputpath + "sum_" + t + ".root")
    os.system("rm -r " + inputpath + "Limitinput")
    # print "done clearing!"
    # ###this is correcting the 3b/4b normalization to 2b. Should only be applied when ttbar stats makes no sense!
    # if "syst_tt_" in t or "JET_JER" in t or "JET_JMR" in t: ##only for ttbar variations for now
    #      Tophack(inputpath=inputpath)
    # #Tophack(inputpath=inputpath)
    os.system("python get_count.py --dosyst " + " --inputdir " + t)
    ##ttbar has weird smoothing behaviour, use ttbar + qcd for final distribution now
    os.system("python dump_hists.py " + " --inputdir " + t + (" --dosyst" if "syst_tt_" in t else ""))

def Tophack(inputpath):
    '''If use this, will copy the ttbar_comb_test to ttbar_comb_origin,
    replace the ttbar_comb_test hist-MiniNtuple.root with itself, except in 
    3b and 4b directories, histograms are scaled to the original Moriond yield 
    times syst 2bs/original 2bs ratio.
    '''
    ##first rename the file; don't over do it though
    if os.path.isfile(inputpath + "ttbar_comb_test/hist-MiniNTuple_org.root"):
        pass
    else:
        os.system("mv " + inputpath + "ttbar_comb_test/hist-MiniNTuple.root " + inputpath + "ttbar_comb_test/hist-MiniNTuple_org.root ")
    refroot = ROOT.TFile.Open(CONF.inputpath + "Moriond/" + "ttbar_comb_test/hist-MiniNTuple.root", "read")
    orgroot = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist-MiniNTuple_org.root", "read")
    outroot = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist-MiniNTuple.root", "recreate")

    scaledic = {}
    for tag in ["FourTag", "ThreeTag"]:
        for region in ["Sideband", "Control", "Signal", "Incl"]:
            dirname = tag + "_" + region
            dir2bname = "TwoTag_split" + "_" + region
            #print refroot.Get(dirname + "/mHH_l").Integral(), refroot.Get(dir2bname + "/mHH_l").Integral()
            scaledic[dirname] = refroot.Get(dirname + "/mHH_l").Integral()/ refroot.Get(dir2bname + "/mHH_l").Integral()
    ##copy the file
    CopyDir(orgroot, outroot, scaledic)
    
    ##finish
    refroot.Close()
    orgroot.Close()
    outroot.Close()
    print "DONE!"

def CopyDir(inputdir, outputdir, scaledic={}):
    '''recursive copying code: copy all the TH1s'''
    for key in inputdir.GetListOfKeys():
        kname = key.GetName()
        temp_item = inputdir.Get(kname)
        temp_name = temp_item.GetName()
        if temp_item.InheritsFrom("TH1"):
            outputdir.cd()
            if "FourTag" in outputdir.GetName() or "ThreeTag" in outputdir.GetName():
                #print temp_name
                #print "try to scale:", outputdir.GetName(), scaledic[outputdir.GetName()]
                #print "before scale:", temp_item.Integral()
                copy_item = temp_item.Clone() ##clone, otherwise have memory issue
                try:
                    copy_item.Scale(scaledic[outputdir.GetName()])
                except KeyError:
                    pass
                #print "after scale:", copy_item.Integral()
                copy_item.Write()
            else:
                temp_item.Write()
        elif temp_item.InheritsFrom("TDirectory"):
            outputdir.mkdir(temp_name)
            if "FourTag" in temp_name or "ThreeTag" in temp_name:
                dir2b = temp_name.replace("FourTag", "TwoTag_split").replace("ThreeTag", "TwoTag_split")
                #print temp_item, dir2b
                try:
                    CopyDir(inputdir.Get(dir2b), outputdir.Get(temp_name), scaledic)
                except AttributeError:
                    CopyDir(temp_item, outputdir.Get(temp_name))
            else:
                CopyDir(temp_item, outputdir.Get(temp_name))
    return


if __name__ == '__main__': 
    main()
