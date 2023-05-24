'''
Code to convert individual river data files into georeferenced lat long shapefiles.
'''

import math
import numpy as np
import fiona
from shapely.geometry import shape, mapping, LineString
from glob import glob
from fiona.crs import from_epsg
from pyproj import CRS
import json
import os.path as path

# BSk_36_b80a024b_4f67_4bdd_b612_dafa46455008_river_0

# path to river data files
# for filename in glob('/Users/stuart/gdbm/Results/*/BSk_36_b80a024b_4f67_4bdd_b612_dafa46455008_river_0.csv'):

for filename in glob('/Users/stuart/gdbm/Results/*/*river_*.csv')[::1000]:
    print(filename)
    data = np.genfromtxt(filename, delimiter=',')

    lat = data[:, 2]
    long = data[:, 3]

    river = LineString(list(zip(long, lat)))

    fname = path.basename(filename).split('_riv')[0]

    epsg = 4326
    crs = from_epsg(epsg)

    schema = {'geometry': 'LineString', 'properties': {'id': 'str'}}

    with fiona.open('{}_ll.shp'.format(filename[:-4]), 'w', 'ESRI Shapefile', schema, crs=crs) as c:
        c.write({'geometry': mapping(river), 'properties': {'id': fname}})
