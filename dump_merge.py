import argparse, copy, os, sys, glob, math
from array import array
import ROOT, rootlogon
import Xhh4bUtils.BkgFit.smoothfit_Ultimate as smoothfit
import helpers, help_table
import config as CONF
ROOT.gROOT.SetBatch()
try:
    import simplejson as json                 
except ImportError:
    import json


treename  = "XhhMiniNtuple"
cut_lst = ["FourTag", "ThreeTag", "TwoTag_split"]
#setup fit initial values; tricky for the fits...

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    parser.add_argument("--chosenhist", default="l")
    return parser.parse_args()

def main():
    global ops
    ops = options()
    #setup basics;
    global bsyst
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
    print len(bsyst)
    global method_qcd_syst
    method_qcd_syst = [
    "smoothQ0up", 
    "smoothQ0down", 
    "smoothQ1up", 
    "smoothQ1down", 
    "smoothQ2up", 
    "smoothQ2down", 
    "smoothFuncup", 
    "smoothFuncdown",
    "normY0up",
    "normY0down",
    "normY1up",
    "normY1down",
    "normY2up",
    "normY2down",
    "normY3up",
    "normY3down",
    "normY4up",
    "normY4down",
    "normY5up",
    "normY5down",
    "QCDShapeCRup",
    "QCDShapeCRdown",
    "QCDNormCRup",
    "QCDNormCRdown",
    ]
    inputtasks = []
    inputtasks.append({"inputdir":"b77"})
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
    for i in range(1, len(bsyst)):
        # if i == 11 or i == 37 or i == 40 or i == 45:
        #     continue
        inputtasks.append({"inputdir":"syst_b_" + str(i)})

    #create output root files
    global outfiles
    outfiles = {}
    global finaldis
    finaldis = ops.chosenhist
    for c in cut_lst:
        outfiles[c]  = ROOT.TFile("%s/b77_limit_%s_fullsys%s.root" % (CONF.inputpath  + "b77/Limitinput", c, "" if "pole" not in finaldis else "_pole"), "Recreate")
    ##run it, order matters, because the pole file replaces the previous one!
    masterdic = {}
    masterdic.update(merge_method_sys())
    ##masterdic.update(merge_mc_sys(inputtasks[0]))
    for task in inputtasks:
        masterdic.update(merge_mc_sys(task))

    with open(CONF.inputpath + "b77/sum_syst" + ("" if "pole" not in finaldis else "_pole") + ".txt", "w") as f:
         json.dump(masterdic, f)

    keylist = masterdic.keys()
    keylist.sort()
    for key in keylist:
        print key, masterdic[key]

    #Generate systemtics table
    f1 = open(CONF.inputpath + "b77/sum_syst"+ ("" if "pole" not in finaldis else "_pole") + ".txt", 'r')
    masterdic = json.load(f1)
    summarydic = {}
    for c in cut_lst:
       summarydic[c] = GetTable(masterdic, c)
       plot_RSG_syst(masterdic, c)
       plot_RSG_syst_detail(masterdic, c)
    
    #save the summary dic
    with open(CONF.inputpath + "b77/sum_syst_summary" + ("" if "pole" not in finaldis else "_pole") + ".txt", "w") as f:
         json.dump(summarydic, f)
    #Generate Signal Region table
    GetSignalTable(masterdic, summarydic)
    #print masterdic
    for key, file in outfiles.iteritems():
        file.Close()
    f1.close()


def merge_mc_sys(config):
    inputdir = config["inputdir"]
    print inputdir,

    inputpath = CONF.inputpath + inputdir 
    outputpath = inputpath + "/Limitinput/"
    global pltoutputpath
    pltoutputpath = inputpath + "/Plot/"+ "Smooth/"
    global mass_lst
    mass_lst = CONF.mass_lst

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    outtablepath = inputpath + "/Plot/" + "/Tables/"
    if not os.path.exists(outtablepath):
        os.makedirs(outtablepath)

    infodic = {}
    postname = "_" +  inputdir
    if "b77" in postname:
        postname = ""
    elif "syst_b" in postname:#get the bsystematic name
        #print inputdir.split("_")
        postname = "_" + bsyst[int(inputdir.split("_")[-1])]

    for c in cut_lst:
        global infile
        infile  = ROOT.TFile("%s/%s_limit_%s.root" % (outputpath, inputdir, c + ("" if "pole" not in finaldis else "_pole")), "READ")
        #print c
        #get the mass plot
        tempdic = {}
        #find the correct outputfile
        outfiles[c].cd()
        histdic = {"data":"data_hh", "totalbkg_est":"totalbkg_hh", "qcd_est":"qcd_hh", "ttbar_est":"ttbar_hh", "zjet_est":"zjet_hh"}
        for mass in mass_lst:
            histdic.update({"RSG1_" + str(mass) + "_est" : "signal_RSG_c10_hh_m" + str(mass)})
        for histname, hist in histdic.iteritems():
            #print histname, infile.Get(hist).GetName()
            tempdic[histname]  =  GetIntegral(infile.Get(hist).Clone(hist + postname), outfiles[c])
        infodic[c + postname] = tempdic
        infile.Close()

    print postname, "Done! "
    return infodic

def merge_method_sys():
    #find Michael's file
    infodic = {}
    inputpath = CONF.toppath + "/MakePlot/Xhh4bUtils/mHH_" + finaldis
    for c in cut_lst:
        infile  = ROOT.TFile("%s/outfile_boosted_%s.root" % (inputpath, c), "READ")

        for syst in method_qcd_syst:
            hist_temp_qcd   = infile.Get("qcd_hh").Clone("qcd_hh_" + syst)
            hist_temp_ttbar   = infile.Get("ttbar_hh").Clone("ttbar_hh_" + syst)
            infile.cd()
            for key in ROOT.gDirectory.GetListOfKeys():
                #print key.GetName()
                if ("qcd_hh_" + syst) in key.GetName():
                    hist_temp_qcd   = infile.Get("qcd_hh_" + syst).Clone("qcd_hh_" + syst)
                if ("ttbar_hh_" + syst) in key.GetName():
                    hist_temp_ttbar   = infile.Get("ttbar_hh_" + syst).Clone("ttbar_hh_" + syst)
            #total bkg   
            hist_temp_total   = hist_temp_qcd.Clone("totalbkg_hh_" + syst)
            hist_temp_total.Add(hist_temp_ttbar, 1)
            tempdic = {}
            tempdic["qcd_est"]    =  GetIntegral(hist_temp_qcd, outfiles[c])
            tempdic["ttbar_est"]  =  GetIntegral(hist_temp_ttbar, outfiles[c])
            tempdic["totalbkg_est"]  =  GetIntegral(hist_temp_total, outfiles[c])
            infodic[c + "_method_" + syst] = tempdic


        infile.Close()
    return infodic

def GetIntegral(hist, outfile):
    #print hist.GetName()
    tempdic = {}
    err = ROOT.Double(0.)
    tempdic["int"] = hist.IntegralAndError(0, hist.GetXaxis().GetNbins()+1, err)
    tempdic["int" + "_err"] = float(err)
    outfile.cd()
    hist.Write()
    del hist
    return tempdic

def GetTable(masterdic, c):
    texoutpath = CONF.inputpath + "b77" + "/" + "Plot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + c + "_fullsyst" + ("" if "pole" not in finaldis else "_pole") + ".tex", "w")
    tableList = []
    column_lst = ["totalbkg", "qcd", "ttbar", "RSG1_1000", "RSG1_2000", "RSG1_3000"]
    column_dic = {}
    for col in column_lst:
        column_dic[col] = {}
    ###this is super complicated...let's get them one by one
    help_table.add_table_head(tableList, column_lst, title=c)
    systag_lst = {"JER":"JER", "JMR":"JMR", "Rtrk":"JES/JMS", "method":"Bkg Est", "EFF":"b-tag SF"}
    #systag_lst = {"method":"Bkg Est"}
    #add each systematics
    for systag, systagname in systag_lst.iteritems():
        column_dic[systag] = {}
        #get the corresponding region
        outstr = ""
        outstr += systagname
        #print masterdic, systag
        for col in column_lst:
            #print col, systag
            temp_col_dic = find_syst(masterdic, c, systag, col)
            outstr += help_table.add_entry(add_syst(temp_col_dic), doerr=False, percent=True)
            column_dic[col].update(temp_col_dic)
        #finish the current entry
        outstr+="\\\\"
        tableList.append(outstr)
    #add all systematics:
    tableList.append("\\hline")
    outstr = ""
    outstr += "Total Sys"
    for col in column_lst:
        outstr += help_table.add_entry(add_syst(column_dic[col]), doerr=False, percent=True)
    outstr+="\\\\"
    tableList.append(outstr)
    #add all stat uncertainty:
    tableList.append("\\hline")
    outstr = ""
    outstr += "Stat"
    for col in column_lst:
        for key2 in masterdic[c]:
            if col in key2:
                outstr += help_table.add_entry(masterdic[c][key2]["int_err"]/masterdic[c][key2]["int"], doerr=False, percent=True)
    outstr+="\\\\"
    tableList.append(outstr)

    #add all values:
    tableList.append("\\hline")
    outstr = ""
    outstr += "Estimated Events"
    for col in column_lst:
        for key2 in masterdic[c]:
            if col in key2:
                outstr += help_table.add_entry(masterdic[c][key2]["int"], doerr=False, percent=False)
    outstr+="\\\\"
    tableList.append(outstr)


    #finish the table
    help_table.add_table_tail(tableList, column_lst)
    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")

    outFile.close()
    return column_dic

#find a bunch of systematics
def find_syst(masterdic, c, systag, col):
    debug = False
    sys_lst = {}
    #loopoing throught the dictionary
    for key1 in masterdic:#get to the 2b/3b/4b region; containes the systemtaic info as well
        if (c in key1) and (systag in key1):
            for key2 in masterdic[key1]:#get to the qcd/ttbar/rsg region
                if col in key2:
                    if debug: 
                        print systag, col, key1, key2
                    value_def  = abs(masterdic[key1][key2]["int"] / masterdic[c][key2]["int"] - 1) 
                    value_def_err  = abs(helpers.ratioerror(masterdic[key1][key2]["int"], masterdic[c][key2]["int"], masterdic[key1][key2]["int_err"], masterdic[c][key2]["int_err"]))
                    sys_lst.update({key1: (value_def, value_def_err)})
    return sys_lst

#add them up!
def add_syst(sys_lst):
    value = 0
    value_err = 0

    for sysname, temp in sys_lst.iteritems():
        #print sysname, temp
        value_temp = temp[0]
        value_temp_err = temp[1]
        if "up" in sysname:
            value_temp = max(sys_lst[sysname][0], sys_lst[sysname.replace("up", "down")][0])
            value_temp_err = max(sys_lst[sysname][1], sys_lst[sysname.replace("up", "down")][1])
        elif "down" in sysname:
            value_temp = 0
            value_temp_err = 0
        value = ROOT.TMath.Sqrt(value_temp ** 2 + value ** 2)
        value_err += value_temp_err * value_temp
    #compute!
    value_err = 0 if value == 0 else value_err/value
    return (value, value_err)

#singal region table
def GetSignalTable(masterdic, summarydic):
    texoutpath = CONF.inputpath + "b77" + "/" + "Plot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + "SR_summary.tex", "w")
    tableList = []
    help_table.add_table_head(tableList, cut_lst, title="Sample")
    raw_lst = ["qcd", "ttbar", "totalbkg"]
    for raw in raw_lst:
        #get the corresponding region
        outstr = ""
        outstr += raw
        #print masterdic, systag
        for c in cut_lst:   
            totalsyst = add_syst(summarydic[c][raw])[0]
            valuetuple = (masterdic[c][raw + "_est"]["int"], totalsyst * masterdic[c][raw + "_est"]["int"])
            outstr += help_table.add_entry(valuetuple)
        #finish the current entry
        outstr+="\\\\"
        tableList.append(outstr)
    #add data:
    tableList.append("\\hline")
    outstr = ""
    outstr += "Data"
    for c in cut_lst:
        outstr += help_table.add_entry((masterdic[c]["data"]["int"], masterdic[c]["data"]["int_err"]))
    outstr+="\\\\"
    tableList.append(outstr)
    #finish the table
    help_table.add_table_tail(tableList, cut_lst)
    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")
    outFile.close()

def plot_RSG_syst(masterdic, cut):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region
    canv = ROOT.TCanvas(cut  + "_" +  "RSG" + "_" + "syst", "Sytematics", 800, 800)
    xleg, yleg = 0.52, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    # load input MC file
    mass_lst = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    systag_lst = ["JER", "JMR", "Rtrk", "EFF", "Stat"]
    systag_dic = {"JER":"JER", "JMR":"JMR", "Rtrk":"JES/JMS", "EFF":"b-tag SF", "Stat":"Stats"}
    eff_lst = []
    graph_lst = []
    maxbincontent = 100.0
    minbincontent = -0.001
    lowmass  = 950
    highmass = 3150

    for i, syst in enumerate(systag_lst):
        eff_lst.append( ROOT.TH1F(syst, "%s; Mass, GeV; Systematic Percentage Diff" %syst, int((highmass-lowmass)/100), lowmass, highmass) )
        for mass in mass_lst:
            if syst is "Stat":
                for key2 in masterdic[cut]:
                    if "RSG1_" + str(mass) in key2:
                        eff_lst[i].SetBinContent(eff_lst[i].GetXaxis().FindBin(mass), masterdic[cut][key2]["int_err"]/masterdic[cut][key2]["int"] * 100)
                        eff_lst[i].SetBinError(eff_lst[i].GetXaxis().FindBin(mass), 0)
            else:
                temp_col_dic = find_syst(masterdic, cut, syst, "RSG1_" + str(mass))
                syst_eff = add_syst(temp_col_dic) #this is a tuple!
                eff_lst[i].SetBinContent(eff_lst[i].GetXaxis().FindBin(mass), syst_eff[0] * 100)
                eff_lst[i].SetBinError(eff_lst[i].GetXaxis().FindBin(mass), 0)
            #print syst_eff[0]
            maxbincontent = max(maxbincontent, syst_eff[0])
        #start the canvas
        canv.cd()
        #convert it to a TGraph
        graph_lst.append(helpers.TH1toTAsym(eff_lst[i]))
        graph_lst[i].SetLineColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerStyle(20 + i)
        graph_lst[i].SetMarkerColor(CONF.clr_lst[i])
        graph_lst[i].SetMarkerSize(1)
        graph_lst[i].SetMaximum(maxbincontent * 1.5)
        graph_lst[i].SetMinimum(minbincontent)
        legend.AddEntry(graph_lst[i], systag_dic[syst].replace("_", " "), "apl")
        if syst==systag_lst[0]: 
            graph_lst[i].Draw("APC")
            #gr.Draw("same L hist")
        else: 
            graph_lst[i].Draw("PC")
            #gr.Draw("same L hist")

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()
    # draw reference lines
    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    watermarks = [atlas, hh4b, lumi]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()
    # finish up
    helpers.checkpath(CONF.inputpath + ops.inputdir + "/" + "Plot/Syst/")
    canv.SaveAs(CONF.inputpath + ops.inputdir + "/" + "Plot/Syst/"  +  canv.GetName() + ".pdf")
    canv.Close()

def plot_RSG_syst_detail(masterdic, cut):
    ### the first argument is the input directory
    ### the second argument is the output prefix name
    ### the third argument is relative to what normalization: 0 for total number of events
    ### 1 for signal mass region
    canv = ROOT.TCanvas(cut  + "_" +  "RSG" + "_" + "syst_detail", "Sytematics", 800, 800)
    xleg, yleg = 0.52, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    # setup basic plot parameters
    # load input MC file
    mass_lst = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
    eff_lst = []
    graph_lst = []
    maxbincontent = 100.0
    minbincontent = -0.001
    lowmass  = 950
    highmass = 3150

    #create bsyst list
    bsyst_lst = []
    for i in bsyst:
        if "up" in i:
            bsyst_lst.append(i.replace("up", ""))

    #now loop
    draw_counter = 0
    for i, syst in enumerate(bsyst_lst):
        eff_lst.append( ROOT.TH1F(syst, "%s; Mass, GeV; Systematic Percentage Diff" %syst, int((highmass-lowmass)/100), lowmass, highmass) )
        maxsyst = 0.0
        for mass in mass_lst:
            temp_col_dic = find_syst(masterdic, cut, syst, "RSG1_" + str(mass))
            syst_eff = add_syst(temp_col_dic) #this is a tuple!
            # if (syst_eff[0] * 100 < 3): #if the systematic contribution is less than 3 percent
            #     continue
            eff_lst[i].SetBinContent(eff_lst[i].GetXaxis().FindBin(mass), syst_eff[0] * 100)
            eff_lst[i].SetBinError(eff_lst[i].GetXaxis().FindBin(mass), 0)
            print syst, syst_eff[0]
            maxbincontent = max(maxbincontent, syst_eff[0] * 100)
            maxsyst = max(maxsyst, syst_eff[0] * 100)
        #start the canvas
        canv.cd()
        #convert it to a TGraph
        graph_lst.append(helpers.TH1toTAsym(eff_lst[i]))
        if maxsyst < 3:#don't draw everything
            continue
        graph_lst[i].SetLineColor(CONF.clr_lst[draw_counter])
        graph_lst[i].SetMarkerStyle(20 + draw_counter)
        graph_lst[i].SetMarkerColor(CONF.clr_lst[draw_counter])
        graph_lst[i].SetMarkerSize(1)
        graph_lst[i].SetMaximum(maxbincontent * 1.5)
        graph_lst[i].SetMinimum(minbincontent)
        legend.AddEntry(graph_lst[i], syst.replace("_", " "), "apl")
        if draw_counter==0: 
            graph_lst[i].Draw("APC")
            draw_counter += 1
        else: 
            graph_lst[i].Draw("PC")
            draw_counter += 1

    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()
    # draw reference lines
    # draw watermarks
    xatlas, yatlas = 0.35, 0.87
    atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
    hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "RSG c=1.0")
    lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "MC #sqrt{s} = 13 TeV")
    watermarks = [atlas, hh4b, lumi]
    for wm in watermarks:
        wm.SetTextAlign(22)
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
        wm.SetNDC()
        wm.Draw()
    # finish up
    helpers.checkpath(CONF.inputpath + ops.inputdir + "/" + "Plot/Syst/")
    canv.SaveAs(CONF.inputpath + ops.inputdir + "/" + "Plot/Syst/"  +  canv.GetName() + ".pdf")
    canv.Close()

if __name__ == '__main__': 
    main()
