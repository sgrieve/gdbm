#!/bin/bash

#$ -cwd
#$ -j y
#$ -N gdbm-resolution
#$ -o /data/Geog-c2s2/gdbm/
#$ -pe smp 1
#$ -l node_type=sm
#$ -l h_vmem=64G
#$ -l highmem
#$ -l h_rt=0:30:0
#$ -t 1-1818
#$ -tc 100

module load gdal/2.3.1
module load gcc/6.3.0
module load python/3.6.3
module load proj/5.2.0

# Parse parameter file to get variables.
number=$SGE_TASK_ID
paramfile=/data/home/faw513/gdbm/processing/resolution_array_params.txt

index=`sed -n ${number}p $paramfile | awk '{print $1}'`
variable1=`sed -n ${number}p $paramfile | awk '{print $2}'`
variable2=`sed -n ${number}p $paramfile | awk '{print $3}'`
variable3=`sed -n ${number}p $paramfile | awk '{print $4}'`

# Run the application.
sh /data/home/faw513/gdbm/processing/res_runner.sh $variable1 $variable2 $variable3
