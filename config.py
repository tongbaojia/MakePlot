#Tony: master configuration file, specifies all the necessary paths
import ROOT, helpers, os

#get current directory
currpath    = os.path.abspath(os.curdir)
#change this to your home directory of everything; should be where the code is checked out
#toppath     =  os.path.dirname(currpath)
toppath     =  "/afs/cern.ch/work/g/gputnam/public"
#input top directory for the root files
#outputname = "/trkpt-ratio-Outputs/"
#outputname = "/detacut-outputs/"
outputname = "/Output/"
inputpath   =  toppath + outputname
helpers.checkpath(inputpath)
#output top directory for the output plots/root files
outputpath  =  toppath + outputname
helpers.checkpath(outputpath)
#output top directory for only plots
outplotpath =  toppath +"/Plot/"
helpers.checkpath(outplotpath)
#check if reference folder exists
refpath     =  toppath + outputname + "ref/"
if not os.path.exists(refpath):
	print "please copy the directory: /afs/cern.ch/user/b/btong/work/public/RunIIHH4b/ref over to Output/ref!!!"
else:
	pass
#setup all the other constants
#MC mass points
mass_lst   = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
#plot color variables
clr_lst  = [ROOT.kRed+1, ROOT.kBlue+1, ROOT.kOrange+7, ROOT.kGreen+3, ROOT.kPink-8, 
	ROOT.kSpring-7, ROOT.kMagenta+2, ROOT.kCyan+1, ROOT.kViolet-6, ROOT.kTeal+3, ROOT.kBlue+6, 
	ROOT.kRed-1, ROOT.kBlue-1, ROOT.kOrange-7, ROOT.kGreen-3, ROOT.kPink+8]
#plot marker style variables
mrk_lst  = range(20, 40)
#defuault root file name
hist_r = "hist-MiniNTuple.root"
#current total luminiosity, in fb
totlumi = 13.3
#color dictionary for plotting style
col_dic = {"syst":ROOT.kGray+2}
#size for legend
legsize = 17
paperlegsize = 28
