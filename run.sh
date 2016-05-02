#for gather tables and histograms
python get_count.py --inputdir b70
python get_count.py --inputdir b77
python get_count.py --inputdir b80
python get_count.py --inputdir b85
python get_count.py --inputdir b90
python get_count.py --inputdir SB68
python get_count.py --inputdir SB88
python get_count.py --inputdir SB108
python get_count.py --inputdir SB128
python get_count.py --inputdir SB168

# for signal efficiency
# python plot_sigeff.py --inputdir b70
# python plot_sigeff.py --inputdir b77
# python plot_sigeff.py --inputdir b80
# python plot_sigeff.py --inputdir b85
# python plot_sigeff.py --inputdir b90

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