inputdir="Moriond_bkg_9"
python Paperplt_all.py --inputdir $inputdir
##python Paperplt_table.py
python Paperplt_acc.py --inputdir $inputdir
python Paperplt_other.py --inputdir $inputdir
python Paperplt_mHH.py --inputdir $inputdir
echo "Done!!!"