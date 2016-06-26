import ROOT, rootlogon
import argparse, array, copy, glob, os, sys, time
import simplejson as json
import helpers
import config as CONF
#from ROOT import *
#ROOT.gROOT.LoadMacro("AtlasStyle.C") 
#ROOT.gROOT.LoadMacro("AtlasLabels.C")
#SetAtlasStyle()

ROOT.gROOT.SetBatch(True)

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="TEST_c10-cb")
    return parser.parse_args()

#this script is used to plot different mu qcd fit parameters as a funciton of the SB size
def main():

    start_time = time.time()
    ops = options()
    global inputdir
    inputdir = ops.inputdir

    global syst_lst
    syst_lst=["", "CR_High", "CR_Low", "CR_Small", "SB_Large", "SB_Small", "SB_High", "SB_Low"]#, "b70", "b77", "b80", "b85", "b90"]

    global region_lst
    region_lst = ["Sideband", "Control", "Signal"]

    global tag_lst
    tag_lst = ["FourTag", "ThreeTag", "TwoTag_split"]

    global inputpath
    inputpath = CONF.inputpath
    global outputpath
    outputpath = CONF.outplotpath + ""
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    global outputroot
    outputroot = ROOT.TFile.Open(outputpath + "temp.root", "recreate")
    # Fill the histogram from the table

    for tag in tag_lst:
        Dump_Compare(tag=tag, title="CR_Varations", region="Control")
        Dump_BKGCompare(tag=tag, title="SR_Varations", region="Signal")

    # Finish the work
    print("--- %s seconds ---" % (time.time() - start_time))

### 
def Dump_Compare(tag="FourTag", title="CR_Varations", region="Control"):

    texoutpath = inputpath + inputdir + "/" + "Plot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + tag + "_" + title + ".tex", "w")
    title += " " + tag
    column_lst = ["Data", "Prediction", "(Predict - Data)/Data"]
    column_key_lst = ["data", "data_est", "dataEstDiff"] #for looping through the objects
    ### 
    tableList = []
    ###
    add_table_head(tableList, column_lst, title=title)

    for i, syst in enumerate(syst_lst):
        #get the corresponding region
        outstr = ""
        outstr += syst.replace("_", " ") if syst is not "" else "Nominal"
        systpath = "_" + syst if syst is not "" else ""
        inputtex = inputpath + inputdir + (systpath + "/" + "sum_" + inputdir + systpath + ".txt")
        f1 = open(inputtex, 'r')
        masterdic = json.load(f1)
        #print masterdic, tag
        outstr += add_entry(masterdic["data"][tag][region], state=masterdic["data"][tag][region+"_err"])
        outstr += add_entry(masterdic["data_est"][tag][region], state=masterdic["data_est"][tag][region+"_err"])
        outstr += add_entry(masterdic["dataEstDiff"][tag][region], state=masterdic["dataEstDiff"][tag][region+"_err"], percent=True)
        #finish up
        del(masterdic)
        f1.close()
        #finish the current entry
        outstr+="\\\\"
        tableList.append(outstr)
        #add extra line
        if (syst!=syst_lst[-1]):
            tableList.append("\\hline")

    #finish the table
    add_table_tail(tableList, column_lst)

    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")


def Dump_BKGCompare(tag="FourTag", title="SR_Varations", region="Signal"):

    column_lst = ["Prediction", "QCD", "ttbar"]
    column_key_lst = ["data_est", "qcd_est", "ttbar_est"] #for looping through the objects
    texoutpath = inputpath + inputdir + "/" + "Plot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + tag + "_" + title + ".tex", "w")
    ### 
    tableList = []
    ###
    #start the table
    add_table_head(tableList, column_lst, title=" " + tag)
    ##save a temp value
    nominal = {}
    for i, syst in enumerate(syst_lst):
        #get the corresponding region
        outstr = ""
        outstr += syst.replace("_", " ") if syst is not "" else "Nominal"
        systpath = "_" + syst if syst is not "" else ""
        inputtex = inputpath + inputdir + (systpath + "/" + "sum_" + inputdir + systpath + ".txt")
        f1 = open(inputtex, 'r')
        masterdic = json.load(f1)
        #save the noiminal values
        if (syst is ""):
            for Types in column_key_lst:
                nominal[Types]  = helpers.round_sig(masterdic[Types][tag][region], 2)
                nominal[Types+"_err"]  = helpers.round_sig(masterdic[Types][tag][region+"_err"], 2)
        #print masterdic, tag
        for Types in column_key_lst:
            value = (masterdic[Types][tag][region]/nominal[Types] - 1) * 100
            error = helpers.ratioerror(masterdic[Types][tag][region], nominal[Types],
                masterdic[Types][tag][region+"_err"], nominal[Types+"_err"]) * 100
            outstr += add_entry(value, error, percent=True)
        #finish up
        del(masterdic)
        f1.close()
        #finish the current entry
        outstr+="\\\\"
        if (syst!=syst_lst[0]):
            tableList.append(outstr)

    #finish the table
    add_table_tail(tableList, column_lst)

    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")

#three funtions for generating tables!!!
def add_entry(value, state=None, percent=False):
    temstr = ""
    temstr += " & "
    temstr += str(helpers.round_sig(value, 2))
    temstr += " $\\%$ " if percent else ""
    if state is not None:
        temstr += " $\\pm$ "
        temstr += str(helpers.round_sig(state, 2))
        temstr += " $\\%$ " if percent else ""
    return temstr

def add_table_head(tableList, column_lst, title=""):
    title_lst = [title.replace("_", " ")] + column_lst
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c" + "{0}".format("|c" * len(column_lst)) + "}")
    tableList.append(" & ".join(title_lst) + " \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("{0}\\\\".format("& " * len(column_lst)))

def add_table_tail(tableList, column_lst):
    tableList.append("{0}\\\\".format("& " * len(column_lst)))
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")
    tableList.append("\\end{footnotesize}")
    tableList.append("\\newline")


if __name__ == "__main__":
    main()

