#Tony: master configuration file, specifies all the necessary paths
import ROOT, helpers, os

#get current directory
currpath    = os.path.abspath(os.curdir)
#change this to your home directory of everything; should be where the code is checked out
toppath     =  os.path.dirname(currpath)
#input top directory for the root files
inputpath   =  toppath + "/Output/"
helpers.checkpath(inputpath)
#output top directory for the output plots/root files
outputpath  =  toppath +"/Output/"
helpers.checkpath(outputpath)
#output top directory for only plots
outplotpath =  toppath +"/Plot/"
helpers.checkpath(outplotpath)
#check if reference folder exists
refpath     =  toppath +"/Output/ref/"
if not os.path.exists(outputpath):
	print "please copy the directory: /afs/cern.ch/user/b/btong/work/public/RunIIHH4b/ref over to Output/ref!!!"
else:
	pass

#setup all the other constants
#MC mass points
mass_lst   = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
#plot color variables
clr_lst  = [ROOT.kRed+1, ROOT.kBlue+1, ROOT.kOrange+7, ROOT.kGreen+3, ROOT.kPink-8, ROOT.kSpring-7, ROOT.kMagenta+2, ROOT.kCyan+1, ROOT.kViolet-6, ROOT.kTeal+3, ROOT.kBlue+6]
#defuault root file name
hist_r = "hist-MiniNTuple.root"
