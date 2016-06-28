# channels=(b77_c00-15-allcut b77_c00-15-btagcut b77_c00-15-halfcut)
# ch_ind=(0 2 4)
channels=(b77_c00-15-nocut)
ch_ind=(0)
inputdir=TONY-DATA

for ((i=0;i<${#channels[@]};++i)); do
	ch=${channels[$i]}
	i=${ch_ind[$i]}
        #python PlotTinyTree.py --inputdir $inputdir --outputdir $ch --cut_ind $i
	##python get_count.py --inputdir $ch --full False
	#python get_count.py --inputdir $ch --full True
	##python test.py --inputdir $ch --full True
	python plot.py --inputdir $ch
	# python reweight.py --inputdir $ch
	# python plot_trigeff.py --inputdir $ch
	# python plot_sigeff.py --inputdir $ch
	# python plot_cutflow.py --inputdir $ch
	#python plot_prediction.py --inputdir $ch
	# python dump_hists.py --inputdir $ch
	# python plot_random.py --inputdir $ch
	# python plot_smooth.py --inputdir $ch
done
