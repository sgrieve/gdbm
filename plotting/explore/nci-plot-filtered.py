import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

zones = ['a.csv', 'b.csv', 'c.csv', 'd.csv']
labels = {'a': 'Tropical', 'b': 'Arid', 'c': 'Temperate', 'd': 'Cold'}

params = ['straightness_proportion', 'pit_length_proportion']
values = [0.01, 0.005]

for param in params:
    for value in values:
        count = 0
        for filename in zones:
            data = pd.read_csv(filename)

            nci_s = data.where(data[param] < value)['NCI']
            sns.kdeplot(nci_s.dropna(), label=labels[filename[0]], shade=True)

            count += len(nci_s.dropna())

        plt.xlabel('NCI')
        plt.ylabel('Density')
        plt.title('{} < {}% (n={})'.format(param.title().replace('_',' '), value * 100, count))
        plt.legend()
        plt.savefig('nci-data-{}-{}.png'.format(param, value * 100))
        plt.clf()
