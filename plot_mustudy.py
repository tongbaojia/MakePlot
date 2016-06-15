import ROOT, rootlogon
import argparse, array, copy, glob, os, sys, time, json
import helpers
import config as CONF
from ROOT import *
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
SetAtlasStyle()

ROOT.gROOT.SetBatch(True)


#this script is used to plot different mu qcd fit parameters as a funciton of the SB size
def main():

    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir

    global channels
    channels=["SB48", "SB58", "SB68", "SB78", "SB88", "SB98", "SB108", "SB128", "SB168", "SB999"]#, "b70", "b77", "b80", "b85", "b90"]

    global region_lst
    region_lst = ["Sideband", "Control", "ZZ", "Signal"]

    global inputpath
    inputpath = CONF.inputpath
    global outputpath
    outputpath = CONF.outplotpath + ""
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    global outputroot
    outputroot = ROOT.TFile.Open(outputpath + "temp.root", "recreate")
    # Fill the histogram from the table
    DrawFitParameters("Nb=4")
    DrawFitParameters("Nb=3")
    DrawFitParameters("Nb=2s")
    DrawFitParameters("Nb=2")
    DrawFitParameters("Nb=1")
    DrawUncertaintyCompare("FourTag")
    DrawUncertaintyCompare("ThreeTag")
    DrawUncertaintyCompare("TwoTag split")

    # Finish the work
    print("--- %s seconds ---" % (time.time() - start_time))

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

### 
def DrawFitParameters(region="4b"):
    outputroot.cd()
    canv = ROOT.TCanvas(region.replace("Nb=", "Nb") + "_" + "mustudy", "mustudy", 800, 800)
    h_muqcd = ROOT.TH1D(region.replace("Nb=", "Nb") + "_" + "muqcd","muqcd",1,1,2)
    h_muqcd.SetMarkerStyle(20)
    h_muqcd.SetMarkerColor(1)
    h_muqcd.SetLineColor(1)
    h_muqcd.SetMarkerSize(1)
    h_muqcd.GetYaxis().SetTitle("#mu qcd")
    h_mutop = ROOT.TH1D(region.replace("Nb=", "Nb") + "_" + "mutop","mutop",1,1,2)
    h_mutop.SetMarkerStyle(21)
    h_mutop.SetMarkerColor(1)
    h_mutop.SetLineColor(1)
    h_mutop.SetMarkerSize(1)
    h_mutop.GetYaxis().SetTitle("#mu top")

    for i, ch in enumerate(channels):
        inputtex = inputpath + ch + "/" + "/Plot/Tables/normfit.tex"
        f1 = open(inputtex, 'r')
        for line in f1: 
            #very stupid protection to distinguish 2b and 2bs
            if (region  + " ") in line:
                templine = line.split("&")
                tempqcd = templine[1].split(" ")
                muqcd = float(tempqcd[1])
                muqcd_err = float(tempqcd[3])
                temptop = templine[2].split(" ")
                mutop = float(temptop[1])
                mutop_err = float(temptop[3])
                #print tempqcd
                h_muqcd.Fill(ch, muqcd)
                h_muqcd.SetBinError(h_muqcd.GetXaxis().FindBin(ch), muqcd_err)
                h_mutop.Fill(ch, mutop)
                h_mutop.SetBinError(h_mutop.GetXaxis().FindBin(ch), mutop_err)
        f1.close()
    h_muqcd.SetMaximum(h_muqcd.GetMaximum() * 1.5)   
    h_muqcd.Draw("EPL")
    myText(0.5, 0.87, 1, "Region: %s" % region, 42)
    canv.SaveAs(outputpath + h_muqcd.GetName() + ".pdf")
    canv.Clear()
    h_mutop.SetMaximum(h_mutop.GetMaximum() * 1.5) 
    h_mutop.Draw("EPL")
    myText(0.5, 0.87, 1, "Region: %s" % region, 42)
    canv.SaveAs(outputpath + h_mutop.GetName() + ".pdf")
    canv.Close()



### 
def DrawUncertaintyCompare(Tags="FourTag"):
    outputroot.cd()
    canv = ROOT.TCanvas(Tags.replace(" ", "_") + "_" + "sigma_compare", "sigma_compare", 800, 800)
    xleg, yleg = 0.62, 0.7
    legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
    h_lst = []

    temp_h_max = 1
    for j, region in enumerate(region_lst):
        h_muqcd = ROOT.TH1D(Tags + "_" + region + "_" + "sigma_compare_SB", "sigma_compare;SB size",1,1,2)
        
        for i, ch in enumerate(channels):
            inputtex = inputpath + ch + "/" + "sum_" + ch + ".tex"
            f1 = open(inputtex, 'r')
            for line in f1: 
                #print line
                #very stupid protection to distinguish 2b and 2bs
                if (Tags) in line:
                    templine = line.split("&")
                    #print templine
                    tempqcd = templine[j + 1].split(" ")
                    tempqcd_syst_err =  tempqcd[5].split("\\\\") #this is the fit uncertainty
                    muqcd = float(tempqcd[1]) #this is the number of events
                    muqcd_err = float(tempqcd_syst_err[0]) #this is the fit uncertainty
                    #print tempqcd
                    h_muqcd.SetMarkerStyle(20 + j)
                    h_muqcd.SetMarkerColor(CONF.clr_lst[j])
                    h_muqcd.SetLineColor(CONF.clr_lst[j])
                    h_muqcd.SetMarkerSize(1)
                    h_muqcd.GetYaxis().SetTitle("#sigma_{Fit Syst}/#sigma_{Stat}")
                    h_muqcd.Fill(ch, muqcd_err/ROOT.TMath.Sqrt(muqcd))
                    h_muqcd.SetBinError(h_muqcd.GetXaxis().FindBin(ch), helpers.ratioerror(ROOT.TMath.Sqrt(muqcd), muqcd) * muqcd_err/ROOT.TMath.Sqrt(muqcd))

            f1.close()
        temp_h_max = max(temp_h_max, h_muqcd.GetMaximum())
        legend.AddEntry(h_muqcd, region, "apl")
        h_lst.append(h_muqcd)

    for j, h_muqcd in enumerate(h_lst):
        h_muqcd.SetMaximum(temp_h_max * 1.5)
        h_muqcd.Draw("EPL" if j== 0 else "same EPL")

    #myText(0.5, 0.87, 1, "Region: %s" % region, 42)
    legend.SetBorderSize(0)
    legend.SetMargin(0.3)
    legend.SetTextSize(0.04)
    legend.Draw()
    canv.SaveAs(outputpath + canv.GetName() + ".pdf")
    canv.Close()
    del(h_lst)

if __name__ == "__main__":
    main()

