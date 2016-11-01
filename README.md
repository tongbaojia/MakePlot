# MakePlot
*hh to 4b analysis code*

**Created by Baojia(Tony) Tong**

Currently in development!!! :+1:

This code is designed for the ATLAS boosted hh4b analysis.
With help and support from Michael Kagan, Qi Zeng, Alex Tuna and Tomo Lazovich.
Active contributors are Gray Putnam.
To make it work, Xhh4bUtiles, created by Michael Kagan, is also needed.


###### First setup
You should do:(in the direcotry where you have XhhCommon and Xhh4bBoosted) <br />
```
git clone https://github.com/tongbaojia/MakePlot.git
cd MakePlot
git clone https://github.com/tongbaojia/Xhh4bUtils
```

###### Setup each time
Before you run code in MakePlot, do outside the MakePlot folder: <br />
(to setup the up to date root and python version on lxplus) <br />
```
rcSetup
lsetup 'sft releases/pyanalysis/1.5_python2.7-d641e'
```


###### Introduction to the work flow
You will need the input file from XhhBoosted first. Contact me to get input files.

- To skim input MiniNtuple to boosted only(having at least 2 large R jets in the events): skimFile.py
- To split files from ProcessXhhMiniNtuples to smaller copies: splitFile.py
- To generate histograms, or reweighted histograms, from TinyTree: PlotTinyeTree.py
- To generate master dictionary, do fit on the leading large R jet mass and predictions: get_count.py
- To plot all the distributions: plot.py
- To genearte reweighting values: reweight.py
- To plot trigger efficiency studies: plot_trigeff.py
- To plot signal sample efficiencies: plot_sigeff.py
- To generate cutflow table: plot_cutflow.py
- To generate signal significance prediction: python plot_prediction.py
- To generate inputfiles for limit setting and smoothing: dump_hists.py
- To generate other distributions: python plot_random.py
- To generate smoothed signal region predictions: python plot_smooth.py
- To generate sysmtatics table: python syst_vari.py
- For an example, see run.sh