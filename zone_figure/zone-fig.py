import matplotlib.pyplot as plt
import fiona
from glob import glob
from shapely.geometry import shape
import seaborn as sns

palette = sns.color_palette()

koppen = {'1': 'Af', '2': 'Am', '3': 'Aw', '4': 'BWh', '5': 'BWk',
          '6': 'BSh', '7': 'BSk', '8': 'Cs', '11': 'Cw', '14': 'Cf',
          '17': 'Ds', '21': 'Dw', '25': 'Df'}

colors = [0,0,0,1,1,1,1,2,2,2,3,3,3]

labels = ['Tropical', 'Arid', 'Temperate', 'Cold']

plt.figure(figsize=(12,5))

for i, zone in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '11', '14', '17', '21', '25']):

    for filename in glob('../climate_zones/singlepart_files_split/{}_*.shp'.format(zone)):

        with fiona.open(filename) as shp:
            poly = shape(shp[0]['geometry'])

        plt.plot(*poly.exterior.xy, color=palette[colors[i]], linewidth=0.75)


# Hacking a legend
for i in range(4):
    plt.plot([0.01,0.02], [0.01, 0.02], c=palette[i], label=labels[i],
             linewidth=0.75)

plt.plot([0.01,0.02], [0.01, 0.02], c='w', linewidth=7.5)

plt.legend()
plt.axis('equal')
plt.ylabel('Latitude ($^\circ$)')
plt.xlabel('Longitude ($^\circ$)')
plt.tight_layout()
plt.savefig('tiles.eps')
