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
    parser.add_argument("--nfiles", default=7)
    return parser.parse_args()



def split(targetpath="data_test"):
    start_time = time.time()

    ops = options()
    nfiles = ops.nfiles
    global inputpath
    inputpath = CONF.inputpath + "TEST/" + targetpath
    global outputpath
    outputpath = CONF.inputpath + "TEST/" +  targetpath
    helpers.checkpath(outputpath)

    f = ROOT.TFile(inputpath + "/" + "hist-MiniNTuple.root", "read")
    #load the target tree
    t = f.Get("TinyTree")
    cutflow_weight = f.Get("CutFlowWeight").Clone()
    cutflow = f.Get("CutFlowNoWeight").Clone()
    cutflow_weight.Scale(1.0/(nfiles * 1.0))
    cutflow.Scale(1.0/(nfiles * 1.0))

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
        cutflow_weight.Write()
        cutflow.Write()
        outfile[i].Close()
    f.Close()

    print("--- %s seconds ---" % (time.time() - start_time))
    print "Finish!"

def main():
    split(targetpath="data_test")
    split(targetpath="signal_QCD")

#def clearbranches():
if __name__ == "__main__":
    main()
