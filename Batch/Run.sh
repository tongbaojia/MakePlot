#bsub -q 1nh -J "myrun[1]" < runBatchJob.sh
#bsub -q 8nh -J "myrun[3]" < runBatchJob.sh #for debug failed jobs
#bsub -q 1nh -J "myrun[1-14]" < runBatchJob.sh #for all study jobs
#bsub -q 1nh -J "mysysrun[1-55]" < runBatchJob_sys.sh #for all syst jobs
bsub -q 8nh -J "myrun[1-7]" < runBatchJob.sh #for debug sys jobs