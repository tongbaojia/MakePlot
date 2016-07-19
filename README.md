# MakePlot
*hh to 4b analysis code*

**Created by Baojia(Tony) Tong**

Currently in development!!! :+1:

This code is designed for the ATLAS boosted hh4b analysis.
With help and support from Michael Kagan, Qi Zeng, Alex Tuna and Tomo Lazovich.
Active contributors are Gray Putnam.

To make it work, Xhh4bUtiles, created by Michael Kagan, is also needed:
https://github.com/tongbaojia/Xhh4bUtils

###### Introduction to the work flow
You will need the input file from XhhBoosted first. Contact me to get input files.

- To skim input MiniNtuple to Boosted only: skimFile.py
- To split files: splitFile.py
- To generate histograms, or reweighted histograms, from TinyTree: PlotTinyeTree.py
- To generate master dictionary and predictions: get_count.py
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