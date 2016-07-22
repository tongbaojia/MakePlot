import ROOT, rootlogon
import argparse
import copy
import glob
import helpers
import os
import sys
import time
import config as CONF
from array import array
import numpy as np
import sys
from plot_2dhists import DrawHists 

# load landau-gauss file
ROOT.gROOT.LoadMacro("langaus.C")

outputdir = CONF.outplotpath
CONF.inputpath = "../Output/"
basedir = "F_c10-cb-b85/"
signals = []
data = []

# mass_lst = [700, 800, 900, 1000, 1100, 1200, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
#mass_lst = [1000, 1100, 1200, 1400, 1500, 1600, 1800, 2000]
mass_lst = [2500, 2750, 3000]


for mass in mass_lst:
    signals.append( basedir + ("signal_G_hh_c10_M%d/hist-MiniNTuple.root" % mass))
    #signals.append(basedir  + ("signal_2HDM_hh_c10_M%d/hist-MiniNTuple.root" % mass))

data.append( basedir + "data_test15/hist-MiniNTuple.root")
data.append( basedir + "data_test16/hist-MiniNTuple.root")

"""
scuts = ["AllTag_Signal/h0_tj_pt_dR", "AllTag_Signal/h1_tj_pt_dR"]
dcuts = ["Alltag/h0_tj_pt_dR", "Alltag/h1_tj_pt_dR"]

deltas = np.linspace(0, .5, 21)
masses = np.linspace(225.0/2, 325.0/2, 21)

cutvals = [(m,d) for m in masses for d in deltas]
cutstr = "m: %.1f, #delta: %.3f"
"""

#scuts = ["ThreeTag_Incl/mH0H1", "FourTag_Incl/mH0H1", "TwoTag_split_Incl/mH0H1"]
#dcuts = ["ThreeTag_Incl/mH0H1", "FourTag_Incl/mH0H1", "TwoTag_split_Incl/mH0H1"]
scuts = ["AllTag_Incl/mH0H1"]
dcuts = ["NoTag_Incl/mH0H1"]


cutvals = np.linspace(0.5, 1.5, 11)
cutvals = [(c0,c1) for c0 in cutvals for c1 in cutvals)]
cutstr = "max pt ratio: %.1f"

def main():

    ops = options()
    # create output file
    output = ROOT.TFile.Open(CONF.outplotpath + "sig_truth.root", "recreate")

    print output

    # # Draw the efficiency plot relative to the all normalization
    # name of the canvas
    cname = "roc_plot_pt-ratio.pdf"
    cut_func = pass_ptmax
    DrawRoc(output, scuts[0], dcuts[0], cut_func, cname, histdim=1)
    output.Close()


def passcut_dR(pt, dR, m, d):
    if pt > 1000.0:
	return True
    cval = 2*m/pt
    return abs(cval - dR) < d

def passcut_SR(m0, m1, cutval):
    a = cutval[0]
    cor = cutval[1]
    m0term = (m0*(m0-124)/124**2)
    m1term = (m1*(m1-115)/115**2)
    return np.sqrt( m0term**2 + m1term**2 + cor*m0term*m1term ) < a

def pass_SR(m0, m1, d):
    return np.sqrt( ((m0-124)/(0.1*m0))**2 + ((m1-115)/(0.1*m1))**2 ) < d

def pass_extended_SR(m0, m1, cutvals):
    m0pole = 124
    m1pole = 115

    r = cutvals[0]
    extend0 = cutvals[1]
    extend1 = cutvals[2]

    # first try h0:
    if m0 > m0pole:
	h0comp = m0pole
    elif m0 < m0pole - extend0:
	h0comp = m0pole - extend0
    else:
	h0comp = m0
    tryh0 = np.sqrt( ((m0-h0comp)/(0.1*m0))**2 + ((m1-m1pole)/(0.1*m1))**2 ) < r
    if tryh0:
	return True

    # now try h1:
    if m1 > m1pole:
	h1comp = m1pole
    elif m1 < m1pole - extend1:
	h1comp = m1pole - extend1
    else:
	h1comp = m1
    tryh1 = np.sqrt( ((m0-m0pole)/(0.1*m0))**2 + ((m1-h1comp)/(0.1*m1))**2 ) < r
    return tryh1

def pass_bean(m0,m1,a):
    x = (m0 - 124)
    y = (m1 - 115)
    r = np.sqrt(x**2 + y**2)
    ret = (-x**5 - (r**2)*y**3) < (r**6)*a 
    return ret

def pass_Landau(m0,m1,cutval):
    cor = cutval[1]
    r = cutval[0]

    p0 = ROOT.TMath.Landau(124-m0, -5.26469, 5.89952)
    p1 = ROOT.TMath.Landau(115-m1, -5.73268, 8.88988)
    if p0 < 1e-10 or p1 < 1e-10:
	return False
  
    m0term = np.array(.01/p0)
    m1term = np.array(.01/p1)
    return np.sqrt( m0term**2 + m1term**2 + cor*m0term*m1term ) < r

def pass_LandauGauss(m0,m1,cutval):
    cor = cutval[1]
    r = cutval[0]
    
    h0param = array("d",[3.73036e+00, -1.39094e+02, 2.66003e+01, 7.65407e+00])
    h1param = array("d",[5.90745e+00, -1.31344e+02, 2.72896e+01, 1.01674e+01])

    p0 = ROOT.langaus( array("d",[m0]), h0param )
    p1 = ROOT.langaus( array("d",[m1]), h1param )
    if p0 < 1e-10 or p1 < 1e-10:
	return False
  
    m0term = np.array(.01/p0)
    m1term = np.array(.01/p1)
    return np.sqrt( m0term**2 + m1term**2 + cor*m0term*m1term ) < r

def pass_ptmax(h0ptratio, h1ptratio, cutval):
    return h0ptratio < cutval && h1ptratio < cutval

def cut_eff(cutval, cutfunc, histdim, *hists):
    retvals = []
    for h in hists:
	retvals.append(0)
        # only iterate over values for dR < 2.5
	#ny = h.GetYaxis().FindBin(2.5)

        nx = h.GetNbinsX()
	if histdim == 2:
	    ny = h.GetNbinsY()

	for ix in range(nx):
	    xval = h.GetXaxis().GetBinCenter(ix)
	    if histdim == 2:
	        for iy in range(ny):
		    yval = h.GetYaxis().GetBinCenter(iy)
		    if cutfunc(xval, yval, cutval):
		        retvals[-1] += h.GetBinContent(ix, iy)	    
	    else:
	        if cutfunc(xval, cutbal):
		    retvals[-1] += h.GetBinContent(ix)

    #print retvals
    return retvals

def DrawRoc(outputroot, scut, dcut, cut_func, canv_name, histdim=2):
    #signalmc = ROOT.TH2F(scut, "dR between lead, subleading track jet", 350, 0, 3500, 130, 0, 6.5)
    #datamc = ROOT.TH2F(dcut, "dR between lead, subleading track jet", 350, 0, 3500, 130, 0, 6.5)

    sig_file_list = []
    # iterate over signal files
    input_mcs = []
    for f in signals:
	input_mcs.append( ROOT.TFile.Open(CONF.inputpath + f) )
        if not input_mcs[-1]: 
            print CONF.inputpath + f
        try: 
            sig_file_list.append( input_mcs[-1].Get(scut).Clone() ) 
        except: 
            print CONF.inputpath + f
            print scut 
            raise 
	#input_mc.Close()

    # set up our base histogram
    sigbase = sig_file_list[0]
    if histdim == 2:
        signalmc = ROOT.TH2F(scut, "roc signal", sigbase.GetXaxis().GetNbins(), sigbase.GetXaxis().GetXmin(), sigbase.GetXaxis().GetXmax(),
				sigbase.GetYaxis().GetNbins(), sigbase.GetYaxis().GetXmin(), sigbase.GetYaxis().GetXmax() ) 
    elif histdim == 1:
        signalmc = ROOT.TH1F(scut, "roc signal", sigbase.GetXaxis().GetNbins(), sigbase.GetXaxis().GetXmin(), sigbase.GetXaxis().getXmax() ) 
    else:
        raise ValueError("histdim must be 1 or 2")

    ROOT.SetOwnership(signalmc, False)

    # scale all mass points equally
    for i in range(len(sig_file_list)):
	scalefactor = sig_file_list[i].Integral()
        sig_file_list[i].Scale(1/scalefactor)
        signalmc.Add( sig_file_list[i] ) 

    # iterate over all the data
    data_file_list = []
    dinput_mcs = []
    for f in data:
	dinput_mcs.append( ROOT.TFile.Open(CONF.inputpath + f) )
        if not dinput_mcs[-1]: 
            print CONF.inputpath + f
        try: 
            data_file_list.append( dinput_mcs[-1].Get(scut).Clone() ) 
        except: 
            print CONF.inputpath + f
            print dcut 
            raise 
	#input_mc.Close()

    # set up data base hist
    database = data_file_list[0]
    if histdim == 2:
        datamc = ROOT.TH2F(dcut, "roc signal", database.GetXaxis().GetNbins(), database.GetXaxis().GetXmin(), database.GetXaxis().GetXmax(),
				database.GetYaxis().GetNbins(), database.GetYaxis().GetXmin(), database.GetYaxis().GetXmax() )
				sigbase.GetYaxis().GetNbins(), sigbase.GetYaxis().GetXmin(), sigbase.GetYaxis().GetXmax() )
    elif histdim == 1:
	datamc = ROOT.TH1F(dcut, "roc signal", sigbase.GetXaxis().GetNbins(), database.GetXaxis().GetXmin(), database.GetXaxis().getXmax() )
    else:
	raise ValueError("histdim must be 1 or 2")

    ROOT.SetOwnership(datamc, False)

    # don't scale for data
    for i in range(len(data_file_list)):
        datamc.Add( data_file_list[i] )

    # rebin for speed
    if histdim == 2:
        signalmc.Rebin2D(2,2)
        datamc.Rebin2D(2,2)
    elif histdim == 1:
        signalmc.Rebin(2)
        datamc.Rebin(2)

    sigsize = signalmc.Integral()
    datasize = datamc.Integral()

    coords = []
    testvals = []

    for c in cutvals:
	# status feedback to user
	print " "*45
	sys.stdout.write("\033[F")
	print c
	sys.stdout.write("\033[F")

	cutsize = cut_eff(c, cut_func, histdim, signalmc, datamc)
	if abs(cutsize[1]/datasize) < 1e-4:
	    continue
	coords.append( (cutsize[0]/sigsize, 1 - cutsize[1]/datasize) )
	testvals.append( c )

    # make the ROC plot onto a canvas
    canv = ROOT.TCanvas("RP","Roc Plot",200,10,700,500);
    xs = [x for x,y in coords]
    ys = [y for x,y in coords]
    roc = ROOT.TGraph(len(xs), np.array(xs,dtype="float64"), np.array(ys,dtype="float64"))
    roc.Draw("ap")

    roc.GetXaxis().SetTitle("Signal Eff")
    roc.GetYaxis().SetTitle("1 - Background Eff")

    # Draw Watermarks
    wm = helpers.DrawWatermarks(0.35,0.35)

    # get the optimal parameter set


    sig = map(lambda x: x[0]/np.sqrt(1-x[1]), coords)

    sig9 = map(lambda x: x[0]/np.sqrt(1-x[1]), [c if c[0] > .9 else (0,0) for c in coords ])

    print "\n\nOptimal S/sqrt(B) for any signal efficiency:"
    print "Value: " + str(max(sig))
    print "Cutvals: " + str(testvals[sig.index(max(sig))])
    print "ROC coords: " + str(coords[sig.index(max(sig))])
     
    """
    print "\nOptimal S/sqrt(B) for signal efficiency > .9:"
    print "Value: " + str( max(sig9))
    print "Cutvals: " + str(testvals[sig9.index(max(sig9))])
    print "ROC coords: " + str(coords[sig9.index(max(sig9))])
    """

    # draw on canvas optimal cut info
    sBmax = max(sig)
    coordmax = coords[sig.index(max(sig))]
    vmax = testvals[sig.index(max(sig))]

    xdraw = 0.75
    ydraw = 0.85
    sBmax_info = ROOT.TLatex(xdraw, ydraw, "S/#sqrt{B}: %.2f" % sBmax)
    coord_info = ROOT.TLatex(xdraw, ydraw-0.06, "coords: %.2f, %.2f" % (coordmax[0], coordmax[1]))
    vmax_info = ROOT.TLatex(xdraw, ydraw-0.12, cutstr % vmax)
    # Draw
    words = helpers.DrawWords(sBmax_info, coord_info, vmax_info)
  
    # arrow!
    arr = ROOT.TArrow(0.85,0.75,coordmax[0], coordmax[1])
    arr.Draw()    

    canv.SaveAs(outputdir + canv_name)
    canv.Close()

    return

    # decide on the histogram range
    if "h0" in scut:
	pTrange = (450, 2000)
    elif "h1" in scut:
	pTrange = (250, 2000)

    # now draw histograms in signal and data
    DrawHists(outputroot, [scut], "", signals, "mc_", cutvals=vmax, Xrange=pTrange)
    DrawHists(outputroot, [dcut], "", data, "data_", cutvals=vmax,  Xrange=pTrange) 

def ratioerror(a, b):
    if a > 0:
        return a / b * ROOT.TMath.Sqrt(1.0/a + 1.0/b)
    else:
        return 0

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="TEST")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def warn(message):
    print
    print "Warning in %s: %s" % (__file__, message)
    print

if __name__ == "__main__":
    main()
