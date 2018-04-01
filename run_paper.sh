inputdir="Moriond_bkg_9"
# python Paperplt_all.py   --inputdir $inputdir ### this is the 2D plot
# python Paperplt_table.py --inputdir $inputdir
python Paperplt_acc.py   --inputdir $inputdir ### this is the efficiency plot
# python Paperplt_other.py --inputdir $inputdir 
#python Paperplt_mHH.py   --inputdir $inputdir ### this is the Dijet SR/CR region plot
# python Paperplt_other.py --inputdir "Moriond" ### this does the trackjet pT plots
# python Paperplt_other.py --inputdir "Moriond_TT" ### this does the TT MJJ plots
# python Paperplt_other.py --inputdir "Moriond_ZZ" ### this does the ZZ MJJ plots
echo "Done!!!"