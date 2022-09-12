import fiona
from glob import glob
from shapely.geometry import shape
from rasterstats import zonal_stats
import rasterio
import json
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def ai(value):

    if value < 0:
        return 'No data'
    if value <= 0.03:
        return 'Hyper-arid'
    if value > 0.03 and value <= 0.2:
        return 'Arid'
    if value > 0.2 and value <= 0.5:
        return 'Semi-arid'
    if value > 0.5 and value <= 0.65:
        return 'Dry sub-humid'
    if value > 0.65:
        return 'Humid'

    return 'No Data'

with rasterio.open('/data/Geog-c2s2/ai.tif') as src:
     affine = src.transform
     array = src.read(1)

ai_data = {}

for i, zone in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '11', '14', '17', '21', '25']):
    print(zone)
    for filename in glob('/data/home/faw513/gdbm2/climate_zones/singlepart_files_split/{}_*.shp'.format(zone)):

        with fiona.open(filename) as shp:
            poly = shape(shp[0]['geometry'])

        zs = zonal_stats(poly, array, affine=affine, stats='median')
        median = zs[0]['median']

        ai_data[filename] = [median, ai(median)]

with open('/data/Geog-c2s2/sinu/ai-tiles.json', 'w') as f:
    json.dump(ai_data, f, indent=4, sort_keys=True)
