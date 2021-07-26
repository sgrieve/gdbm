import math
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy import stats

zones = ['A', 'B', 'C', 'D',]
euc = []
areas = []

for i, z in enumerate(zones):
    files = glob('/Users/stuart/CardiffProject/Results/{0}*/{0}*_river*.csv'.format(z))
    files = files[::30]
    print(len(files))
    for filename in files:
        data = np.genfromtxt(filename, delimiter=',')

        flow_length = np.max(np.abs(data[:, 5] - np.max(data[:, 5])))

        area = np.max(data[:, 6])

        top = (data[0][0], data[0][1])
        bottom = (data[-1][0], data[-1][1])

        euc_dist = math.hypot(bottom[0] - top[0], bottom[1] - top[1]) * 30
        euc.append(euc_dist)
        areas.append(area)

x = np.log(areas)
y = np.log(euc)


slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print(slope)

plt.plot(x, y, 'k.')
plt.plot(x, intercept + (x * slope), 'b-')

plt.title('Euclidean Distance ($h = {}$)'.format(round(slope, 3)))

plt.xlabel('Drainage area ($km^2$)')
plt.ylabel('Length ($km$)')

axes = plt.gca()
a=axes.get_xticks().tolist()
a = [int(round(np.power(np.e, q)/1000000, 0)) for q in a]
axes.set_xticklabels(a)

a=axes.get_yticks().tolist()
a = [int(round(np.power(np.e, q)/1000, 0)) for q in a]
axes.set_yticklabels(a)

plt.savefig('euclidean.eps')
