import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from glob import glob

from pytablewriter import MarkdownTableWriter


def hack(x, h, k):
    return k * (x ** h)


files = glob('*_data.csv')

tmp = []
for f in files:
    tmp.append(pd.read_csv(f))

data = pd.concat(tmp)

lowers = [0.00, 0.03, 0.20, 0.50, 0.65]
uppers = [0.03, 0.20, 0.50, 0.65, data['ai_mean'].max()]
ai_classes = ['Hyper-arid', 'Arid', 'Semi-arid', 'Dry sub-humid', 'Humid']
table = []

for i, ai_class in enumerate(ai_classes):

    data_slice = data[data['ai_mean'].between(lowers[i], uppers[i], inclusive='right')]

    area = data_slice['Area']
    length = data_slice['FlowLength']

    x = area
    y = length

    popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])

    h = round(popt[0], 3)
    c = round(popt[1], 3)
    r2 = round(r2_score(y, hack(x, popt[0], popt[1])), 2)

    table.append([ai_class, h, c, r2])


writer = MarkdownTableWriter(table_name='Aridity Index h values',
                         headers=['AI Category', 'h', 'c', 'R-squared'],
                         value_matrix=table)

writer.dump('task-2b.md')
