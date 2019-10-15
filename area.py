from glob import glob
import numpy as np
import os
import json

# total = []
#
# for z in ['Af', 'Am', 'Aw', 'BSh', 'BWh', 'BWk', 'Cf', 'Cs', 'Cw', 'Df', 'Ds', 'Dw', 'BSk']:
#     print(z)
#     for f in glob('Results/{}/*iver*.csv'.format(z)):
#         data = np.genfromtxt(f, delimiter=',')
#         total.append(data[0][6])
#
# print(np.mean(total))

mydict = {}

for z in ['Af', 'Am', 'Aw', 'BSh', 'BWh', 'BWk', 'Cf', 'Cs', 'Cw', 'Df', 'Ds', 'Dw', 'BSk']:
    print(z)
    for f in glob('Results/{}/*iver*.csv'.format(z)):
        data = np.genfromtxt(f, delimiter=',')
        mydict[os.path.splitext(os.path.basename(f))[0]] = [data[0][2], data[0][3], data[0][6]]

with open('newdata.json', 'w') as output:
    json.dump(mydict, output)
