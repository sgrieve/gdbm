import json
import sys

# Skip these zones as they need much more time and memory than everything else
skips = ['1_81.shp', '25_102_a8e17245_17bf_4dca_b6ba_73be4baa04c6_0.shp',
         '7_94_6c14f0b5_8acb_496d_879b_bdcf64b86ab9_0.shp',
         '7_94_bb6f1329_2eb7_4c6a_90fd_1b3f1efb4cd7_0.shp']

# Load input args, the first is the lower number of tiles and the second is
# the upper number of tiles to include in this array job
lower = int(sys.argv[1])
upper = int(sys.argv[2])


with open('download_links.json') as srtm:
    links = json.load(srtm)

with open('bboxes.json') as bbox:
    bboxes = json.load(bbox)

with open('threshold_areas.json') as bbox:
    threshes = json.load(bbox)

# Count the number of files to download for each sub zone
counts = []
for key, urls in links.items():
    if len(urls) > 0:
        counts.append((key, len(urls)))

counts.sort(key=lambda tup: tup[1], reverse=True)

# Filter the data by the input args, and remove any zones in the skip list
to_process = [x for x in counts if (x[1] > lower and x[1] <= upper) and
              (x[0] not in skips)]

# Write the required params for each job into a file in the format:
# job_id shapefile_name(no extension) utm_zone north/south no-of-tiles drainage_threshold min_basin_size max_basin_size
with open('array_params_{}_{}.txt'.format(lower, upper), 'w') as f:
    for i, a in enumerate(to_process, start=1):
        utm = bboxes[a[0]]['utm_zone']
        thresh_data = threshes[a[0][:-4]]
        f.write('{} {} {} {} {} {} {} {}\n'.format(str(i).zfill(4), a[0][:-4],
                                                   utm[0], utm[1], a[1],
                                                   thresh_data[0],
                                                   thresh_data[1],
                                                   thresh_data[2]))
