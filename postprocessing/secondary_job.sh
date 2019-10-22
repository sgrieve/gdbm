#!/bin/bash

#$ -cwd
#$ -j y
#$ -N gdbm-postpro
#$ -o /data/Geog-c2s2/gdbm/
#$ -pe smp 1
#$ -l node_type=nxv
#$ -l h_vmem=4G
#$ -l h_rt=10:0:0

module load python/3.6.3

source /data/home/faw513/toku-env/bin/activate

# Run the application.
python /data/home/faw513/gdbm/postprocessing/secondary_analysis.py
