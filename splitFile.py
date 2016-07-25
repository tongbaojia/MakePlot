###Tony: split a single tree into n paterners
import ROOT, rootlogon, helpers
import argparse, copy, glob, os, sys, time
#for parallel processing!
import multiprocessing as mp
import config as CONF
#import tree configuration
ROOT.gROOT.SetBatch(True)
#this is probably the worse parallel effort
#but whatever

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", default="TEST")
    parser.add_argument("--nfiles", default=14)
    return parser.parse_args()


def split(targetpath="data_test"):
    start_time = time.time()

    ops = options()
    nfiles = ops.nfiles
    inputdir = ops.inputdir
    global inputpath
    inputpath = CONF.inputpath + inputdir + "/" + targetpath
    global outputpath
    outputpath = CONF.inputpath + inputdir + "/" +  targetpath
    helpers.checkpath(outputpath)

    print "split! target: ", targetpath
    f = ROOT.TFile(inputpath + "/" + "hist-MiniNTuple.root", "read")
    #load the target tree
    t = f.Get("TinyTree")
    #load the histograms
    hist_list = ["CutFlowWeight", "CutFlowNoWeight", "h_leadHCand_pT_pre_trig", "h_leadHCand_pT_aft_trig"]
    temp_hist_list = []
    for j, hist in enumerate(hist_list):
        temp_hist_list.append(f.Get(hist).Clone())
        temp_hist_list[j].Scale(1.0/(nfiles * 1.0))

    outfile = []
    outtree = []
    for i in range(nfiles):
        outfile.append(ROOT.TFile(inputpath + "/" + "hist-MiniNTuple_%s.root" % (str(i)), "recreate"))
        outtree.append(t.CloneTree(0))

    #open and copy
    nentries = t.GetEntries()
    for n in range(nentries):
        t.GetEntry(n)
        #print n%nfiles
        outtree[n%nfiles].Fill()

    for i in range(nfiles):
        outfile[i].cd()
        outtree[i].Write()
        for j, hist in enumerate(temp_hist_list):
            hist.Write()
        outfile[i].Close()
    f.Close()
    del(t)
    del(outtree)
    del(temp_hist_list)

    print("--- %s seconds ---" % (time.time() - start_time))
    print "Finish!"


def main():
    split(targetpath="data_test")
    #split(targetpath="ttbar_comb_test")
    #split(targetpath="signal_QCD")

#def clearbranches():
if __name__ == "__main__":
    main()
