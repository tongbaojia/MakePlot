import ROOT, rootlogon
import argparse, array, copy, glob, os, sys, time
import helpers
import config as CONF

ROOT.gROOT.SetBatch(True)

def main():

    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir

    global channels
    channels=["SB58", "SB68", "SB78", "SB88", "SB98", "SB108", "SB128", "SB168", "SB999"]#, "b70", "b77", "b80", "b85", "b90"]

    global inputpath
    inputpath = CONF.inputpath
    global outputpath
    outputpath = CONF.outplotPath
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    global outputroot
    outputroot = ROOT.TFile.Open(outputpath + "temp.root", "recreate")
    # Fill the histogram from the table
    DrawFitParameters("4b")
    DrawFitParameters("3b")
    DrawFitParameters("2bs")
    DrawFitParameters("2b")
    DrawFitParameters("1b")
    # Finish the work
    print("--- %s seconds ---" % (time.time() - start_time))

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

### 
def DrawFitParameters(region="4b"):
    outputroot.cd()
    canv = ROOT.TCanvas(region + "_" + "mustudy", "mustudy", 800, 800)
    h_muqcd = ROOT.TH1D(region + "_" + "muqcd","muqcd",1,1,2)
    h_muqcd.SetMarkerStyle(20)
    h_muqcd.SetMarkerColor(1)
    h_muqcd.SetLineColor(1)
    h_muqcd.SetMarkerSize(1)
    h_muqcd.GetYaxis().SetTitle("#mu qcd")
    h_mutop = ROOT.TH1D(region + "_" + "mutop","mutop",1,1,2)
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
                h_muqcd.Fill(h_muqcd.GetXaxis().FindBin(ch), muqcd)
                h_muqcd.SetBinError(h_muqcd.GetXaxis().FindBin(ch), muqcd_err)
                h_mutop.Fill(h_mutop.GetXaxis().FindBin(ch), mutop)
                h_mutop.SetBinError(h_mutop.GetXaxis().FindBin(ch), mutop_err)
        f1.close()
    h_muqcd.SetMaximum(h_muqcd.GetMaximum() * 1.5)   
    h_muqcd.Draw("EPL")
    canv.SaveAs(outputpath + h_muqcd.GetName() + ".pdf")
    canv.Clear()
    h_mutop.SetMaximum(h_mutop.GetMaximum() * 1.5) 
    h_mutop.Draw("EPL")
    canv.SaveAs(outputpath + h_mutop.GetName() + ".pdf")
    canv.Close()


if __name__ == "__main__":
    main()

