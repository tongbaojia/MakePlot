import ROOT, rootlogon
import argparse, array, copy, glob, os, sys, time
import helpers
import config as CONF
from ROOT import *
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
SetAtlasStyle()

ROOT.gROOT.SetBatch(True)

def main():

    start_time = time.time()
    ops = options()
    inputdir = ops.inputdir

    global channels
    channels = ["Rhh" + str(i) for i in range(20, 160, 20)]
    #print channels
    #channels=["Rhh20", "Rhh30", "Rhh40", "Rhh50", "Rhh60", "Rhh70", "Rhh80", "Rhh90", "Rhh100", "Rhh110", "Rhh120", "Rhh130", "Rhh140", "Rhh150"]#, "b70", "b77", "b80", "b85", "b90"]
    global tag_lst
    tag_lst = ["OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
    global inputpath
    inputpath = CONF.inputpath + "musplit_test/" #musplit_test;mutest
    global outputpath 
    outputpath = CONF.outplotpath + "musplit_test/" #musplit_test; mutest
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    global outputroot
    outputroot = ROOT.TFile.Open(outputpath + "temp.root", "recreate")
    # Fill the histogram from the table
    #DrawMuqcd(qcdmc=True) ##inputpath mu_test
    DrawMuqcd_split()
    # Finish the work
    print("--- %s seconds ---" % (time.time() - start_time))

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

### 
def DrawMuqcd(qcdmc=False):
    outputroot.cd()

    input_data = ROOT.TFile.Open(inputpath + "data_test/hist.root", "read")
    input_ttbar = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist.root", "read")
    input_zjet = ROOT.TFile.Open(inputpath + "zjets_test/hist.root", "read")
    if (qcdmc):
        input_qcd = ROOT.TFile.Open(inputpath + "signal_QCD/hist.root", "read")

    for j, cut in enumerate(tag_lst): 
        canv = ROOT.TCanvas(cut + "_" + "mustudy", "mustudy", 800, 800)
        xleg, yleg = 0.52, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)

        h_muqcd = ROOT.TH1D("data_" + cut + "_" + "muqcd","muqcd",1,1,2)
        h_muqcd.SetMarkerStyle(20)
        h_muqcd.SetMarkerColor(1)
        h_muqcd.SetLineColor(1)
        h_muqcd.SetMarkerSize(1)
        h_muqcd.GetYaxis().SetTitle("#mu qcd")
        legend.AddEntry(h_muqcd, "Data Est", "apl")

        if (qcdmc):
            mc_muqcd = ROOT.TH1D("mc_" + cut + "_" + "muqcd","muqcd",1,1,2)
            mc_muqcd.SetMarkerStyle(20)
            mc_muqcd.SetMarkerColor(2)
            mc_muqcd.SetLineColor(2)
            mc_muqcd.SetMarkerSize(1)
            mc_muqcd.GetYaxis().SetTitle("#mu qcd")
            legend.AddEntry(mc_muqcd, "Dijet MC", "apl")

        #very stupid protection to distinguish 2b and 2bs
        for k, ch in enumerate(channels):
            histname = cut + "_" + ch + "/mHH_l"
            #print histname
            hist_data = input_data.Get(histname).Clone()
            hist_ttbar = input_ttbar.Get(histname).Clone()
            hist_zjet = input_zjet.Get(histname).Clone()
            hist_temp = hist_data.Clone()
            hist_temp.Add(hist_ttbar, -1)
            hist_temp.Add(hist_zjet, -1)

            Nqcd_err = ROOT.Double(0.)
            Nqcd = hist_temp.IntegralAndError(0, hist_temp.GetXaxis().GetNbins()+1, Nqcd_err)
            #get the 0 tag numbers
            refname = "NoTag" + "_" + ch + "/mHH_l"
            ref_data = input_data.Get(refname).Clone()
            ref_ttbar = input_ttbar.Get(refname).Clone()
            ref_zjet = input_zjet.Get(refname).Clone()
            ref_temp = ref_data.Clone()
            ref_temp.Add(ref_ttbar, -1)
            ref_temp.Add(ref_zjet, -1)

            refqcd_err = ROOT.Double(0.)
            refqcd = ref_temp.IntegralAndError(0, ref_temp.GetXaxis().GetNbins()+1, refqcd_err)

            #print cut, ch, Nmcqcd, refmcqcd
            #compute mu qcd
            if refqcd > 0:
                h_muqcd.Fill(ch, Nqcd/refqcd)
                h_muqcd.SetBinError(h_muqcd.GetXaxis().FindBin(ch), helpers.ratioerror(Nqcd, refqcd, ea=Nqcd_err, eb=refqcd_err))

            #for QCD MC
            if (qcdmc):
                hist_mcqcd = input_qcd.Get(histname).Clone()
                Nmcqcd_err = ROOT.Double(0.)
                Nmcqcd = hist_mcqcd.IntegralAndError(0, hist_mcqcd.GetXaxis().GetNbins()+1, Nmcqcd_err)
                ref_mcqcd = input_qcd.Get(refname).Clone()
                refmcqcd_err = ROOT.Double(0.)
                refmcqcd = ref_mcqcd.IntegralAndError(0, ref_mcqcd.GetXaxis().GetNbins()+1, refmcqcd_err)
                if refmcqcd > 0:
                    mc_muqcd.Fill(ch, Nmcqcd/refmcqcd)
                    mc_muqcd.SetBinError(mc_muqcd.GetXaxis().FindBin(ch), helpers.ratioerror(Nmcqcd, refmcqcd, ea=Nmcqcd_err, eb=refmcqcd_err))


        h_muqcd.SetMaximum(h_muqcd.GetMaximum() * 2.5)   
        h_muqcd.Draw("EPL")
        #canv.SaveAs(outputpath + h_muqcd.GetName() + ".pdf")
        #canv.Clear()
        if (qcdmc):
            mc_muqcd.SetMaximum(mc_muqcd.GetMaximum() * 2.5)   
            mc_muqcd.Draw("EPL SAME")
        
        legend.SetBorderSize(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.04)
        legend.Draw()
        canv.SaveAs(outputpath + h_muqcd.GetName() + ".pdf")
        canv.Close()

    input_data.Close()
    input_ttbar.Close()
    input_zjet.Close()


def DrawMuqcd_split(prename="", qcdmc=False):

    input_data = ROOT.TFile.Open(inputpath + "data_test/hist.root", "read")
    input_ttbar = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist.root", "read")
    input_zjet = ROOT.TFile.Open(inputpath + "zjets_test/hist.root", "read")
    outputroot.cd()
    if (qcdmc):
        input_qcd = ROOT.TFile.Open(inputpath + "signal_QCD/hist.root", "read")

    for j, cut in enumerate(tag_lst): 

        for i in range(4):#4 regions

            h_muqcd = ROOT.TH1D(str(i) + "_" + "data_" + cut + "_" + "muqcd", "muqcd",1,1,2)
            h_muqcd.GetYaxis().SetTitle("#mu qcd")

            if (qcdmc):
                mc_muqcd = ROOT.TH1D(str(i) + "_" + "mc_" + cut + "_" + "muqcd","muqcd",1,1,2)
                mc_muqcd.GetYaxis().SetTitle("#mu qcd")
            #very stupid protection to distinguish 2b and 2bs
            for k, ch in enumerate(channels):
                aftercutname =  "_" + "r" + str(i) + "_" + ch + "/mHH_l"
                histname = cut + aftercutname 
                #print histname
                hist_data = input_data.Get(histname).Clone()
                hist_ttbar = input_ttbar.Get(histname).Clone()
                hist_zjet = input_zjet.Get(histname).Clone()
                hist_temp = hist_data.Clone()
                hist_temp.Add(hist_ttbar, -1)
                hist_temp.Add(hist_zjet, -1)

                Nqcd_err = ROOT.Double(0.)
                Nqcd = hist_temp.IntegralAndError(0, hist_temp.GetXaxis().GetNbins()+1, Nqcd_err)
                #get the 0 tag numbers
                refname = "NoTag" + aftercutname
                ref_data = input_data.Get(refname).Clone()
                ref_ttbar = input_ttbar.Get(refname).Clone()
                ref_zjet = input_zjet.Get(refname).Clone()
                ref_temp = ref_data.Clone()
                ref_temp.Add(ref_ttbar, -1)
                ref_temp.Add(ref_zjet, -1)

                refqcd_err = ROOT.Double(0.)
                refqcd = ref_temp.IntegralAndError(0, ref_temp.GetXaxis().GetNbins()+1, refqcd_err)

                #print cut, ch, Nmcqcd, refmcqcd
                #compute mu qcd
                if refqcd > 0:
                    h_muqcd.Fill(ch, Nqcd/refqcd)
                    h_muqcd.SetBinError(h_muqcd.GetXaxis().FindBin(ch), helpers.ratioerror(Nqcd, refqcd, ea=Nqcd_err, eb=refqcd_err))
                else:
                    #print refqcd, histname
                    h_muqcd.Fill(ch, 0)
                    h_muqcd.SetBinError(h_muqcd.GetXaxis().FindBin(ch), 0)

                if (qcdmc):
                    hist_mcqcd = input_qcd.Get(histname).Clone()
                    Nmcqcd_err = ROOT.Double(0.)
                    Nmcqcd = hist_mcqcd.IntegralAndError(0, hist_mcqcd.GetXaxis().GetNbins()+1, Nmcqcd_err)
                    ref_mcqcd = input_qcd.Get(refname).Clone()
                    refmcqcd_err = ROOT.Double(0.)
                    refmcqcd = ref_mcqcd.IntegralAndError(0, ref_mcqcd.GetXaxis().GetNbins()+1, refmcqcd_err)
                    if refmcqcd > 0:
                        mc_muqcd.Fill(ch, Nmcqcd/refmcqcd)
                        mc_muqcd.SetBinError(mc_muqcd.GetXaxis().FindBin(ch), helpers.ratioerror(Nmcqcd, refmcqcd, ea=Nmcqcd_err, eb=refmcqcd_err))

            h_muqcd.SetMaximum(h_muqcd.GetMaximum() * 1.5)   
            h_muqcd.Write()
            if (qcdmc):
                hist_mcqcd.Write()

    input_data.Close()
    input_ttbar.Close()
    input_zjet.Close()

    #make the plot from the saved macro, it is stupid
    for j, cut in enumerate(tag_lst): 
        canv = ROOT.TCanvas(cut + "_" + "mustudy", "mustudy", 800, 800)
        xleg, yleg = 0.52, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.3, yleg+0.2)
        for i in range(4):
            h_muqcd = outputroot.Get(str(i) + "_" + "data_" + cut + "_" + "muqcd")
            h_muqcd.SetMarkerStyle(20 + i)
            h_muqcd.SetMarkerColor(1 + i)
            h_muqcd.SetLineColor(1 + i)
            h_muqcd.SetMarkerSize(1)
            h_muqcd.Draw("EPL" + "" if i==0 else "SAME")
            #h_muqcd.SetMaximum(h_muqcd.GetMaximum()) 
            legend.AddEntry(h_muqcd, "region " + str(i), "apl")

        legend.SetBorderSize(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.04)
        legend.Draw()
        canv.SaveAs(outputpath + canv.GetName() + ".pdf")
        canv.Close()



if __name__ == "__main__":
    main()