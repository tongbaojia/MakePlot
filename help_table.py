import argparse, copy, os, sys, glob, math
from array import array
import ROOT
import helpers
import config as CONF
ROOT.gROOT.SetBatch()

#singal region table
def TableExample(masterdic, summarydic):
    texoutpath = CONF.inputpath + "b77" + "/" + "Plot/Tables/"
    if not os.path.exists(texoutpath):
        os.makedirs(texoutpath)
    outFile = open( texoutpath + "SR_summary.tex", "w")
    tableList = []
    add_table_head(tableList, cut_lst, title="Sample")
    raw_lst = ["qcd", "ttbar", "totalbkg"]
    for raw in raw_lst:
        #get the corresponding region
        outstr = ""
        outstr += raw
        #print masterdic, systag
        for c in cut_lst:   
            totalsyst = add_syst(summarydic[c][raw])[0]
            valuetuple = (masterdic[c][raw + "_est"]["int"], totalsyst * masterdic[c][raw + "_est"]["int"])
            outstr += add_entry(valuetuple)
        #finish the current entry
        outstr+="\\\\"
        tableList.append(outstr)
    #add data:
    tableList.append("\\hline")
    outstr = ""
    outstr += "Data"
    for c in cut_lst:
        outstr += add_entry((masterdic[c]["data"]["int"], masterdic[c]["data"]["int_err"]))
    outstr+="\\\\"
    tableList.append(outstr)
    #finish the table
    add_table_tail(tableList, cut_lst)
    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")
    outFile.close()

def add_entry(valuetuple, doerr=True, percent=False):
    '''add the entry: tuple or value, 
    option of filling the error and as a percentage'''
    temstr = ""
    temstr += " & "
    if isinstance(valuetuple, tuple):
        if valuetuple[0] == 0:
            temstr += " - " 
            return temstr
        else:
            temstr += str(helpers.round_sig(valuetuple[0] * (100 if percent else 1), 2)) 
            if doerr:
                temstr += " $\\pm$ "
                temstr += str(helpers.round_sig(valuetuple[1] * (100 if percent else 1), 2)) #cause sqrt(a^2 + b^2) is sigma*a/sqrt(a^2 + b^2) 
    else:
        temstr += str(helpers.round_sig(valuetuple * (100 if percent else 1), 2)) 
    return temstr


def add_table_head(tableList, column_lst, title="", special_raw=None):
    '''add the table header: the string, the columns and the title'''
    title_lst = [title.replace("_", " ")]
    for t in column_lst:
        title_lst.append(t.replace("_", " "))
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c" + "{0}".format("|c" * len(column_lst)) + "}")
    if special_raw is not None:
        special_lst = [" "]
        for s in special_raw:
            special_lst.append("{" + s.replace("_", " ") + "}")
        tableList.append(" & \multicolumn{2}{c}".join(special_lst) + " \\\\")
    tableList.append(" & ".join(title_lst) + " \\\\")
    tableList.append("\\hline\\hline")
    #tableList.append("{0}\\\\".format("& " * len(column_lst)))

def add_table_tail(tableList, column_lst):
    '''add the table ending line: the string, the columns'''
    #tableList.append("{0}\\\\".format("& " * len(column_lst)))
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")
    tableList.append("\\end{footnotesize}")
    tableList.append("\\newline")

if __name__ == '__main__': 
    main()
