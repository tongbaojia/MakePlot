import ROOT, rootlogon
import argparse
import array
import copy
import glob
import helpers
import os
import sys
import time
import yaml
#import plotConfig

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.Macro("../XhhCommon/post_processing/helpers.C")
ROOT.gROOT.Macro("../XhhCommon/post_processing/cross_sections.C")

timestamp = time.strftime("%Y-%m-%d-%Hh%Mm%Ss")

debug = True
stack = True

def main():

    ops = options()

    if not ops.plotter:
        fatal("Need --plotter for configuration.")
    elif ".yml" in ops.plotter:
        print "use yml"
        plotter = yaml.load(open(ops.plotter))
    else: plotter = plotConfig.getConfig(ops.plotter)
        

    if not "directory" in plotter:
        plotter["directory"] = "."
        warn("No directory given. Writing output to cwd.")

    if not "tree" in plotter:
        print "No input Tree, assuming hists"
        files   = {}
        folders = {}
        useTree = False
    else:
        useTree = True

    trees   = {}
    plots   = {}
    weights = {}
    colors  = {}
    labels  = {}
    stack   = {}
    overlay = {}
    is_data = {}
    samples = []
    prename = plotter["prename"]
    inputpath = ""
    if ops.inputdir:
        inputpath = ops.inputdir + "/"
        prename = ops.inputdir + "_" + prename

    # retrieve inputs
    print time.strftime("%Y-%m-%d-%Hh%Mm%Ss"),"Retrieving input files"
    for sample in plotter["samples"]:
        print sample
        name = sample["name"]
        samples.append(name)

        # input files
        paths = sample["path"]
        #set the full path directory here
        paths = "../Output/" + inputpath + paths

        if not glob.glob(paths):
            fatal("Found no files at %s" % (paths))

        if useTree: 
            trees[name] = ROOT.TChain(plotter["tree"])
            for path in glob.glob(paths):
                if len(path) > 100: print "adding file:",path[0:50]+"..."+path[len(path)-50:]
                else:               print "adding file:",path
                trees[name].Add(path)

        else:
            path = paths
            files[name] = ROOT.TFile(path,"READ")
            folders[name] = sample["folder"]

        # misc
        if useTree: weights[name] = " * ".join(sample["weights"]) if "weights" in sample else "1"
        else      : weights[name] = sample["weights"]
        print sample["weights"]
        colors[name]  = eval(sample["color"]) if sample["color"].startswith("ROOT") else sample["color"] 
        labels[name]  = sample["label"]
        stack[name]   = sample["stack"]
        overlay[name] = sample["overlay"]
        is_data[name] = sample["is_data"]

    # create output file
    if not os.path.isdir(plotter["directory"]):
        os.makedirs(plotter["directory"])
    output = ROOT.TFile.Open("%s/%splots.root" % (plotter["directory"], prename), "recreate")

    # make money
    for plot in plotter["plots"]:

        hists = {}
        draw = {}
        if "bins" in plot:
            draw["bins"]  = array.array("d", [float(x) for x in plot["bins"]])
        draw["title"]     = ";%s;%s" % (plot["xtitle"], plot["ytitle"])
        draw["variable"]  = plot["variable"]
        if "selection" in plotter: draw["selection"] = " && ".join(plotter["selection"])

        canv = ROOT.TCanvas(plot["name"], plot["name"], 800, 800)
        canv.Draw()
        canv.SetLogy(plot["logY"])

        stacks   = ROOT.THStack(plot["name"]+"stacks",   draw["title"])
        overlays = ROOT.THStack(plot["name"]+"overlays", draw["title"])
        do_stack = False
        do_overlay = False
        
        for sample in reversed(sorted(samples)):
            draw["name"]   = plot["name"]+"__"+sample
            draw["weight"] = weights[sample]
            if useTree:
                for option in ["weight"]:
                    draw[option] = "(%s)" % (draw[option])

            if useTree:
                if "bins" in plot:
                    hists[sample] = ROOT.TH1F(draw["name"], draw["title"], len(draw["bins"])-1, draw["bins"])
                else:
                    hists[sample] = ROOT.TH1F(draw["name"], draw["title"], plot["n_bins"], plot["bin_low"], plot["bin_high"])
                hists[sample].Sumw2()

            else:
                if folders[sample] != "": 
                    hists[sample] = files[sample].Get(folders[sample]+"/"+draw["variable"])
                else:
                    hists[sample] = files[sample].Get(draw["variable"])

                hists[sample].SetName(draw["name"])
                hists[sample].SetTitle(draw["title"])
                hists[sample].Rebin(plot["rebin"])
                if "bin_high" in plot.keys():
                    bin_low  = float(plot["bin_low"])
                    bin_high = float(plot["bin_high"])
                    hists[sample].GetXaxis().SetRangeUser(bin_low,bin_high)

            if is_data[sample]:
                hists[sample].SetMarkerStyle(20)
                hists[sample].SetMarkerSize(1)

            if useTree: trees[sample].Draw("%(variable)s >> %(name)s" % draw, "(%(selection)s) * %(weight)s" % draw, "goff")
            else      : 
                hists[sample].Sumw2()
                hists[sample].Scale(float(draw["weight"]))
                hists[sample].Draw()

            # hists[sample].Scale(1/hists[sample].Integral(0, hists[sample].GetNbinsX()))

            if stack[sample]:
                do_stack = True
                hists[sample].SetFillColor(colors[sample])
                hists[sample].SetLineColor(ROOT.kBlack)
                hists[sample].SetLineWidth(2)
                stacks.Add(copy.copy(hists[sample]), ("ep" if is_data[sample] else "hist"))
                if not useTree and "bin_high" in plot.keys():#have to set stack xaxis range for zooming because ROOT SUCKS
                    stacks.Draw()
                    stacks.GetXaxis().SetRangeUser(bin_low,bin_high)

            if overlay[sample]:
                do_overlay = True
                hists[sample].SetFillColor(0)
                hists[sample].SetLineColor(colors[sample])
                hists[sample].SetMarkerColor(colors[sample])
                hists[sample].SetLineWidth(3)
                h = copy.copy(hists[sample])
                if plotter["norm"]:
                    print h.GetName()
                    scale = h.Integral(0, h.GetXaxis().GetNbins()+1)
                    if scale != 0:
                        h.Scale(1.0/scale)
                overlays.Add(h, ("ep" if is_data[sample] else "hist"))
                
            print sample
            print "Integral:",hists[sample].Integral(0, hists[sample].GetNbinsX()+1)
            print " Entries:",hists[sample].GetEntries()

        # draw
        maximum = max([stacks.GetMaximum(), overlays.GetMaximum("nostack")])
        maximum = maximum*(100.0 if plot["logY"]     else 2.0)
        maximum = maximum*(1.2   if plotter["ratio"] else 1.0)
        minimum = max([stacks.GetMinimum(), overlays.GetMinimum("nostack")])
        minimum = minimum/(2 if plot["logY"] else 1.2)

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

        if plotter["data"]:
            pass

        if plotter["ratio"] and stacks.GetStack():

            # numerator definition is a placeholder.
            # only works if overlay[0]=data.
            if plotter["autoRatio"]:
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

            ratio = helpers.ratio(name   = canv.GetName()+"_ratio",
                                  numer  = overlays.GetHists()[0],   # AHH KILL ME
                                  denom  = stacks.GetStack().Last(),
                                  min    = ratioMin,
                                  max    = ratioMax,
                                  ytitle = "Data / pred."
                                  )
            share,top,bot = helpers.same_xaxis(name          = canv.GetName()+"_share",
                                       top_canvas    = canv,
                                       bottom_canvas = ratio,
                                       )
            canv.SetName(canv.GetName()+"_noratio")
            share.SetName(share.GetName().replace("_share", ""))
            canv = share

        elif plotter["ratio"] and not stacks.GetStack():
            warn("Want to make ratio plot but dont have stack. Skipping ratio.")

        # stack legend
        xleg, yleg = 0.6, 0.7
        legend = ROOT.TLegend(xleg, yleg, xleg+0.2, yleg+0.2)

        if do_stack:
            for hist in reversed(stacks.GetHists()):
                legend.AddEntry(hist, labels[hist.GetName().split("__")[1]], "f")

        if do_overlay:
            for hist in reversed(overlays.GetHists()):
                legend.AddEntry(hist, labels[hist.GetName().split("__")[1]], "l")
        
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetMargin(0.3)
        legend.SetTextSize(0.04)
        legend.Draw()

        # watermarks
        xatlas, yatlas = 0.38, 0.87
        atlas = ROOT.TLatex(xatlas,      yatlas, "ATLAS Internal")
        hh4b  = ROOT.TLatex(xatlas, yatlas-0.06, "X #rightarrow HH #rightarrow 4b")
        lumi  = ROOT.TLatex(xatlas, yatlas-0.12, "13 TeV")
        watermarks = [atlas, hh4b, lumi]

        # KS, chi2
        if stacks.GetStack():
            if plotter.get("ks"):
                kolg, chi2, ndf = helpers.compare(overlays.GetHists()[0],
                                                  stacks.GetStack().Last(),
                                                  ) # AH KILL ME
                yks   = 0.975
                ychi2 = 0.975
                xks   = 0.27
                xchi2 = 0.55
                
                ks = ROOT.TLatex(xks,   yks,   "KS = %5.3f" % (kolg))
                ch = ROOT.TLatex(xchi2, ychi2, "#chi^{2} / ndf = %.1f / %i" % (chi2, ndf))
                watermarks += [ks, ch]

        # draw watermarks
        for wm in watermarks:
            wm.SetTextAlign(22)
            wm.SetTextSize(0.04)
            wm.SetTextFont(42)
            wm.SetNDC()
            wm.Draw()

        canv.SaveAs(os.path.join(plotter["directory"], prename + canv.GetName()+".pdf"))

        output.cd()
        canv.Write() 

    output.Close()

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotter")
    parser.add_argument("--inputdir", default="")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def warn(message):
    print
    print "Warning in %s: %s" % (__file__, message)
    print

if __name__ == "__main__":
    main()
        
