import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

zones = ['a.csv', 'b.csv', 'c.csv', 'd.csv']
labels = {'a': 'Tropical', 'b': 'Arid', 'c': 'Temperate', 'd': 'Cold'}

count = 0
for filename in zones:
    data = pd.read_csv(filename)
    sns.kdeplot(data['NCI'], label=labels[filename[0]], shade=True)
    count+= len(data['NCI'])

plt.xlabel('NCI')
plt.ylabel('Density')
plt.title('Full Data (n={})'.format(count))
plt.legend()
plt.savefig('full-data.png')
