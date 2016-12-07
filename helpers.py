import copy
import math
import ROOT
import os, sys
from array import array
import time
import glob

ROOT.gROOT.SetBatch(True)
canv = None

#
#  Get Options
#
def parseOpts():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-c', '--config',       dest="config",         default="plotConfig.py", help="Input Config")
    parser.add_option('-i', '--interactive',  action="store_true",   default=False, help="Run interactive")
    parser.add_option('-o', '--output',       dest="outputDir",      default=".",   help="output dir")
    parser.add_option(      '--inputDir',     dest="inputDir",       default=".",   help="input dir")
    parser.add_option("--plotter",            dest="plotter",        default=None, help="Plotter")
    parser.add_option("--prename",            dest="prename",        default=None, help="file first name")
    (o,a) = parser.parse_args()

    if not o.plotter:
        fatal("Need --plotter for configuration.")
    return (o,a)


def plotterConfig(plotter):
    if not "tree" in plotter:
        print "No input Tree, assuming hists"
        plotter["files"]      = {}

    plotter["foldersTag"] = {}
    plotter["weights"]    = {}
    plotter["is_data"]    = {}
    plotter["stack"]      = {}
    plotter["colors"]     = {}
    plotter["rColors"]    = {}
    plotter["overlay"]    = {}
    plotter["labels"]     = {}
    plotter["output"]     = None
    plotter["trees"]      = {}
    if not "directory" in plotter:
        plotter["directory"] = "."
        warn("No directory given. Writing output to cwd.")

    # retrieve inputs
    timestamp = time.strftime("%Y-%m-%d-%Hh%Mm%Ss")
    print time.strftime("%Y-%m-%d-%Hh%Mm%Ss"),"Retrieving input files"


    for sample in plotter["samples"]:
        name = sample["name"]
        #samples.append(name)

        # input files
        paths = sample["path"]
        if not glob.glob(paths):
            fatal("Found no files at %s" % (paths))

        if plotter["useTree"]: 
            plotter["trees"][name] = ROOT.TChain(plotter["tree"])
            for path in glob.glob(paths):
                if len(path) > 100: print "adding file:",path[0:50]+"..."+path[len(path)-50:]
                else:               print "adding file:",path
                plotter["trees"][name].Add(path)

        else:
            path                        = paths
            plotter["files"][name]      = ROOT.TFile(path,"READ")
            plotter["foldersTag"][name] = sample["folderTag"]
            plotter["cutName"]          = sample["folderCuts"]
            plotter["regionName"]       = sample["folderReg"]


        if plotter["useTree"]: plotter["weights"][name] = " * ".join(sample["weights"]) if "weights" in sample else "1"
        else                 : plotter["weights"][name] = sample["weights"]
        plotter["colors"][name]  = eval(sample["color"]) if sample["color"].startswith("ROOT") else sample["color"] 
        if "rColor" in sample.keys():
            plotter["rColors"][name] = eval(sample["rColor"]) if sample["rColor"].startswith("ROOT") else sample["rColor"] 
        plotter["labels"] [name]  = sample["label"]
        plotter["stack"]  [name]  = sample["stack"]
        plotter["overlay"][name]  = sample["overlay"]
        plotter["is_data"][name]  = sample["is_data"]

    # create output file
    if not os.path.isdir(plotter["directory"]):
        os.makedirs(plotter["directory"])

    print "Saving ROOT File of Canvas:", "%s/plots.%s.canv.root" % (plotter["directory"], timestamp)
    plotter["output"] = ROOT.TFile.Open("%s/plots.%s.canv.root" % (plotter["directory"], timestamp), "recreate")
    return plotter


#
#
#
def listVars(varName,regionName,plotter):
    inputDir = plotter["files"][plotter["samples"][0]["name"]].Get(regionName)
    
    for k in inputDir.GetListOfKeys():
        thisName = k.GetName()

        if thisName.find(varName) == -1: continue

        if isinstance(inputDir.Get(thisName),ROOT.TH1):
            print thisName


#
#
#
def clear():
    global canv
    if canv:
        canv.Close()

#
#  Make the actual plot
#
def plot(var, cut, region, plotter_config,  **kw):

    global legend, watermarks, canv, shared

    #
    # Un pack som plotter config
    #
    foldersTag = plotter_config["foldersTag"]
    files      = plotter_config["files"]
    samples    = plotter_config["samples"]
    weights    = plotter_config["weights"]
    is_data    = plotter_config["is_data"]
    stack      = plotter_config["stack"]
    colors     = plotter_config["colors"]
    rColors    = plotter_config["rColors"]
    overlay    = plotter_config["overlay"]
    labels     = plotter_config["labels"]
    output     = plotter_config["output"]


    testSampleName = samples[0]["name"]
    testDirName    = foldersTag[testSampleName]
    
    if var.find("*") != -1: return listVars(var.replace("*",""),cut+testDirName+region, plotter_config)

    xtitle = None
    ytitle = None
    name   = None
    x_min  = None
    x_max  = None

    if not plotter_config["useTree"]:
        if cut+foldersTag[testSampleName]+region != "": 
            histPath = cut+foldersTag[testSampleName]+region+"/"+var
        else: 
            histPath = var

        testHist = files[samples[0]["name"]].Get(histPath)
        xtitle   = testHist.GetXaxis().GetTitle()
        ytitle   = testHist.GetYaxis().GetTitle()
        name     = testHist.GetName()
        x_min    = testHist.GetXaxis().GetXmin()
        x_max    = testHist.GetXaxis().GetXmax()
        
    bins      = kw.get('bins'     ,  None) 
    xtitle    = kw.get('xtitle'   ,  xtitle) 
    ytitle    = kw.get('ytitle'   ,  ytitle) 
    selection = kw.get('selection',  None) 
    name      = kw.get('name'     ,  name) 
    n_bins    = kw.get('n_bins'   ,  None) 
    x_min     = kw.get('x_min'    ,  x_min) 
    x_max     = kw.get('x_max'    ,  x_max) 
    rebin     = kw.get('rebin'    ,  None) 
    logY      = kw.get('logY'     ,  None)
    options   = kw.get('options'  ,  '')
    canvSize  = kw.get('canvSize' ,  [700,700])
    rMargin   = kw.get('rMargin'  ,  0)

    hists = {}
    draw = {}
    if bins:
        draw["bins"]  = array.array("d", [float(x) for x in bins])
    draw["title"]     = ";%s;%s" % (xtitle, ytitle)
    draw["variable"]  = var
    if selection: draw["selection"] = " && ".join(selection)

    canv = ROOT.TCanvas(name, name, canvSize[0], canvSize[1])
    canv.Draw()
    canv.Update()
    canv.SetLogy(logY)

    stacks   = ROOT.THStack(name+"stacks",   draw["title"])
    overlays = ROOT.THStack(name+"overlays", draw["title"])
    do_stack = False
    do_overlay = False
    
    for sample in reversed(sorted(samples)):
        sampleName = sample["name"]
        draw["name"]   = name+"__"+sampleName
        draw["weight"] = weights[sampleName]


        if plotter_config["useTree"]:
            for option in ["weight"]:
                draw[option] = "(%s)" % (draw[option])

        if plotter_config["useTree"]:
            if bins:
                hists[sampleName] = ROOT.TH1F(draw["name"], draw["title"], len(draw["bins"])-1, draw["bins"])
            else:
                hists[sampleName] = ROOT.TH1F(draw["name"], draw["title"], n_bins, x_min, x_max)
            hists[sampleName].Sumw2()

        else:
            if cut+foldersTag[sampleName]+region != "": histPath = cut+foldersTag[sampleName]+region+"/"+draw["variable"]
            else: histPath = draw["variable"]
            hists[sampleName] = files[sampleName].Get(histPath)
            hists[sampleName].SetName(draw["name"])
            hists[sampleName].SetTitle(draw["title"])
            if "TH2" in str(hists[sampleName]):
                hists[sampleName].RebinX(rebin)
                hists[sampleName].RebinY(rebin)
                hists[sampleName].GetYaxis().SetTitleOffset(1.5)
            else:
                if isinstance(rebin,list):
                    hists[sampleName]=helpers.do_variable_rebinning(hists[sampleName], rebin)
                elif rebin:
                    hists[sampleName].Rebin(rebin)
            if x_max:
                x_min  = float(x_min)
                x_max = float(x_max)
                hists[sampleName].GetXaxis().SetRangeUser(x_min,x_max)

        if is_data[sampleName]:
            hists[sampleName].SetMarkerStyle(20)
            hists[sampleName].SetMarkerSize(1)

        if plotter_config["useTree"]: trees[sampleName].Draw("%(variable)s >> %(name)s" % draw, "(%(selection)s) * %(weight)s" % draw, "goff")
        else      : 
            hists[sampleName].Sumw2()
            hists[sampleName].Scale(float(draw["weight"]))
            hists[sampleName].Draw(options)
            if rMargin: ROOT.gPad.SetRightMargin(rMargin)

        # hists[sampleName].Scale(1/hists[sampleName].Integral(0, hists[sampleName].GetNbinsX()))

        if stack[sampleName]:
            do_stack = True
            hists[sampleName].SetFillColor(colors[sampleName])
            hists[sampleName].SetLineColor(ROOT.kBlack)
            hists[sampleName].SetLineWidth(2)
            stacks.Add(copy.copy(hists[sampleName]), ("ep" if is_data[sampleName] else "hist"))
            if not plotter_config["useTree"] and x_max:#have to set stack xaxis range for zooming because ROOT SUCKS
                stacks.Draw()
                stacks.GetXaxis().SetRangeUser(x_min,x_max)
                                               
        if overlay[sampleName]:
            do_overlay = True
            hists[sampleName].SetFillColor(0)
            hists[sampleName].SetLineColor(colors[sampleName])
            hists[sampleName].SetLineWidth(3)
            overlays.Add(copy.copy(hists[sampleName]), ("ep" if is_data[sampleName] else "hist"))
            
        print sampleName
        #print "Integral:",hists[sample].Integral(0, hists[sample].GetNbinsX()+1)
        print "Integral:",hists[sampleName].Integral()
        print " Entries:",hists[sampleName].GetEntries()

    # draw
    maximum = max([stacks.GetMaximum(), overlays.GetMaximum("nostack")])
    maximum = maximum*(20.0 if logY    else 1.3)
    maximum = maximum*(1.2   if plotter_config['ratio']   else 1.0)
    minimum = max([stacks.GetMinimum(), overlays.GetMinimum("nostack")])
    minimum = (minimum/2 if logY else 0)


    if do_stack:
        stacks.SetMaximum(maximum)
        stacks.SetMinimum(minimum)
        stacks.Draw()
        h1stackerror = copy.copy(stacks.GetStack().Last())
        h1stackerror.SetName("stat. error")
        h1stackerror.SetFillColor(ROOT.kGray+3)
        h1stackerror.SetFillStyle(3005)
        h1stackerror.SetMarkerStyle(0)
        h1stackerror.Draw("SAME,E2")

    if do_overlay and do_stack:
        overlays.SetMaximum(maximum)
        overlays.SetMinimum(minimum)
        overlays.Draw("nostack,same")
    elif do_overlay:
        overlays.SetMaximum(maximum)
        overlays.SetMinimum(minimum)
        overlays.Draw("nostack")

    if plotter_config["data"]:
        pass

    if plotter_config["ratio"] and stacks.GetStack():

        # numerator definition is a placeholder.
        # only works if overlay[0]=data.
        if plotter_config["autoRatio"]:

            top = overlays.GetHists()[0].Clone("hnew")
            bottom = stacks.GetStack().Last().Clone("hnew")
            top.Divide(bottom)
            ratioBins = []
            for bin in range(top.GetSize()):
                if top.GetBinContent(bin) != 0.0 and top.GetBinContent(bin)*top.GetBinError(bin) < 5.0:
                    ratioBins.append(top.GetBinContent(bin))
            if not ratioBins: ratioBins = [0]

            ratioMin = float(int(min(ratioBins)*100))/100
            ratioMax = float(int(max(ratioBins)*100))/100
            if ratioMax-ratioMin < 0.1:
                ratioMin = ratioMin-.05
                ratioMax = ratioMax+0.5

        else:
            ratioMin = 0
            ratioMax = 2 

        if sampleName not in rColors.keys(): rColors[sampleName] = ROOT.kRed

        ratio = helpers.ratio(name   = canv.GetName()+"_ratio",
                              numer  = overlays.GetHists().Last(),   # AHH KILL ME
                              denom  = stacks.GetStack().Last(),
                              min    = ratioMin,
                              max    = ratioMax,
                              ytitle = "Data / pred.",
                              color  = rColors[sampleName]
                              )

        canv. SetFillColorAlpha(1, 0.0);

        share,top_pad, bottom_pad = helpers.same_xaxis(name          = canv.GetName()+"_share",
                                                       top_canvas    = canv,
                                                       bottom_canvas = ratio,
                                                       )
        
        
        canv .SetName(canv.GetName()+"_noratio")
        share.SetName(share.GetName().replace("_share", ""))
        canv = share
        
    elif plotter_config["ratio"] and not stacks.GetStack():
        warn("Want to make ratio plot but dont have stack. Skipping ratio.")

    # stack legend
    if do_stack or do_overlay:
        xleg, yleg = 0.79, 0.79
        legend = ROOT.TLegend(xleg, yleg, xleg+0.15, (yleg+0.125))


        if do_overlay:
            for hist in reversed(overlays.GetHists()):
                legend.AddEntry(hist, labels[hist.GetName().split("__")[1]], "l")

        if do_stack:
            for hist in reversed(stacks.GetHists()):
                legend.AddEntry(hist, labels[hist.GetName().split("__")[1]], "f")
    
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.03)
        legend.Draw()
        legend.Draw()
        
    # watermarks
    xatlas, yatlas = 0.5, 0.90
    atlas = ROOT.TLatex(xatlas+0.02,   yatlas, "ATLAS Internal")
    hh4b   = ROOT.TLatex(xatlas+0.015, yatlas-0.042, "X #rightarrow HH #rightarrow 4b")
    lumi   = ROOT.TLatex(xatlas, yatlas-0.10,  "#sqrt{s} = 13 TeV,  #int L dt = "+plotter_config["lumi"])
    watermarks = [atlas, hh4b, lumi]


    # KS, chi2
    if stacks.GetStack():
        if plotter_config.get("ks"):
            print "Getting KS from:",overlays.GetHists().Last(),stacks.GetStack().Last()
            kolg, chi2, ndf = helpers.compare(overlays.GetHists().Last(),
                                              stacks.GetStack().Last(),
                                              ) # AH KILL ME
            yks   = 0.975
            ychi2 = 0.975
            xks   = 0.27
            xchi2 = 0.55
            
            ks = ROOT.TLatex(xks,   yks,   "KS = %5.3f" % (kolg))
            if ndf: ch = ROOT.TLatex(xchi2, ychi2, "#chi^{2} / ndf = %.1f / %i = %.3f" % (chi2, ndf, chi2/ndf))
            else:   ch = ROOT.TLatex(xchi2, ychi2, "#chi^{2} / ndf = %.1f / %i" % (chi2, ndf))
            watermarks += [ks, ch]

    wmNum = 0
    # draw watermarks
    for wm in watermarks:
        wm.SetTextAlign(22)
        if wmNum == 0:
            wm.SetTextSize(0.04)
            wm.SetTextFont(72)
        #elif wmNum == 1:
        #    wm.SetTextSize(0.04)
        #    wm.SetTextFont(62)
        else:
            wm.SetTextSize(0.03)
            wm.SetTextFont(42)
        wmNum+=1
        wm.SetNDC()
        wm.Draw()

    canv.SaveAs(os.path.join(plotter_config["directory"], canv.GetName()+".pdf"))

    output.cd()
    canv.Write() 
    canv.Update()


def show_overflow(hist):
    """ Show overflow and underflow on a TH1. h/t Josh """

    nbins          = hist.GetNbinsX()
    underflow      = hist.GetBinContent(   0   )
    underflowerror = hist.GetBinError  (   0   )
    overflow       = hist.GetBinContent(nbins+1)
    overflowerror  = hist.GetBinError  (nbins+1)
    firstbin       = hist.GetBinContent(   1   )
    firstbinerror  = hist.GetBinError  (   1   )
    lastbin        = hist.GetBinContent( nbins )
    lastbinerror   = hist.GetBinError  ( nbins )

    if underflow != 0 :
        newcontent = underflow + firstbin
        if firstbin == 0 :
            newerror = underflowerror
        else:
            newerror = math.sqrt( underflowerror * underflowerror + firstbinerror * firstbinerror )
        hist.SetBinContent(1, newcontent)
        hist.SetBinError  (1, newerror)

    if overflow != 0 :
        newcontent = overflow + lastbin
        if lastbin == 0 :
            newerror = overflowerror
        else:
            newerror = math.sqrt( overflowerror * overflowerror + lastbinerror * lastbinerror )
        hist.SetBinContent(nbins, newcontent)
        hist.SetBinError  (nbins, newerror)

def ratio(name, numer, denom, min, max, ytitle, color = ROOT.kRed):

    numerdenom = copy.copy(numer)
    denomdenom = copy.copy(numer)

    numerdenom.SetName(numer.GetName()+"numerdenom")
    denomdenom.SetName(numer.GetName()+"denomdenom")

    for hist in [numerdenom, denomdenom]:
        hist.Reset()
        hist.SetMinimum(min)
        hist.SetMaximum(max)
        hist.GetYaxis().SetTitle(ytitle)
        hist.GetYaxis().SetTitleOffset(1.5)
        ROOT.SetOwnership(hist, False)

    nbins = numer.GetNbinsX()
    for bin in xrange(0, nbins+2):

        nc = numer.GetBinContent(bin)
        dc = denom.GetBinContent(bin)
        ne = numer.GetBinError(bin)
        de = denom.GetBinError(bin)

        numerdenom.SetBinContent(bin, nc/dc if dc else 0)
        denomdenom.SetBinContent(bin, 1.0   if dc else 0)
        numerdenom.SetBinError(  bin, ne/dc if dc else 0)
        denomdenom.SetBinError(  bin, de/dc if dc else 0)

    canvas = ROOT.TCanvas(name, name, 700, 700)
    #denomdenom.SetFillColor(ROOT.kAzure-9)
    denomdenom.SetFillColor(color)
    denomdenom.SetMarkerSize(0.0)
    denomdenom.Draw("E2, same")
    
    # Fix for error bars when points arent on the ratio
    numerdenom.Draw("PE, same")
    oldSize = numerdenom.GetMarkerSize()
    numerdenom.SetMarkerSize(0)
    numerdenom.SetMarkerSize(0)
    numerdenom.DrawCopy("same e0")
    numerdenom.SetMarkerSize(oldSize)
    numerdenom.Draw("PE same")    

    # x1, x2 = canvas.GetUxmin(), canvas.GetUxmax()
    # y = 1
    # line10 = ROOT.TLine(x1, y, x2, y)
    # line10.SetLineColor(ROOT.kBlack)
    # line10.SetLineWidth(5)
    # line10.SetLineStyle(1)
    # line10.Draw()

    return canvas

def same_xaxis(name, top_canvas, bottom_canvas, split=0.35, axissep=0.04, ndivs=[505, 503]):

    canvas = ROOT.TCanvas(name, name, 700, 700)
    canvas.cd()
    
    top_pad = ROOT.TPad(canvas.GetName()+"_top_pad", "",  0, split, 1, 1, 0, 0, 0)
    top_pad.Draw()

    bottom_pad = ROOT.TPad(canvas.GetName()+"_bottom_pad", "",  0, 0, 1, split, 0, 0, 0)
    bottom_pad.Draw()

    top_pad.cd()
    top_canvas.DrawClonePad()

    bottom_pad.cd()
    bottom_canvas.DrawClonePad()

    top_pad.SetTopMargin(canvas.GetTopMargin()*1.0/(1.0-split))
    top_pad.SetBottomMargin(axissep)
    top_pad.SetRightMargin(canvas.GetRightMargin())
    top_pad.SetLeftMargin(canvas.GetLeftMargin())
    top_pad.SetFillStyle(0) # transparent
    top_pad.SetBorderSize(0)


    bottom_pad.SetTopMargin(axissep)
    bottom_pad.SetBottomMargin(canvas.GetBottomMargin()*1.0/split)
    bottom_pad.SetRightMargin(canvas.GetRightMargin())
    bottom_pad.SetLeftMargin(canvas.GetLeftMargin())
    bottom_pad.SetFillStyle(0) # transparent
    bottom_pad.SetBorderSize(0)


    pads = [top_pad, bottom_pad]
    #factors = [0.9/(1.0-split), 0.9/split]
    factors = [0.67/(1.0-split), 0.9/split]
    for i_pad, pad in enumerate(pads):
        ROOT.SetOwnership(pad, False)
        factor = factors[i_pad]
        ndiv = ndivs[i_pad]
        prims = [ p.GetName() for p in pad.GetListOfPrimitives() ]
        for name in prims:
            h = pad.GetPrimitive(name)
            if any([isinstance(h, obj) for obj in [ROOT.TH1, 
                                                   ROOT.THStack, 
                                                   ROOT.TGraphAsymmErrors,
                                                   ]]):
                try:
                    h = h.GetHistogram()
                except:
                    pass
                #h.SetLabelSize(h.GetLabelSize("Y")*factor, "Y")
                #h.SetLabelSize(0.05, "Y")
                #h.SetLabelSize(h.GetLabelSize("Y"), "Y")
                h.SetTitleSize(h.GetTitleSize("X")*factor, "X")
                h.SetTitleSize(h.GetTitleSize("Y")*factor, "Y")
                h.SetTitleOffset(h.GetTitleOffset("Y")/factor, "Y")
                h.GetYaxis().SetNdivisions(ndiv)
                h.GetXaxis().SetNdivisions()               

                if i_pad == 0:
                    h.SetLabelSize(0.0, "X")
                    h.SetLabelSize(0.05, "Y")
                    h.GetXaxis().SetTitle("")
                else:
                    #h.SetLabelSize(h.GetLabelSize("X")*factor, "X")
                    h.SetLabelSize(0.1, "X")
                    h.SetLabelSize(0.1, "Y")
                    #h.SetLabelSize(h.GetLabelSize("X"), "X")

    canvas.cd()
    return canvas, top_pad, bottom_pad

def compare(data, pred):
    ks   = data.KolmogorovTest(pred)
    chi2 =        data.Chi2Test(pred, "QUW CHI2")
    ndf  = chi2 / data.Chi2Test(pred, "QUW CHI2/NDF") if chi2 else 0.0
    return ks, chi2, ndf



#
# The following is to get the history 
#
global historyPath
global output

def initHistory():

    global historyPath
    historyPath = os.path.expanduser("~/.pyhistory")
    try:
        import readline
    except ImportError:
        print "Module readline not available."
    else:

        import rlcompleter        
        
        if os.path.exists(historyPath):
            readline.read_history_file(historyPath)
        
        
        class IrlCompleter(rlcompleter.Completer):
            """
            This class enables a "tab" insertion if there's no text for
            completion.
        
            The default "tab" is four spaces. You can initialize with '\t' as
            the tab if you wish to use a genuine tab.
        
            """
        
            def __init__(self, tab='    '):
                self.tab = tab
                rlcompleter.Completer.__init__(self)
        
        
            def complete(self, text, state):
                if text == '':
                    readline.insert_text(self.tab)
                    return None
                else:
                    return rlcompleter.Completer.complete(self,text,state)
        
        
        #you could change this line to bind another key instead tab.
        #readline.parse_and_bind("tab: complete")
        import sys
        thisSys = sys.platform
        onMac = (not thisSys.find('darwin') == -1)
        if onMac:
            readline.parse_and_bind ("bind ^I rl_complete") 
        
        #readline.parse_and_bind('tab: complete')
        readline.set_completer(IrlCompleter('\t').complete)
    

    return historyPath


# -----------------------------------------------------------------
def save_history():
    global historyPath
    try:
        import readline
    except ImportError:
        print "Module readline not available."
    else:
        readline.write_history_file(historyPath)



#
#   Do variable rebinning for a histogram
#
def do_variable_rebinning(hist,bins):
    newhist=ROOT.TH1F(hist.GetName(),
                      hist.GetTitle()+";"+hist.GetXaxis().GetTitle()+";"+hist.GetYaxis().GetTitle(),
                      len(bins)-1,
                      array('d',bins))
    a=hist.GetXaxis()
    newa=newhist.GetXaxis()
    for b in range(1, hist.GetNbinsX()+1):
        newb=newa.FindBin(a.GetBinCenter(b))
        val=newhist.GetBinContent(newb)
        err=newhist.GetBinError(newb)
        ratio_bin_widths=newa.GetBinWidth(newb)/a.GetBinWidth(b)
        val=val+hist.GetBinContent(b)/ratio_bin_widths
        err=math.sqrt(err*err+hist.GetBinError(b)/ratio_bin_widths*hist.GetBinError(b)/ratio_bin_widths)
        newhist.SetBinContent(newb,val)
        newhist.SetBinError(newb,err)

    return newhist

def clear_negbin(hist, value=0.0):
    for ibin in range(0, hist.GetNbinsX()+1):
        if hist.GetBinContent(ibin) < value:
            hist.SetBinContent(ibin, value)
            hist.SetBinError(ibin, value)
    return

def ratioerror(a, b, ea=-1, eb=-1):
    if ea > 0 and eb > 0:
        return 1 / b * ea + a / b / b * eb
    elif a > 0:
        return a / b * ROOT.TMath.Sqrt(1.0/a + 1.0/b)
    else:
        return 0

def map_phi(phi):
    while phi >= math.pi:
        phi -= math.pi
    while phi < -(math.pi):
        phi += math.pi
    return phi

def dR(eta1, phi1, eta2, phi2):
    phi1 = map_phi(phi1)
    phi2 = map_phi(phi2)
    return ROOT.TMath.Sqrt((eta1-eta2) ** 2 + (phi1-phi2) ** 2)

#round the significant numbers
def round_sig(x, sig=2):
    if x == 0:
        return 0
    if x > 1:
        return round(x, sig)
    else:
        return round(x, sig-int(ROOT.TMath.Log10(abs(x))))

def checkpath(outputpath):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

def drawProgressBar(percent, barLen = 20):
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        elif i == int(barLen * percent):
            progress += ">"
        else:
            progress += " "
    print ("[ %s ] %.2f%%" % (progress, percent * 100))
    #sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100) + "\r")


def TH1toTAsym(hist, cutvalue=0, pltrange=(0, 0), efficiency=True):
    #only for efficiency plot now!
    x = array("f", [])
    y = array("f", [])
    exl = array("f", [])
    eyl = array("f", [])
    exh = array("f", [])
    eyh = array("f", [])
    #print pltrange
    if pltrange==(0, 0):
        xMin = hist.GetXaxis().GetXmin()
        xMax = hist.GetXaxis().GetXmax()
    else:
        xMin = pltrange[0]
        xMax = pltrange[1]
    n = 0
    for i in range(0, hist.GetNbinsX()):
        if (hist.GetBinCenter(i) < xMin):
            continue
        if (hist.GetBinCenter(i) > xMax):
            continue
        if hist.GetBinContent(i) > cutvalue:
            n += 1
            x.append(hist.GetBinCenter(i))
            y.append(hist.GetBinContent(i))
            exl.append(0)
            exh.append(0)
            eyl.append(hist.GetBinError(i))
            if efficiency: 
                eyh.append(min(hist.GetBinError(i), 1 - hist.GetBinContent(i)))
            else:
                eyh.append(hist.GetBinError(i))
    #print n, x
    gr = ROOT.TGraphAsymmErrors(n,x,y,exl,exh,eyl,eyh)
    gr.GetXaxis().SetLimits(xMin, xMax)
    gr.SetName(hist.GetName() + "_") #add _ to make sure no overlap pointer...
    gr.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    gr.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    return gr

# Gray's function
# NOTE: you __must__ store the return variable from this function and keep it in scope
# until you save the associated canvas, otherwise python will grabage collect the 
# watermakrs and they will __not__ show up on your canvas
def DrawWatermarks(xatlas=0.35, yatlas=0.87, deltay=0.6, deltax=None, watermarks=None):
    if deltax is not None:
        deltay = 0.0
	if watermarks is None:
	    assert len(deltax) == 2
  	else:
	    assert len(deltax) == len(watermarks) -1

    if watermarks is None:
        atlas = ROOT.TLatex(xatlas, yatlas, "ATLAS Internal")
        hh4b  = ROOT.TLatex(xatlas+deltax[0], yatlas-deltay, "RSG c=1.0")
        lumi  = ROOT.TLatex(xatlas+deltax[1], yatlas-deltay*2, "MC #sqrt{s} = 13 TeV")
        watermarks = [atlas, hh4b, lumi]
    else:
	deltax = [0] + deltax
	watermarks = [ROOT.TLatex(xatlas + deltax[i], yatlas - deltay*(i-1), s) for i,s in enumerate(watermarks)]	

    return DrawWords(*watermarks)

def DrawWords(*words):
    for w in words:
        w.SetTextAlign(22)
        w.SetTextSize(0.04)
        w.SetTextFont(42)
        w.SetNDC()
        w.Draw()

    return words

#needs further fix
def syst_adderror(a, b, ea = 0, eb = 0, corr=0):
    if ea != 0 and eb != 0:
        return ROOT.TMath.Sqrt((a * ea) ** 2 + (b * eb) ** 2 + a * b * ea * eb * corr)
    else:
        return ROOT.TMath.Sqrt((a) ** 2 + (b) ** 2 + 2 * (a * b * corr))
