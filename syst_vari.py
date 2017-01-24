import ROOT, rootlogon
import argparse, array, copy, glob, os, sys, time
try:
    import simplejson as json                 
except ImportError:
    import json 
import helpers
import config as CONF
#from ROOT import *
#ROOT.gROOT.LoadMacro("AtlasStyle.C") 
#ROOT.gROOT.LoadMacro("AtlasLabels.C")
#SetAtlasStyle()

ROOT.gROOT.SetBatch(True)

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
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
        #for SR region shape variations
        for inputname in syst_lst:
            if inputname is not "":
                #DrawSRcomparison(inputname=inputname, tag=tag, keyword="totalbkg_hh")
                DrawSRcomparison(inputname=inputname, tag=tag, keyword="qcd_hh")

    #for ZZ unblinding
    Dump_ZZCompare(title="ZZ_Signal_Region", region="Signal")

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

def Dump_ZZCompare(title="ZZ_Signal_Region", region="Signal"):

    texoutpath = inputpath + inputdir + "/" + "Plot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + title + ".tex", "w")
    column_lst = ["Data", "Prediction", "(Predict - Data)/Data"]
    column_key_lst = ["data", "data_est", "dataEstDiff"] #for looping through the objects
    ### 
    tableList = []
    ###
    add_table_head(tableList, column_lst, title=title)

    for i, tag in enumerate(tag_lst):
        #get the corresponding region
        outstr = ""
        outstr += tag.replace("_", " ") if tag is not "" else "Nominal"
        inputtex = inputpath + inputdir + ("_ZZ" + "/" + "sum_" + inputdir + "_ZZ" + ".txt")
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
        if (tag!=tag_lst[-1]):
            tableList.append("\\hline")

    #finish the table
    add_table_tail(tableList, column_lst)

    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")

def DrawSRcomparison(inputname="CR_High", tag="", keyword="totalbkg_hh", prename="", Xrange=[0, 0], Yrange=[0, 0], norm=True, Logy=0):
    #print inputdir, inputname
    histdir   = inputdir + "_" + inputname
    inputroot = ROOT.TFile.Open(CONF.inputpath + "/" + histdir +  "/Limitinput/" + histdir + "_limit_" + tag  + ".root")
    refroot   = ROOT.TFile.Open(CONF.inputpath + "/" + inputdir  + "/Limitinput/" + inputdir + "_limit_" + tag  + ".root")
    
    tempname = inputname + "_" + "compare" + "_" + tag + "_" + keyword + ("" if Logy == 0 else "_" + str(Logy))
    canv = ROOT.TCanvas(tempname, tempname, 800, 800)
    canv.SetLogy(Logy)
    xleg, yleg = 0.5, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.15, yleg+0.2)
    counter = 0
    maxbincontent = (0.2 if Logy ==0 else 10)


    temp_hist = inputroot.Get(keyword)
    #print temp_hist.GetName()
    temp_hist.SetLineColor(2)
    temp_hist.SetMarkerStyle(20)
    temp_hist.SetMarkerColor(2)
    temp_hist.SetMarkerSize(1)

    ref_hist = refroot.Get(keyword)
    #print temp_hist.GetName()
    ref_hist.SetLineColor(1)
    ref_hist.SetMarkerStyle(21)
    ref_hist.SetMarkerColor(1)
    ref_hist.SetMarkerSize(1)

    #scale to correct normalization diff
    #temp_hist.Scale(ref_hist.Integral()/temp_hist.Integral())

    #continue
    maxbincontent = max(maxbincontent, ref_hist.GetMaximum(), temp_hist.GetMaximum())
    temp_hist.SetMaximum(maxbincontent * 1.5 * 100)
    ref_hist.SetMaximum(maxbincontent * 1.5 * 100)
    legend.AddEntry(temp_hist, inputname.replace("_", " "), "apl")
    legend.AddEntry(ref_hist, "ref", "apl")


    # top pad
    pad0 = ROOT.TPad("pad0", "pad0", 0.0, 0.31, 1., 1.)
    pad0.SetLogy(1)
    pad0.SetRightMargin(0.05)
    pad0.SetBottomMargin(0.0001)
    pad0.SetFrameFillColor(0)
    pad0.SetFrameBorderMode(0)
    pad0.SetFrameFillColor(0)
    pad0.SetBorderMode(0)
    pad0.SetBorderSize(0)

    pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.0, 1., 0.30)
    pad1.SetRightMargin(0.05)
    pad1.SetBottomMargin(0.38)
    pad1.SetTopMargin(0.0001)
    pad1.SetFrameFillColor(0)
    pad1.SetFillStyle(0) # transparent
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(0)

    canv.cd()
    pad0.Draw()
    pad0.cd()

    temp_hist.Draw("")
    ref_hist.Draw("same")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()

    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, tag.replace("_", " "))
    watermarks = [atlas, hh4b]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()


    canv.cd()
    pad1.Draw()
    pad1.cd()

    #ratio of the two plots
    ratiohist = temp_hist.Clone("ratio")
    ratiohist.Divide(ref_hist)
    ratiohist.GetYaxis().SetRangeUser(0.8, 1.2) #set range for ratio plot
    ratiohist.GetYaxis().SetTitle("Varaition/Nominal") #set range for ratio plot
    ratiohist.GetYaxis().SetTitleFont(43)
    ratiohist.GetYaxis().SetTitleSize(28)
    ratiohist.GetYaxis().SetLabelFont(43)
    ratiohist.GetYaxis().SetLabelSize(28)
    ratiohist.GetYaxis().SetNdivisions(405)
    ratiohist.GetXaxis().SetTitleFont(43)
    ratiohist.GetXaxis().SetTitleOffset(3.5)
    ratiohist.GetXaxis().SetTitleSize(28)
    ratiohist.GetXaxis().SetLabelFont(43)
    ratiohist.GetXaxis().SetLabelSize(28)
    ratiohist.Draw("")

    xMin = ref_hist.GetXaxis().GetBinLowEdge(1)
    xMax = ref_hist.GetXaxis().GetBinUpEdge(ref_hist.GetXaxis().GetNbins())
    line = ROOT.TLine(xMin, 1.0, xMax, 1.0)
    line.SetLineStyle(1)
    line.Draw()
    #canv.SetLogy(1)
    helpers.checkpath(CONF.inputpath + inputdir + "/Plot/Syst/")
    canv.SaveAs(CONF.inputpath + inputdir + "/Plot/Syst/" + canv.GetName() + ".pdf")
    pad0.Close()
    pad1.Close()
    canv.Close()
    inputroot.Close()
    refroot.Close()

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

