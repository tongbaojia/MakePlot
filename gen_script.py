###this file is used to generate reweighting instructions
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
    parser.add_argument("--inputdir", default=CONF.workdir)
    parser.add_argument("--full", default=False) #4times more time
    return parser.parse_args()

#currently reweighting all of them at once...may not be optimal...
def write_reweight(fname="TEST", reweight_dic={}, 
    region_dic = [("2bs", "TwoTag_split_Sideband"), ("3b","ThreeTag_Sideband"), ("4b","FourTag_Sideband")], split=False, cond=False):
    '''write reweight output '''
    motherfolder="Moriond"
    helpers.checkpath("script")
    #building the inputdictionary
    #creat an empty dictionary
    #ready to dump file
    f = open("script/" + fname + ".txt", "w")
    #make sure over write everytime!
    f.truncate()
    f.write( "#reweighting script for hh4b analysis \n")
    #iteration; Ntrk; parameter; inputfolder; parameterfile
    for i in range(iteration):
        f.write( "#iteration:" + str(i) + "\n")
        #space is very important!!!!
        for region, region_fname in region_dic:
            for var, var_fname in reweight_dic.iteritems():
                if split: #this is to reweight leading pT and trk pT seperately
                    if "j0_pt" in var and i%2 == 1: #for even skip j0_pt
                        continue
                    elif "j0_pt" not in var and i%2 != 1: #for odd, skip other
                        continue
                    # if "j0_pt" in var and i%4 > 1: #for even skip j0_pt
                    #     continue
                    # elif "j0_pt" not in var and i%4 <= 1: #for odd, skip other
                    #     continue
                ##notice this onlyputs condition on subl, lead reweighting; reweight lead's subl and subl's lead
                if "lead" in region_fname and "lead" in var_fname: 
                    continue
                if "subl" in region_fname and "subl" in var_fname:
                    continue
                templine = ""
                templine += str(i) + " " #iteration
                templine += region + " " #Ntrk
                templine += "event." + var + " " #parameter
                templine += motherfolder + ("_" + fname + "_" + str(i-1) if i!= 0 else "") + " " #look for the original iteration
                templine += "r" + str(i) + "_" + region_fname + "_" + var_fname + ".txt" + " " #parameterfile;
                ##add in condition; be very careful, this means the TinyNtuple has to be produced with the correct b-tagging MV2Cut
                ##also the definition of condition needs to agree with the PlotTinyTree region condition!!! STUPID but be very careful!!!
                if cond:
                    if "2Trk_split_lead" in region_fname:
                        templine += "((event.j0_nb==1)and(event.j1_nb==0))" + " " #condition
                    if "2Trk_split_subl" in region_fname:
                        templine += "((event.j0_nb==0)and(event.j1_nb==1))" + " " #condition
                    if "3Trk_lead" in region_fname:
                        templine += "((event.j0_nb==1)and(event.j1_nb==0))" + " " #condition
                    if "3Trk_subl" in region_fname:
                        templine += "((event.j0_nb==0)and(event.j1_nb==1))" + " " #condition
                    if "4Trk_lead" in region_fname:
                        templine += "((event.j0_nb==2)and(event.j1_nb==0))" + " " #condition
                    if "4Trk_subl" in region_fname:
                        templine += "((event.j0_nb==0)and(event.j1_nb==2))" + " " #condition
                templine += "\n"
                print templine
                f.write(templine)
    #finish
    f.close()

#do everything in one main?
def main():
    global iteration
    iteration = 10
    # #next one; alltrk
    # reweight_dic = {
    #     "j0_trk0_pt":"leadHCand_trk0_Pt",
    #     "j0_trk1_pt":"leadHCand_trk1_Pt",
    #     "j1_trk0_pt":"sublHCand_trk0_Pt",
    #     "j1_trk1_pt":"sublHCand_trk1_Pt",
    #     "j0_pt":"leadHCand_Pt_m",
    #     }
    # write_reweight("j0pT-alltrk-fin", reweight_dic)
    # #next one; leadtrk
    # reweight_dic = {
    #     "j0_trk0_pt":"leadHCand_trk0_Pt",
    #     "j1_trk0_pt":"sublHCand_trk0_Pt",
    #     "j0_pt":"leadHCand_Pt_m",
    #     }
    # write_reweight("j0pT-leadtrk-fin", reweight_dic)
    # #next one; subltrk
    # reweight_dic = {
    #     "j0_trk1_pt":"leadHCand_trk1_Pt",
    #     "j1_trk1_pt":"sublHCand_trk1_Pt",
    #     "j0_pt":"leadHCand_Pt_m",
    #     }
    # write_reweight("j0pT-subltrk-fin", reweight_dic)
    # #next one; trks_Pt
    # reweight_dic = {
    #     "j0_trk0_pt":"trks_Pt",
    #     "j0_trk1_pt":"trks_Pt",
    #     "j1_trk0_pt":"trks_Pt",
    #     "j1_trk1_pt":"trks_Pt",
    #     "j0_pt":"leadHCand_Pt_m",
    #     }
    # write_reweight("j0pT-trks-fin", reweight_dic)


    reweight_dic = {
        "j0_trk0_pt":"leadHCand_trk0_Pt",
        "j0_trk1_pt":"leadHCand_trk1_Pt",
        "j1_trk0_pt":"sublHCand_trk0_Pt",
        "j1_trk1_pt":"sublHCand_trk1_Pt",
        "j0_pt":"leadHCand_Pt_m",
        "j1_pt":"sublHCand_Pt_m",
        }
    region_dic = [
        ("2bs","NoTag_2Trk_split_lead_Incl"),
        ("2bs", "NoTag_2Trk_split_subl_Incl"),
        ("3b", "NoTag_3Trk_lead_Incl"),
        ("3b", "NoTag_3Trk_subl_Incl"),
        ("4b", "NoTag_4Trk_lead_Incl"),
        ("4b", "NoTag_4Trk_subl_Incl"),
    ]
    write_reweight("bkg", reweight_dic, region_dic, cond=True)
    
    print "DONE"

### end
if __name__ == "__main__":
    main()