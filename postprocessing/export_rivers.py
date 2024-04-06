import csv
import os
import sys
from collections import Counter
import rasterio

def koppen_number_to_string(filename):
    '''
    Helper function to convert a filename with a numerical koppen code into
    a string koppen code, using the dictionary below.
    '''
    koppen = {'1': 'Af', '2': 'Am', '3': 'Aw', '4': 'BWh', '5': 'BWk',
              '6': 'BSh', '7': 'BSk', '8': 'Cs', '11': 'Cw', '14': 'Cf',
              '17': 'Ds', '21': 'Dw', '25': 'Df'}

    split_sub_zone = filename.split('_')
    koppen_zone = koppen[split_sub_zone[0]]
    return koppen_zone + '_' + '_'.join(split_sub_zone[1:])

# Processing the input filename to get the climate zone number and sub number
input_file = sys.argv[1]
filename = os.path.basename(input_file)
sub_zone = filename.split('RawBasins')[0][:-1]

# This file gives us a list of the row,col of each filled pit above a theshold
pit_id_file = '{}_pit_id.csv'.format(sub_zone)

if os.path.isfile(input_file) and os.path.isfile(pit_id_file):

    # Not using csv reader here as we want the whole row
    with open(pit_id_file) as pit_file:
        pit_keys = pit_file.readlines()

    # Dump all the row,col id pairs into a list, then convert to a set for more
    # efficient lookup: O(1) vs O(n)
    pit_keys = [p.strip() for p in pit_keys]
    pit_keys = set(pit_keys)

    # We want to convert back from the numerical climate zone codes to the strings
    sub_zone = koppen_number_to_string(sub_zone)

    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip the header
        next(reader)

        # Load all of the basin ids from the file
        basin_ids = []
        for r in reader:
            basin_ids.append(r[9])

        # Set will give us a unique set of basin ids with no duplicates
        basin_ids = set(basin_ids)

        # Create a dictionary keyed with basin ids and the values are empty lists
        basins = {id: [] for id in basin_ids}

        # Jump back to the start of the file and skip the header
        csvfile.seek(0)
        next(reader)

        # Select the data we want from the raw file so we have a list of rows of
        # data for each basin.
        for row in reader:
            basins[row[9]].append((row[1:9] + row[10:]))

    source_path = '/data/Geog-c2s2/ai.tif'
    with rasterio.open(source_path) as src:

        # get the main stem ID for each basin in the input file
        for basin_key in basins:
            sources = []

            for x in basins[basin_key]:
                sources.append(x[7])

            # Main stem is the ID of the longest channel in each basin
            main_stem = Counter(sources).most_common()[0][0]

            # Write each main stem's data to its own file
            with open('{}_river_{}.csv'.format(sub_zone, main_stem), 'w') as o:
                for data in basins[basin_key][::-1]:
                    if data[7] == main_stem:
                        # sample returns a generator, so we use next() to yield
                        # the first (and only) result
                        ai = next(src.sample([(float(data[3]), float(data[2]))]))[0]

                        if ai >= 0:
                            ai = str(round(ai, 4))
                        else:
                            ai = 'NaN'

                        # pit_flag is 0 if there has not been any changes to the DEM cell
                        # and is 1 if there has been
                        pit_flag = '0'
                        pit_key = ','.join(data[:2])
                        if pit_key in pit_keys:
                            pit_flag = '1'

                        o.write(','.join(data[:9]) + ',' + ai + ',' + pit_flag + ',' + ','.join(data[9:]) + '\n')

    # These two print statements will allow me to grep for failure and success
    print('Successfully generated some river files')
else:
    print('No rivers to process, as the basins file was not found')
