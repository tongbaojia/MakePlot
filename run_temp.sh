###
python PlotTinyTree.py --inputdir ICHEP --outputdir test_ichep
python get_count.py --inputdir test_ichep
python dump_hists.py --inputdir test_ichep

# python PlotTinyTree.py --inputdir ICHEP --outputdir test_3b_b60 --MV2 0.8529
# python get_count.py --inputdir test_3b_b60
# python dump_hists.py --inputdir test_3b_b60

# python PlotTinyTree.py --inputdir ICHEP --outputdir test_3b_b70 --MV2 0.6455
# python get_count.py --inputdir test_3b_b70
# python dump_hists.py --inputdir test_3b_b70