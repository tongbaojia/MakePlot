import ROOT, helpers
import config as CONF
import argparse, copy, glob, os, sys, time

temp_dic = {"j0_trk0_pt":"leadHCand_trk0_Pt",
    "j0_trk1_pt":"leadHCand_trk1_Pt",
    "j1_trk0_pt":"sublHCand_trk0_Pt",
    "j1_trk1_pt":"sublHCand_trk1_Pt",
    "j0_pt":"leadHCand_Pt_m",
    "j1_pt":"sublHCand_Pt_m"}


#define functions
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="b77")
    parser.add_argument("--full", default=False) #4times more time
    return parser.parse_args()

#currently reweighting all of them at once...may not be optimal...
def write_reweight(fname="TEST", reweight_dic={}):
    motherfolder="f_c10-cb"
    helpers.checkpath("script")
    #building the inputdictionary
    region_dic = {"2bs":"TwoTag_split", "3b":"ThreeTag", "4b":"FourTag"}
    #creat an empty dictionary
    #ready to dump file
    f = open("script/" + fname + ".txt", "w")
    #make sure over write everytime!
    f.truncate()
    f.write( "#reweighting script for hh4b analysis \n")
    #iteration; Ntrk; parameter; inputfolder; parameterfile
    iteration = 8
    for i in range(iteration):
        f.write( "#iteration:" + str(i) + "\n")
        #space is very important!!!!
        for region, region_fname in region_dic.iteritems():
            for var, var_fname in reweight_dic.iteritems():
                templine = ""
                templine += str(i) + " " #iteration
                templine += region + " " #Ntrk
                templine += "event." + var + " " #parameter
                if i == 0:
                    templine += motherfolder + " " #look for the original iteration
                else:
                    templine += motherfolder + "_" + fname + "_" + str(i-1) + " " #look for the first iteration
                templine += "r0_" + region_fname + "_Sideband_" + var_fname + ".txt" + " " #parameterfile;
                templine += "\n"
                print templine
                f.write(templine)
    #finish
    f.close()

#do everything in one main?
def main():
    #next one; alltrk
    reweight_dic = {
        "j0_trk0_pt":"leadHCand_trk0_Pt",
        "j0_trk1_pt":"leadHCand_trk1_Pt",
        "j1_trk0_pt":"sublHCand_trk0_Pt",
        "j1_trk1_pt":"sublHCand_trk1_Pt",
        "j0_pt":"leadHCand_Pt_m",
        }
    write_reweight("j0pT-alltrk", reweight_dic)
    #next one; leadtrk
    reweight_dic = {
        "j0_trk0_pt":"leadHCand_trk0_Pt",
        "j1_trk0_pt":"sublHCand_trk0_Pt",
        "j0_pt":"leadHCand_Pt_m",
        }
    write_reweight("j0pT-leadtrk", reweight_dic)
    #next one; subltrk
    reweight_dic = {
        "j0_trk1_pt":"leadHCand_trk1_Pt",
        "j1_trk1_pt":"sublHCand_trk1_Pt",
        "j0_pt":"leadHCand_Pt_m",
        }
    write_reweight("j0pT-subltrk", reweight_dic)
    #next one; trks_Pt
    reweight_dic = {
        "j0_trk0_pt":"trks_Pt",
        "j0_trk1_pt":"trks_Pt",
        "j1_trk0_pt":"trks_Pt",
        "j1_trk1_pt":"trks_Pt",
        "j0_pt":"leadHCand_Pt_m",
        }
    write_reweight("j0pT-trks", reweight_dic)
    print "DONE"
### end
if __name__ == "__main__":
    main()