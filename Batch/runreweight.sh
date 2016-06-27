#!/bin/bash 
## SUBMIT WITH: bsub -q 1nh -J "myrun[1-10]" < runBatchJob.sh
## ----------------------------------------------------------

#################################################
## DEFINE INPUT, TESTAREA AND OUTPUT AREA ###
#Runnumber=$1
filenamelist=/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis/MakePlot/Batch/reweight_1.txt ##267638
echo "the input file is " $filenamelist
yourtestarea=/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis ## replace with here if you don't have a testarea
#eosoutputarea=/eos/atlas/user/b/btong/TESTAREA/muonSW/output  ## your output forlder MUST exist
youroutputarea=/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis/Output ##your output area
#athenaVer="20.1.X-VAL,rel_1, gcc48 --testarea=$yourtestarea"  ## the release you want to setup
#################################################
tmpworkdir=$youroutputarea/run_${Runnumber}_$inputstream_$LSB_JOBID.$LSB_JOBINDEX
#mkdir $tmpworkdir
dopythonrun="true"
# for a local test, just do: "./runBatchJob.sh --test <INDEX>"
if [ $1 == "--test" ]; then
    LSB_JOBINDEX=$2
    LSB_JOBID=$2
	#tmpworkdir=$PWD/run_$Runnumber.$LSB_JOBINDEX #stop doing this for now
	#mkdir $tmpworkdir
fi
#cd $tmpworkdir

#Setup ATHENA
export AtlasSetup=/afs/cern.ch/atlas/software/dist/AtlasSetup
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

#go to workdirectory
cd $yourtestarea

#setup working environment
if [ $dopythonrun == "true" ];then
	#Setup rc
	lsetup rcSetup -u
	lsetup rcsetup
	lsetup 'sft releases/pyanalysis/1.5_python2.7-d641e' #correct python version
	#Setup eos
fi

# set input file to be processed
INOPTION=`sed -n "$LSB_JOBINDEX"p $filenamelist`
echo $INOPTION
#OUTFILE=Tony_test.$LSB_JOBINDEX.root
# # # # # # # # # # # # # #

re=$(grep -o -P '(?<=re:).*(?=:re)' <<< $INOPTION)
echo "doing reweighting on: " $re

if [ $dopythonrun == "true" ]; then
	cd MakePlot
	inch="TEST_c10-cb"
	ch="b77_c10-cb"$"_"$re
	homepath="/afs/cern.ch/user/b/btong/"
	workpath="/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis/Output/"
	python PlotTinyTree.py --inputdir $inch --outputdir $ch --reweight $re
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
	#find $workpath$ch$"/Plot/Sideband/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
	#find $workpath$ch$"/Plot/Control/" -name '*.png' -exec cp {} $homepath"/www/share/hh4b/plot/"$ch \;
	cd $homepath"/www/share/"
	python createHtmlOverview.py
	echo "Done!"
fi
echo "DONE!!!"



