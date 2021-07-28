import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

zones = ['../../Results/{}A_data.csv', '../../Results/{}B_data.csv',
         '../../Results/{}C_data.csv', '../../Results/{}D_data.csv']

titles = ['Tropical', 'Arid', 'Temperate', 'Cold']

plt.figure(figsize=[6.4, 7.2])
plt.rcParams['font.family'] = 'sans-serif'


for i, zone in enumerate(zones, start=1):

    plt.subplot(2, 4, i)

    low = pd.read_csv(zone.format('sensi-l/'))
    full = pd.read_csv(zone.format(''))
    high = pd.read_csv(zone.format('sensi-h/'))

    # need to pad the data with nans so it is the same shape
    # https://stackoverflow.com/a/62299349/1627162
    maxsize = len(full)
    data = {'{}'.format(round(22.5 * 0.75, 1)): low['FlowLength'],
            '{}'.format(22.5): full['FlowLength'],
            '{}'.format(round(22.5 * 1.25, 1)): high['FlowLength']}
    data_pad = {k:np.pad(v, pad_width=(0, maxsize-v.size,), mode='constant', constant_values=np.nan) for k, v in data.items()}

    df = pd.DataFrame(data_pad)

    sns.violinplot(data=df, inner=None, cut=0, bw=0.1)

    for j,l in enumerate(df):
        plt.hlines(np.nanmedian(df[l]), j-0.5, j+0.5, color='w', linewidth=1.25)

    plt.ylim(0, 390000)

    ax = plt.gca()
    a = ax.get_yticks().tolist()

    a = [round(q / 1000) for q in a]
    ax.set_yticklabels(a)

    plt.title(titles[i - 1], size=12)

    if i > 1:
        ax.set_yticklabels([])
        plt.yticks([])
        sns.despine(left=True, bottom=False, right=True, ax=ax)
    else:
        plt.ylabel('Channel length (km)', size=12)
        sns.despine(left=False, bottom=False, right=True, ax=ax)

    ax.set_xticklabels([])
    plt.xticks([])

for i, zone in enumerate(zones, start=5):
    plt.subplot(2, 4, i)
    low = pd.read_csv(zone.format('sensi-l/'))
    full = pd.read_csv(zone.format(''))
    high = pd.read_csv(zone.format('sensi-h/'))

    maxsize = len(full)
    data = {'{}'.format(round(22.5 * 0.75, 1)): low['NCI'],
            '{}'.format(22.5): full['NCI'],
            '{}'.format(round(22.5 * 1.25, 1)): high['NCI']}
    data_pad = {k:np.pad(v, pad_width=(0,maxsize-v.size,), mode='constant', constant_values=np.nan) for k,v in data.items()}

    df = pd.DataFrame(data_pad)

    sns.violinplot(data=df, inner=None, cut=0, bw=0.1)

    for j,l in enumerate(df):
        plt.hlines(np.nanmedian(df[l]), j-0.5, j+0.5, color='w', linewidth=1.25)

    ax = plt.gca()
    if i > 5:
        ax.set_yticklabels([])
        plt.yticks([])
        sns.despine(left=True, bottom=False, right=True, ax=ax)
    else:
        plt.ylabel('NCI', size=12)
        plt.xlabel('\t\t\t\t\t\t\t\t\tDrainage area ($km^2$)', size=12)
        sns.despine(left=False, bottom=False, right=True, ax=ax)

plt.tight_layout()

plt.gcf().text(0.1, 0.94, 'a', ha='center', size=14, weight='bold')
plt.gcf().text(0.1, 0.48, 'b', ha='center', size=14, weight='bold')

plt.savefig('sensi.png')
plt.savefig('sensi.pdf')
