inch=F_c10-cb
# inch=b77_c10-cb
#ch=b77_c10-cb$"_"$re
ch=f_c10-cb-$1-$2
homepath="/afs/cern.ch/user/g/gputnam/"
workpath="/afs/cern.ch/work/g/gputnam/public/Output/"
reweight="run$1"

echo $reweight
echo $ch

python PlotTinyTree.py --inputdir $inch --outputdir $ch --reweight $reweight #$re
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
cd ~/public/Xhh45/MakePlot
echo "Done!"
