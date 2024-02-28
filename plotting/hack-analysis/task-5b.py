import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from glob import glob
from sklearn.metrics import r2_score


def hack(x, k):
    return k * (x ** 0.531)


koppen_zones = ['A', 'C', 'D', 'B']
titles = ['Tropical', 'Temperate', 'Continental', 'Dry']

for i, zone in enumerate(koppen_zones):

    ax = plt.subplot(2, 2, i+1)

    files = glob('{}*.csv'.format(zone))

    tmp = []
    for f in files:
        tmp.append(pd.read_csv(f))

    data = pd.concat(tmp)

    area = data['Area']
    length = data['FlowLength']

    x = area
    y = length

    plt.scatter(x, y, c='k', s=2, alpha=0.1)

    ax = plt.gca()

    ax.set_yscale('log')
    ax.set_xscale('log')

    popt, pcov = curve_fit(hack, x, y, bounds=([0.9, 4]), p0=[1.4])

    plt.plot(x, hack(x, popt[0]), 'r-')

    plt.title(titles[i])


    info_label = 'c={}\n$r^2$={}'.format(round(popt[0], 3), round(r2_score(y, hack(x, popt[0])), 2))
    plt.text(408000000, 1500, info_label)


    plt.xlim(23430968, 2624323291)
    plt.ylim(353, 462600)


plt.tight_layout(pad=1.5)
plt.gcf().add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.ylabel('Channel Length ($m$)')
plt.xlabel('Drainage Area ($m^2$)')



plt.savefig('task-5b.png')
