import argparse, copy, os, sys, glob, math
from array import array
import ROOT, rootlogon
import Xhh4bUtils.BkgFit.smoothfit_Ultimate as smoothfit
from helpers import round_sig
import config as CONF
ROOT.gROOT.SetBatch()


treename  = "XhhMiniNtuple"
cut_lst = ["FourTag", "ThreeTag", "TwoTag_split"]
#setup fit initial values; tricky for the fits...
init_dic = {"l":{"FourTag":{"ttbar":[-30, -5, -10], "qcd":[-5, 20, -2]}, \
"ThreeTag":{"ttbar":[-30, -5, -10], "qcd":[-5, 20, -5]},\
"TwoTag_split":{"ttbar":[-30, -10, -10], "qcd":[-5, 20, -5]}}, \
    "pole":{"FourTag":{"ttbar":[-50, -50, -20], "qcd":[-5, 20, -3]}, \
"ThreeTag":{"ttbar":[-50, -50, -20], "qcd":[-1, 20, -3]},\
"TwoTag_split":{"ttbar":[-14, 20, -10], "qcd":[-1, 20, -3]}}}


#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    parser.add_argument("--Xhh", action='store_true') #4times more time
    return parser.parse_args()

def main():
    global ops
    ops = options()
    global inputdir
    inputdir = ops.inputdir
    #setup basics;
    #run it, order matters, because the pole file replaces the previous one!
    dump("l")
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
        outfile  = ROOT.TFile("%s/%s_limit_%s.root" % (outputpath, inputdir, c + ("_pole" if "pole" in finaldis else "")), "RECREATE")
        #get the mass plot
        tempdic = {}
        cut = c + "_Signal_mHH" + pltname
        qcdsmoothrange = (1200, 3000)
        topsmoothrange = (1100, 3000)
        if "pole" in finaldis:
            qcdsmoothrange = (1200, 3000)
            topsmoothrange = (1200, 3000)
        savehist(ifile, "data_" + cut,  "data_hh")#blind data now
        tempdic["data_est"]  = savehist(ifile,   "data_est_" + cut,  "totalbkg_hh", dosmooth=True, smoothrange = qcdsmoothrange, initpar=init_dic[finaldis][c]["qcd"])
        tempdic["qcd_est"]   = savehist(ifile,   "qcd_est_" + cut,   "qcd_hh",      dosmooth=True, smoothrange = qcdsmoothrange, initpar=init_dic[finaldis][c]["qcd"])
        tempdic["ttbar_est"] = savehist(ifile,   "ttbar_est_" + cut, "ttbar_hh",    dosmooth=True, smoothrange = topsmoothrange, initpar=init_dic[finaldis][c]["ttbar"])
        savehist(ifile, "zjet_" + cut,      "zjet_hh")

        for mass in mass_lst:
            savehist(ifile, "RSG1_" + str(mass) + "_" + cut, "signal_RSG_c10_hh_m" + str(mass))
            if(ops.Xhh):
                savehist(ifile, "Xhh_" + str(mass) + "_" + cut, "signal_X_hh_m" + str(mass))
        outfile.Close()
        makeSmoothedMJJPlots("%s/%s_limit_%s.root" % (outputpath, inputdir, c), pltoutputpath + c + pltname + "_smoothed.pdf")
        masterdic[c] = tempdic

    #print masterdic
    fit_outtex = open(outtablepath + "smoothfit" + pltname + ".tex", "w")
    WriteFitResult(masterdic, fit_outtex)

    ifile.Close()
    print "Done! "

def savehist(inputroot, inname, outname, dosmooth=False, smoothrange = (1100, 3000), smoothfunc="Dijet", initpar=[], Rebin=True):
    hist  = inputroot.Get(inname).Clone()
    if ("totalbkg" in outname):
        #hist_zjet = inputroot.Get(inname.replace("data_est", "zjet")).Clone()
        #hist.Add(hist_zjet, -1)
        hist_qcd = inputroot.Get(inname.replace("data", "qcd")).Clone()
        hist_ttbar = inputroot.Get(inname.replace("data", "ttbar")).Clone()
        hist_qcd.Add(hist_ttbar, 1)
        hist = hist_qcd.Clone(inname)
    #always clear the negative bins before smoothing!
    ClearNegBin(hist)
    #rebin is also done here, will be send to limit input
    #print inname, smoothrange, initpar
    if Rebin:
        hist = do_variable_rebinning(hist, array('d', range(0, 4000, 100)))

    #here do smoothing
    if dosmooth:
        #print inname, smoothrange, initpar ##for debug
        sm = smoothfit.smoothfit(hist, fitFunction = smoothfunc, fitRange = smoothrange, \
            makePlots = True, verbose = False, outfileName=inname, ouutfilepath=pltoutputpath, initpar=initpar)
        #hist = smoothfit.MakeSmoothHistoWithError(hist, sm)
        hist =  smoothfit.MakeSmoothHisto(hist, sm["nom"])
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

def do_variable_rebinning(hist,bins, scale=1):
    a=hist.GetXaxis()

    newhist=ROOT.TH1F(hist.GetName()+"_rebinned",
                      hist.GetTitle()+";"+hist.GetXaxis().GetTitle()+";"+hist.GetYaxis().GetTitle(),
                      len(bins)-1,
                      array('d',bins))

    newhist.Sumw2()
    newa=newhist.GetXaxis()
    #print "check size ", hist.GetNbinsX(), newhist.GetNbinsX()
    for b in range(0, hist.GetNbinsX()+1):
        newb             = newa.FindBin(a.GetBinCenter(b))

        # Get existing new content (if any)                                                                                                              
        val              = newhist.GetBinContent(newb)
        err              = newhist.GetBinError(newb)
        # Get content to add
        ratio_bin_widths = scale*newa.GetBinWidth(newb)/a.GetBinWidth(b)
        #print "ratio_bin_widths",ratio_bin_widths
        #val              = val+hist.GetBinContent(b)/ratio_bin_widths
        #err              = math.sqrt(err*err+hist.GetBinError(b)/ratio_bin_widths*hist.GetBinError(b)/ratio_bin_widths)
        val              = val+hist.GetBinContent(b)
        err              = math.sqrt(err*err+hist.GetBinError(b)*hist.GetBinError(b))
        #print "bin", newb, " new value ", val, " change ", hist.GetBinContent(b)
        newhist.SetBinContent(newb,val)
        newhist.SetBinError(newb,err)
    return newhist

def ClearNegBin(hist):
    for ibin in range(0, hist.GetNbinsX()+1):
        if hist.GetBinContent(ibin) < 0:
            hist.SetBinContent(ibin, 0)
            hist.SetBinError(ibin, 0)
    return

if __name__ == '__main__': 
    main()
