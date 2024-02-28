import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from glob import glob
from sklearn.metrics import r2_score


def hack(x, h, k):
    return k * (x ** h)

files = glob('D*.csv')

d = []
for f in files:
    d.append(pd.read_csv(f))


x = pd.concat(d)

for file in [x]:

    # data = pd.read_csv(file)

    data = file

    area = data['Area']
    length = data['FlowLength']

    # x = np.log(area)
    # y = np.log(length)

    x = area
    y = length

    plt.scatter(x, y, c='k', s=2, alpha=0.1)

    ax = plt.gca()

    ax.set_yscale('log')
    ax.set_xscale('log')

    popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])
    print(popt)

    plt.plot(x, hack(x, popt[0], popt[1]), 'r-')
    plt.title('h={}, c={}, $r^2$={}'.format(round(popt[0], 3), round(popt[1], 3), round(r2_score(y, hack(x, popt[0], popt[1])), 2)))

    # slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    # print(slope)
    # plt.plot(x, intercept + (x * slope), 'b-')


    plt.savefig('d.png') #.format(file))
    plt.clf()


# tropical temperate continental dry
# A C D B
# .528 .529 0.527 .536
