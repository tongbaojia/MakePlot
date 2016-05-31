import argparse, array, copy, os, sys, glob
import ROOT, rootlogon
import Xhh4bUtils.BkgFit.smoothfit as smoothfit
from helpers import round_sig
import confg as CONF
ROOT.gROOT.SetBatch()


treename  = "XhhMiniNtuple"
cut_lst = ["FourTag", "ThreeTag", "TwoTag_split"]

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

def main():
    ops = options()
    global inputdir
    inputdir = ops.inputdir
    #setup basics
    dump()
    dump("pole")

def dump(finaldis="l"):

    pltname = "_" + finaldis
    inputpath = CONF.inputpath + inputdir 
    outputpath = inputpath + "/Limitinput/"
    global pltoutputpath
    pltoutputpath = inputpath + "/Plot/"+ "Smooth/"
    ifile = ROOT.TFile(inputpath + "/" + "sum_" + inputdir + ".root")
    global mass_lst
    mass_lst = CONF.mass_lst

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    outtablepath = inputpath + "/Plot/" + "/Tables/"
    if not os.path.exists(outtablepath):
        os.makedirs(outtablepath)

    masterdic = {}
    for c in cut_lst:
        print "start ", c, " file conversion "
        global outfile
        outfile  = ROOT.TFile("%s/%s_limit_%s.root" % (outputpath, inputdir, c), "RECREATE")
        #get the mass plot
        tempdic = {}
        cut = c + "_Signal_mHH" + pltname
        #cut = c + "_Signal_mHH_pole"
        savehist(ifile, "data_est_" + cut,  "data_hh")#blind data now
        tempdic["data_est"] = savehist(ifile, "data_est_" + cut,  "totalbkg_hh", dosmooth=True)
        tempdic["qcd_est"] = savehist(ifile, "qcd_est_" + cut,   "qcd_hh", dosmooth=True)
        tempdic["ttbar_est"] = savehist(ifile, "ttbar_est_" + cut, "ttbar_hh", dosmooth=True, smoothrange = (875, 2500), smoothfunc="Dijet")
        savehist(ifile, "zjet_" + cut,      "zjet_hh")

        for mass in mass_lst:
            savehist(ifile, "RSG1_" + str(mass) + "_" + cut, "signal_RSG_c10_hh_m" + str(mass))
        outfile.Close()

        makeSmoothedMJJPlots("%s/%s_limit_%s.root" % (outputpath, inputdir, c), pltoutputpath + c + pltname + "_smoothed.pdf")

        masterdic[c] = tempdic

    #print masterdic
    fit_outtex = open(outtablepath + "smoothfit" + pltname + ".tex", "w")
    WriteFitResult(masterdic, fit_outtex)

    ifile.Close()
    print "Done! "

def savehist(inputroot, inname, outname, dosmooth=False, smoothrange = (1000, 3200), smoothfunc="Dijet"):
    hist  = inputroot.Get(inname).Clone()
    if dosmooth:
        sm = smoothfit.smoothfit(hist, fitFunction = smoothfunc, fitRange = smoothrange, \
            makePlots = True, verbose = False, outfileName=inname, ouutfilepath=pltoutputpath)
        hist = smoothfit.MakeSmoothHistoWithError(hist, sm)
    hist.SetName(outname)
    hist.SetTitle(outname)
    #hist.SetBins(60, 200, 3200)
    outfile.cd()
    hist.Write()

    if dosmooth:
        return sm["res"]

### 
def WriteFitResult(inputdic, outFile, npar=3):
    ### 
    tableList = []
    ###
    tableList.append("\\begin{footnotesize}")
    tableList.append("\\begin{tabular}{c|c|c|c|c|c|c}")
    tableList.append("Region & $ a_{t\\bar{t}}$ & $ b_{t\\bar{t}}$ & $ c_{t\\bar{t}}$ & $ a_{qcd}$ & $ b_{qcd}$ & $c_{qcd}$ \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& & & & & &\\\\")

    for i, cut in enumerate(cut_lst):
    #get the mass plot
        outstr = ""
        outstr += cut.replace("_", " ")
        outstr += " & "
        #print inputdic[cut]["ttbar_est"]["paramerrs"][0]
        outstr += str(round_sig(inputdic[cut]["ttbar_est"]["params"][0], 2))
        outstr += " $\\pm$ "
        outstr += str(round_sig(inputdic[cut]["ttbar_est"]["paramerrs"][0], 2))
        outstr += " & "
        outstr += str(round_sig(inputdic[cut]["ttbar_est"]["params"][1], 2))
        outstr += " $\\pm$ "
        outstr += str(round_sig(inputdic[cut]["ttbar_est"]["paramerrs"][1], 2))
        outstr += " & "
        outstr += str(round_sig(inputdic[cut]["ttbar_est"]["params"][2], 2))
        outstr += " $\\pm$ "
        outstr += str(round_sig(inputdic[cut]["ttbar_est"]["paramerrs"][2], 2))
        outstr += " & "
        outstr += str(round_sig(inputdic[cut]["qcd_est"]["params"][0], 2))
        outstr += " $\\pm$ "
        outstr += str(round_sig(inputdic[cut]["qcd_est"]["paramerrs"][0], 2))
        outstr += " & "
        outstr += str(round_sig(inputdic[cut]["qcd_est"]["params"][1], 2))
        outstr += " $\\pm$ "
        outstr += str(round_sig(inputdic[cut]["qcd_est"]["paramerrs"][1], 2))
        outstr += " & "
        outstr += str(round_sig(inputdic[cut]["qcd_est"]["params"][2], 2))
        outstr += " $\\pm$ "
        outstr += str(round_sig(inputdic[cut]["qcd_est"]["paramerrs"][2], 2))
        outstr+="\\\\"
        tableList.append(outstr)

    tableList.append("& & & & & &\\\\")
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")
    tableList.append("\\end{footnotesize}")
    tableList.append("\\newline")

    #return the table
    for line in tableList:
        print line
        outFile.write(line+" \n")

def makeSmoothedMJJPlots( infileName, outfileName):

    f = ROOT.TFile(infileName, "READ")
    
    qcd = f.Get("qcd_hh").Clone()
    top = f.Get("ttbar_hh").Clone()
    bkg = qcd.Clone("bkg_hh")

    #stack qcd on top of top
    bkg.Add(top)
    
    #make canvas
    c=ROOT.TCanvas()
    ROOT.gPad.SetLogy()
       
    bkg.SetLineColor(ROOT.kBlack)
    bkg.SetFillColor(ROOT.kAzure-9)
    bkg.SetXTitle("m_{JJ} [GeV]")
    bkg.SetYTitle("Events")

    bkg.GetXaxis().SetTitleOffset(1.2)
    bkg.GetXaxis().SetTitleSize(0.04)
    bkg.GetYaxis().SetTitleOffset(1.2)
    bkg.GetYaxis().SetTitleSize(0.04)

    bkg.Draw("HIST")

    top.SetLineColor(ROOT.kBlack)
    top.SetFillColor(ROOT.kRed)
    top.Draw("HISTsame")

    bkg_err = bkg.Clone("bkg_err")
    bkg_err.SetFillColor(ROOT.kBlack)
    bkg_err.SetFillStyle(3001)
    bkg_err.Draw("sameE2")
    

    top_err = top.Clone("top_err")
    top_err.SetFillColor(ROOT.kBlack)
    top_err.SetFillStyle(3001)
    #top_err.Draw("sameE2")

    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetBorderSize(0)
    leg.SetMargin(0.3)
    leg.SetTextSize(0.04)
    leg.AddEntry(bkg, "QCD", "F")
    leg.AddEntry(top, "t #bar{t}", "F")
    leg.Draw()

    c.SaveAs(outfileName)

    return


if __name__ == '__main__': 
    main()
