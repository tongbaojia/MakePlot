homepath="/afs/cern.ch/user/b/btong/"
workpath="/afs/cern.ch/work/b/btong/bbbb/MoriondAnalysis/Output/"

# #### Testing
re=bkg
inch=TEST
iter=-1
##first reweight
ch=Moriond
echo $workpath$ch$"/Plot_r"$(($iter + 1))$"/Sideband/"
#python reweight.py --inputdir $ch --iter $(($iter + 1))
##this is for the first round
#echo $ch, "is the channel and iteration!"
#python PlotTinyTree.py --inputdir $inch --outputdir $ch --reweight $re --iter $iter #$re
##this is for the testing round!
#ch=Moriond$"_"$re"_"$iter
#echo $ch, "is the channel and iteration!"
#python PlotTinyTree.py --inputdir $inch --outputdir $ch --reweight $re --iter $iter #$re
#python get_count.py --inputdir $ch --full
python plot.py --inputdir $ch 
python reweight.py --inputdir $ch --iter $(($iter + 1)) --var j0pT
python reweight.py --inputdir $ch --iter $(($iter + 1)) --var bkg
python reweight.py --inputdir $ch --iter $(($iter + 1)) --var bkgsb
#publish online
echo "Publish!"
#rm -rf $homepath"/www/share/hh4b/reweight/"$ch
if [ ! -d $homepath"/www/share/hh4b/reweight/"$ch ]; then
  mkdir $homepath"/www/share/hh4b/reweight/"$ch
fi
if [ ! -d $homepath"/www/share/hh4b/plot/"$ch ]; then
  mkdir $homepath"/www/share/hh4b/plot/"$ch
fi
if [ ! -d $homepath"/www/share/hh4b/express/"$ch ]; then
  mkdir $homepath"/www/share/hh4b/express/"$ch
fi
for plt in leadHCand_Mass sublHCand_Mass mHH_l_1 trk0_Pt trk1_Pt leadHCand_Pt_m_1 sublHCand_Pt_m_1 trk_dr; do
	find $workpath$ch$"/Plot_r"$(($iter + 1))$"/Incl/" -name "*"$plt".png" -exec cp {} $homepath"/www/share/hh4b/reweight/"$ch \;
	find $workpath$ch$"/Plot_r"$(($iter + 1))$"/Sideband/" -name "*"$plt".png" -exec cp {} $homepath"/www/share/hh4b/reweight/"$ch \;
	find $workpath$ch$"/Plot/Sideband/" -name "*"$plt".png" -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
	find $workpath$ch$"/Plot/Control/" -name "*"$plt".png" -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
done
find $workpath$ch$"/Plot/Sideband/" -name '*mHH_l_1.png' -exec cp {} $homepath"/www/share/hh4b/express/"$ch \;
find $workpath$ch$"/Plot/Control/" -name '*mHH_l_1.png' -exec cp {} $homepath"/www/share/hh4b/express/"$ch \;
##generate the text file 
echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/express/"$ch$"/"shortdescription.txt
echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/plot/"$ch$"/"shortdescription.txt
echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/reweight/"$ch$"/"shortdescription.txt
cd $homepath"/www/share/"
python createHtmlOverview.py
cd -
echo "Done!"


#iteration of reweighting!!!, takes the first argument as the reweighting configuration file under script
# for i in {0..19}
# do
# 	re=$1	
# 	inch=TEST
# 	iter=$i
# 	ch=DS1_cb$"_"$re"_"$iter
# 	#ch=f_c10-cb
# 	echo $ch, "is the channel and iteration!"
# 	python PlotTinyTree.py --inputdir $inch --outputdir $ch --reweight $re --iter $iter #$re
# 	python get_count.py --inputdir $ch --full
# 	python plot.py --inputdir $ch
# 	python reweight.py --inputdir $ch

# 	##publish online
# 	echo "Publish!"
# 	if [ ! -d $homepath"/www/share/hh4b/reweight/"$ch ]; then
# 	  mkdir $homepath"/www/share/hh4b/reweight/"$ch
# 	fi
# 	if [ ! -d $homepath"/www/share/hh4b/plot/"$ch ]; then
# 	  mkdir $homepath"/www/share/hh4b/plot/"$ch
# 	fi
# 	if [ ! -d $homepath"/www/share/hh4b/express/"$ch ]; then
# 	  mkdir $homepath"/www/share/hh4b/express/"$ch
# 	fi
# 	for plt in leadHCand_Mass_s mHH_l trk0_Pt trk1_Pt leadHCand_Pt_m sublHCand_Pt; do
# 		find $workpath$ch$"/Plot_r0/Sideband/" -name "*"$plt".png" -exec cp {} $homepath"/www/share/hh4b/reweight/"$ch \;
# 		find $workpath$ch$"/Plot/Sideband/" -name "*"$plt".png" -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
# 		find $workpath$ch$"/Plot/Control/" -name "*"$plt".png" -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
# 	done
# 	find $workpath$ch$"/Plot/Sideband/" -name '*mHH_l.png' -exec cp {} $homepath"/www/share/hh4b/express/"$ch \;
# 	find $workpath$ch$"/Plot/Control/" -name '*mHH_l.png' -exec cp {} $homepath"/www/share/hh4b/express/"$ch \;
# 	##generate the text file 
# 	echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/express/"$ch$"/"shortdescription.txt
# 	echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/plot/"$ch$"/"shortdescription.txt
# 	echo " reweight: "$re$" iter: "$iter > $homepath"/www/share/hh4b/reweight/"$ch$"/"shortdescription.txt
# 	cd $homepath"/www/share/"
# 	python createHtmlOverview.py
# 	cd -
# 	echo "Done!"
# done


