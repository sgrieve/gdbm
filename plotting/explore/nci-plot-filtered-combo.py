import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import basename

zones = ['../../Results/A_data.csv', '../../Results/B_data.csv',
         '../../Results/C_data.csv', '../../Results/D_data.csv']
labels = {'A_data.csv': 'Tropical', 'B_data.csv': 'Arid',
          'C_data.csv': 'Temperate', 'D_data.csv': 'Cold'}

params = ['straightness_proportion', 'pit_length_proportion']
values = [0.01, 0.005]

for value in values:
    count = 0
    for filename in zones:
        data = pd.read_csv(filename)

        nci_s = data.where((data[params[0]] < value) & (data[params[1]] < value))['NCI']
        sns.kdeplot(nci_s.dropna(), label=labels[basename(filename)], shade=True)

        count += len(nci_s.dropna())

    plt.xlabel('NCI')
    plt.ylabel('Density')
    plt.title('{} and {} < {}% (n={})'.format(params[0].title().replace('_',' '), params[1].title().replace('_',' '), value * 100, count))
    plt.legend()
    plt.savefig('nci-data-combo-{}.png'.format(value * 100))
    plt.clf()
