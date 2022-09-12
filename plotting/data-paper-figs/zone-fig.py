import matplotlib.pyplot as plt
import fiona
from glob import glob
from shapely.geometry import shape
import seaborn as sns
import json

palette = sns.color_palette()

koppen = {'1': 'Af', '2': 'Am', '3': 'Aw', '4': 'BWh', '5': 'BWk',
          '6': 'BSh', '7': 'BSk', '8': 'Cs', '11': 'Cw', '14': 'Cf',
          '17': 'Ds', '21': 'Dw', '25': 'Df'}

colors = [0,0,0,1,1,1,1,2,2,2,3,3,3]

labels = ['Tropical', 'Arid', 'Temperate', 'Cold']

plt.figure(figsize=(12, 10))

plt.subplot(2, 1, 1)

for i, zone in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '11', '14', '17', '21', '25']):

    for filename in glob('../../climate_zones/singlepart_files_split/{}_*.shp'.format(zone)):

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

plt.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=False)

# ------------------------------

def ai_convert(value):

    if value < 0:
        return 0
    if value <= 0.03:
        return 1
    if value > 0.03 and value <= 0.2:
        return 2
    if value > 0.2 and value <= 0.5:
        return 3
    if value > 0.5 and value <= 0.65:
        return 4
    if value > 0.65:
        return 5


labels = ['No data',
          'Hyper-arid ($AI \leq 0.03$)',
          'Arid ($0.03 < AI \leq 0.2$)' ,
          'Semi-arid ($0.2 < AI \leq 0.5$)',
          'Dry sub-humid ($0.5 < AI \leq 0.65$)',
          'Humid ($AI > 0.65$)']

with open('ai-tiles.json') as ai:
    ai_tiles = json.load(ai)

palette = sns.color_palette('YlOrBr', as_cmap=False)


plt.subplot(2, 1, 2)

for i, zone in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '11', '14', '17', '21', '25']):

    for filename in glob('../../climate_zones/singlepart_files_split/{}_*.shp'.format(zone)):

        with fiona.open(filename) as shp:
            poly = shape(shp[0]['geometry'])

        color = palette[ai_convert(ai_tiles[filename][0])]
        plt.plot(*poly.exterior.xy, color=color, linewidth=0.75)


# Hacking a legend
for i in range(1,6):
    plt.plot([0.01,0.02], [0.01, 0.02], c=palette[i], label=labels[i],
             linewidth=0.75)

plt.plot([0.01,0.02], [0.01, 0.02], c='w', linewidth=7.5)

plt.legend()
plt.axis('equal')
plt.ylabel('Latitude ($^\circ$)')
plt.xlabel('Longitude ($^\circ$)')


plt.gcf().text(0.08, 0.95, 'a', ha='center', size=12)
plt.gcf().text(0.08, 0.48, 'b', ha='center', size=12)

plt.tight_layout()
plt.savefig('tiles.png')
plt.savefig('tiles.pdf')
