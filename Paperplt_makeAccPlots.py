import optparse
parser = optparse.OptionParser()
parser.add_option('--signalDir',                dest="signalDir",             default="", help="")
parser.add_option('-o', '--out',                dest="output",                default="/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Plot/", help="")
parser.add_option('-c', '--couping',            dest="coupling",              default="boosted10", help="")
o, a = parser.parse_args()

import os
import ROOT, rootlogon
ROOT.gROOT.SetBatch(1)
from ROOT import gStyle    
try:
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    SetAtlasStyle()
except:
    print "Passing on AtlasStyle.C"
    pass



if not os.path.isdir(o.output):
    os.mkdir(o.output)



doResolved = True

if o.coupling == "1.0":
    #massPts = ["300","400","500" ,"600" ,"700" ,"800" ,"900" ,"1000","1100","1200","1300","1500"]    
    massPts = ["400","500" ,"600" ,"700" ,"800" ,"900" ,"1000","1100","1200","1300","1400","1500"]    
    dirMap = {
          "300" :"RSG_c10_M300",  
          "400" :"RSG_c10_M400",  
          "500" :"RSG_c10_M500",  
          "600" :"RSG_c10_M600",  
          "700" :"RSG_c10_M700",  
          "800" :"RSG_c10_M800",  
          "900" :"RSG_c10_M900",  
          "1000":"RSG_c10_M1000",  
          "1100":"RSG_c10_M1100",  
          "1200":"RSG_c10_M1200",
          "1300":"RSG_c10_M1300",
          "1400":"RSG_c10_M1400",
          "1500":"RSG_c10_M1500",
          }
elif o.coupling == "2.0":

    #massPts = ["300","400","500" ,"600" ,"700" ,"800" ,"900" ,"1000","1100","1200","1300","1500"]    
    massPts = ["400","500" ,"600" ,"700" ,"800" ,"900" ,"1000","1100","1200","1300","1400","1500"]    
    dirMap = {"300" :"RSG_c20_M300", 
              "400" :"RSG_c20_M400", 
              "500" :"RSG_c20_M500", 
              "600" :"RSG_c20_M600", 
              "700" :"RSG_c20_M700", 
              "800" :"RSG_c20_M800", 
              "900" :"RSG_c20_M900", 
              "1000":"RSG_c20_M1000",
              "1100":"RSG_c20_M1100",
              "1200":"RSG_c20_M1200",
              "1300":"RSG_c20_M1300",
              "1400":"RSG_c20_M1400",
              "1500":"RSG_c20_M1500",
              }
elif o.coupling in ["boosted10","boosted2HDM"]:
    doResolved = False
    import json
    json_data=open("boosted_AccepEffNumbers.json").read()
    data = json.loads(json_data)
    massPts = ["500" ,"600","700", "800" ,"900" ,"1000","1100","1200","1300","1400","1500","1600","1800","2000","2250","2500","2750","3000"]    
    print data.keys()
    print data["RSG_c10"].keys()
    #print data["RSG_c10"]['SR3b']
    if o.coupling == "boosted10":
        boostedData = data["RSG_c10"]
    else:
        boostedData = data["2HDM"]

else:
    #massPts = ["300","400","500" ,"600" ,"700" ,"800" ,"900" ,"1000","1100","1200","1300","1500"]    
    massPts = ["500" ,"600" ,"700" ,"800" ,"900" ,"1000","1100","1200","1300","1400","1500"]    
    dirMap = {"300" :"Hhh_M300", 
              "400" :"Hhh_M400", 
              "500" :"Hhh_M500", 
              "600" :"Hhh_M600", 
              "700" :"Hhh_M700", 
              "800" :"Hhh_M800", 
              "900" :"Hhh_M900", 
              "1000":"Hhh_M1000",
              "1100":"Hhh_M1100",
              "1200":"Hhh_M1200",
              "1300":"Hhh_M1300",
              "1400":"Hhh_M1400",
              "1500":"Hhh_M1500",
              }

def getMassPt(inputList, m):
    #print "gettimg ",m
    for i in inputList:
        #print i[0],m,float(i[0]) == float(m)
        if float(i[0]) == float(m): return float(i[1])
    return 1.0

def savePlot(can,name):
    can.SaveAs(name+".pdf")
    can.SaveAs(name+".eps")
    can.SaveAs(name+".png")

if doResolved:
    signalFiles = {}
    for d in dirMap: 
        signalFiles[d] = ROOT.TFile(o.signalDir+"/"+dirMap[d]+"/hist-tree.root", "READ")

total = {}

class cutValue:
    
    def __init__(self, name, legName="", color=ROOT.kBlack, style=0):
        self.name = name
        self.massYeilds = {}
        self.color = color
        self.style = style
        self.legName = legName

    def makeGraph(self, massPts, norm, doPrint=False):
        self.graph = ROOT.TGraph(len(massPts))
        self.graph.SetLineWidth(2)
        self.graph.SetLineColor  (self.color)
        self.graph.SetMarkerColor(self.color)
        
        if self.style:
            self.graph.SetMarkerStyle(self.style)
        
        pointCount = 0
        for m in massPts:
            
            if not norm.massYeilds[m]: continue
            eff = float(self.massYeilds[m])/norm.massYeilds[m]
            if doPrint: print m, eff
                
            self.graph.SetPoint(pointCount, float(m), eff)
            pointCount += 1


    def makeGraphResolved(self, massPts):
        self.graph = ROOT.TGraph(11)
        self.graph.SetLineWidth(2)
        self.graph.SetLineColor  (self.color)
        self.graph.SetMarkerColor(self.color)
        
        if self.style:
            self.graph.SetMarkerStyle(self.style)
        
        pointCount = 0
        for m in massPts:
            if int(m) < 1600:
                eff = float(self.massYeilds[m])
                self.graph.SetPoint(pointCount, float(m), eff)
                pointCount += 1

    def makeGraphBoosted(self, massPts):
        self.graph = ROOT.TGraph(15)
        self.graph.SetLineWidth(2)
        self.graph.SetLineColor  (self.color)
        self.graph.SetMarkerColor(self.color)
        
        if self.style:
            self.graph.SetMarkerStyle(self.style)
        
        pointCount = 0
        for m in massPts:
            if int(m) > 700:
                eff = float(self.massYeilds[m])
                self.graph.SetPoint(pointCount, float(m), eff)
                pointCount += 1
                                
    




cutList = []
if doResolved:
    totals = cutValue("AllEvents")
    # cutList.append( cutValue("NJetsAbove3"     ) )
    cutList.append( cutValue("NBJetsEqual4"    ,  "4 b-tagged jets",      ROOT.kBlue,    25) )
    cutList.append( cutValue("PassBJetSkim"    ,  "2 dijets",      ROOT.kBlue,    22) )
    # cutList.append( cutValue("PassTrig"        ,  "Trigger",       ROOT.kBlack,    22) )
    cutList.append( cutValue("PassM4j"         ,  "Mass Dependent Cuts",           ROOT.kBlue-5,  23) )
    cutList.append( cutValue("PassTTVeto"      ,  "t#bar{t} Veto",        ROOT.kBlue-5,  24) )
    cutList.append( cutValue("PassTTVetoSignal",  "Signal Region", ROOT.kRed,     28) )
else:
    #cutList.append( cutValue("2JJ"    ,  "2 large-R Jets",      ROOT.kBlue,    25) )
    #cutList.append( cutValue("dEtaCut"         ,  "#Delta #eta", ROOT.kBlue, 22) )
    #cutList.append( cutValue("4TrackJet"      ,  "4 Track-jet",        ROOT.kBlue-5,  23) )
    #cutList.append( cutValue("Xhh"           , "Xhh", ROOT.kBlue-5, 24))
    cutList.append( cutValue("SRres", "Resolved 4-tag", ROOT.kPink+8,     25) ) 
    cutList.append( cutValue("SR3b",  "Boosted 3-tag", ROOT.kBlue+1,     28) )    
    cutList.append( cutValue("SR4b",  "Boosted 4-tag", ROOT.kGreen+4,     34) )    



if doResolved:
    for m in massPts:
        cutFlowHists = signalFiles[m].Get("CutFlow4bWeighted")
    
        totals.massYeilds[m] = cutFlowHists.GetBinContent(cutFlowHists.GetXaxis().FindBin(totals.name))             
        
        for c in cutList:
            #print m, cutFlowHists.GetBinContent(cutFlowHists.GetXaxis().FindBin(c.name))             
                
            c.massYeilds[m] = cutFlowHists.GetBinContent(cutFlowHists.GetXaxis().FindBin(c.name))             

else:
    for m in massPts:
        for c in cutList:
            #print boostedData.keys()
            #print boostedData[c.name]
            #print getMassPt(boostedData[c.name], m)
            #print m, c.name, getMassPt(boostedData[c.name],m)
            c.massYeilds[m] = getMassPt(boostedData[c.name], m)


can = ROOT.TCanvas("cutEFfs","cutEFfs")
can.cd()
didFirst = False

xpos = 0.59
xwidth = 0.34
ypos = 0.73
ywidth = 0.2

leg = ROOT.TLegend(xpos,ypos,xpos+xwidth,ypos+ywidth)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.04)

for c in cutList:
    if doResolved:
        doPrint = (c.name == "PassTTVetoSignal")
        c.makeGraph(massPts, totals, doPrint)
    else:
        if c.name == "SRres":
            c.makeGraphResolved(massPts)
        else:
            c.makeGraphBoosted(massPts)

    leg.AddEntry(c.graph, c.legName, "PL")

    if not didFirst:
        #c.graph.GetYaxis().SetRangeUser(0,0.2)
        if doResolved:
            if o.coupling in ["1.0","2.0"]:
                c.graph.GetYaxis().SetRangeUser(0,0.19)
                c.graph.GetXaxis().SetTitle("m_{G*}_{KK} [GeV]")
                c.graph.GetXaxis().SetTitleSize(0.07)
                c.graph.GetXaxis().SetTitleOffset(0.9)
            else:
                c.graph.GetYaxis().SetRangeUser(0,0.17)
                c.graph.GetXaxis().SetTitle("m_{H} [GeV]")
                c.graph.GetXaxis().SetTitleSize(0.07)
                c.graph.GetXaxis().SetTitleOffset(0.9)
        else:
            c.graph.GetYaxis().SetRangeUser(0, 0.19)
            if o.coupling in ["boosted10"]:
                c.graph.GetXaxis().SetTitle("m_{G*_{KK}} [GeV]")
                #c.graph.GetXaxis().SetTitleSize(0.07)
                #c.graph.GetXaxis().SetTitleOffset(0.9)
            else:
                c.graph.GetXaxis().SetTitle("m_{H} [GeV]")
                #c.graph.GetXaxis().SetTitleSize(0.07)
                #c.graph.GetXaxis().SetTitleOffset(0.9)
        c.graph.GetYaxis().SetTitle("Acceptance x Efficiency")
        c.graph.SetTitle("")

        didFirst = True
        c.graph.GetXaxis().SetLimits(300, 3200)
        c.graph.Draw("APL")
        leg.Draw("same")
        c.graph.Draw("PL")
    else:
        c.graph.GetXaxis().SetLimits(300, 3200)
        c.graph.Draw("PL")


watermarks = []

xatlas, yatlas = 0.2, 0.88
atlas = ROOT.TLatex(xatlas,   yatlas,      "ATLAS Simulation Internal")
watermarks += [atlas]
#internal = ROOT.TLatex(xatlas+0.17,   yatlas,      "Internal")
#internal = ROOT.TLatex(xatlas+0.24,   yatlas,      "Internal")
#watermarks += [internal]
if o.coupling in ["1.0","2.0"]:
    cTag  = ROOT.TLatex(xatlas+0.01,   yatlas-0.06, "Bulk RS, k/#bar{M}_{Pl} = "+str(int(float(o.coupling))))
    resolved  = ROOT.TLatex(xatlas+0.04,   yatlas-0.12, "Resolved, #sqrt{s} = 13 TeV")
    watermarks += [resolved]
    watermarks += [cTag]

elif o.coupling == "boosted10":
    cTag  = ROOT.TLatex(xatlas,   yatlas-0.06, "Bulk RS, k/#bar{M}_{Pl} = 1.0")
    watermarks += [cTag]
    boosted  = ROOT.TLatex(xatlas,   yatlas-0.12, "Signal Region, #sqrt{s} = 13 TeV")
    watermarks += [boosted]
else:
    cTag  = ROOT.TLatex(xatlas+0.08,   yatlas-0.06, "H#rightarrow hh, with fixed #Gamma_{H} = 1 GeV")
    watermarks += [cTag]
    if not o.coupling.find("boosted") == -1:
        boosted  = ROOT.TLatex(xatlas+0.04,   yatlas-0.11, "Boosted, #sqrt{s} = 13 TeV")
        watermarks += [boosted]
    else:
        resolved  = ROOT.TLatex(xatlas+0.04,   yatlas-0.11, "Resolved, #sqrt{s} = 13 TeV")
        watermarks += [resolved]
#sqrtS  = ROOT.TLatex(xatlas-0.01,   yatlas-0.12, "#sqrt{s} = 13 TeV")
#watermarks += [sqrtS]

wmNum = 0

for wm in watermarks:
    #wm.SetTextAlign(22)
    if wmNum == 0:
        wm.SetTextSize(0.04)
        wm.SetTextFont(72)
    else:
        wm.SetTextSize(0.04)
        wm.SetTextFont(42)
    wmNum+=1
    wm.SetNDC()
    wm.Draw()


can.Update()
if o.coupling == "1.0":
    savePlot(can, o.output+"/SignalAcc_c10")
elif o.coupling == "2.0":
    savePlot(can, o.output+"/SignalAcc_c20")
elif o.coupling == "boosted10": 
    savePlot(can, o.output+"/SignalAcc_combinedc10")
elif o.coupling == "boosted2HDM": 
    savePlot(can, o.output+"/SignalAcc_boosted2HDM")
else:
    savePlot(can, o.output+"/SignalAcc_2HDM")


if   o.coupling == "1.0":
    outFile = ROOT.TFile(o.output+"/SignalAcc_c10.root","RECREATE")
elif o.coupling == "2.0":
    outFile = ROOT.TFile(o.output+"/SignalAcc_c20.root","RECREATE")
elif o.coupling == "boosted10":
    outFile = ROOT.TFile(o.output+"/SignalAcc_combinedc10.root","RECREATE")
else:
    outFile = ROOT.TFile(o.output+"/SignalAcc_2HDM.root","RECREATE")

can.Write()
outFile.Close()
