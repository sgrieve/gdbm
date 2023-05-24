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

'''
Af_81_5b46db40_6f01_4398_8166_bb1f34bfe720_river_350_ll
Am_41_river_398_ll

BWh_17_7d288d47_b527_4c30_b3fd_5fc7037ab569_river_295_ll - shows different drainage pattern - need topo to show we are right here
BWh_27_cab81d29_d2b9_4369_b406_a690606747f2_river_508_ll - shows different drainage pattern - need topo to show we are right here
BWh_6_d527a345_8a95_493f_98b6_14be03730f06_river_885_ll  - shows different drainage pattern - need topo to show we are right here

BWh_27_6bfc7f20_93e8_48ef_a023_cb7cfc41b18e_river_211_ll
BWh_27_c566a273_b019_4224_a4e0_2ff620e9f0f4_river_400_ll

Cs_74_ad11a41e_a724_4c62_9411_74c785fdddcd_river_39_ll
Cw_30_f82b0908_cfbd_40c8_b3c5_50e57b02cc52_river_588_ll
Cf_69_8ae4980e_df64_4ca9_b278_55dd411a9f66_0_river_538_ll

Df_102_7382c7f4_921a_4eb0_b33f_84801e0668e6_river_736_ll
Df_44_c90ad0c5_baa1_4d42_9585_d71ff7a5cc1b_0_river_438_ll
Dw_10_fcc9447b_fae6_4307_8729_90d9575e5b12_0_river_417_ll

'''

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
