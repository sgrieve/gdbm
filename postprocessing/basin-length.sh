#!/bin/bash

#$ -cwd
#$ -j y
#$ -N gdbm-total-length
#$ -o /data/Geog-c2s2/gdbm/
#$ -pe smp 1
#$ -l node_type=nxv
#$ -l h_vmem=6G
#$ -l h_rt=4:0:0

module load python/3.6.3

source /data/home/faw513/toku-env/bin/activate

python /data/home/faw513/gdbm/postprocessing/get_total_basin_length.py
