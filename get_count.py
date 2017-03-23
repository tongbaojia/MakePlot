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
#import plotting style
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.SetAtlasStyle()
#end of import for now

ROOT.gROOT.SetBatch(True)

#set global variables
# cut_lst = ["2Trk_in1_NoTag", "2Trk_in1_OneTag", "2Trk_in1_TwoTag", \
#     "2Trk_NoTag", "2Trk_OneTag", "2Trk_TwoTag_split", \
#     "3Trk_NoTag", "3Trk_OneTag", "3Trk_TwoTag", "3Trk_TwoTag_split", "3Trk_ThreeTag", \
#     "4Trk_NoTag", "4Trk_OneTag", "4Trk_TwoTag", "4Trk_TwoTag_split", "4Trk_ThreeTag", "4Trk_FourTag",
#     "NoTag", "OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
# input are exclusive trkjets

evtsel_lst = ["All", "PassGRL", "PassTrig", "PassJetClean", "Pass2FatJets", "PassDiJetPt", "PassDetaHH", "PassSignal"]
dump_lst = ["NoTag", "OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"] #"ThreeTag_1loose", "TwoTag_split_1loose", "TwoTag_split_2loose"]
##setup the list of folders to process; these histograms are savedls
cut_lst = ["NoTag", "NoTag_2Trk_split", "NoTag_3Trk", "NoTag_4Trk", \
"NoTag_2Trk_split_lead", "NoTag_2Trk_split_subl", "NoTag_3Trk_lead", "NoTag_3Trk_subl", "NoTag_4Trk_lead", "NoTag_4Trk_subl",\
"OneTag_lead", "TwoTag_lead", "OneTag_subl", "TwoTag_subl",\
"OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
#"OneTag_lead", "TwoTag_lead", "OneTag_subl", "TwoTag_subl",
#"ThreeTag_1loose", "TwoTag_split_1loose", "TwoTag_split_2loose"]
word_dict  = {"FourTag":0, "ThreeTag":1, "TwoTag":3,"TwoTag_split":2, "OneTag":4, "NoTag":5}
numb_dict  = {4:"FourTag", 3:"ThreeTag", 2:"TwoTag", 1:"OneTag", 0:"NoTag"}
region_lst = ["Incl", "Sideband", "Control", "Signal"]

#setup dictionary for signal regions and background estimations
#default: ["FourTag", "ThreeTag", "TwoTag_split", "TwoTag", "OneTag"]
bkgest_lst = ["FourTag", "ThreeTag", "TwoTag_split"] 
#setup the dictionary for background estiamtions
##default: {"FourTag":"NoTag_4Trk", "ThreeTag":"NoTag_3Trk", "TwoTag_split":"NoTag_2Trk_split", "TwoTag":"NoTag", "OneTag":"NoTag"}
#bkgest_dict = {"FourTag":"NoTag_4Trk", "ThreeTag":"NoTag_3Trk", "TwoTag_split":"NoTag_2Trk_split", "TwoTag":"NoTag", "OneTag":"NoTag"}
bkgest_dict       = {"FourTag":"NoTag_4Trk",  "ThreeTag":"NoTag_3Trk", "TwoTag_split":"NoTag_2Trk_split",  "TwoTag":"OneTag",  "OneTag":"NoTag"}
#bkgest_dict_NoTag = {"FourTag":"NoTag",       "ThreeTag":"NoTag",      "TwoTag_split":"NoTag",       "TwoTag":"NoTag", "OneTag":"NoTag"}
#bkgest_dict_OneTag= {"FourTag":"TwoTag",      "ThreeTag":"TwoTag",     "TwoTag_split":"OneTag", "TwoTag":"NoTag", "OneTag":"NoTag"}
weight_dict       = {"FourTag":("NoTag", "NoTag_2Trk_split"),  "ThreeTag":("NoTag", "NoTag_2Trk_split"), "TwoTag_split":("NoTag", "NoTag_2Trk_split"), "TwoTag":("NoTag", "OneTag")}


#set list of dumping yields
yield_lst        = ["qcd_est", "ttbar_est", "zjet", "data_est", "data", "RSG1_1000", "RSG1_2000", "RSG1_3000"]
yield_dic        = {"qcd_est":"QCD Est", "ttbar_est":"$t\\bar{t}$ Est. ", "zjet":"$Z+jets$", "data_est":"Total Bkg Est",\
 "data":"Data", "RSG1_1000":"$c=1.0$,$m=1.0TeV$", "RSG1_2000":"$c=1.0$,$m=2.0TeV$", "RSG1_3000":"$c=1.0$,$m=3.0TeV$"}
yield_tag_lst    = ["TwoTag_split", "ThreeTag", "FourTag"]
yield_region_lst = ["Sideband", "Control", "Signal"]

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
    parser.add_argument("--dosyst", action='store_true')
    #parser.add_argument("--full", default=True) #4times more time
    parser.add_argument("--full", action='store_true') #4times more time
    parser.add_argument("--Xhh", action='store_true') #4times more time
    return parser.parse_args()

def main():
    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir
    #set the defult options
    global background_model #0 is NoTag, 1 is OneTag, s is the special case
    background_model = 0
    global fullhists
    fullhists = ops.full
    global mass_lst
    #mass_lst = [1000, 2000, 3000]
    mass_lst = CONF.mass_lst
    global plt_lst
    plt_lst = []
    if fullhists is True and CONF.fullstudy: 
        print "full histos: true"
        plt_lst = ["mHH_l", "mHH_pole", "hCandDr", "hCandDeta", "hCandDphi",\
            "leadHCand_Pt_m", "leadHCand_Eta", "leadHCand_Phi", "leadHCand_Mass", "leadHCand_Mass_s", "leadHCand_trk_dr",\
            "sublHCand_Pt_m", "sublHCand_Eta", "sublHCand_Phi", "sublHCand_Mass", "sublHCand_Mass_s", "sublHCand_trk_dr",\
            "leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt",\
            "leadHCand_ntrk", "sublHCand_ntrk", "leadHCand_trk_pt_diff_frac", "sublHCand_trk_pt_diff_frac"]
            #"leadHCand_trk0_Eta", "leadHCand_trk0_Phi", "sublHCand_trk0_Eta", "sublHCand_trk0_Phi",\
    elif fullhists is True : ##this is used to skip histograms
        plt_lst = ["mHH_l", "mHH_pole",\
            "leadHCand_Pt_m",\
            "sublHCand_Pt_m",\
            "leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt"]
    else:
        print "full histos: false"
        plt_lst = ["mHH_l", "mHH_pole"]
        #"leadHCand_trks_Pt", "sublHCand_trks_Pt", "trks_Pt"]
    global plt_m
    plt_m = "mHH_l"
    #set fast test version, with all the significance output still

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
    inputtasks.append({"inputdir":inputpath + "ttbar_comb_test/hist-MiniNTuple.root", "histname":"ttbar"})
    inputtasks.append({"inputdir":inputpath + "zjets_test/hist-MiniNTuple.root", "histname":"zjet"})
    inputtasks.append({"inputdir":inputpath + "data_test/hist-MiniNTuple.root", "histname":"data"})
    for mass in mass_lst:
        inputtasks.append({"inputdir":inputpath + "signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass, "histname":"RSG1_%i" % mass})
        if (ops.Xhh):
            inputtasks.append({"inputdir":inputpath + "signal_X_hh_M%i/hist-MiniNTuple.root" % mass, "histname":"Xhh_%i" % mass})


    #do the fit first
    ####################################################
    #Do qcd background estimation from the fit
    print "Start Fit!"
    global fitresult
    global useOneTop
    useOneTop = False
    fitresult = BackgroundFit(inputpath + "data_test/hist-MiniNTuple.root", \
        inputpath + "ttbar_comb_test/hist-MiniNTuple.root", inputpath + "zjets_test/hist-MiniNTuple.root", \
        distributionName = ["leadHCand_Mass"], whichFunc = "XhhBoosted", output = inputpath + "Plot/", NRebin=2, \
        BKG_lst=bkgest_lst, BKG_dic=bkgest_dict, use_one_top_nuis=useOneTop, fitzjets=True) #Weight_dic = weight_dict, 
    
    # global fitresult_NoTag
    # fitresult_NoTag = BackgroundFit(inputpath + "data_test/hist-MiniNTuple.root", \
    #     inputpath + "ttbar_comb_test/hist-MiniNTuple.root", inputpath + "zjets_test/hist-MiniNTuple.root", \
    #     distributionName = ["leadHCand_Mass"], whichFunc = "XhhBoosted", output = inputpath + "Plot/", NRebin=2, BKG_lst=bkgest_lst, BKG_dic=bkgest_dict_NoTag, fitzjets=False)
    # global fitresult_OneTag
    # fitresult_OneTag = BackgroundFit(inputpath + "data_test/hist-MiniNTuple.root", \
    #     inputpath + "ttbar_comb_test/hist-MiniNTuple.root", inputpath + "zjets_test/hist-MiniNTuple.root", \
    #     distributionName = ["leadHCand_Mass"], whichFunc = "XhhBoosted", output = inputpath + "Plot/", NRebin=2, BKG_lst=bkgest_lst, BKG_dic=bkgest_dict_OneTag, fitzjets=False)
    
    # global fitresult_NoTag
    # fitresult_NoTag = BackgroundFit(inputpath + "data_test/hist-MiniNTuple.root", \
    #     inputpath + "ttbar_comb_test/hist-MiniNTuple.root", inputpath + "zjets_test/hist-MiniNTuple.root", \
    #     distributionName = ["leadHCand_Mass"], whichFunc = "XhhBoosted", output = inputpath + "Plot/", NRebin=2, BKG_model=0, fitzjets=False)
    # global fitresult_OneTag
    # fitresult_OneTag = BackgroundFit(inputpath + "data_test/hist-MiniNTuple.root", \
    #     inputpath + "ttbar_comb_test/hist-MiniNTuple.root", inputpath + "zjets_test/hist-MiniNTuple.root", \
    #     distributionName = ["leadHCand_Mass"], whichFunc = "XhhBoosted", output = inputpath + "Plot/", NRebin=2, BKG_model=1, fitzjets=False)
    print "End of Fit!"

    #setup multiprocessing
    #start calculating the dictionary
    print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    npool = min(len(inputtasks), mp.cpu_count()-1)
    pool  = mp.Pool(npool)
    for result in pool.map(GetEvtCount, inputtasks):
        masterinfo.update(result[0])
        outroot.cd()
        for plt in result[1]:
            plt.Write()
            del(plt)
    # for task in inputtasks:
    #     result = GetEvtCount(task) #dictionary of values, plots
    #     masterinfo.update(result[0])
    #     outroot.cd()
    #     for plt in result[1]:
    #         plt.Write()
    #         del(plt)
    # #WriteEvtCount(masterinfo["ttbar"], output, "$t\\bar{t}$")
    # #WriteEvtCount(masterinfo["zjet"], output, "z+jets")
    WriteEvtCount(masterinfo["data"], output, "data")
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
    #WriteEvtCount(masterinfo["dataEstDiffnofit"], output, "Data Est no fit Diff Percentage")
    ###
    #masterinfo.update(fitestimation("qcd_est", masterinfo)) 
    #WriteEvtCount(masterinfo["qcd_est"], output, "qcd Est")
    #print "old method"
    #masterinfo.update(fitestimation("qcd_est", masterinfo))
    masterinfo.update(fitestimation("qcd_est", masterinfo, weight=False))
    #WriteEvtCount(masterinfo["qcd_est"], output, "qcd Est")
    masterinfo.update(fitestimation("ttbar_est", masterinfo, weight=False))
    #WriteEvtCount(masterinfo["ttbar_est"], output, "ttbar Est")
    # print "new method"
    #masterinfo.update(fitestimation_test("qcd_est", masterinfo))
    #masterinfo.update(fitestimation_test("ttbar_est", masterinfo))
    #WriteEvtCount(masterinfo["ttbar_est"], output, "top Est")
    # # #Do data estimation
    masterinfo.update(GetdataEst(masterinfo, "data_est", dosyst=True))
    WriteEvtCount(masterinfo["data_est"], output, "data Est")
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

    # #save time if do systematics ## turn it off now...
    # if (not ops.dosyst and True):
    #     ##Do overlay signal region predictions
    #     print " Running %s jobs on %s cores" % (len(inputtasks), mp.cpu_count()-1)
    #     npool = min(len(inputtasks), mp.cpu_count()-1)
    #     pool  = mp.Pool(npool)
    #     for result in pool.map(GetSignificance, mass_lst):
    #         masterinfo.update(result)
    #         #WriteEvtCount(masterinfo["RSG1_" + str(mass)+ "sig_est"], output, "RSG %i Significance" % mass)
    #     ##produce the significance plots
    #     DumpSignificance(masterinfo)

    #finish and quit
    with open(inputpath + "sum%s_%s.txt" % ("" if background_model==0 else str(background_model), inputdir), "w") as f:
        json.dump(masterinfo, f)
    outroot.Close()
    output.close()
    print("--- %s seconds ---" % (time.time() - start_time))

### for mulitple processing
#def MultiWork(config):

### returns the data estimate from qcd dictionary
def GetdataEst(inputdic, histname="", dosyst=False):
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
                #htemp_qcd.Add(htemp_zjet, 1) #disable adding zjets
                htemp_qcd.Write()
                del(htemp_qcd)
                del(htemp_zjet)
                del(htemp_ttbar)
            plttemp = outroot.Get(histname + "_" + cut + "_" + region + "_" + plt_m)
            err = ROOT.Double(0.)
            cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
            cutcounts[region + "_err"] = float(err)
            cutcounts[region + "_syst_up"] = 0
            cutcounts[region + "_syst_down"] = 0
            del(plttemp)
            #start systematics
            if (dosyst):
                if (region + "_syst_muqcd_fit_up") in inputdic["qcd_est"][cut].keys():
                    cutcounts[region + "_syst_muqcd_fit_up"]   = helpers.syst_adderror(inputdic["qcd_est"][cut][region + "_syst_muqcd_fit_up"], inputdic["ttbar_est"][cut][region + "_syst_muqcd_fit_up"], corr=inputdic["qcd_est"][cut][region + "_corr"])
                    cutcounts[region + "_syst_muqcd_fit_down"] = helpers.syst_adderror(inputdic["qcd_est"][cut][region + "_syst_muqcd_fit_down"], inputdic["ttbar_est"][cut][region + "_syst_muqcd_fit_down"], corr=inputdic["qcd_est"][cut][region + "_corr"])
                    ##for now the total systematics is just the muqcd fit systematics
                    cutcounts[region + "_syst_up"]   = cutcounts[region + "_syst_muqcd_fit_up"]
                    cutcounts[region + "_syst_down"] = cutcounts[region + "_syst_muqcd_fit_down"]
        data_est[cut] = cutcounts
    return {histname:data_est}

### returns the estimation dictionary;
def fitestimation_test(histname="", inputdic={}):
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
            Ftransfer_err = 0.0
            Ftransfer_OneTag = 1.0
            Ftransfer_OneTag_err = 0.0
            Ftransfer_NoTag = 1.0
            Ftransfer_NoTag_err = 0.0
            Ftransfer_corr = 0.0
            Ntransfer = 1.0
            #define where the qcd come from
            ref_cut = "NoTag"
            ref_cut_NoTag = "NoTag"
            ref_cut_OneTag = "NoTag"
            if cut in bkgest_dict.keys():
                ref_cut = bkgest_dict[cut]
                ref_cut_NoTag = bkgest_dict_NoTag[cut]
                ref_cut_OneTag = bkgest_dict_OneTag[cut]
            #reset for top, use the correct MCs
            if "ttbar" in histname: 
                ref_cut = cut
            #start the temp calculation of Ftransfer

            #print ref_cut, histname, cut, region
            #print fitresult
            if fitresult and cut in word_dict.keys():
                if word_dict[cut] < len(fitresult["mu" + histname.replace("_est", "")]):
                    Ftransfer            = fitresult["mu" + histname.replace("_est", "")][word_dict[cut]]
                    Ftransfer_err        = fitresult["mu" + histname.replace("_est", "") + "_e"][word_dict[cut]]
                    Ftransfer_NoTag      = fitresult_NoTag["mu" + histname.replace("_est", "")][word_dict[cut]]
                    Ftransfer_NoTag_err  = fitresult_NoTag["mu" + histname.replace("_est", "") + "_e"][word_dict[cut]]
                    Ftransfer_OneTag     = fitresult_OneTag["mu" + histname.replace("_est", "")][word_dict[cut]]
                    Ftransfer_OneTag_err = fitresult_OneTag["mu" + histname.replace("_est", "") + "_e"][word_dict[cut]]
                    corr_temp = fitresult["corr_m"][word_dict[cut]]
                    Ftransfer_corr = corr_temp[word_dict[cut] + len(corr_temp)/2] if not useOneTop else corr_temp[-1]
                    #print "cor is, ", fitresult["corr_m"], Ftransfer_corr, cut, histname, word_dict[cut]
                else:
                    Ftransfer = inputdic["qcd"][cut]["Sideband"]/inputdic["qcd"][ref_cut]["Sideband"]
                    Ftransfer_err = helpers.ratioerror(inputdic["qcd"][cut]["Sideband"], inputdic["qcd"][ref_cut]["Sideband"])
            #print histname, cut, Ftransfer, Ftransfer_NoTag, Ftransfer_OneTag
            for hst in plt_lst:
                htemp_qcd = outroot.Get(histname.replace("_est", "") + "_" + ref_cut + "_" + region + "_" + hst).Clone()
                htemp_qcd_NoTag = outroot.Get(histname.replace("_est", "") + "_" + ref_cut_NoTag + "_" + region + "_" + hst).Clone()
                htemp_qcd_OneTag = outroot.Get(histname.replace("_est", "") + "_" + ref_cut_OneTag + "_" + region + "_" + hst).Clone()
                #for ttbar, for mscale and mll, use 3b instead of 4b
                if "ttbar" in histname and ("FourTag" in cut or "ThreeTag" in cut):
                    hist_temp = outroot.Get(histname.replace("_est", "") + "_" + "TwoTag_split" + "_" + region + "_" + hst).Clone()
                    hist_temp.Scale(htemp_qcd.Integral(0, htemp_qcd.GetNbinsX()+1)/hist_temp.Integral(0, hist_temp.GetNbinsX()+1))
                    htemp_qcd = hist_temp.Clone()
                    del(hist_temp)
                #proceed!
                Ntransfer = htemp_qcd.Integral(0, htemp_qcd.GetNbinsX()+1)
                htemp_qcd.SetName(histname + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Scale(Ftransfer)

                ##this is nasty for now
                if "qcd" in histname:
                    if ("split" in cut): ##2bs; this works wonderfully
                        htemp_qcd_NoTag.Scale(Ftransfer_NoTag)
                        htemp_qcd_OneTag.Scale(Ftransfer_OneTag)
                        htemp_qcd.Add(htemp_qcd_OneTag, 1)
                        htemp_qcd.Add(htemp_qcd_NoTag, -1)
                    elif ("ThreeTag" in cut):
                        htemp_qcd_NoTag.Scale(Ftransfer_NoTag)
                        htemp_qcd_OneTag.Scale(Ftransfer_OneTag)
                        htemp_qcd.Add(htemp_qcd_OneTag, 1)
                        htemp_qcd.Add(htemp_qcd_NoTag, -1)
                        #htemp_qcd.Add(htemp_qcd_NoTag, -1)
                    elif ("FourTag" in cut):
                        htemp_qcd_NoTag.Scale(Ftransfer_NoTag)
                        htemp_qcd_OneTag.Scale(Ftransfer_OneTag)
                        htemp_qcd.Add(htemp_qcd_OneTag, 1)
                        htemp_qcd.Add(htemp_qcd_NoTag, -1)
                        ##directly scale from 2tag
                        # htemp_qcd.Scale(2)
                        # htemp_qcd.Add(htemp_qcd_NoTag, -1)

                elif "ttbar" in histname:
                    htemp_qcd.Scale(1/Ftransfer)#unscale
                    if ("split" in cut): ##2bs; this works wonderfully
                        htemp_qcd.Scale(Ftransfer + Ftransfer_OneTag - Ftransfer_NoTag)
                    elif ("ThreeTag" in cut):
                        htemp_qcd.Scale(Ftransfer + Ftransfer_OneTag - Ftransfer_NoTag )
                    elif ("FourTag" in cut):
                        htemp_qcd.Scale(Ftransfer + Ftransfer_OneTag - Ftransfer_NoTag) #htemp_qcd.Scale(2 * Ftransfer - Ftransfer_NoTag)


                htemp_qcd.Write()
                del(htemp_qcd)
                del(htemp_qcd_NoTag)
                del(htemp_qcd_OneTag)

            #get the notag sideband for the current version
            plttemp = outroot.Get(histname + "_" + cut + "_" + region + "_" + plt_m)
            err = ROOT.Double(0.)
            cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
            cutcounts[region + "_err"] = float(err)
            cutcounts[region + "_syst_muqcd_fit_up"] = Ftransfer_err * Ntransfer
            cutcounts[region + "_syst_muqcd_fit_down"] = -Ftransfer_err * Ntransfer
            cutcounts[region + "_scale_factor"] = Ftransfer
            cutcounts[region + "_corr"] = Ftransfer_corr
            #print cut, region, Ntransfer, Ftransfer_err, cutcounts[region + "_syst_muqcd_fit_up"]
            del(plttemp)
        est[cut] = cutcounts
    return {histname:est}

### returns the estimation dictionary;
def fitestimation(histname="", inputdic={}, weight=False):
    '''weight controls whether the a/b tag ratio is applied'''
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
            Ftransfer_err = 0.0
            Ftransfer_corr = 0.0
            Ntransfer = 1.0
            #define where the qcd come from
            ref_cut = "NoTag"
            if cut in bkgest_dict.keys():
                ref_cut = bkgest_dict[cut]
            #reset for top, use the correct MCs
            if "ttbar" in histname: 
                ref_cut = cut

            #print ref_cut, histname, cut, region
            #start the temp calculation of Ftransfer
            #print fitresult
            if fitresult and cut in word_dict.keys():
                if word_dict[cut] < len(fitresult["mu" + histname.replace("_est", "")]):
                    Ftransfer = fitresult["mu" + histname.replace("_est", "")][word_dict[cut]]
                    Ftransfer_err = fitresult["mu" + histname.replace("_est", "") + "_e"][word_dict[cut]]
                    corr_temp = fitresult["corr_m"][word_dict[cut]]
                    Ftransfer_corr = corr_temp[word_dict[cut] + len(corr_temp)/2]  if not useOneTop else corr_temp[-1]
                    #print "cor is, ", fitresult["corr_m"], Ftransfer_corr, cut, histname, word_dict[cut]
                else:
                    Ftransfer = inputdic["qcd"][cut]["Sideband"]/inputdic["qcd"][ref_cut]["Sideband"]
                    Ftransfer_err = helpers.ratioerror(inputdic["qcd"][cut]["Sideband"], inputdic["qcd"][ref_cut]["Sideband"])
            #print histname, Ftransfer
            for hst in plt_lst:
                htemp_qcd = outroot.Get(histname.replace("_est", "") + "_" + ref_cut + "_" + region + "_" + hst).Clone()
                #for ttbar, for mscale and mll, use 3b instead of 4b
                if "ttbar" in histname and ("FourTag" in cut or "ThreeTag" in cut):
                    #print ref_cut, histname, cut, region, htemp_qcd.Integral(0, htemp_qcd.GetNbinsX()+1)
                    hist_temp = outroot.Get(histname.replace("_est", "") + "_" + "TwoTag_split" + "_" + region + "_" + hst).Clone()
                    hist_temp.Scale(htemp_qcd.Integral(0, htemp_qcd.GetNbinsX()+1)/hist_temp.Integral(0, hist_temp.GetNbinsX()+1))
                    #print ref_cut, histname, cut, region, hist_temp.Integral(0, hist_temp.GetNbinsX()+1)
                    htemp_qcd = hist_temp.Clone()
                    del(hist_temp)
                #proceed!
                Ntransfer = htemp_qcd.Integral(0, htemp_qcd.GetNbinsX()+1)
                htemp_qcd.SetName(histname + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Scale(Ftransfer)
                ## add weight!
                if weight:
                    #print ref_cut, histname, cut, region
                    if cut in weight_dict.keys():
                        hist_temp_base = outroot.Get(histname.replace("_est", "") + "_" + weight_dict[cut][0] + "_" + "Sideband" + "_" + hst).Clone("base")
                        hist_temp_model = outroot.Get(histname.replace("_est", "") + "_" + weight_dict[cut][1] + "_" + "Sideband" + "_" + hst).Clone("model")
                        hist_temp_base.Scale(hist_temp_model.Integral()/hist_temp_base.Integral())
                        hist_temp_model.Divide(hist_temp_base)
                        htemp_qcd.Multiply(hist_temp_model)
                        hist_temp_model.SetName(histname + "_" + cut + "_" + region + "_" + hst + "_weight")
                        hist_temp_model.Write()
                        del(hist_temp_model)
                        del(hist_temp_base)
                    else:
                        pass
                ## end of add weight
                htemp_qcd.Write()
                del(htemp_qcd)

            #get the notag sideband for the current version
            plttemp = outroot.Get(histname + "_" + cut + "_" + region + "_" + plt_m)
            err = ROOT.Double(0.)
            cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
            cutcounts[region + "_err"] = float(err)
            cutcounts[region + "_syst_muqcd_fit_up"] = Ftransfer_err * Ntransfer
            cutcounts[region + "_syst_muqcd_fit_down"] = -Ftransfer_err * Ntransfer
            cutcounts[region + "_scale_factor"] = Ftransfer
            cutcounts[region + "_corr"] = Ftransfer_corr
            #print plttemp.GetName(), cut, region, cutcounts[region], cutcounts[region + "_err"], cutcounts[region + "_syst_muqcd_fit_up"]
            del(plttemp)
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
                del(htemp_qcd)
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
            if dic2[cut][region] != 0:
            	cutcounts[region] = (dic1[cut][region] - dic2[cut][region])/dic2[cut][region] * 100
                cutcounts[region + "_err"] = helpers.ratioerror(dic1[cut][region], dic2[cut][region], \
                    dic1[cut][region + "_err"], dic2[cut][region + "_err"]) * 100
                cutcounts[region + "_syst_up"] = (dic1[cut][region + "_syst_up"])/dic2[cut][region] * 100
                cutcounts[region + "_syst_down"] = (dic1[cut][region + "_syst_down"])/dic2[cut][region] * 100
            else:
            	cutcounts[region] = 0
                cutcounts[region + "_err"] = 0
                cutcounts[region + "_syst_up"] = 0
                cutcounts[region + "_syst_down"] = 0
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
                ##do the ttbar correction here as well
                if ("FourTag" in cut or "ThreeTag" in cut):
                    htemp_ttbar = outroot.Get("ttbar" + "_" + "TwoTag_split" + "_" + region + "_" + hst).Clone()
                    htemp_ttbar_temp = outroot.Get("ttbar" + "_" + cut + "_" + region + "_" + hst).Clone()
                    htemp_ttbar.Scale(htemp_ttbar_temp.Integral(0, htemp_ttbar_temp.GetNbinsX()+1)/htemp_ttbar.Integral(0, htemp_ttbar.GetNbinsX()+1))
                    del(htemp_ttbar_temp)
                else:
                    htemp_ttbar = outroot.Get("ttbar" + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_zjet  = outroot.Get("zjet" + "_" + cut + "_" + region + "_" + hst).Clone()
                htemp_qcd   = outroot.Get("data" + "_" + cut + "_" + region + "_" + hst).Clone()
                ##check error
                ## if hst is "mHH_l":
                ##     print "data", cut, region, htemp_qcd.GetBinCenter(200), "content:", htemp_qcd.GetBinContent(200), "sqrt:", ROOT.TMath.Sqrt(htemp_qcd.GetBinContent(200)), "err:", htemp_qcd.GetBinError(200)
                ##     print "top", cut, region, htemp_ttbar.GetBinCenter(200),"content:", htemp_ttbar.GetBinContent(200), "sqrt:", ROOT.TMath.Sqrt(htemp_ttbar.GetBinContent(200)), "err:", htemp_ttbar.GetBinError(200)
                ##     print "zjet", cut, region, htemp_zjet.GetBinCenter(200),"content:", htemp_zjet.GetBinContent(200), "sqrt:", ROOT.TMath.Sqrt(htemp_zjet.GetBinContent(200)), "err:", htemp_zjet.GetBinError(200)
                htemp_qcd.SetName("qcd" + "_" + cut + "_" + region + "_" + hst)
                htemp_qcd.Add(htemp_ttbar, -1) #substract the ttbar from MC
                htemp_qcd.Add(htemp_zjet, -1)
                ##check error
                ## if hst is "mHH_l":
                ##     print "after", cut, region, htemp_qcd.GetBinCenter(200), "content:", htemp_qcd.GetBinContent(200), "sqrt:", ROOT.TMath.Sqrt(htemp_qcd.GetBinContent(200)), "err:", htemp_qcd.GetBinError(200)
                helpers.clear_negbin(htemp_qcd)
                htemp_qcd.Write()
                del(htemp_qcd)
                del(htemp_zjet)
                del(htemp_ttbar)
            #get qcd prediction shapes
            plttemp = outroot.Get("qcd" + "_" + cut + "_" + region + "_" + plt_m)
            if ("Signal" in region) & ("NoTag" not in cut) & CONF.blind:
                cutcounts[region] = 0
                cutcounts[region + "_err"] = 0
            else:
                err = ROOT.Double(0.)
                cutcounts[region] = plttemp.IntegralAndError(0, plttemp.GetXaxis().GetNbins()+1, err)
                cutcounts[region + "_err"] = float(err)
            del(plttemp)
        qcd[cut] = cutcounts
    return {histname: qcd}

def WriteEvtCount(inputdic, outFile, samplename="region"):
    ### 
    tableList = []
    ###
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c|c|c|c}")
    tableList.append("%s & Sideband & Control & Signal \\\\" % samplename)
    tableList.append("\\hline\\hline")
    tableList.append("& & & \\\\")

    for i, cut in enumerate(dump_lst):
        #get the corresponding region
        outstr = ""
        outstr += cut.replace("_", " ") 
        for j, region in enumerate(yield_region_lst):
            #get the mass plot
            outstr += " & "
            outstr += str(helpers.round_sig(inputdic[cut][region], 2))
            outstr += " $\\pm$ "
            outstr += str(helpers.round_sig(inputdic[cut][region + "_err"], 2))
            if region + "_syst_up" in inputdic[cut].keys():
                outstr += " $\\substack{"
                outstr += "+ " + str(helpers.round_sig(inputdic[cut][region+"_syst_up"], 2))
                outstr += "\\\\"
                outstr += "- " + str(helpers.round_sig(inputdic[cut][region+"_syst_down"], 2))
                outstr += "}$ "
                # if (ROOT.TMath.Sqrt(inputdic[cut][region]) > 0):
                #     outstr += " rel "
                #     outstr += " $\\substack{"
                #     outstr += "+ " + str(helpers.round_sig(inputdic[cut][region+"_syst_up"]/ROOT.TMath.Sqrt(inputdic[cut][region]), 2))
                #     outstr += "\\\\"
                #     outstr += "- " + str(helpers.round_sig(inputdic[cut][region+"_syst_down"]/ROOT.TMath.Sqrt(inputdic[cut][region]), 2))
                #     outstr += "}$ "
            else:
                outstr += " $\\pm$ sys"
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
    tableList.append("%s & Sideband & Control & Signal \\\\" % cut.replace("_", " "))
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
            # if region + "_syst_up" in inputdic[file][cut].keys():
            #     outstr += " $\\substack{"
            #     outstr += "+ " + str(helpers.round_sig(inputdic[file][cut][region+"_syst_up"], 2))
            #     outstr += "\\\\"
            #     outstr += "- " + str(helpers.round_sig(inputdic[file][cut][region+"_syst_down"], 2))
            #     outstr += "}$ "
            # else:
            #     outstr += " $\\pm$ sys"
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
    cutflow_temp = input_f.Get("CutFlowWeight")
    ###
    eventcounts = {}
    histcopies = []
    ###
    #outdir = outroot.mkdir(histname)
    #get things from cutflow table
    for i, cut in enumerate(evtsel_lst):
        eventcounts[cut] = cutflow_temp.GetBinContent(cutflow_temp.GetXaxis().FindBin(cut))
        eventcounts[cut+"_err"] = cutflow_temp.GetBinError(cutflow_temp.GetXaxis().FindBin(cut))
        #print histname, cut, eventcounts[cut], eventcounts[cut+"_err"]

    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            #print cut, region, config
            #deal with the other plots
            for hst in plt_lst:
                hst_temp = input_f.Get(cut + "_" + region + "/" + hst).Clone()
                hst_temp.SetName(histname + "_" + cut + "_" + region + "_" + hst)
                hst_temp.SetDirectory(0)
                
                if ("Signal" in region) & (("TwoTag_split" in cut) \
                    or ("ThreeTag" in cut) or ("FourTag" in cut)) & CONF.blind & (histname == "data"):
                    hst_temp.Reset()
                histcopies.append(hst_temp)
                
                if plt_m in hst:
                    if ("Signal" in region) & (("TwoTag_split" in cut) \
                        or ("ThreeTag" in cut) or ("FourTag" in cut)) & CONF.blind & (histname == "data"):
                        cutcounts[region] = 0
                        cutcounts[region + "_err"] = 0
                    else:
                        err = ROOT.Double(0)
                        cutcounts[region] = hst_temp.IntegralAndError(0, hst_temp.GetXaxis().GetNbins()+1, err)
                        err = float(err) #convert it back...so that python likes it
                        cutcounts[region + "_err"] = err

                # outroot.cd()
                # if ("Signal" in region) & (("TwoTag_split" in cut) \
                #     or ("ThreeTag" in cut) or ("FourTag" in cut)) & CONF.blind & (histname == "data"):
                #     hst_temp.Reset()
                # hst_temp.Write()
                # del(hst_temp)

            #get the mass plot
            plttemp = outroot.Get(histname + "_" + cut + "_" + region + "_" + plt_m)
            del(plttemp)
        #finish the for loop
        eventcounts[cut] = cutcounts

    #close the file before exit
    del(cutflow_temp)
    input_f.Close()
    #return the table
    return {histname: eventcounts}, histcopies

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
        integralbin_min, integralbin_max = GetMassWindow(h_signal, 0.68)   # or 0.95; the width contorl here
        
        S_err = ROOT.Double(0.)
        S = h_signal.IntegralAndError(integralbin_min, integralbin_max, S_err)

        B_err = ROOT.Double(0.)
        B = h_bkg.IntegralAndError(integralbin_min, integralbin_max, B_err)

        if S==0 or B==0:
            return(0, 0, S, B)
        # sensitivity = 1.0*S/ROOT.TMath.Sqrt(B)
        # sensitivity_err = sensitivity * ROOT.TMath.Sqrt((1.0*S_err/S)**2 + (1.0*B_err/(2*B))**2)
        ## a better definition for low stats
        #sensitivity = (1.0*S)/(1 + ROOT.TMath.Sqrt(B))
        #sensitivity_err = sensitivity * ROOT.TMath.Sqrt((1.0*S_err/S)**2 + (1./(4*B))*((1.0*B_err/(1+ROOT.TMath.Sqrt(B)))**2))
        ## real sensitivity, see https://www.pp.rhul.ac.uk/~cowan/stat/notes/SigCalcNote.pdf
        sensitivity = ROOT.TMath.Sqrt(2 * ((S + B) * ROOT.TMath.Log(1 + S / B) - S))
        sensitivity_err = (ROOT.TMath.Log(1 + S / B) * S_err + (ROOT.TMath.Log(1 + S / B) - S / B) * B_err) / sensitivity
        #return the sensitivity, error, number of signal and number of background estimated in this window
        return (sensitivity, sensitivity_err, S, B)

### 
def GetSignificance(mass):   
    histname =  "RSG1_" + str(mass)
    eventcounts = {}
    eventcounts_err = {}
    ### 
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        cutcounts_err = {}
        for j, region in enumerate(region_lst):
            #needs fix!!!
            plttemp_sig = outroot.Get("RSG1_" + str(mass) + "_" + cut + "_" + region + "_" + plt_m).Clone()
            plttemp_bkg = outroot.Get("data_est" + "_" + cut + "_" + region + "_" + plt_m).Clone()
            #needs to rebin here!!! use 50 GeV binning at least...
            plttemp_sig.Rebin(5)
            plttemp_bkg.Rebin(5)
            #can scale to a different lumi here; note this is only for significance tests!
            plttemp_sig.Scale(2.5)
            plttemp_bkg.Scale(2.5)
            cutcounts[region], cutcounts_err[region], S, B = GetSensitivity(plttemp_sig, plttemp_bkg)
            if mass == 2000 and region is "Signal":
                print "m:{:>5} c:{:>24} r:{:>8}; INFO-- sig:{:10.4f}  S:{:10.4f}  B:{:10.4f}  Entry:{:10.4f}".format(mass, cut, region, cutcounts[region], S, B, plttemp_sig.GetEntries())
            #get the mass plot
            # if ("Signal" in region) & (("OneTag" in cut) or ("TwoTag" in cut) \
            #     or ("ThreeTag" in cut) or ("FourTag" in cut)) & CONF.blind:\ 
            del(plttemp_sig)
            del(plttemp_bkg)
        eventcounts[cut] = cutcounts
        eventcounts_err[cut] = cutcounts_err 
    return {histname + "_sig_est": eventcounts, histname + "_sig_est_err": eventcounts_err}

### 
def DumpSignificance(inputdic):    
    ###
    outroot.cd()
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        for j, region in enumerate(region_lst):
            #for all the mass points:
            temp_plt = ROOT.TH1D("%s_%s_Significance" % (cut, region), ";mass, GeV; Significance", 62, -50, 6150)
            for mass in mass_lst:
                temp_plt.SetBinContent(temp_plt.GetXaxis().FindBin(mass), inputdic["RSG1_" + str(mass) + "_sig_est"][cut][region])
                temp_plt.SetBinError(temp_plt.GetXaxis().FindBin(mass), inputdic["RSG1_" + str(mass) + "_sig_est_err"][cut][region])
            temp_plt.Write()
            del(temp_plt)
    return 0


if __name__ == "__main__":
    main()
