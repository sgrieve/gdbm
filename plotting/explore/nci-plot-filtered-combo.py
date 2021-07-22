import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

zones = ['a.csv', 'b.csv', 'c.csv', 'd.csv']
labels = {'a': 'Tropical', 'b': 'Arid', 'c': 'Temperate', 'd': 'Cold'}

params = ['straightness_proportion', 'pit_length_proportion']
values = [0.01, 0.005]

for value in values:
    count = 0
    for filename in zones:
        data = pd.read_csv(filename)

        nci_s = data.where((data[params[0]] < value) & (data[params[1]] < value))['NCI']
        sns.kdeplot(nci_s.dropna(), label=labels[filename[0]], shade=True)

        count += len(nci_s.dropna())

    plt.xlabel('NCI')
    plt.ylabel('Density')
    plt.title('{} and {} < {}% (n={})'.format(params[0].title().replace('_',' '), params[1].title().replace('_',' '), value * 100, count))
    plt.legend()
    plt.savefig('nci-data-combo-{}.png'.format(value * 100))
    plt.clf()
