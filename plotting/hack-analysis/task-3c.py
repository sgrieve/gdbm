import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from glob import glob
from sklearn.metrics import r2_score


def hack(x, h, k):
    return k * (x ** h)


files = glob('*_data.csv')

tmp = []
for f in files:
    tmp.append(pd.read_csv(f))

# sample with frac=1 shuffles the entire dataframe, so we are plotting points
# randomly, and the colour patterns are not biased by the order we loaded the data
data = pd.concat(tmp).sample(frac=1)

data = data.loc[data['Area'] > 100000000]

area = data['Area']
length = data['FlowLength']
AI = data['ai_mean']

x = area
y = length

plt.scatter(x, y, c=AI, s=0.2, alpha=1)
cbar = plt.colorbar(label='Aridity Index', ticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
plt.clim(0, 1)
cbar.ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '>1'])


ax = plt.gca()
ax.set_yscale('log')
ax.set_xscale('log')

popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])

plt.plot(x, hack(x, popt[0], popt[1]), 'r-')


info_label = 'h={}\n$r^2$={}'.format(round(popt[0], 3), round(r2_score(y, hack(x, popt[0], popt[1])), 2))
plt.text(408000000, 1500, info_label)


plt.xlim(23430968, 2624323291)
plt.ylim(353, 462600)

plt.ylabel('Channel Length ($m$)')
plt.xlabel('Drainage Area ($m^2$)')

plt.tight_layout()
plt.savefig('task-3c.png')
