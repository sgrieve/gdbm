import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from glob import glob
from sklearn.metrics import r2_score


def hack(x, k):
    return k * (x ** 0.531)

files = glob('*_data.csv')

tmp = []
for f in files:
    tmp.append(pd.read_csv(f))

data = pd.concat(tmp)

ai_classes = ['Hyper-arid', 'Arid', 'Semi-arid', 'Dry sub-humid', 'Humid']
lowers = [0.00, 0.03, 0.20, 0.50, 0.65]
uppers = [0.03, 0.20, 0.50, 0.65, data['ai_mean'].max()]

# Need a longer figure to fit a third row of plots without any squashing
plt.gcf().set_size_inches(6.4, 7.2)

for i, ai_class in enumerate(ai_classes):

    ax = plt.subplot(3, 2, i+1)

    data_slice = data[data['ai_mean'].between(lowers[i], uppers[i], inclusive='right')]

    area = data_slice['Area']
    length = data_slice['FlowLength']

    x = area
    y = length

    plt.scatter(x, y, c='k', s=2, alpha=0.1)

    ax = plt.gca()

    ax.set_yscale('log')
    ax.set_xscale('log')

    popt, pcov = curve_fit(hack, x, y, bounds=([0.9, 4]), p0=[1.4])

    plt.plot(x, hack(x, popt[0]), 'r-')

    plt.title(ai_classes[i])

    info_label = 'c={}\n$r^2$={}'.format(round(popt[0], 3), round(r2_score(y, hack(x, popt[0])), 2))
    plt.text(408000000, 1500, info_label)


    plt.xlim(23430968, 2624323291)
    plt.ylim(353, 462600)


plt.tight_layout(pad=1.5)
plt.gcf().add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.ylabel('Channel Length ($m$)')
plt.xlabel('Drainage Area ($m^2$)')

plt.savefig('task-5d.png')
