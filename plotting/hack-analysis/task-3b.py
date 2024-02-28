import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

from pytablewriter import MarkdownTableWriter

def hack(x, h, k):
    return k * (x ** h)

koppen_zones = ['Af','Am','Aw','BWh','BWk','BSh','BSk','Cs','Cw','Cf','Ds','Dw','Df']

table = []

for zone in koppen_zones:

    data = pd.read_csv('{}_data.csv'.format(zone))

    data = data.loc[data['Area'] > 100000000]

    area = data['Area']
    length = data['FlowLength']

    x = area
    y = length

    popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])


    h = round(popt[0], 3)
    c = round(popt[1], 3)
    r2 = round(r2_score(y, hack(x, popt[0], popt[1])), 2)

    table.append([zone, h, c, r2])


writer = MarkdownTableWriter(table_name='Koppen Zone h values (large basins only)',
                             headers=['Koppen Zone', 'h', 'c', 'R-squared'],
                             value_matrix=table)

writer.dump('task-3b.md')
