import ROOT, rootlogon
import argparse
import copy
import glob
import helpers
import os
import sys
import time
from Xhh4bUtils.BkgFit.BackgroundFit_Ultimate import BackgroundFit
import Xhh4bUtils.BkgFit.smoothfit as smoothfit
#end of import for now

ROOT.gROOT.SetBatch(True)

#set global variables
#mass_lst = [1000, 2000, 3000]
mass_lst = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
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
#set list of plotting items
plt_m = "_mHH_l"
plt_lst = ["mHH_l", "hCandDr", "hCandDeta", "hCandDphi",\
"leadHCand_Pt_m", "leadHCand_Eta", "leadHCand_Phi", "leadHCand_Mass", "leadHCand_Mass_s", "leadHCand_trk_dr",\
"sublHCand_Pt_m", "sublHCand_Eta", "sublHCand_Phi", "sublHCand_Mass", "sublHCand_Mass_s", "sublHCand_trk_dr",\
"leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt",\
"leadHCand_ntrk", "sublHCand_ntrk", "leadHCand_trk_pt_diff_frac", "sublHCand_trk_pt_diff_frac"]

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

def main():
    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir
    background_model = 0
    fullchain = False

    # create output file
    inputpath = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/" + inputdir + "/"
    output = open(inputpath + "sum%s_%s.tex" % ("" if background_model==0 else str(background_model), inputdir), "w")
    outroot = ROOT.TFile.Open(inputpath + "sum%s_%s.root" % ("" if background_model==0 else str(background_model), inputdir), "recreate")

    print "input is", inputpath
    #print GetEvtCount(inputpath + "ttbar_comb_test.root")
    # Create the master dictionary for cutflows and plots
    masterinfo = {}
    # Get the dic of counts for split signal sample
    if fullchain:
        for mass in mass_lst:
            masterinfo["RSG1_" + str(mass)] = GetEvtCount(inputpath + "signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass, outroot, "RSG1_%i" % mass)
            #WriteEvtCount(masterinfo["RSG1_" + str(mass)], output, "RSG %i" % mass)

    #Get ttbar samples
    masterinfo["ttbar"] = GetEvtCount(inputpath + "ttbar_comb_test.root", outroot, "ttbar")
    #WriteEvtCount(masterinfo["ttbar"], output, "$t\\bar{t}$")
    # # Get Zjet samples
    masterinfo["zjet"] = GetEvtCount(inputpath + "zjets_test/hist-MiniNTuple.root", outroot, "zjet")
    #WriteEvtCount(masterinfo["zjet"], output, "z+jets")
    # # Get Signal samples; do not unblind now
    masterinfo["data"] = GetEvtCount(inputpath + "data_test/hist-MiniNTuple.root", outroot, "data")
    #WriteEvtCount(masterinfo["data"], output, "data")
    # # Get qcd from data 
    masterinfo["qcd"] = Getqcd(masterinfo, outroot)
    #WriteEvtCount(masterinfo["qcd"], output, "qcd")
    ####################################################
    #Do qcd background estimation from the fit
    print "Start Fit!"
    fitresult = BackgroundFit(inputpath + "data_test/hist-MiniNTuple.root", \
        inputpath + "ttbar_comb_test.root", inputpath + "zjets_test/hist-MiniNTuple.root", \
        distributionName = "leadHCand_Mass", whichFunc = "XhhBoosted", output = inputpath, NRebin=2, BKG_model=background_model)
    print "End of Fit!"
    #print fitresult
    masterinfo["qcd_est"] = fitestimation(masterinfo["qcd"], "qcd", fitresult, outroot, background_model)
    #WriteEvtCount(masterinfo["qcd_est"], output, "qcd Est")
    masterinfo["ttbar_est"] = fitestimation(masterinfo["ttbar"], "ttbar", fitresult, outroot, background_model)
    #(masterinfo["ttbar_est"], output, "top Est")
    # # #Do data estimation
    masterinfo["data_est"] = GetdataEst(masterinfo, outroot)
    #WriteEvtCount(masterinfo["data_est"], output, "data Est")
    # # #Do data estimation Difference comparision in control and ZZ region
    masterinfo["dataEstDiff"] = GetDiff(masterinfo["data_est"], masterinfo["data"])
    WriteEvtCount(masterinfo["dataEstDiff"], output, "Data Est Diff Percentage")
    # masterinfo["ttbarEstDiff"] = GetDiff(masterinfo["ttbar_est"], masterinfo["ttbar"])
    # WriteEvtCount(masterinfo["ttbarEstDiff"], output, "top Est Diff Percentage")
    
    #finish and quit
    outroot.Close()
    output.close()
    print("--- %s seconds ---" % (time.time() - start_time))

### returns the data estimate from qcd dictionary
def GetdataEst(inputdic, outroot, optionalqcd="qcd_est"):
    outroot.cd()
    data_est = {}
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            #scale all the qcd estimation plots
            for hst in plt_lst:
                if "nofit" in optionalqcd:
                    htemp_ttbar = outroot.Get("ttbar" + "_" + cut + "_" + region + "_" + hst).Clone()
                else:
                    htemp_ttbar = outroot.Get("ttbar_est" + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_zjet  = outroot.Get("zjet" + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_qcd   = outroot.Get(optionalqcd + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_qcd.SetName("data_est" + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Add(htemp_ttbar, 1)
                htemp_qcd.Add(htemp_zjet, 1)
                htemp_qcd.Write()
            if "nofit" in optionalqcd: 
                cutcounts[region] = inputdic[optionalqcd][cut][region] + inputdic["ttbar"][cut][region] + inputdic["zjet"][cut][region]
            else: 
                cutcounts[region] = inputdic[optionalqcd][cut][region] + inputdic["ttbar_est"][cut][region] + inputdic["zjet"][cut][region]
            cutcounts[region + plt_m] = outroot.Get("data_est" + "_" + cut + "_" + region + plt_m)

        data_est[cut] = cutcounts
    return data_est

### returns the estimation dictionary;
def fitestimation(inputdic, inputname, fitresult, outroot, background_model=0):
    #now do the real work
    print "***** estimation *****"
    #do a dump fill first
    outroot.cd()
    est = {}
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            #start the histogram as a dumb holder
            Ftransfer = 1.0
            #define where the qcd come from
            ref_cut = numb_dict[background_model]
            # if ("2Trk_in1" in cut):
            #     ref_cut = "2Trk_in1_NoTag"
            # elif ("2Trk" in cut):
            #     ref_cut = "2Trk_NoTag"
            # elif ("3Trk" in cut):
            #     ref_cut = "3Trk_NoTag"
            # elif ("4Trk" in cut):
            #     ref_cut = "4Trk_NoTag"
            if ("Trk" not in cut):
                ref_cut = numb_dict[background_model]
                if ("split" in cut):
                    ref_cut = numb_dict[background_model] + "_2Trk_split"
                elif ("ThreeTag" in cut):
                    ref_cut = numb_dict[background_model] + "_3Trk"
                elif ("FourTag" in cut):
                    ref_cut = numb_dict[background_model] + "_4Trk"
            #reset for top, use the correct MCs
            if "ttbar" in inputname: 
                ref_cut = cut
            #start the temp calculation of Ftransfer
            if fitresult and cut in word_dict.keys():
                if word_dict[cut] < len(fitresult["mu" + inputname]):
                    Ftransfer = fitresult["mu" + inputname][word_dict[cut]]
            #print inputname, Ftransfer
            #scale all the inputdic estimation plots
            for hst in plt_lst:
                htemp_qcd = outroot.Get(inputname + "_" + ref_cut + "_" + region + "_" + hst).Clone()
                htemp_qcd.SetName(inputname + "_est" + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Scale(Ftransfer)
                htemp_qcd.Write()
            #get the notag sideband for the current version
            cutcounts[region] = Ftransfer * inputdic[ref_cut][region]
            cutcounts[region + plt_m] = outroot.Get(inputname + "_est" + "_" + cut + "_" + region + plt_m)
            cutcounts[region + "scale_factor"] = Ftransfer
        est[cut] = cutcounts
    return est

### returns the qcd estimation dictionary;
def qcd_estimation(qcd, outroot):
    #now do the real work
    print "***** estimation *****"
    #do a dump fill first
    outroot.cd()
    est = {}
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            #start the histogram as a dumb holder
            Ftransfer = 1.0
            #define where the qcd come from
            ref_cut = "NoTag"
            # if ("2Trk_in1" in cut):
            #     ref_cut = "2Trk_in1_NoTag"
            # elif ("2Trk" in cut):
            #     ref_cut = "2Trk_NoTag"
            # elif ("3Trk" in cut):
            #     ref_cut = "3Trk_NoTag"
            # elif ("4Trk" in cut):
            #     ref_cut = "4Trk_NoTag"
            if ("Trk" not in cut):
                ref_cut = "NoTag"
            #start the temp calculation of Ftransfer
            Ftransfer = qcd[cut]["Sideband"]/qcd[ref_cut]["Sideband"]
            #print "qcd", Ftransfer
            #scale all the qcd estimation plots
            for hst in plt_lst:
                htemp_qcd = outroot.Get("qcd" + "_" + ref_cut + "_" + region + "_" + hst).Clone()
                htemp_qcd.SetName("qcd_est_nofit" + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Scale(Ftransfer)
                htemp_qcd.Write()

            #get the notag sideband for the current version
            cutcounts[region] = Ftransfer * qcd[ref_cut][region]
            cutcounts[region + plt_m] = outroot.Get("qcd_est_nofit" + "_" + cut + "_" + region + plt_m)
            cutcounts[region + "scale_factor"] = Ftransfer

        est[cut] = cutcounts
    return est

### returns the qcd from data dictionary
def GetDiff(dic1, dic2):
    result = {}
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            if dic1[cut][region]!= 0:
                cutcounts[region] = (dic1[cut][region] - dic2[cut][region])/dic1[cut][region] * 100
            else:
                cutcounts[region] = 0
            result[cut] = cutcounts
    return result

### returns the qcd from data dictionary
def Getqcd(inputdic, outroot):
    outroot.cd()
    qcd = {}
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            for hst in plt_lst:
                htemp_ttbar = outroot.Get("ttbar" + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_zjet  = outroot.Get("zjet" + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_qcd   = outroot.Get("data" + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_qcd.SetName("qcd" + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Add(htemp_ttbar, -1)
                htemp_qcd.Add(htemp_zjet, -1)
                htemp_qcd.Write()
            if ("Signal" in region) & ("NoTag" not in cut) & blind:
                cutcounts[region] = 0
            else:
                cutcounts[region] = inputdic["data"][cut][region] - inputdic["ttbar"][cut][region] - inputdic["zjet"][cut][region]
            #get qcd prediction shapes
            cutcounts[region + plt_m] = outroot.Get("qcd" + "_" + cut + "_" + region + plt_m)

        qcd[cut] = cutcounts
    return qcd

def WriteEvtCount(inputdic, outFile, samplename="region"):
    ### 
    tableList = []
    ###
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c|c|c|c|c}")
    tableList.append("%s & Sideband & Control & ZZ & Signal \\\\" % samplename)
    tableList.append("\\hline\\hline")
    tableList.append("& & & & \\\\")

    for i, cut in enumerate(dump_lst):
        #get the corresponding region
        outstr = ""
        outstr += cut.replace("_", " ") 
        for j, region in enumerate(region_lst):
            #get the mass plot
            outstr += " & "
            outstr += str(round(inputdic[cut][region], 4))
        outstr+="\\\\"
        tableList.append(outstr)

    tableList.append("& & & & \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")
    tableList.append("\\end{footnotesize}")
    tableList.append("\\newline")

    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")


### 
def GetEvtCount(inputdir, outroot, histname=""):
    #get input file
    input_f = ROOT.TFile.Open(inputdir, "read")
    ###
    eventcounts = {}
    ###
    #outdir = outroot.mkdir(histname)
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            #deal with the other plots
            for hst in plt_lst:
                hst_temp = input_f.Get(cut + "_" + region + "/" + hst).Clone()
                hst_temp.SetName(histname + "_" + cut + "_" + region + "_" + hst)
                outroot.cd()
                hst_temp.Write()

            #get the mass plot
            mHH_temp = outroot.Get(histname + "_" + cut + "_" + region + plt_m)
            if ("Signal" in region) & (("OneTag" in cut) or ("TwoTag" in cut) \
                or ("ThreeTag" in cut) or ("FourTag" in cut)) & blind & (histname == "data"):
                cutcounts[region] = 0
            else:
                cutcounts[region] = mHH_temp.Integral(0, mHH_temp.GetXaxis().GetNbins()+1)
            #save the mass plot into the dictionary
            cutcounts[region + plt_m] = outroot.Get(histname + "_" + cut + "_" + region + plt_m)
        #finish the for loop
        eventcounts[cut] = cutcounts

    #close the file before exit
    input_f.Close()
    #return the table
    return eventcounts



if __name__ == "__main__":
    main()
