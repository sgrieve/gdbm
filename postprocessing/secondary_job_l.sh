#!/bin/bash

#$ -cwd
#$ -j y
#$ -N gdbm-post-l
#$ -o /data/Geog-c2s2/gdbm-sensi-l/
#$ -pe smp 1
#$ -l h_vmem=4G
#$ -l h_rt=1:0:0
#$ -t 1-13
#$ -tc 13

module load python/3.6.3

source /data/home/faw513/toku-env/bin/activate

# Parse parameter file to get variables.
number=$SGE_TASK_ID
paramfile=/data/home/faw513/gdbm2/postprocessing/params.txt

index=`sed -n ${number}p $paramfile | awk '{print $1}'`
variable1=`sed -n ${number}p $paramfile | awk '{print $2}'`

python /data/home/faw513/gdbm2/postprocessing/secondary_analysis_l.py $variable1
