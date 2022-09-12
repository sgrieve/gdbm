'''
Code to convert individual river data files into georeferenced UTM shapefiles.
'''

import math
import numpy as np
import matplotlib.pyplot as plt
import fiona
from shapely.geometry import shape, mapping, LineString
from glob import glob
from scipy import stats
from fiona.crs import from_epsg
from pyproj import CRS
import json
import os.path as path

# BSk_36_b80a024b_4f67_4bdd_b612_dafa46455008_river_0

# path to river data files
for filename in glob('/Users/stuart/gdbm/Results/*/*iver*.csv'):
    print(filename)
    data = np.genfromtxt(filename, delimiter=',')

    eastings = data[:, 0]
    northings = data[:, 1]

    river = LineString(list(zip(eastings, northings)))

    with open('/Users/stuart/gdbm/processing/bboxes.json') as bbox:
        bboxes = json.load(bbox)

    koppen = {'Af': '1', 'Am': '2', 'Aw': '3', 'BWh': '4', 'BWk': '5', 'BSh': '6',
              'BSk': '7', 'Cs': '8', 'Cw': '11', 'Cf': '14', 'Ds': '17',
              'Dw': '21', 'Df': '25'}

    fname = path.basename(filename).split('_riv')[0]
    print(fname)

    tile_info = bboxes['{}_{}.shp'.format(koppen[fname.split('_')[0]],
                                          '_'.join(fname.split('_')[1:]))]['utm_zone']

    hemisphere = False

    if tile_info[1] == 'south':
        hemisphere = True

    crs = CRS.from_dict({'proj': 'utm', 'zone': tile_info[0], 'south': hemisphere})

    epsg = crs.to_authority()[1]

    crs = from_epsg(epsg)

    schema = {'geometry': 'LineString', 'properties': {'id': 'str'}}

    with fiona.open('{}.shp'.format(filename[:-4]), 'w', 'ESRI Shapefile', schema, crs=crs) as c:
        c.write({'geometry': mapping(river), 'properties': {'id': fname}})
