import ROOT, rootlogon
import argparse
import array
import copy
import glob
import helpers
import os
import sys
import time

ROOT.gROOT.SetBatch(True)

def main():

    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir

    global inputpath
    inputpath = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/" + inputdir + "/"
    global outputpath
    outputpath = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/" + inputdir + "/" + "Plot/Tables/"
    global blind
    blind=True

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    #set global draw options
    global mass_lst
    mass_lst = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    global lowmass
    lowmass = 650
    global highmass
    highmass = 3150
    #create the cutflow dictionary
    masterinfo = {}
    # select the cuts
    global evtsel_lst, evtsel_dic
    evtsel_lst = ["All", "PassGRL", "PassTrig", "PassJetClean", "Pass2FatJets", "PassDiJetPt", "PassDetaHH", "PassSignal"]
    global datasel_lst, datasel_dic
    datasel_lst = ["All", "PassGRL", "PassTrig", "PassJetClean", "Pass2FatJets", "PassDiJetPt", "PassDetaHH"]
    datasel_dic = {"All":"Initial", "PassGRL":"Pass GRL", "PassTrig":"Pass Trigger", "PassJetClean":"Pass Jet Cleaning", \
     "Pass2FatJets":"N(fiducial large-R jets)$\geq 2$", "PassDiJetPt":"Pass Large-R jet Selection", "PassDetaHH":"$|\Delta\eta(JJ)|<1.7$"}
    global region_lst, region_dic
    region_lst = ["Sideband", "Control", "Signal"]
    region_dic = {"Sideband":"Sideband", "Control":"Control", "Signal":"Signal"}
    #region_dic = {"Sideband":"35.8<$R_{hh}<108$", "Control":"$X_{hh}>1.6$ and $R_{hh}<35.8$", "Signal":"$X_{hh}<1.6$"}
    global cut_lst, cut_dic
    cut_lst = ["NoTag", "OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
    cut_dic = {"NoTag":"0 b-tags", "OneTag":"1 b-tags", "TwoTag":"2 b-tags", "TwoTag_split":"2 b-tags, split", "ThreeTag":"3 b-tags", "FourTag":"4 b-tags"}
    global sample_lst
    sample_lst = ["data", "RSG1_1000", "RSG1_2000", "RSG1_3000", "ttbar", "zjet"]
    global mcsel_lst, mcsel_dic
    mcsel_lst = ["All", "Pass2FatJets", "PassDetaHH", "PassSignal", "TwoTag_split", "ThreeTag", "FourTag"]
    mcsel_dic = {"All":"Mini-ntuple Skimming", "Pass2FatJets":"2 large-R jets", "PassDetaHH":"$|\Delta\eta(JJ)|<1.7$", "PassSignal":"Signal Region", \
    "TwoTag_split":"2b split Signal Region", "ThreeTag":"3b Signal Region", "FourTag":"4b Signal Region"}

    #Get MC signal samples
    for mass in mass_lst:
        masterinfo["RSG1_" + str(mass)] = GetEvtCount(inputpath + "signal_G_hh_c10_M%i/hist-MiniNTuple.root" % mass, "RSG1_%i" % mass)

    #Get ttbar samples
    masterinfo["ttbar"] = GetEvtCount(inputpath + "ttbar_comb_test.root", "ttbar")
    # # Get Zjet samples
    masterinfo["zjet"] = GetEvtCount(inputpath + "zjets_test/hist-MiniNTuple.root", "zjet")
    # # Get Signal samples; do not unblind now
    masterinfo["data"] = GetEvtCount(inputpath + "data_test/hist-MiniNTuple.root", "data")

    # Draw the efficiency plot relative to the all normalization
    # print masterinfo
    # Write the data cutflow table
    data_outtex = open(outputpath + "cutflow.tex", "w")
    DataCutFlow(masterinfo, data_outtex)
    # Write the MC cutflow table
    MC_outtex = open(outputpath + "SignalEffTable_RSG_c10.tex", "w")
    MCCutFlow(masterinfo, MC_outtex)
    # Finish the work
    print("--- %s seconds ---" % (time.time() - start_time))

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

### 
def DataCutFlow(inputdic, outFile, samplename="region"):
    ### 
    tableList = []
    ###
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c|c|c|c|c|c|c}")
    tableList.append("Cut & Data & $m_{G}=1$TeV & $m_{G}=2$TeV & $m_{G}=3$TeV & $t\\bar{t}$ & $Z+jets$ \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& & & & & & \\\\")

    ### do the cuts based on cutflow table
    for i, cut in enumerate(datasel_lst):
        outstr = ""
        outstr += datasel_dic[cut]
        for k, sample in enumerate(sample_lst):
            outstr += " & "
            value = inputdic[sample][cut]
            outstr += str(helpers.round_sig(value, 2))
        outstr+="\\\\"
        tableList.append(outstr)
    ### do the cuts based on the number of entries in each plot
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        for j, region in enumerate(region_lst):
            outstr = ""
            outstr += cut_dic[cut]  + ", " + region_dic[region]
            #get the mass plot
            for k, sample in enumerate(sample_lst):
                outstr += " & "
                value = inputdic[sample][cut][region]
                if sample == "data" and region == "Signal" and (("TwoTag_split" in cut) \
                or ("ThreeTag" in cut) or ("FourTag" in cut)) and blind:
                    outstr += " blinded "
                else:
                    outstr += str(helpers.round_sig(value, 2))

            outstr+="\\\\"
            tableList.append(outstr)

    tableList.append("& & & & & & \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")
    tableList.append("\\end{footnotesize}")
    tableList.append("\\newline")

    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")


### 
def GetEvtCount(inputdir, histname=""):
    #get input file
    input_f = ROOT.TFile.Open(inputdir, "read")
    cutflow_temp = input_f.Get("CutFlowWeight") #notice here we use no weight for now!
    ###
    eventcounts = {}
    ### do the cuts based on the cutflow plot
    for i, cut in enumerate(evtsel_lst):
        eventcounts[cut] = cutflow_temp.GetBinContent(cutflow_temp.GetXaxis().FindBin(cut))
    ### do the cuts based on the number of entries in each plot
    for i, cut in enumerate(cut_lst):
        #get the corresponding region
        cutcounts = {}
        for j, region in enumerate(region_lst):
            #get the mass plot
            mHH_temp = input_f.Get(cut + "_" + region + "/" + "mHH_l").Clone()
            if ("Signal" in region) & (("OneTag" in cut) or ("TwoTag" in cut) \
                or ("ThreeTag" in cut) or ("FourTag" in cut)) & blind & (histname == "data"):
                cutcounts[region] = 0
            else:
                cutcounts[region] = mHH_temp.Integral(0, mHH_temp.GetXaxis().GetNbins()+1)
        #finish the for loop
        eventcounts[cut] = cutcounts

    #close the file before exit
    input_f.Close()
    #return the table
    return eventcounts

### 
def MCCutFlow(inputdic, outFile, samplename="region"):
    ### 
    tableList = []
    ###
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c|c|c|c|c|c|c|c}")
    tableList.append("Resonance Mass [GeV] & Mini-ntuple Skimming & 2 large-R jets & $\Delta\eta$ & Xhh < 1.6 & 2bs SR & 3b SR & 4b SR \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& & & & & & &\\\\")

    ### do the cuts based on the number of entries in each plot
    for i, mass in enumerate(mass_lst):
        #get the corresponding region
        outstr = ""
        outstr += str(mass)
        #get the mass plot
        for k, cut in enumerate(mcsel_lst):
            outstr += " & "
            value = 0
            if type(inputdic["RSG1_%i" % mass][cut]) is dict:
                value = inputdic["RSG1_%i" % mass][cut]["Signal"]
            else:
                value = inputdic["RSG1_%i" % mass][cut]
            outstr += str(helpers.round_sig(value, 2))
        outstr+="\\\\"
        tableList.append(outstr)

    tableList.append("& & & & & & &\\\\")
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")
    tableList.append("\\end{footnotesize}")
    tableList.append("\\newline")

    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")





if __name__ == "__main__":
    main()
