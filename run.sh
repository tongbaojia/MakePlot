#channels=(b70 b77 b80 b85 b90)
#channels=(jl400 jl425 jl450 jl400js275 jl425js275 jl450js275 jl400js300 jl425js300 jl450js300)
#channels=(SB48 SB53 SB58 SB63 SB68 SB73 SB78 SB88 SB98 SB108 SB128 SB168)

channels=(b77_c00-15-allcut b77_c00-15-allcut-loose b77_c00-15-btagcut)
#channels=(b77_c00-15 b77_c00-16 b77_c10-15 b77_c10-16 ref)
#channels=(b77_c10-cb TEST_c10-cb_CR_High TEST_c10-cb_CR_Low TEST_c10-cb_CR_Small TEST_c10-cb_SB_Large TEST_c10-cb_SB_Small TEST_c10-cb_SB_High TEST_c10-cb_SB_Low)
#channels=(TEST_c10-cb)
#for gather tables and histograms

for ch in ${channels[@]}; do
	##python get_count.py --inputdir $ch --full False
	python get_count.py --inputdir $ch --full True
	##python test.py --inputdir $ch --full True
	python plot.py --inputdir $ch
	#python reweight.py --inputdir $ch
channels=(CR_High CR_Low CR_Small SB_Large SB_Small SB_High SB_Low)

