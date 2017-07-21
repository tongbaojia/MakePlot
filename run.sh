#channels=(b70 b77 b80 b85 b90)
#channels=(jl400 jl425 jl450 jl400js275 jl425js275 jl450js275 jl400js300 jl425js300 jl450js300)
channels=(56 60)
#channels=(b77_c00-15 b77_c00-16 b77_c10-15 b77_c10-16 ref)
#channels=(syst_b_0)
channels=(CR_High CR_Low CR_Small SB_High SB_Low SB_Large SB_Small)
#channels=(ZZ TT)
#channels=(b77)
#channels=(bkgdr bkgeta bkgsb bkgtrk j0pT-alltrk-fin j0pT-leadtrk-fin j0pT-leadtrk-trkdr-fin j0pT-subltrk-fin)
#for gather tables and histograms

for ch in ${channels[@]}; do
	ch=$"Moriond_"$ch
	# out=$"SB"$ch
	# cd Output
	# if [ ! -d $ch$"/data_est" ]; then
	# 	mkdir $ch$"/data_est"
	# fi
	# cd $ch$"/data_est"
	# rm hist-MiniNTuple.root
	# ln -s ../../b77/data_est/hist-MiniNTuple.root hist-MiniNTuple.root
	# cd ../../..
	#python Run_reweight.py --var $ch
	#python PlotTinyTree.py --outputdir $out --SB $ch
	#python get_count.py --inputdir $out
	#python test.py --inputdir $ch --full True
	#python get_count.py --inputdir $ch --full
	#python plot.py --inputdir $ch
	#python reweight.py --inputdir $ch
	#python plot_trigeff.py --inputdir $ch
	#python plot_sigeff.py --inputdir $ch
	#python plot_cutflow.py --inputdir $ch
	#python plot_prediction.py --inputdir $ch
	#python dump_hists.py --inputdir $ch
	#python plot_random.py --inputdir $ch
	#python plot_smooth.py --inputdir $ch
done

##finish syst part
#python dump_syst.py --hist pole ##generate limit input file
#python dump_syst.py 
python plot_sigsyst.py --hist pole
python plot_sigsyst.py

#specify the paths to gather!
# inputpath="/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis/Output/"
# plotpath="/Plot/SigEff/"
# plotname="_relsig_0_3100_1.pdf"
# tablepath="/Plot/Tables/"
# tablename="normfit.tex"
# outputpath="/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis/Plot/"

#pick scipt
# for ch in ${channels[@]}; do
# 	#cp $inputpath$ch$plotpath$ch$plotname $outputpath$"/."
# 	#cp $inputpath$ch$tablepath$tablename $outputpath$"/"$ch$"_"$tablename
# 	echo $ch
# 	#more $inputpath$ch$tablepath$tablename
# 	more $inputpath$ch$"/sum_"$ch$".tex"
# 	#cp $inputpath$ch$"/sum_"$ch$".tex" $outputpath$"/sum_"$ch$".tex"
# done
#pick syst
# for ch in ${channels[@]}; do
# 	for syst in ${systs[@]}; do
# 		#cp $inputpath$ch$plotpath$ch$plotname $outputpath$"/."
# 		#cp $inputpath$ch$tablepath$tablename $outputpath$"/"$ch$"_"$tablename
# 		echo $ch"_"$syst
# 		#more $inputpath$ch$tablepath$tablename
# 		more $inputpath$ch"_"$syst$"/Plot/Tables/ThreeTag_yield.tex"
# 		#cp $inputpath$ch$"/sum_"$ch$".tex" $outputpath$"/sum_"$ch$".tex"
# 	done
# done


