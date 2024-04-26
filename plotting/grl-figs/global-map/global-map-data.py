import csv

out_data = ['river_id,lat,long,total_length,area,AI_median,GC\n']

zones = ['Af','Am','Aw','BWh','BWk','BSh','BSk','Cs','Cw','Cf','Ds','Dw','Df']

for zone in zones:
    print(zone)
    with open('/data/Geog-c2s2/gdbm/Results/{}_data.csv'.format(zone), 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # Skip the header

        for row in reader:
            name = row[0]
            length = row[3]
            area = row[5]
            AI = row[7]
            GC = row[-1]

            with open('/data/Geog-c2s2/gdbm/Results/{}/{}.csv'.format(zone, name), 'r') as f2:
                raw_data = csv.reader(f2, delimiter=',')
                first_row_raw = next(raw_data)
                lat = first_row_raw[2]
                long = first_row_raw[3]
                out_data.append('{},{},{},{},{},{},{}\n'.format(name, lat, long, length, area, AI, GC))

with open('/data/Geog-c2s2/gdbm/global_data.csv', 'w') as w:
    for l in out_data:
        w.write(l)
