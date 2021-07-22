#!/bin/bash

#$ -cwd
#$ -j y
#$ -N gdbm-sensi-3h
#$ -o /data/Geog-c2s2/gdbm-sensi-h/
#$ -pe smp 1
#$ -l h_vmem=128G
#$ -l h_rt=4:0:0
#$ -t 1-634:3
#$ -tc 100

module load gdal/2.3.1
module load gcc/6.3.0
module load python/3.6.3
module load proj/5.2.0

# Using the Tokunaga environment as it has rasterio installed
source /data/home/faw513/toku-env/bin/activate

# Parse parameter file to get variables.
number=$SGE_TASK_ID
paramfile=/data/home/faw513/gdbm2/processing/array_params_15_99h.txt

index=`sed -n ${number}p $paramfile | awk '{print $1}'`
variable1=`sed -n ${number}p $paramfile | awk '{print $2}'`
variable2=`sed -n ${number}p $paramfile | awk '{print $3}'`
variable3=`sed -n ${number}p $paramfile | awk '{print $4}'`
# The fifth param is the number of SRTM tiles - dont need this at this stage
variable4=`sed -n ${number}p $paramfile | awk '{print $6}'`
variable5=`sed -n ${number}p $paramfile | awk '{print $7}'`
variable6=`sed -n ${number}p $paramfile | awk '{print $8}'`

# Run the application.
sh /data/home/faw513/gdbm2/processing/runner_h.sh $variable1 $variable2 $variable3 $variable4 $variable5 $variable6
