import matplotlib.pyplot as plt
import pyproj
from shapely.geometry import mapping, MultiLineString
from shapely.ops import transform
from functools import partial
import fiona

'''
Data files used to generate this figure:
Humid: Af_72_RawBasins.csv
Arid: BWh_6_fb4df8b4_bcfc_4ad9_86f3_02782e742005_RawBasins.csv
Cold: Dw_10_ec7164ec_3c42_4f75_9dbe_dc478ce15f7b_RawBasins.csv
'''

def load_line(path):
    tmp = []
    with fiona.open(path) as shp:
        for g in shp:
            if g['geometry']:
                tmp.append(g['geometry']['coordinates'])
    return MultiLineString(tmp)

def project_and_plot(lines, width=0.45, color='k'):

    for i, l in enumerate(lines):
        line_equal = transform(partial(pyproj.transform,
                                       pyproj.Proj(init='EPSG:4326'),
                                       pyproj.Proj(proj='aea',
                                                   lat1=l.bounds[1],
                                                   lat2=l.bounds[3])), l)

        y, x = (line_equal.xy)

        plt.plot(x, y, color=color, linewidth=width)


def format_axis(ax):

    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.axis('equal')
    ax.invert_yaxis()
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off')

    return x0, x1, y0, y1

def plot_bottom_panels(rivers):

    for i, river in enumerate(rivers, start=1):

        ax = plt.subplot(2, 2, 2 + i)
        project_and_plot(load_line(river), color='b')
        project_and_plot(load_line(mainstem[i]), color='r')

        # Basins split into 2 files so uniform line weight where overlaps occur
        project_and_plot(load_line(basins[i][0]), 0.2)
        project_and_plot(load_line(basins[i][1]), 0.2)

        x0, x1, y0, y1 = format_axis(ax)

        if i == 1:
            plt.plot([9394000,9404000], [11285500, 11285500],
                     'k-', linewidth=3)
        elif i == 2:
            plt.plot([10145500, 10155500], [14289500, 14289500],
                     'k-', linewidth=3)

    return x0, x1, y0, y1

def plot_top_panels(x0, x1, y0, y1):

    for i in range(1, 3):

        ax = plt.subplot(2, 2, i)

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        plt.tick_params(axis='both', which='both', bottom='off', top='off',
                        left='off', right='off')


rivers = ['shapefiles/humid_line.shp', 'shapefiles/arid_line_s.shp']
mainstem = [None, 'shapefiles/humid_mainstem.shp',
            'shapefiles/arid_mainstem.shp']
basins = [None, ('shapefiles/humid_outline.shp','shapefiles/humid_all.shp'),
          ('shapefiles/arid_outline.shp','shapefiles/arid_all.shp')]

plt.figure(figsize=(12,8))
x0, x1, y0, y1 = plot_bottom_panels(rivers)
plot_top_panels(x0, x1, y0, y1)
plt.tight_layout()
plt.savefig('summary.eps')
