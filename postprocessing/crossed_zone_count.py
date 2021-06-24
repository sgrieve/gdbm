import re
from glob import glob

logs = glob('/data/Geog-c2s2/gdbm/gdbm-?.o*.*')

koppen = {'1': 'Af', '2': 'Am', '3': 'Aw', '4': 'BWh', '5': 'BWk',
          '6': 'BSh', '7': 'BSk', '8': 'Cs', '11': 'Cw', '14': 'Cf',
          '17': 'Ds', '21': 'Dw', '25': 'Df'}

# Build a dict keyed by climate zone, with empty lists ready to be appended to
crossed_zone_counts = {}
for key, value in koppen.items():
    crossed_zone_counts[value] = []

for log in logs:
    with open(log) as f:
        log_data = f.read()

    # Grab the climate zone numerical code, and convert to koppen id
    zone = re.search("\d+_.+\.bil", log_data)
    zone = koppen[zone[0].split('_')[0]]

    # Getting the before and after values from the log
    before = re.search("Right, I\'ve pruned those and have \d+ junctions left", log_data)
    before = int(re.findall('\d+', before[0])[0])
    after = re.search("I now have \d+ Junctions left", log_data)
    after = int(re.findall('\d+', after[0])[0])

    crossed_zone_counts[zone].append(before - after)


print('\nBasins crossing zone or tile boundaries by Koppen Climate Zone:\n')
total_count = []
for key in crossed_zone_counts:
    count = sum(crossed_zone_counts[key])
    print('\t', key, count)
    total_count.append(count)

print('\nThere are a total of {} basins which cross zone or tile boundaries.'.format(sum(total_count)))
