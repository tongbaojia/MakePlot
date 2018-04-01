import os, glob, time


def pack_copy(originpath, targetpath="/Users/renormalization/Desktop/Transfer/", prename=""):
    print originpath
    print targetpath
    return "cp " + originpath + " " + targetpath + ("." if prename=="" else prename)

def main():
    start_time = time.time()

    plotpath      = "/Users/renormalization/mnt/work/bbbb/MoriondAnalysis/Output/"
    limitplotpath = "/Users/renormalization/mnt/work/bbbb/MoriondAnalysis/StatAnalysis/Plots/"
    smoothsystpath= "/Users/renormalization/mnt/work/bbbb/MoriondAnalysis/MakePlot/Xhh4bUtils/mHH_l/"
    notepath      = "/Users/renormalization/SVN/HH4b/hh4b-2017-paper/figures/boosted/"



# #for unBlinded mHH 2D
#     lst_dir    = ["Moriond_bkg_9"]
#     lst_region = ["Other"]
#     lst_type   = [""]
#     lst_plt    = ["NoTag_Incl_mH0H1", "TwoTag_split_Incl_mH0H1"]
#     lst_form   = ["pdf", "eps", "C", "png"]
#     note_dir   = "background"
#     note_name  = []

#     for Dir in lst_dir:
#         for region in lst_region:
#             for Type in lst_type:
#               for form in lst_form:
#                   for i, plt in enumerate(lst_plt):
#                       originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + plt + "." + form
#                       os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))

#for unBlinded Signal efficiency
    lst_dir    = ["Moriond_bkg_9"]
    lst_region = ["SigEff"]
    lst_type   = [""]
    lst_plt    = ["G_hh_c10_region_lst_Moriond_bkg_9_Efficiency_PreSel", "G_hh_c10_evtsel_Moriond_bkg_9_Efficiency_PreSel"]
    lst_form   = ["pdf"]
    note_dir   = "selection"
    note_name  = ["region_lst_Moriond_bkg_9_Efficiency_PreSel", "evtsel_Moriond_bkg_9_Efficiency_PreSel"]

    for Dir in lst_dir:
        for region in lst_region:
            for Type in lst_type:
              for form in lst_form:
                  for i, plt in enumerate(lst_plt):
                      originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + plt + "." + form
                      os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/", prename=note_name[i] + "." + form))

#for unBlinded Signal efficiency
    lst_dir    = ["Moriond_bkg_9"]
    lst_region = ["SigEff"]
    lst_type   = [""]
    lst_plt    = ["X_hh_region_lst_Moriond_bkg_9_Efficiency_PreSel", "X_hh_evtsel_Moriond_bkg_9_Efficiency_PreSel"]
    lst_form   = ["pdf"]
    note_dir   = "selection"
    note_name  = ["X_hh_region_lst_Moriond_bkg_9_Efficiency_PreSel", "X_hh_evtsel_Moriond_bkg_9_Efficiency_PreSel"]

    for Dir in lst_dir:
        for region in lst_region:
            for Type in lst_type:
              for form in lst_form:
                  for i, plt in enumerate(lst_plt):
                      originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + plt + "." + form
                      os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/", prename=note_name[i] + "." + form))

# #for unBlinded Sideband Regions
#     lst_dir    = ["Moriond_bkg_9"]
#     lst_region = ["Sideband"]
#     lst_type   = ["FourTag", "ThreeTag", "TwoTag_split"]
#     lst_plt    = ["leadHCand_Mass_s"]
#     lst_form   = ["pdf", "eps", "C", "png"]
#     note_dir   = "background"
#     note_name  = []

#     for Dir in lst_dir:
#         for region in lst_region:
#             for Type in lst_type:
#               for form in lst_form:
#                   for i, plt in enumerate(lst_plt):
#                       originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + Dir + "_" + Type + "_" + region + "_" + plt + "." + form
#                       os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))

# # #for unBlinded Control Regions
# #     lst_dir    = ["Moriond_bkg_9"]
# #     lst_region = ["Control"]
# #     lst_type   = ["FourTag", "ThreeTag", "TwoTag_split"]
# #     lst_plt    = ["mHH_l_1"]
# #     lst_form   = ["pdf", "eps", "C", "png"]
# #     note_dir   = "background"
# #     note_name  = []

# #     for Dir in lst_dir:
# #         for region in lst_region:
# #             for Type in lst_type:
# #                 for form in lst_form:
# #                     for i, plt in enumerate(lst_plt):
# #                         originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + Dir + "_" + Type + "_" + region + "_" + plt + "." + form
# #                         os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))

# # #for unBlinded Signal Regions
# #     lst_dir    = ["Moriond_bkg_9"]
# #     lst_region = ["Signal"]
# #     lst_type   = ["FourTag", "ThreeTag", "TwoTag_split"]
# #     lst_plt    = ["mHH_pole_1", "mHH_pole"]
# #     lst_form   = ["pdf", "eps", "C", "png"]
# #     note_dir   = "results"
# #     note_name  = []

# #     for Dir in lst_dir:
# #         for region in lst_region:
# #             for Type in lst_type:
# #                 for form in lst_form:
# #                     for i, plt in enumerate(lst_plt):
# #                         originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + Dir + "_" + Type + "_" + region + "_" + plt + "." + form
# #                         os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))


# # #for unBlinded TT and ZZ Regions
# #     lst_dir    = ["Moriond_TT", "Moriond_ZZ"]
# #     lst_region = ["Signal"]
# #     lst_type   = ["FourTag", "ThreeTag", "TwoTag_split"]
# #     lst_plt    = ["mHH_l", "mHH_l_1"]
# #     lst_form   = ["pdf", "eps", "C", "png"]
# #     note_dir   = "others/Validations"
# #     note_name  = []

# #     for Dir in lst_dir:
# #         for region in lst_region:
# #             for Type in lst_type:
# #                 for form in lst_form:
# #                     for i, plt in enumerate(lst_plt):
# #                         originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + Dir + "_" + Type + "_" + region + "_" + plt + "." + form
# #                         os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))

# #for Trackjet distributions
#     lst_dir    = ["Moriond"]
#     lst_region = ["Sideband"]
#     lst_type   = ["FourTag", "ThreeTag", "TwoTag_split"]
#     lst_plt    = ["leadHCand_trk0_Pt"]
#     lst_form   = ["pdf", "eps", "C", "png"]
#     note_dir   = "others/Prereweight"
#     note_name  = []

#     for Dir in lst_dir:
#         for region in lst_region:
#             for Type in lst_type:
#                 for form in lst_form:
#                     for i, plt in enumerate(lst_plt):
#                         originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + Dir + "_" + Type + "_" + region + "_" + plt + "." + form
#                         os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))

# #for unBlinded Sideband Regions
#     lst_dir    = ["Moriond_bkg_9"]
#     lst_region = ["Sideband"]
#     lst_type   = ["FourTag", "ThreeTag", "TwoTag_split"]
#     lst_plt    = ["mHH_l_1", "leadHCand_trk0_Pt"]
#     lst_form   = ["pdf", "eps", "C", "png"]
#     note_dir   = "others/Postreweight"
#     note_name  = []

#     for Dir in lst_dir:
#         for region in lst_region:
#             for Type in lst_type:
#                 for form in lst_form:
#                     for i, plt in enumerate(lst_plt):
#                         originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + Dir + "_" + Type + "_" + region + "_" + plt + "." + form
#                         os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))


# #for prereweight Sideband/Control Regions
#     lst_dir    = ["Moriond"]
#     lst_region = ["Control", "Sideband"]
#     lst_type   = ["FourTag", "ThreeTag", "TwoTag_split"]
#     lst_plt    = ["mHH_l_1"]
#     lst_form   = ["pdf", "eps", "C", "png"]
#     note_dir   = "others/Prereweight"
#     note_name  = []

#     for Dir in lst_dir:
#         for region in lst_region:
#             for Type in lst_type:
#                 for form in lst_form:
#                     for i, plt in enumerate(lst_plt):
#                         originpath = plotpath + Dir + "/PaperPlot/" + region + "/" + Dir + "_" + Type + "_" + region + "_" + plt + "." + form
#                         os.system(pack_copy(originpath, targetpath=notepath + note_dir + "/"))


    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': 
    main()