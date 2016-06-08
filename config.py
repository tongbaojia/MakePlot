#Tony: master configuration file, specifies all the necessary paths
import ROOT
#change this to your home directory of everything
toppath = "/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/"
#input top directory for the root files
inputpath  =  toppath + "Output/"
#output top directory for the output plots/root files
outputpath =  toppath +"Output/"
#output top directory for only plots
outplotpath =  toppath +"Plot/"
#MC mass points
mass_lst   = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
#other variables
clr_lst  = [ROOT.kRed+1, ROOT.kBlue+1, ROOT.kOrange+7, ROOT.kGreen+3, ROOT.kPink-8, ROOT.kSpring-7, ROOT.kMagenta+2, ROOT.kCyan+1, ROOT.kViolet-6, ROOT.kTeal+3]