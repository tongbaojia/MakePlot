#bsub -q 1nh -J "myrun[1]" < runBatchJob.sh
#bsub -q 8nh -J "myrun[3]" < runBatchJob.sh #for debug failed jobs
#bsub -q 1nh -J "myrun[1-14]" < runBatchJob.sh #for all study jobs
#bsub -q 1nh -J "mysysrun[1-55]" < runBatchJob_sys.sh #for all syst jobs
#bsub -q 2nd -J "myrun[2-9]" < runreweight.sh #for reweighting, because someone is so smart
bsub -q 8nh -J "myrun[1-9]" < runBatchJob.sh #for debug sys jobs
#bsub -q 1nh -J "myrun[1-8]" < runBatchJob.sh #for debug sys jobs
#bsub -q 1nd -J "myrun[4]" < runreweight.sh
#bsub -q 1nd -J "myrun[9]" < runreweight.sh
#bsub -q 1nd -J "myrun[6]" < runreweight.sh
#bsub -q 1nd -J "myrun[8]" < runreweight.sh
#bsub -q 8nh -J "myrun[3]" < runBatchJob.sh