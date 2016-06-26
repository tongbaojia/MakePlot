#!/bin/bash 
## SUBMIT WITH: bsub -q 1nh -J "myrun[1-10]" < runBatchJob.sh
## ----------------------------------------------------------

#################################################
## DEFINE INPUT, TESTAREA AND OUTPUT AREA ###
#Runnumber=$1
filenamelist=/afs/cern.ch/work/b/btong/bbbb/CHEPAnalysis/MakePlot/Batch/input.txt ##267638
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

ch=$(grep -o -P '(?<=ch:).*(?=:ch)' <<< $INOPTION)
echo "plotting channel: " $ch
syst=$(grep -o -P '(?<=syst:).*(?=:syst)' <<< $INOPTION)
echo "plotting syst: " $syst
inputdir=$ch$"_"$syst

if [ $dopythonrun == "true" ]; then
	cd MakePlot
	python PlotTinyTree.py --inputdir $ch --outputdir $ch --dosyst $syst
	python get_count.py --inputdir $inputdir --full True
	python plot.py --inputdir $inputdir
fi
echo "DONE!!!"



