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
    channels=["Rhh20", "Rhh30", "Rhh40", "Rhh50", "Rhh60", "Rhh70", "Rhh80", "Rhh90", "Rhh100", "Rhh110", "Rhh120", "Rhh130", "Rhh140", "Rhh150"]#, "b70", "b77", "b80", "b85", "b90"]
    global tag_lst
    tag_lst = ["OneTag", "TwoTag", "TwoTag_split", "ThreeTag", "FourTag"]
    global inputpath
    inputpath = CONF.inputpath + "mutest/"
    global outputpath
    outputpath = CONF.outplotpath
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    global outputroot
    outputroot = ROOT.TFile.Open(outputpath + "temp.root", "recreate")
    # Fill the histogram from the table
    DrawMuqcd()
    # Finish the work
    print("--- %s seconds ---" % (time.time() - start_time))

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="b77")
    return parser.parse_args()

### 
def DrawMuqcd():
    outputroot.cd()

    input_data = ROOT.TFile.Open(inputpath + "data_test/hist.root", "read")
    input_ttbar = ROOT.TFile.Open(inputpath + "ttbar_comb_test/hist.root", "read")
    input_zjet = ROOT.TFile.Open(inputpath + "zjets_test/hist.root", "read")
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

        mc_muqcd = ROOT.TH1D("mc_" + cut + "_" + "muqcd","muqcd",1,1,2)
        mc_muqcd.SetMarkerStyle(20)
        mc_muqcd.SetMarkerColor(2)
        mc_muqcd.SetLineColor(2)
        mc_muqcd.SetMarkerSize(1)
        mc_muqcd.GetYaxis().SetTitle("#mu qcd")

        legend.AddEntry(h_muqcd, "Data Est", "apl")
        legend.AddEntry(mc_muqcd, "Dijet MC", "apl")
        #very stupid protection to distinguish 2b and 2bs
        for k, ch in enumerate(channels):
            histname = cut + "_" + ch + "/mHH_l"
            #print histname
            hist_data = input_data.Get(histname).Clone()
            hist_ttbar = input_ttbar.Get(histname).Clone()
            hist_zjet = input_zjet.Get(histname).Clone()
            hist_qcd = input_qcd.Get(histname).Clone()
            hist_temp = hist_data.Clone()
            hist_temp.Add(hist_ttbar, -1)
            hist_temp.Add(hist_zjet, -1)

            Nqcd_err = ROOT.Double(0.)
            Nqcd = hist_temp.IntegralAndError(0, hist_temp.GetXaxis().GetNbins()+1, Nqcd_err)
            Nmcqcd_err = ROOT.Double(0.)
            Nmcqcd = hist_qcd.IntegralAndError(0, hist_qcd.GetXaxis().GetNbins()+1, Nmcqcd_err)
            #get the 0 tag numbers
            refname = "NoTag" + "_" + ch + "/mHH_l"
            ref_data = input_data.Get(refname).Clone()
            ref_ttbar = input_ttbar.Get(refname).Clone()
            ref_zjet = input_zjet.Get(refname).Clone()
            ref_qcd = input_qcd.Get(refname).Clone()
            ref_temp = ref_data.Clone()
            ref_temp.Add(ref_ttbar, -1)
            ref_temp.Add(ref_zjet, -1)

            refqcd_err = ROOT.Double(0.)
            refqcd = ref_temp.IntegralAndError(0, ref_temp.GetXaxis().GetNbins()+1, refqcd_err)
            refmcqcd_err = ROOT.Double(0.)
            refmcqcd = ref_qcd.IntegralAndError(0, ref_qcd.GetXaxis().GetNbins()+1, refmcqcd_err)

            #print cut, ch, Nmcqcd, refmcqcd
            #compute mu qcd
            if refqcd > 0:
                h_muqcd.Fill(h_muqcd.GetXaxis().FindBin(ch), Nqcd/refqcd)
                h_muqcd.SetBinError(h_muqcd.GetXaxis().FindBin(ch), helpers.ratioerror(Nqcd, refqcd, ea=Nqcd_err, eb=refqcd_err))
            if refmcqcd > 0:
                mc_muqcd.Fill(mc_muqcd.GetXaxis().FindBin(ch), Nmcqcd/refmcqcd)
                mc_muqcd.SetBinError(mc_muqcd.GetXaxis().FindBin(ch), helpers.ratioerror(Nmcqcd, refmcqcd, ea=Nmcqcd_err, eb=refmcqcd_err))


        h_muqcd.SetMaximum(h_muqcd.GetMaximum() * 2.5)   
        h_muqcd.Draw("EPL")
        #canv.SaveAs(outputpath + h_muqcd.GetName() + ".pdf")
        #canv.Clear()
        mc_muqcd.SetMaximum(mc_muqcd.GetMaximum() * 2.5)   
        mc_muqcd.Draw("EPL SAME")
        
        legend.SetBorderSize(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.04)
        legend.Draw()
        canv.SaveAs(outputpath + mc_muqcd.GetName() + ".pdf")
        canv.Close()

    input_data.Close()
    input_ttbar.Close()
    input_zjet.Close()



if __name__ == "__main__":
    main()