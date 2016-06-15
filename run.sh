#channels=(b70 b77 b80 b85 b90 SB58 SB68 SB78 SB88 SB98 SB108 SB128 SB168 SB999)
#channels=(jl400 jl425 jl450 jl400js275 jl425js275 jl450js275 jl400js300 jl425js300 jl450js300)
channels=(SB48 SB53 SB58 SB63 SB68 SB73 SB78 SB88 SB98 SB108 SB128 SB168)
#channels=(ref)
#channels=(reweight_3)
#for gather tables and histograms

for ch in ${channels[@]}; do
	python get_count.py --inputdir $ch
	#python test.py --inputdir $ch --full True
	#python plot.py --inputdir $ch
	#python reweight.py --inputdir $ch
	#python plot_trigeff.py --inputdir $ch
	#python plot_sigeff.py --inputdir $ch
	#python plot_prediction.py --inputdir $ch
	#python dump_hists.py --inputdir $ch
	#python plot_random.py --inputdir $ch
	#python plot_smooth.py --inputdir $ch
done


#specify the paths to gather!
inputpath="/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Output/"
plotpath="/Plot/SigEff/"
plotname="_relsig_0_3100_1.pdf"
tablepath="/Plot/Tables/"
tablename="normfit.tex"
outputpath="/afs/cern.ch/work/b/btong/bbbb/NewAnalysis/Plot/"
#pick scipt
for ch in ${channels[@]}; do
	#cp $inputpath$ch$plotpath$ch$plotname $outputpath$"/."
	#cp $inputpath$ch$tablepath$tablename $outputpath$"/"$ch$"_"$tablename
	echo $ch
	#more $inputpath$ch$tablepath$tablename
	more $inputpath$ch$"/sum_"$ch$".tex"
	cp $inputpath$ch$"/sum_"$ch$".tex" $outputpath$"/sum_"$ch$".tex"
done

# for distributions, old
# python plot_boosted.py --plotter=boosted_data_qcd_4b.yml --inputdir b70 > log_4b_70.txt
# python plot_boosted.py --plotter=boosted_data_qcd_4b.yml --inputdir b77 > log_4b_77.txt
# python plot_boosted.py --plotter=boosted_data_qcd_4b.yml --inputdir b80 > log_4b_80.txt
# python plot_boosted.py --plotter=boosted_data_qcd_4b.yml --inputdir b85 > log_4b_85.txt
# python plot_boosted.py --plotter=boosted_data_qcd_4b.yml --inputdir b90 > log_4b_90.txt
# python plot_boosted.py --plotter=boosted_data_qcd_3b.yml --inputdir b70 > log_3b_70.txt
# python plot_boosted.py --plotter=boosted_data_qcd_3b.yml --inputdir b77 > log_3b_77.txt
# python plot_boosted.py --plotter=boosted_data_qcd_3b.yml --inputdir b80 > log_3b_80.txt
# python plot_boosted.py --plotter=boosted_data_qcd_3b.yml --inputdir b85 > log_3b_85.txt
# python plot_boosted.py --plotter=boosted_data_qcd_3b.yml --inputdir b90 > log_3b_90.txt