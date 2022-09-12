import numpy as np
from glob import glob
from geopy import distance

reach = 300
zones = ['A', 'B', 'C', 'D']

for i, z in enumerate(zones):
    x = []

    files = glob('/data/Geog-c2s2/gdbm-submitted-2021/*/{}*_river*.csv'.format(z))
    print(z)
    for filename in files:
        data = np.genfromtxt(filename, delimiter=',')
        data_length = len(data[:,1])

        if data_length > reach:
            for start, end in zip(range(0, data_length - 1, reach), range(reach, data_length, reach)):

                top = (data[start][2], data[start][3])
                bottom = (data[end][2], data[end][3])

                flow_length = data[end, 5] - data[start, 5]
                euc_dist = distance.geodesic(top, bottom, ellipsoid='WGS-84').meters

                s = '{},{},{}'.format(flow_length, euc_dist, flow_length / euc_dist)

                x.append(s)

    with open('{}-sinu-data.csv'.format(z), 'w') as w:
        for p in x:
            w.write('{}\n'.format(p))
