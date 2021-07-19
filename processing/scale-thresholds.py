from math import ceil
import json

with open('threshold_areas.json') as a:
    areas = json.load(a)

high_areas = {}
low_areas = {}

for k,v in areas.items():
    high_areas[k] = [int(ceil(x * 1.25)) for x in v]
    low_areas[k] = [int(ceil(x * 0.75)) for x in v]

with open('high_threshold_areas.json', 'w') as f:
    json.dump(high_areas, f, sort_keys=True, indent=4)

with open('low_threshold_areas.json', 'w') as f:
    json.dump(low_areas, f, sort_keys=True, indent=4)
