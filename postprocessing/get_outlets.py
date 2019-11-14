import csv
import os
from glob import glob

output_data = []

for input_file in glob('/data/Geog-c2s2/gdbm-complete/*/*river*.csv'):
    filename = os.path.basename(input_file)
    river_name = os.path.splitext(filename)[0]

    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        row = next(reader)
        lat = row[2]
        long = row[3]
        output_data.append('{},{},{}\n'.format(river_name, lat, long))

with open('/data/Geog-c2s2/gdbm-complete/outlets.csv', 'w') as w:
    w.write('river_id,lat,long\n')
    for line in output_data:
        w.write(line)
