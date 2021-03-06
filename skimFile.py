###Tony: split a single tree into n paterners
import ROOT, rootlogon, helpers
import argparse, copy, glob, os, sys, time
#for parallel processing!
import multiprocessing as mp
import config as CONF
#import tree configuration
ROOT.gROOT.SetBatch(True)


'''this file is used to skim the large MiniNtuple 
to events only passing boosted selection!!! 
Will not be suited even for semi-leptonic ttbar studies.
Be careful.
Also, current version only support 1 tree, but not the others.
May have some problems for systematics.
Also be extra careful.
'''

#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="16_13TeV")
    return parser.parse_args()

def selection(config):
    ##load the target tree
    ##only skim the MiniNtuple for now!!!
    f = ROOT.TFile(config["file"], "read")
    t = f.Get("XhhMiniNtuple")
    cutflow_weight = f.Get("cutflow_weighted_XhhMiniNtuple").Clone()
    cutflow        = f.Get("cutflow_XhhMiniNtuple").Clone()
    Metadata       = f.Get("MetaData_EventCount_XhhMiniNtuple").Clone()

    outfile = ROOT.TFile(config["file"] + "_skim", "recreate")
    print "skimming: ", config["file"]
    #outtree = t.CopyTree("hcand_boosted_n >= 2")
    outtree = t.CloneTree(0)
    ##open and copy
    nentries = t.GetEntries()
    for n in range(nentries):
        t.GetEntry(n)
        #add cuts for skimming...so simple...implicit this is a 250, 350 cut
        if n % 20000 == 0:
            helpers.drawProgressBar(n/(nentries*1.0))
        if t.hcand_boosted_n >= 2:
            outtree.Fill()
        else:
            pass
        #print n%nfiles
        
    print "skimming done! ", config["file"]
    #save the output
    outfile.cd()
    outtree.Write()
    cutflow_weight.Write()
    Metadata.Write()
    cutflow.Write()

    del(t)
    del(outtree)
    del(cutflow_weight)
    del(cutflow)
    del(Metadata)
    f.Close()
    outfile.Close()

    return


def skim(targetpath=""):
    start_time = time.time()

    ops = options()
    inputpath = targetpath
    outputpath = targetpath
    helpers.checkpath(outputpath)
    print targetpath

    #setup files
    files = glob.glob(targetpath + "*.MiniNTuple.root")
    config = []
    #setup the dictionary
    for file in files:
        #print file
        temp_dic = {}
        temp_dic["file"] = file
        #add skimming selection now
        if ops.file not in file:
            continue
        #only do skimming once for now!
        if not os.path.isfile(temp_dic["file"] + "_skim"):
            config.append(temp_dic)
    print config
    print " Running %s jobs on %s cores" % (len(config), mp.cpu_count()-1)
    npool = min(len(config), mp.cpu_count()-1)
    pool  = mp.Pool(npool)
    pool.map(selection, config)
    ##for debugging
    #selection(config[0])
    # for conf in config:
    #     print conf
    #     selection(conf)

    print("--- %s seconds ---" % (time.time() - start_time))
    print "Finish!"

def main():
    print "make sure you mount eos!"
    eospath = CONF.toppath + "/eos/atlas/user/b/btong/bb/"
    #skim(targetpath=eospath + "data/vBT-01-00/gridOutput/MiniNTuple/")
    #eospath = CONF.toppath + "/eos/atlas/user/g/gputnam/bb/"
    #skim(targetpath=eospath + "data/v02-00-00/gridOutput/MiniNTuple/")
    #skim(targetpath=eospath + "mc/v02-00-00/gridOutput/MiniNTuple/")
    #skim(targetpath=eospath + "mc/v02-02-03/gridOutput/rawDownload/user.btong.mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.hh4b-02-02-03_MiniNTuple.root/")
    #skim(targetpath="../test_mini/data-MiniNTuple/")
    #split(targetpath="signal_QCD")

#def clearbranches():
if __name__ == "__main__":
    main()
