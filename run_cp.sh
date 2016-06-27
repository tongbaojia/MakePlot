re=alltrk-alltrk-j0_pT-j0_pT-alltrk-j0_pT-j0_pT
inch=TEST_c10-cb
ch=b77_c10-cb$"_"$re
#ch=b77_c10-cb_alltrk
homepath="/afs/cern.ch/user/b/btong/"
workpath="/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis/Output/"
python PlotTinyTree.py --inputdir $inch --outputdir $ch --reweight "test" #$re
python get_count.py --inputdir $ch
python plot.py --inputdir $ch
python reweight.py --inputdir $ch

##publish online
if [ ! -d $homepath"/www/share/hh4b/reweight/"$ch ]; then
  mkdir $homepath"/www/share/hh4b/reweight/"$ch
fi
if [ ! -d $homepath"/www/share/hh4b/plot/"$ch ]; then
  mkdir $homepath"/www/share/hh4b/plot/"$ch
fi
find $workpath$ch$"/Plot_r0/Sideband/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/reweight/"$ch \;
find $workpath$ch$"/Plot/Sideband/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
find $workpath$ch$"/Plot/Control/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
cd $homepath"/www/share/"
python createHtmlOverview.py
echo "Done!"