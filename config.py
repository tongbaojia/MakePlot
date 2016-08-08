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

# returns the number of scores in a list
# that pass the given b-tagging WP
def num_btags(bs, b_tagging_cut = 0.3706): # 77% working point
    return len([b for b in bs if b > b_tagging_cut])

# all b-tagging regions, and their definitions
# for each region, define a function that takes in the b-tagging scores
# of the two top-scored trackjets from both jets in an event, 
# and returns whether that event belongs in that 
# region. Note that the set of regions should be disjoint/orthogonal to one another.
bregions = {
	"NoTag"        : lambda b0,b1: num_btags(b0 + b1) == 0,
	"OneTag"       : lambda b0,b1: num_btags(b0 + b1) == 1,
	"TwoTag"       : lambda b0,b1: (not num_btags(b0) == num_btags(b1)) and num_btags(b0+b1) == 2,
	"TwoTag_split" : lambda b0,b1: num_btags(b0) == num_btags(b1) == 1,
	"ThreeTag"     : lambda b0,b1: num_btags(b0+b1) == 3,
        "FourTag"      : lambda b0,b1: num_btags(b0+b1) == 4,
}

# cuts to be included in signal region
signal_lst = ["FourTag", "ThreeTag", "TwoTag_split"]
# background for each region
bkg_lst = ["Bkg_" + s for s in signal_lst]
cut_lst = signal_lst + bkg_lst

# For each background region, define a function
# that takes in bjet scores and number of trackjets to define whether
# to include a given event
backgrounds = {
	"Bkg_FourTag"      : lambda b0,ntj0,b1,ntj1: bregions["NoTag"](b0,b1) and ntj0 >= 2 and ntj1 >= 2,
	"Bkg_ThreeTag"	   : lambda b0,ntj0,b1,ntj1: bregions["NoTag"](b0,b1) and  
				( (ntj0 >= 1 and ntj1 >= 2) or (ntj0 >= 2 and ntj1 >= 1) ),
        "Bkg_TwoTag_split" : lambda b0,ntj0,b1,ntj1: bregions["NoTag"](b0,b1) and ntj0 >= 1 and ntj1 >= 1,
}



