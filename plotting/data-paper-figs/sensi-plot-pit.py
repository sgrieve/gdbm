import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

zones = ['../../Results/A_data.csv', '../../Results/B_data.csv',
         '../../Results/C_data.csv', '../../Results/D_data.csv']

titles = ['Tropical', 'Arid', 'Temperate', 'Cold']

plt.rcParams['font.family'] = 'sans-serif'


plt.subplot(2, 4, 1)

fig = plt.gcf()

fig.set_size_inches(6.4, 9.6)

for i, zone in enumerate(zones, start=1):
    plt.subplot(2, 4, i)
    full = pd.read_csv(zone)

    pc1 = full['NCI'].where(full['pit_length_proportion'] < 1)
    pc01 = full['NCI'].where(full['pit_length_proportion'] < 0.005)
    pc001 = full['NCI'].where(full['pit_length_proportion'] < 0.001)

    data = {'100': pc1, '0.5': pc1, '0.1': pc001}
    df = pd.DataFrame(data)

    v = sns.violinplot(data=df, inner=None, cut=0, bw=0.1, fontsize=4)
    v.set_xticklabels(v.get_xticklabels())

    for j,l in enumerate(df):
        plt.hlines(np.nanmedian(df[l]), j-0.5, j+0.5, color='w', linewidth=1.25)

    ax = plt.gca()
    if i > 1:
        ax.set_yticklabels([])
        plt.yticks([])
        sns.despine(left=True, bottom=False, right=True, ax=ax)
    else:
        plt.ylabel('NCI', size=12)
        sns.despine(left=False, bottom=False, right=True, ax=ax)

    plt.xlabel(' ', size=12)

    plt.title(titles[i - 1], size=12)


# ---------------------------------------------

for i, zone in enumerate(zones, start=1):
    plt.subplot(2, 4, 4+i)
    full = pd.read_csv(zone)

    pc1 = full['NCI'].where(full['straightness_proportion'] < 1)
    pc01 = full['NCI'].where(full['straightness_proportion'] < 0.005)
    pc001 = full['NCI'].where(full['straightness_proportion'] < 0.001)

    data = {'100': pc1, '0.5': pc1, '0.1': pc001}
    df = pd.DataFrame(data)

    v = sns.violinplot(data=df, inner=None, cut=0, bw=0.1, fontsize=4)
    v.set_xticklabels(v.get_xticklabels())

    for j,l in enumerate(df):
        plt.hlines(np.nanmedian(df[l]), j-0.5, j+0.5, color='w', linewidth=1.25)

    ax = plt.gca()
    if i > 1:
        ax.set_yticklabels([])
        plt.yticks([])
        sns.despine(left=True, bottom=False, right=True, ax=ax)
    else:
        plt.ylabel('NCI', size=12)
        sns.despine(left=False, bottom=False, right=True, ax=ax)

    plt.xlabel(' ', size=12)


plt.gcf().text(0.53, 0.49, 'Pit proportion (%)', ha='center', size=12)
plt.gcf().text(0.53, 0.02, 'Straightness proportion (%)', ha='center', size=12)


plt.gcf().text(0.05, 0.97, 'a', ha='center', size=14)
plt.gcf().text(0.05, 0.49, 'b', ha='center', size=14)

plt.tight_layout()
plt.savefig('sensi-pit.png')
plt.savefig('sensi-pit.pdf')
