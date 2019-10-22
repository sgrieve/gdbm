import os
from scipy import stats
import numpy as np
from glob import glob

for zone in ['Af', 'Am', 'Aw', 'BWh','BWk', 'BSh', 'BSk', 'Cs', 'Cw', 'Cf', 'Ds', 'Dw', 'Df']:

    # We collect each file's data into a list of arrays
    offset_elevs = []
    median_norm_offsets = []

    # The first input argument is the name of the output file, without extension
    output_filename = '/data/Geog-c2s2/gdbm/{}_data'.format(zone)

    # Store the output strings as a list, where the first item is a header
    output = ['RiverName,NCI,Relief,FlowLength,TotalSlope,Area,ai_mean,ai_median,ai_std,ai_min,ai_max,ai_n\n']

    # Get the list of files to be processed from the second command line arg
    final_file_list = glob('/data/Geog-c2s2/gdbm-complete/*/{}*river*.csv'.format(zone))

    # Cycle through every river file in our list and get the metrics.
    for i, filename in final_file_list:

        data = np.genfromtxt(filename, delimiter=',')

        A = data[:, 5]  # FlowLength
        B = data[:, 4]  # Elevation

        area = np.max(data[:, 6])

        AI = data[:, 8]  # Aridity index

        # Cant use np.ptp as it doesnt handle nans
        R = np.nanmax(B) - np.nanmin(B)
        FlowLength = np.nanmax(A) - np.nanmin(A)

        # where x1,y1 x2,y2 are the long profile endpoints
        x = [A[0], np.nanmax(A)]
        y = [B[0], np.nanmax(B)]

        result = stats.linregress(x, y)

        # Unpack the slope and intercept from the result of the linregress function
        m = result[0]
        b = result[1]

        Y = m * A + b  # Y values on the line
        offset_elev = (B - Y) / R

        # Add the results to out list of results
        offset_elevs.append(offset_elev)
        NCI = np.nanmedian(offset_elev)

        # Also need the total river length, river relief, river slope and name
        river_name = os.path.splitext(os.path.basename(filename))[0]

        output.append('{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(river_name, NCI, R,
                                                                    FlowLength, R / FlowLength, area,
                                                                    np.nanmean(AI), np.nanmedian(AI),
                                                                    np.nanstd(AI), np.nanmin(AI),
                                                                    np.nanmax(AI),
                                                                    np.count_nonzero(~np.isnan(AI))
                                                                    ))

    with open('{}.csv'.format(output_filename), 'w') as f:
        for o in output:
            f.write(o)
