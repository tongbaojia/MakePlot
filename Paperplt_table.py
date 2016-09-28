import ROOT, rootlogon, helpers
import help_table as help_table
import dump_merge as dump_merge
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
    outputpath = CONF.outputpath + inputdir + "/" + "PaperPlot/Tables/"
    global blind
    blind=True

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    #set global draw options
    #Get Materinfo
    #create the cutflow dictionary
    inputtex = inputpath + "/" + "sum_" + inputdir + ".txt"
    f1 = open(inputtex, 'r')
    masterinfo = json.load(f1)

    inputtex2 = inputpath + "/" + "sum_" + "syst" + ".txt"
    f2 = open(inputtex2, 'r')
    systinfo = json.load(f2)

    inputtex3 = inputpath + "/" + "sum_" + "syst_summary" + ".txt"
    f3 = open(inputtex3, 'r')
    summaryinfo = json.load(f3)

    # Write the SB/CR cutflow table
    SBCR_table(masterinfo)
    # Write the SR cutflow table
    SR_table(systinfo, summaryinfo)
    # Write the systematics table
    Syst_table(systinfo)
    #SBCR_table(masterinfo)
    # Finish the work
    del(masterinfo)
    f1.close()
    f2.close()
    f3.close()
    print("--- %s seconds ---" % (time.time() - start_time))

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default=CONF.workdir)
    return parser.parse_args()

###
def SBCR_table(masterdic):
    texoutpath = CONF.inputpath + "b77" + "/" + "PaperPlot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + "SBCR_table.tex", "w")
    tableList = []
    tag_lst = ["TwoTag_split", "ThreeTag", "FourTag"]
    region_lst = ["Sideband", "Control"]
    cut_lst = []
    cut_name_lst = []
    for t in tag_lst:
        for r in region_lst:
            cut_lst.append(t + "__" + r)
            cut_name_lst.append(r)
    help_table.add_table_head(tableList, cut_name_lst, title="Source", special_raw=tag_lst)
    raw_lst = ["qcd", "ttbar", "zjet", "data"]
    raw_lst_dic = {"qcd":"Multijet", "ttbar":"\\ttbar", "zjet":"$Z$+jet", "data":"Total"}
    #check and debug
    # keylist = masterdic.keys()
    # keylist.sort()
    # for key in keylist:
    #     print key, masterdic[key]
    for raw in raw_lst:
        #get the corresponding region
        outstr = ""
        outstr += raw_lst_dic[raw]
        #print masterdic, systag
        for c in cut_lst:
            if raw == "zjet":
                raw_tempname = raw
            else:
                raw_tempname = raw + "_est"
            err_fit  = 0
            if c.split("__")[1] + "_syst_muqcd_fit_up" in masterdic[raw_tempname][c.split("__")[0]].keys():
                err_fit = masterdic[raw_tempname][c.split("__")[0]][c.split("__")[1] + "_syst_muqcd_fit_up"]
                #print err_fit
            err_all  = helpers.syst_adderror(masterdic[raw_tempname][c.split("__")[0]][c.split("__")[1] + "_err"], err_fit)
            valuetuple = (masterdic[raw_tempname][c.split("__")[0]][c.split("__")[1]], err_all)
            outstr += help_table.add_entry(valuetuple)
        #finish the current entry
        outstr+="\\\\"
        tableList.append(outstr)
    #add data:
    tableList.append("\\hline")
    outstr = ""
    outstr += "Data"
    for c in cut_lst:
        valuetuple = (masterdic["data"][c.split("__")[0]][c.split("__")[1]], 
                masterdic["data"][c.split("__")[0]][c.split("__")[1] + "_err"])
        outstr += help_table.add_entry(valuetuple)
    outstr+="\\\\"
    tableList.append(outstr)
    #finish the table
    help_table.add_table_tail(tableList, cut_lst)
    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")
    outFile.close()

def SR_table(masterdic, summarydic):
    texoutpath = CONF.inputpath + "b77" + "/" + "PaperPlot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + "SR_table.tex", "w")
    tableList = []
    tag_lst = ["TwoTag_split", "ThreeTag", "FourTag"]
    region_lst = ["Signal"]
    cut_lst = []
    for t in tag_lst:
        for r in region_lst:
            cut_lst.append(t)
    help_table.add_table_head(tableList, cut_lst, title="Source")
    raw_lst = ["qcd", "ttbar", "totalbkg"]
    raw_lst_dic = {"qcd":"Multijet", "ttbar":"\\ttbar", "totalbkg":"Total"}
    #check and debug
    # keylist = masterdic.keys()
    # keylist.sort()
    # for key in keylist:
    #     print key, masterdic[key]
    for raw in raw_lst:
        #get the corresponding region
        outstr = ""
        outstr += raw_lst_dic[raw]
        #print masterdic, systag
        for c in cut_lst:   
            totalsyst = dump_merge.add_syst(summarydic[c][raw])[0]
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

def Syst_table(masterdic):
    texoutpath = CONF.inputpath + "b77" + "/" + "PaperPlot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + "Syst_table.tex", "w")
    tag_lst = ["TwoTag_split", "ThreeTag", "FourTag"]
    sample_lst = ["totalbkg", "RSG1_2000"]
    sample_dic = {"totalbkg":"Background", "RSG1_2000":"\\Grav(2\\,\\TeV)"}
    tableList = []
    column_lst = []
    column_name_lst = []
    column_dic = {}
    for t in tag_lst:
        for r in sample_lst:
            column_lst.append(t + "__" + r)
            column_name_lst.append(sample_dic[r])
    for col in column_lst:
        #print col
        column_dic[col] = {}
    ###this is super complicated...let's get them one by one
    help_table.add_table_head(tableList, column_name_lst, title="Source", special_raw=tag_lst)
    systag_lst = ["Lumi", "JER", "JMR", "tt", "Rtrk",  "EFF", "method", "Stat"]
    systag_dic = {"Lumi":"Luminosity", "JER":"JER", "JMR":"JMR", "tt":"\\ttbar MC", "Rtrk":"JES/JMS", "method":"Bkg Est", "EFF":"$b$-tagging", "Stat":"Statistical"}
    #systag_lst = {"method":"Bkg Est"}
    #add each systematics
    for systag in systag_lst:
        #get the corresponding region
        outstr = ""
        outstr += systag_dic[systag]
        #print masterdic, systag
        for temp_col in column_lst:
            col = temp_col.split("__")[1]
            c   = temp_col.split("__")[0]
            #print temp_col, col, systag
            if (systag == "Stat"):
                for key2 in masterdic[c]:
                    if col in key2:
                        outstr += help_table.add_entry(masterdic[c][key2]["int_err"]/masterdic[c][key2]["int"], doerr=False, percent=True)
                        temp_col_dic = {"stat":(masterdic[c][key2]["int_err"]/masterdic[c][key2]["int"], 0)}
                        column_dic[temp_col].update(temp_col_dic)
            elif (systag == "Lumi"):
                if ("RSG" in col):
                    outstr += help_table.add_entry((0.033, 0), doerr=False, percent=True)
                    temp_col_dic = {"Lumi":(0.033, 0)}
                    column_dic[temp_col].update(temp_col_dic)
                else:
                    outstr += help_table.add_entry((0, 0), doerr=False, percent=True)

            else:
                temp_col_dic = dump_merge.find_syst(masterdic, c, systag, col)
                outstr += help_table.add_entry(dump_merge.add_syst(temp_col_dic), doerr=False, percent=True)
                column_dic[temp_col].update(temp_col_dic)
        #finish the current entry
        outstr+="\\\\"
        tableList.append(outstr)

    #add all systematics:
    tableList.append("\\hline")
    outstr = ""
    outstr += "Total Sys"
    for temp_col in column_lst:
        outstr += help_table.add_entry(dump_merge.add_syst(column_dic[temp_col]), doerr=False, percent=True)
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


if __name__ == "__main__":
    main()
