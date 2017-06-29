import ROOT, rootlogon, helpers
import argparse, array, copy, glob,  os, sys, time
import config as CONF
try:
    import simplejson as json                 
except ImportError:
    import json  

ROOT.gROOT.SetBatch(True)

def main():

    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir

    global inputpath
    inputpath = CONF.inputpath + inputdir + "/"
    global outputpath
    outputpath = CONF.outputpath + inputdir + "/" + "Plot/Tables/"
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
    # select the cuts
    global evtsel_lst, evtsel_dic
    evtsel_lst = ["All", "PassGRL", "PassTrig", "PassJetClean", "Pass2FatJets", "PassDiJetPt", "PassDetaHH", "PassResVeto", "PassSignal"]
    global datasel_lst, datasel_dic
    datasel_lst = ["All", "PassGRL", "PassTrig", "PassJetClean", "Pass2FatJets", "PassDiJetPt", "PassDetaHH"]
    datasel_dic = {"All":"Initial", "PassGRL":"Pass GRL", "PassTrig":"Pass Trigger", "PassJetClean":"Pass Jet Cleaning", \
     "Pass2FatJets":"N(fiducial large-R jets)$\geq 2$", "PassDiJetPt":"Pass Large-R jet Selection", "PassDetaHH":"$|\Delta\eta(JJ)|<1.7$", 
     "PassResVeto":"Veto Resolved SR"}
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
    mcsel_dic = {"All":"Mini-ntuple Skimming", "Pass2FatJets":"2 large-R jets", "PassDetaHH":"$|\Delta\eta(JJ)|<1.7$", \
    "PassResVeto":"Veto Resolved SR", "PassSignal":"Signal Region", \
    "TwoTag_split":"2b split Signal Region", "ThreeTag":"3b Signal Region", "FourTag":"4b Signal Region"}

    #Get Materinfo
    #create the cutflow dictionary
    inputtex = inputpath + "/" + "sum_" + inputdir + ".txt"
    f1 = open(inputtex, 'r')
    masterinfo = json.load(f1)

    # Draw the efficiency plot relative to the all normalization
    # print masterinfo
    # Write the data cutflow table
    data_outtex = open(outputpath + "cutflow.tex", "w")
    DataCutFlow(masterinfo, data_outtex)
    data_outtex.close()
    # Write the MC cutflow table
    MC_outtex = open(outputpath + "SignalEffTable_RSG_c10.tex", "w")
    MCCutFlow(masterinfo, MC_outtex, keyword="RSG1")
    MC_outtex.close()
    if CONF.doallsig:
        # Write the MC cutflow table
        MC_outtex = open(outputpath + "SignalEffTable_RSG_c20.tex", "w")
        MCCutFlow(masterinfo, MC_outtex, keyword="RSG2")
        MC_outtex.close()
        # Write the 2HDM cutflow table
        Xhh_outtex = open(outputpath + "SignalEffTable_Xhh.tex", "w")
        MCCutFlow(masterinfo, Xhh_outtex, keyword="Xhh")
        Xhh_outtex.close()
    # Finish the work
    del(masterinfo)
    f1.close()
    print("--- %s seconds ---" % (time.time() - start_time))

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
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
            outstr += str(helpers.round_sig(inputdic[sample][cut], 2))
            outstr += " $\\pm$ "
            outstr += str(helpers.round_sig(inputdic[sample][cut+"_err"], 2))
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
                #print sample, cut, region
                if sample == "data" and region == "Signal" and (("TwoTag_split" in cut) \
                or ("ThreeTag" in cut) or ("FourTag" in cut)) and blind:
                    outstr += " blinded "
                else:
                    outstr += str(helpers.round_sig(inputdic[sample][cut][region], 2))
                    outstr += " $\\pm$ "
                    outstr += str(helpers.round_sig(inputdic[sample][cut][region + "_err"], 2))

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
def MCCutFlow(inputdic, outFile, keyword="RSG1"):
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
        if mass == 2750 and keyword == "RSG2":
            continue;
        #get the corresponding region
        outstr = ""
        outstr += str(mass)
        #get the mass plot
        for k, cut in enumerate(mcsel_lst):
            outstr += " & "
            value = 0
            value_err = 0
            if type(inputdic[keyword + "_%i" % mass][cut]) is dict:
                value = inputdic[keyword + "_%i" % mass][cut]["Signal"]
                value_err = inputdic[keyword + "_%i" % mass][cut]["Signal"+"_err"]
            else:
                value = inputdic[keyword + "_%i" % mass][cut]
                value_err = inputdic[keyword + "_%i" % mass][cut+"_err"]
            outstr += str(helpers.round_sig(value, 2))
            outstr += " $\\pm$ "
            outstr += str(helpers.round_sig(value_err, 2))
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
