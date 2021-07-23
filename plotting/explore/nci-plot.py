import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import basename

zones = ['../../Results/A_data.csv', '../../Results/B_data.csv',
         '../../Results/C_data.csv', '../../Results/D_data.csv']
labels = {'A_data.csv': 'Tropical', 'B_data.csv': 'Arid',
          'C_data.csv': 'Temperate', 'D_data.csv': 'Cold'}

count = 0
for filename in zones:
    data = pd.read_csv(filename)
    sns.kdeplot(data['NCI'], label=labels[basename(filename)], shade=True)
    count+= len(data['NCI'])

plt.xlabel('NCI')
plt.ylabel('Density')
plt.title('Full Data (n={})'.format(count))
plt.legend()
plt.savefig('full-data.png')
