#!/bin/bash

# $1 - shapefile name without .shp
# $2 - utm zone
# $3 - north or south
# $4 - drainage threshold in pixels
# $5 - min basin size in pixels
# $6 - max basin size in pixels

# Set up paths so we have a folder for each sub zone
cd /data/Geog-c2s2/gdbm/
mkdir $1
cd $1

# Download the tiles we need
python /data/home/faw513/gdbm/processing/get_urls.py $1.shp | xargs -n 1 -P 8 -I FILEPATH /data/home/faw513/aws/v2/current/bin/aws s3 cp FILEPATH . --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request

# Build virtual raster from tiles
gdalbuildvrt input.vrt *.tif

# Clip the merged raster using the corresponding shapefile
gdalwarp -multi -wo 'NUM_THREADS=val/ALL_CPUS' -srcnodata -32768 -dstnodata -9999 -cutline /data/home/faw513/gdbm/climate_zones/singlepart_files_split/$1.shp -crop_to_cutline -of ENVI input.vrt tmp.bil

# Reproject the clipped raster to utm and save as a floating point file
gdalwarp -t_srs '+proj=utm +zone='$2' +datum=WGS84 +'$3'' -of ENVI -ot Float32 tmp.bil $1.bil

# Tidy up some temp files
rm tmp.*
rm *.tif
rm *.vrt

# Run the LSD code (on HPC)
/data/home/faw513/LSDTopoTools_ChiMudd2014/driver_functions_MuddChi2014/gdbm_analysis.exe /data/Geog-c2s2/gdbm/$1/ $1 /data/Geog-c2s2/gdbm/$1/ $1 $4 $5 $6

# Extract the rivers from the output data
python /data/home/faw513/gdbm/postprocessing/export_rivers.py $1_RawBasins.csv

# Remove the raster files
rm $1.bil
rm $1.hdr
rm $1.bil.aux.xml
