import ROOT, rootlogon, helpers
import argparse, copy, glob, os, sys, time
from Xhh4bUtils.BkgFit.BackgroundFit_Ultimate import BackgroundFit
import Xhh4bUtils.BkgFit.smoothfit as smoothfit
import config as CONF
#for parallel processing!
import multiprocessing as mp
#end of import for now

ROOT.gROOT.SetBatch(True)

blind=True
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
"OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
#"ThreeTag_1loose", "TwoTag_split_1loose", "TwoTag_split_2loose"]
word_dict = {"FourTag":0, "ThreeTag":1, "TwoTag":3,"TwoTag_split":2, "OneTag":4, "NoTag":5}
numb_dict = {4:"FourTag", 3:"ThreeTag", 2:"TwoTag", 1:"OneTag", 0:"NoTag"}
region_lst = ["Sideband", "Control", "ZZ", "Signal"]
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
    parser.add_argument("--inputdir", default="sb_test")
    parser.add_argument("--full", default=True) #4times more time
    return parser.parse_args()

def main():
    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir
    #set the defult options
    global background_model
    background_model = 0
    global fullhists
    fullhists = ops.full
    global mass_lst
    #mass_lst = [1000, 2000, 3000]
    mass_lst = CONF.mass_lst
    global plt_lst
    plt_lst = ["mHH_l", "mHH_pole", "leadHCand_Mass", "sublHCand_Mass", \
        "leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt"]
    global plt_m
    plt_m = "_mHH_pole"
    #set fast test version, with all the significance output still
    if not fullhists:
        plt_lst = ["mHH_pole"]

    # create output file
    inputpath = CONF.inputpath + inputdir + "/"
    print "input is", inputpath
    output = open(inputpath + "sum%s_%s.tex" % ("" if background_model==0 else str(background_model), inputdir), "w")
    global outroot
    outroot = ROOT.TFile.Open(inputpath + "sum%s_%s.root" % ("" if background_model==0 else str(background_model), inputdir), "recreate")
    #print GetEvtCount(inputpath + "ttbar_comb_test.root")

    # Create the master dictionary for cutflows and plots
    masterinfo = {}

    #set the input tasks!
    inputtasks = []
    inputtasks.append({"inputdir":inputpath + "ttbar_comb_test/hist.root", "histname":"ttbar"})
    inputtasks.append({"inputdir":inputpath + "zjets_test/hist.root", "histname":"zjet"})
    inputtasks.append({"inputdir":inputpath + "data_test/hist.root", "histname":"data"})
    for mass in mass_lst:
        inputtasks.append({"inputdir":inputpath + "signal_G_hh_c10_M%i/hist.root" % mass, "histname":"RSG1_%i" % mass})

    #start calculating the dictionary
    for task in inputtasks:
        masterinfo.update(GetEvtCount(task))
    ##WriteEvtCount(masterinfo["ttbar"], output, "$t\\bar{t}$")
    ##WriteEvtCount(masterinfo["zjet"], output, "z+jets")
    #WriteEvtCount(masterinfo["data"], output, "data")
    # # Get qcd from data 
    masterinfo.update(Getqcd(masterinfo, "qcd"))
    #WriteEvtCount(masterinfo["qcd"], output, "qcd")
    ####################################################
    # #Do qcd background estimation
    #masterinfo["qcd_est_nofit"] = qcd_estimation(masterinfo["qcd"])
    masterinfo.update(qcd_estimation(masterinfo, "qcd_est_nofit"))
    #WriteEvtCount(masterinfo["qcd_est_nofit"], output, "qcd Est nofit")
    masterinfo.update(GetdataEst(masterinfo, "data_est_nofit"))
    #WriteEvtCount(masterinfo["data_est_nofit"], output, "data Est nofit")
    masterinfo.update(GetDiff(masterinfo["data_est_nofit"], masterinfo["data"], "dataEstDiffnofit"))
    WriteEvtCount(masterinfo["dataEstDiffnofit"], output, "Data Est no fit Diff Percentage")
    ####################################################
    #Do qcd background estimation from the fit
    print "Start Fit!"
    global fitresult
    fitresult = BackgroundFit(inputpath + "data_test/hist.root", \
        inputpath + "ttbar_comb_test/hist.root", inputpath + "zjets_test/hist.root", \
        distributionName = "leadHCand_Mass", whichFunc = "XhhBoosted", output = inputpath, NRebin=2, BKG_model=background_model)
    print "End of Fit!"
    masterinfo.update(fitestimation("qcd_est"))
    #WriteEvtCount(masterinfo["qcd_est"], output, "qcd Est")
    masterinfo.update(fitestimation("ttbar_est"))
    #WriteEvtCount(masterinfo["ttbar_est"], output, "top Est")
    # # #Do data estimation
    masterinfo.update(GetdataEst(masterinfo, "data_est"))
    #WriteEvtCount(masterinfo["data_est"], output, "data Est")
    # # #Do data estimation Difference comparision in control and ZZ region
    masterinfo.update(GetDiff(masterinfo["data_est"], masterinfo["data"], "dataEstDiff"))
    WriteEvtCount(masterinfo["dataEstDiff"], output, "Data Est Diff Percentage")
    # masterinfo["ttbarEstDiff"] = GetDiff(masterinfo["ttbar_est"], masterinfo["ttbar"])
    # WriteEvtCount(masterinfo["ttbarEstDiff"], output, "top Est Diff Percentage")

    ##Dump yield tables
    for tag in yield_tag_lst:
        texoutpath = inputpath + "Plot/Tables/"
        if not os.path.exists(texoutpath):
            os.makedirs(texoutpath)
        yield_tex = open( texoutpath + tag + "_yield.tex", "w")
        WriteYield(masterinfo, yield_tex, tag)

    ##Do overlay signal region predictions
    for mass in mass_lst:
        masterinfo.update(GetSignificance(masterinfo, mass, "RSG1_" + str(mass)))
        #WriteEvtCount(masterinfo["RSG1_" + str(mass)+ "sig_est"], output, "RSG %i Significance" % mass)
    # #produce the significance plots
    DumpSignificance(masterinfo)
    
    #finish and quit
    outroot.Close()
    output.close()
    print("--- %s seconds ---" % (time.time() - start_time))

### for mulitple processing
#def MultiWork(config):

### returns the data estimate from qcd dictionary
def GetdataEst(inputdic, histname=""):
    outroot.cd()
    optionalqcd = histname.replace("data", "qcd")
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
                htemp_qcd.SetName(histname + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Add(htemp_ttbar, 1)
                htemp_qcd.Add(htemp_zjet, 1)
                htemp_qcd.Write()
            plttemp = outroot.Get(histname + "_" + cut + "_" + region + plt_m)
            err = ROOT.Double(0.)
            cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
            cutcounts[region + "_err"] = err
        data_est[cut] = cutcounts
    return {histname:data_est}

### returns the estimation dictionary;
def fitestimation(histname=""):
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
                if ("split" in cut):#map to the specific trackjets
                    ref_cut = numb_dict[background_model] + "_2Trk_split"
                elif ("ThreeTag" in cut):
                    ref_cut = numb_dict[background_model] + "_3Trk"
                elif ("FourTag" in cut):
                    ref_cut = numb_dict[background_model] + "_4Trk"
            #reset for top, use the correct MCs
            if "ttbar" in histname: 
                ref_cut = cut
            #start the temp calculation of Ftransfer
            if fitresult and cut in word_dict.keys():
                if word_dict[cut] < len(fitresult["mu" + histname.replace("_est", "")]):
                    Ftransfer = fitresult["mu" + histname.replace("_est", "")][word_dict[cut]]
            #print histname, Ftransfer
            for hst in plt_lst:
                htemp_qcd = outroot.Get(histname.replace("_est", "") + "_" + ref_cut + "_" + region + "_" + hst).Clone()
                #for ttbar, for mscale and mll, use 3b instead of 4b
                if "ttbar" in histname and "FourTag" in cut and "mHH" in hst:
                    hist_temp = outroot.Get(histname.replace("_est", "") + "_" + "ThreeTag" + "_" + region + "_" + hst).Clone()
                    hist_temp.Scale(htemp_qcd.Integral(0, htemp_qcd.GetNbinsX()+1)/hist_temp.Integral(0, hist_temp.GetNbinsX()+1))
                    htemp_qcd = hist_temp.Clone()
                #proceed!
                htemp_qcd.SetName(histname + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Scale(Ftransfer)
                htemp_qcd.Write()

            #get the notag sideband for the current version
            plttemp = outroot.Get(histname + "_" + cut + "_" + region + plt_m)
            err = ROOT.Double(0.)
            cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
            cutcounts[region + "_err"] = err
            cutcounts[region + "scale_factor"] = Ftransfer
        est[cut] = cutcounts
    return {histname:est}

### returns the qcd estimation dictionary;
def qcd_estimation(inputdic, histname=""):
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
            Ftransfer = inputdic["qcd"][cut]["Sideband"]/inputdic["qcd"][ref_cut]["Sideband"]
            #print "qcd", Ftransfer
            #scale all the qcd estimation plots
            for hst in plt_lst:
                htemp_qcd = outroot.Get("qcd" + "_" + ref_cut + "_" + region + "_" + hst).Clone()
                htemp_qcd.SetName("qcd_est_nofit" + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Scale(Ftransfer)
                htemp_qcd.Write()
            #get the notag sideband for the current version
            cutcounts[region] = Ftransfer * inputdic["qcd"][ref_cut][region]
            cutcounts[region + "scale_factor"] = Ftransfer

        est[cut] = cutcounts
    return {histname:est}

### returns the qcd from data dictionary
def GetDiff(dic1, dic2, histname=""):
    result = {}
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            if dic2[cut][region]!= 0:
                cutcounts[region] = (dic1[cut][region] - dic2[cut][region])/dic2[cut][region] * 100
                cutcounts[region + "_err"] = helpers.ratioerror(dic1[cut][region], dic2[cut][region], \
                    dic1[cut][region + "_err"], dic2[cut][region + "_err"]) * 100
            else:
                cutcounts[region] = 0
                cutcounts[region + "_err"] = 0
            result[cut] = cutcounts
    return {histname:result}

### returns the qcd from data dictionary
def Getqcd(inputdic, histname=""):
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
            #get qcd prediction shapes
            plttemp = outroot.Get("qcd" + "_" + cut + "_" + region + plt_m)
            if ("Signal" in region) & ("NoTag" not in cut) & blind:
                cutcounts[region] = 0
                cutcounts[region + "_err"] = 0
            else:
                err = ROOT.Double(0.)
                cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
                cutcounts[region + "_err"] = err
        qcd[cut] = cutcounts
    return {histname: qcd}

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
            outstr += str(helpers.round_sig(inputdic[cut][region], 2))
            outstr += " $\\pm$ "
            outstr += str(helpers.round_sig(inputdic[cut][region + "_err"], 2))
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

def WriteYield(inputdic, outFile, cut="Signal"):
    ### 
    tableList = []
    ###
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c|c|c|c}")
    tableList.append("%s & Sideband & Control & Signal \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& & & \\\\")

    for i, file in enumerate(yield_lst):
        #get the corresponding region
        outstr = ""
        outstr += yield_dic[file]
        for j, region in enumerate(yield_region_lst):
            #print file, region
            outstr += " & "
            outstr += str(helpers.round_sig(inputdic[file][cut][region], 2))
            outstr += " $\\pm$ "
            outstr += str(helpers.round_sig(inputdic[file][cut][region+"_err"], 2))
            outstr += " $\\pm$ "
            outstr += str("sys")

        outstr+="\\\\"
        tableList.append(outstr)

    tableList.append("& & & \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")
    tableList.append("\\end{footnotesize}")
    tableList.append("\\newline")

    #return the table
    for line in tableList:
        #print line
        outFile.write(line+" \n")

### 
def GetEvtCount(config):
    inputdir = config["inputdir"]
    histname = config["histname"]
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
                #print hst, region, cut, inputdir
                hst_temp = input_f.Get(cut + "_" + region + "/" + hst).Clone()
                hst_temp.SetName(histname + "_" + cut + "_" + region + "_" + hst)
                outroot.cd()
                hst_temp.Write()

            #get the mass plot
            plttemp = outroot.Get(histname + "_" + cut + "_" + region + plt_m)
            if ("Signal" in region) & (("OneTag" in cut) or ("TwoTag" in cut) \
                or ("ThreeTag" in cut) or ("FourTag" in cut)) & blind & (histname == "data"):
                cutcounts[region] = 0
                cutcounts[region + "_err"] = 0
            else:
                err = ROOT.Double(0)
                cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
                err = float(err) #convert it back...so that python likes it
                cutcounts[region + "_err"] = err
                
        #finish the for loop
        eventcounts[cut] = cutcounts

    #close the file before exit
    input_f.Close()
    #return the table
    return {histname: eventcounts}

#functin from Qi
def GetMassWindow(hist, eff):
    min_width = 9e9
    start_bin = 1
    end_bin = hist.GetNbinsX()
    ibinPeak = hist.GetMaximumBin()
    if hist.Integral(0, hist.GetNbinsX()+1) == 0:
        return (0, hist.GetNbinsX()+1)

    for i in range(1, hist.GetNbinsX()+1):
            i_start = i
            i_end = i_start
            frac = 0

            while( (frac < eff) and (i_end != hist.GetNbinsX()) ):
                    frac += hist.GetBinContent(i_end)/hist.Integral(0, hist.GetNbinsX()+1)
                    i_end += 1

            width = hist.GetBinCenter(i_end) - hist.GetBinCenter(i_start)
            if (width < min_width) and (i_end != hist.GetNbinsX()) and (i_start < ibinPeak) and (i_end > ibinPeak):
                    min_width = width
                    start_bin = i_start
                    end_bin = i_end

    return (start_bin, end_bin)

#functin from Qi, modified, no long taking weight
def GetSensitivity(h_signal, h_bkg):
        # get peak position
        maxBin = h_signal.GetMaximumBin()
        maxMass = h_signal.GetBinCenter(maxBin)
        integralbin_min, integralbin_max = GetMassWindow(h_signal, 0.68)   # or 0.95

        S_err = ROOT.Double(0.)
        S = h_signal.IntegralAndError(integralbin_min, integralbin_max, S_err)

        B_err = ROOT.Double(0.)
        B = h_bkg.IntegralAndError(integralbin_min, integralbin_max, B_err)

        if S==0 or B==0:
            return(0, 0, S, B)
        # sensitivity = 1.0*S/ROOT.TMath.Sqrt(B)
        # sensitivity_err = sensitivity * ROOT.TMath.Sqrt((1.0*S_err/S)**2 + (1.0*B_err/(2*B))**2)
        # a better definition for low stats
        sensitivity = (1.0*S)/(1 + ROOT.TMath.Sqrt(B))
        sensitivity_err = sensitivity * ROOT.TMath.Sqrt((1.0*S_err/S)**2 + (1./(4*B))*((1.0*B_err/(1+ROOT.TMath.Sqrt(B)))**2))

        #return the sensitivity, error, number of signal and number of background estimated in this window
        return (sensitivity, sensitivity_err, S, B)

### 
def GetSignificance(inputdic, mass, histname=""):    
    eventcounts = {}
    eventcounts_err = {}
    ### 
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        cutcounts_err = {}
        for j, region in enumerate(region_lst):
            #nees fix!!!
            plttemp_sig = outroot.Get("RSG1_" + str(mass) + "_" + cut + "_" + region + plt_m)
            plttemp_bkg = outroot.Get("data_est" + "_" + cut + "_" + region + plt_m)
            cutcounts[region], cutcounts_err[region], S, B = GetSensitivity(plttemp_sig, plttemp_bkg)
            #print mass, cut, region, " sig ", cutcounts[region], " sigerr ", cutcounts_err[region], " Nsig ", S, " Nbkg ", B
            #get the mass plot
            # if ("Signal" in region) & (("OneTag" in cut) or ("TwoTag" in cut) \
            #     or ("ThreeTag" in cut) or ("FourTag" in cut)) & blind:\ 
        eventcounts[cut] = cutcounts
        eventcounts_err[cut] = cutcounts_err 
    return {histname + "sig_est": eventcounts, histname + "sig_est_err": eventcounts_err}

### 
def DumpSignificance(inputdic, samplename="region"):    
    ###
    outroot.cd()
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        for j, region in enumerate(region_lst):
            #for all the mass points:
            temp_plt = ROOT.TH1D("%s_%s_Significance" % (cut, region), ";mass, GeV; Significance", 32, -50, 3150)
            for mass in mass_lst:
                temp_plt.SetBinContent(temp_plt.GetXaxis().FindBin(mass), inputdic["RSG1_" + str(mass) + "sig_est"][cut][region])
                temp_plt.SetBinError(temp_plt.GetXaxis().FindBin(mass), inputdic["RSG1_" + str(mass) + "sig_est_err"][cut][region])
            temp_plt.Write()
    return 0


if __name__ == "__main__":
    main()
