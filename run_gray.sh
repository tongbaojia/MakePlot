#channels=(b70 b77 b80 b85 b90)
#channels=(jl400 jl425 jl450 jl400js275 jl425js275 jl450js275 jl400js300 jl425js300 jl450js300)
#channels=(SB48 SB53 SB58 SB63 SB68 SB73 SB78 SB88 SB98 SB108 SB128 SB168)
#channels=(b77_c00-15 b77_c00-16 b77_c10-15 b77_c10-16 ref)
#channels=(syst_b_0)

inch=F_c10-cb-16-b77
#channels=(b85-oldcut-try2)
#channels=(f_fin-cb-16-b77-debug)
channels=(f_fin-cb-16-b77-newBkg)
#channels=(b77_c00-15 b77_c00-16 b77_c10-15 b77_c10-16 ref)
#channels=(b77_c10-cb TEST_c10-cb_CR_High TEST_c10-cb_CR_Low TEST_c10-cb_CR_Small TEST_c10-cb_SB_Large TEST_c10-cb_SB_Small TEST_c10-cb_SB_High TEST_c10-cb_SB_Low)
#channels=(TEST_c10-cb)
#for gather tables and histograms

#rs=(1.4 1.6 1.8)
#ext=(3.0 5.0 7.0 9.0)

for ch in ${channels[@]}; do
	echo $ch
	python PlotTinyTree_gray.py --inputdir $inch --outputdir $ch
	python get_count_gray.py --inputdir $ch --full
	##python test.py --inputdir $ch --full True
	python plot.py --inputdir $ch
	python reweight.py --inputdir $ch
	python plot_prediction.py --inputdir $ch
	#python dump_hists.py --inputdir $ch
        #python plot_random.py --inputdir $ch
done
