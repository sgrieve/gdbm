import os
import fiona
import matplotlib.pyplot as plt
from shapely.geometry import shape, mapping, Polygon

def punch_out_lakes(in_path, cz_in, out_path):
    with fiona.open(os.path.join(in_path, cz_in)) as shp:
        cz = shape(shp[0]['geometry'])

    with fiona.open('GLWD-level1/glwd_1.shp') as shp:
        for s in shp:
            lake = shape(s['geometry'])
            if lake.intersects(cz):
                # We only want the external outline of each lake
                lake = Polygon(lake.exterior)
                cz = cz.difference(lake)

    schema = {'geometry': 'Polygon', 'properties': {'id': 'int'}}


    # Clipping out lakes may give us a MultiPolygon which needs split up
    if cz.geom_type == 'MultiPolygon':

        cz_id = os.path.splitext(cz_in)[0]

        for i, sub_cz in enumerate(cz):
            # Arbitraty minimum area of new polygons set at 1/5 of original area
            if sub_cz.area / cz.area > 0.2:
                out_name = '{}_{}.shp'.format(cz_id, i)
                with fiona.open(os.path.join(out_path, out_name), 'w', 'ESRI Shapefile', schema) as c:
                    c.write({'geometry': mapping(sub_cz), 'properties': {'id': i}})

    # otherwise we just write out our single Polygon
    elif cz.geom_type == 'Polygon':
        with fiona.open(os.path.join(out_path, cz_in), 'w', 'ESRI Shapefile', schema) as c:
            c.write({'geometry': mapping(cz), 'properties': {'id': 1}})

    else:
        print(cz_in, 'does not seem to be a polygon, something has gone wrong.')


punch_out_lakes('../climate_zones/singlepart_files_split/',
                '14_197_7405a2dc_fa14_48a1_bdef_d6f844359eda.shp',
                '/Users/stuart/gdbm/lakes/')
