from glob import glob
import json
import os
from math import ceil

# Dict to store the results from all of the files, keyed by river ID
res_data = {}

for file in glob('../res_jsons/*.json'):
    with open(file) as f:
        data = json.loads(f.read())

    river_id = os.path.splitext(os.path.basename(file))[0]

    resolution = data['geoTransform'][1]
    cell_area = resolution ** 2

    # This is the channel threshold, min basin area, max basin area
    res_data[river_id] = [ceil(22500000 / cell_area),
                          ceil(45000000 / cell_area),
                          ceil(450000000 / cell_area)]

with open('../processing/threshold_areas.json', 'w') as f:
    json.dump(res_data, f, sort_keys=True, indent=4)
