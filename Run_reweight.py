#Tony: this is designed to run over the reweighting
import ROOT, helpers
import config as CONF
import argparse, copy, glob, os, sys, time
try:
    import simplejson as json                 
except ImportError:
    import json        
from Xhh4bUtils.BkgFit.BackgroundFit_Ultimate import BackgroundFit
import Xhh4bUtils.BkgFit.smoothfit as smoothfit
#for parallel processing!
import multiprocessing as mp


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="Moriond")
    parser.add_argument("--Xhh",      action='store_true') #4times more time
    parser.add_argument("--var",      default="j0pT-alltrk-fin") #4times more time
    return parser.parse_args()

def main():
    start_time = time.time()
    global ops
    ops = options()

    iter_total = 6
    print "total iteration: ", iter_total
    inputtasks = []
    for i in range(0, iter_total):
        #analysis_pipeline({"motherdir":"TEST", "reweight":"j0pT-alltrk-fin", "iter_re": i}) #2
        #inputtasks.append({"motherdir":"TEST", "reweight":"j0pT-subltrk-fin", "iter_re": i}) #2
        #analysis_pipeline({"motherdir":"TEST", "reweight":"j0pT-leadtrk-fin", "iter_re": i}) #4
        analysis_pipeline({"motherdir":"TEST", "reweight":ops.var, "iter_re": i})
    print("--- %s seconds ---" % (time.time() - start_time))

def analysis_pipeline(config):
    #setup the directories
    motherdir     = config["motherdir"] #the one with TinyTree
    reweight      = config["reweight"]
    iter_re       = config["iter_re"]
    outputdir     = ops.inputdir + "_" + reweight + "_" + str(iter_re) #the output from Plot TinyTree, input for analysis code
    print "the directory is: ", outputdir, " parent dir is: ", motherdir, " reweight: ",  reweight, " iteration: ", iter_re
    ##reweight
    #print "python PlotTinyTree.py --inputdir " + motherdir + " --outputdir " + outputdir +  " --reweight " + reweight + " --iter " + str(iter_re)
    os.system("python PlotTinyTree.py --inputdir " + motherdir + " --outputdir " + outputdir +  " --reweight " + reweight + " --iter " + str(iter_re))
    ##fit and produce plot
    os.system("python get_count.py --full --inputdir " + outputdir)
    os.system("python plot.py --inputdir " + outputdir)
    os.system("python reweight.py --inputdir " + outputdir + " --iter " + str(iter_re + 1)) ##+1 because it is really for the next iteration
    ##for publication purpose
    homepath="/afs/cern.ch/user/b/btong/"
    workpath=CONF.outputpath + outputdir
    print "Publish!"
    helpers.checkpath(homepath + "/www/share/hh4b/reweight/" + outputdir)
    helpers.checkpath(homepath + "/www/share/hh4b/plot/" + outputdir)
    helpers.checkpath(homepath + "/www/share/hh4b/express/" + outputdir)
    ##list of plots
    plt_lst = ["mHH_l_1",\
        "leadHCand_Pt_m", "leadHCand_Eta", "leadHCand_Phi", "leadHCand_Mass", "leadHCand_Mass_s", "leadHCand_trk_dr",\
        "sublHCand_Pt_m", "sublHCand_Eta", "sublHCand_Phi", "sublHCand_Mass", "sublHCand_Mass_s", "sublHCand_trk_dr",\
        "leadHCand_trk0_Pt", "leadHCand_trk1_Pt", "sublHCand_trk0_Pt", "sublHCand_trk1_Pt"]
    #"hCandDr", "hCandDeta", "hCandDphi",\
    ##clean up the current plots
    for pic in glob.glob(homepath + "/www/share/hh4b/reweight/" + outputdir +"/*"):
        os.remove(pic)
    for pic in glob.glob(homepath + "/www/share/hh4b/express/" + outputdir +"/*"):
        os.remove(pic)
        descript = open(homepath + "/www/share/hh4b/express/" + outputdir +"/shortdescription.txt", "w")
        descript.write(" reweight: " +  reweight + " iteration: " + str(iter_re))
        descript.write(" time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())) 
        descript.close()
    for pic in glob.glob(homepath + "/www/share/hh4b/plot/" + outputdir +"/*"):
        os.remove(pic)
    ##copy
    for plot in plt_lst:
        for pic in glob.glob(workpath + "/Plot_r" + str(iter_re + 1) + "/Sideband/*" + plot + ".png"):
            os.system("cp " + pic + " " + homepath + "/www/share/hh4b/reweight/" + outputdir +"/.")
        for pic in glob.glob(workpath + "/Plot" + "/Sideband/*" + plot + ".png"):
            os.system("cp " + pic + " " + homepath + "/www/share/hh4b/plot/" + outputdir +"/.")
            if "mHH_l_1" in pic:
                os.system("cp " + pic + " " + homepath + "/www/share/hh4b/express/" + outputdir +"/.")
        for pic in glob.glob(workpath + "/Plot" + "/Control/*" + plot + ".png"):
            #print pic
            os.system("cp " + pic + " " + homepath + "/www/share/hh4b/plot/" + outputdir +"/.")
            if "mHH_l_1" in pic:
                os.system("cp " + pic + " " + homepath + "/www/share/hh4b/express/" + outputdir +"/.")
                #print "cp " + pic + " " + homepath + "/www/share/hh4b/express/" + outputdir +"/."
    ##publish
    os.chdir(homepath + "/www/share/")
    os.system("python createHtmlOverview.py")
    os.chdir(CONF.currpath)
    print "Done!"


if __name__ == '__main__': 
    main()