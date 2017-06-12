#!/bin/bash 
## SUBMIT WITH: bsub -q 1nh -J "myrun[1-10]" < runBatchJob.sh
## ----------------------------------------------------------
#################################################
## DEFINE INPUT, TESTAREA AND OUTPUT AREA ###
echo "the input file is " $filenamelist
yourtestarea=/afs/cern.ch/work/b/btong/bbbb/MoriondAnalysis ## replace with here if you don't have a testarea
filenamelist=$yourtestarea$"/MakePlot/Batch/input.txt" ##267638
youroutputarea=$yourtestarea$"/Output" ##your output area
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
	lsetup rcSetup -u
	lsetup rcsetup
	lsetup 'sft releases/pyanalysis/1.5_python2.7-d641e' #correct python version
fi

# set input file to be processed
INOPTION=`sed -n "$LSB_JOBINDEX"p $filenamelist`
echo $INOPTION
# # # # # # # # # # # # # #
#setup inputs with reweights
inch=$"TEST"
#setup channels
ch=$(grep -o -P '(?<=ch:).*(?=:ch)' <<< $INOPTION)
echo "plotting channel: " $ch
syst=$(grep -o -P '(?<=syst:).*(?=:syst)' <<< $INOPTION)
echo "plotting syst: " $syst
inputdir=$ch$"_"$syst
echo  "inputdir is: " $inputdir
re=$"bkg"
iter="5"
echo  "reweight: " $re " iteration: " $iter

##start actual running
if [ $dopythonrun == "true" ]; then
	cd MakePlot
	python PlotTinyTree.py --outputdir $ch --dosyst $syst --reweight $re --iter $iter
	python get_count.py    --inputdir $inputdir --full
	python plot.py         --inputdir $inputdir
	python plot_random.py  --inputdir $inputdir
	python dump_smooth.py   --inputdir $inputdir
fi
echo "DONE!!!"



