homepath="/afs/cern.ch/user/g/gputnam/"
workpath="/afs/cern.ch/work/g/gputnam/public/trkpt-ratio-Outputs/"
channels=(f_fin-cb-cleanup-asym-loose  f_fin-cb-cleanup-both-loose  f_fin-cb-cleanup-ptcut f_fin-cb-cleanup-asym-tight  f_fin-cb-cleanup-both-tight  f_fin-cb-cleanup-ref)

##iteration of reweighting!!!, takes the first argument as the reweighting configuration file under script
for ch in ${channels[@]}; do
	##publish online
	echo "Publish!"
	if [ ! -d $homepath"/www/share/hh4b/reweight/"$ch ]; then
	  mkdir $homepath"/www/share/hh4b/reweight/"$ch
	fi
	if [ ! -d $homepath"/www/share/hh4b/plot/"$ch ]; then
	  mkdir $homepath"/www/share/hh4b/plot/"$ch
	fi
	if [ ! -d $homepath"/www/share/hh4b/express/"$ch ]; then
	  mkdir $homepath"/www/share/hh4b/express/"$ch
	fi
	find $workpath$ch$"/Plot_r0/Sideband/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/reweight/"$ch \;
	find $workpath$ch$"/Plot/Sideband/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
	find $workpath$ch$"/Plot/Control/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
	find $workpath$ch$"/Plot/Sideband/" -name '*mHH_l.png' -exec cp {} $homepath"/www/share/hh4b/express/"$ch \;
	find $workpath$ch$"/Plot/Control/" -name '*mHH_l.png' -exec cp {} $homepath"/www/share/hh4b/express/"$ch \;
	##generate the text file 
	echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/express/"$ch$"/"shortdescription.txt
	echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/plot/"$ch$"/"shortdescription.txt
	echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/reweight/"$ch$"/"shortdescription.txt
	cd $homepath"/www/share/"
	python createHtmlOverview.py
	cd ~/public/Xhh2-4-11/MakePlot
	echo "Done!"
done


