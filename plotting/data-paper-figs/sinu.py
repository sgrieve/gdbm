import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


def reject_outliers(data, m = 35):
    '''
    https://stackoverflow.com/a/16562028/1627162
    m==3.5 removes 0.05% of the data
    m==35 removes ~0.01% of the data
    '''
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0
    return data[s<m]

zones = ['A-sinu-data.csv', 'B-sinu-data.csv',
         'C-sinu-data.csv', 'D-sinu-data.csv']

titles = ['All', 'Tropical', 'Arid', 'Temperate', 'Cold']

plt.rcParams['font.family'] = 'sans-serif'

data = {}
data['All'] = []

for i, zone in enumerate(zones, start=1):
    full = pd.read_csv(zone, names=['fl', 'ec', 'r'])

    data[titles[i]] = reject_outliers(full['r'])
    data['All'] += (reject_outliers(full['r']).tolist())

data_pad = {k:np.pad(v, pad_width=(0,len(data['All'])-len(v),), mode='constant', constant_values=np.nan) for k,v in data.items()}
df = pd.DataFrame(data_pad)

v = sns.violinplot(data=df, inner=None, cut=0, bw=0.1, fontsize=4)
v.set_xticklabels(v.get_xticklabels())

for j,l in enumerate(df):
    plt.hlines(np.nanmedian(df[l]), j-0.5, j+0.5, color='w', linewidth=1.25)

plt.plot([0.5, 0.5], [0, 6], 'k--')
plt.ylim(0.5, 5.5)
plt.xlim(-0.45, 4.5)

plt.ylabel('Sinuosity')
plt.tight_layout()

plt.savefig('sinuosity.png')
plt.savefig('sinuosity.pdf')
