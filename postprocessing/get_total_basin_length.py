import csv
import os
from glob import glob
from collections import Counter
import numpy as np

output_data = []

for input_file in glob('*RawBasins.csv'):
    filename = os.path.basename(input_file)
    sub_zone = filename.split('RawBasins')[0][:-1]

    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip the header
        next(reader)

        # Load all of the basin ids from the file
        basin_ids = []
        for r in reader:
            basin_ids.append(r[12])

        # Set will give us a unique set of basin ids with no duplicates
        basin_ids = set(basin_ids)

        # Create a dictionary keyed with basin ids and the values are empty lists
        basins = {id: [] for id in basin_ids}

        river_ids = {}

        # Jump back to the start of the file and skip the header
        csvfile.seek(0)
        next(reader)

        # Select the data we want from the raw file so we have a list of rows of
        # data for each basin.
        for row in reader:
            basins[row[12]].append(row[11])

        # get the main stem ID for each basin in the input file
        for key, value in basins.items():

            # Main stem is the ID of the longest channel in each basin
            main_stem = Counter(value).most_common()[0][0]
            river_ids[key] = main_stem

        # Reset our basins dict to now contain the lengths
        basins = {id: [] for id in basin_ids}

        # Jump back to the start of the file and skip the header
        csvfile.seek(0)
        next(reader)

        # We want to process the first row of data outside the loop so we dont go out of bounds
        first_data_row = next(reader)
        stream_id = first_data_row[11]
        basin_id = first_data_row[12]
        previous_length = float(first_data_row[7])

        for row in reader:
            if row[12] == basin_id and row[11] == stream_id:
                length = previous_length - float(row[7])
                basins[basin_id].append(length)
            elif row[12] == basin_id:
                stream_id = row[11]
            else:
                stream_id = row[11]
                basin_id = row[12]
            previous_length = float(row[7])

    for key, value in basins.items():
        output_data.append('{}_river_{},{}\n'.format(sub_zone,river_ids[key], np.sum(value)))

with open('output.csv', 'w') as w:
    w.write('river_id,total_length\n')
    for line in output_data:
        w.write(line)
