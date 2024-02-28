import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

from pytablewriter import MarkdownTableWriter

def hack(x, k):
    return k * (x ** 0.531)

koppen_zones = ['Af','Am','Aw','BWh','BWk','BSh','BSk','Cs','Cw','Cf','Ds','Dw','Df']

table = []

for zone in koppen_zones:

    data = pd.read_csv('{}_data.csv'.format(zone))

    area = data['Area']
    length = data['FlowLength']

    x = area
    y = length

    popt, pcov = curve_fit(hack, x, y, bounds=([0.9, 4]), p0=[1.4])


    h = 0.531
    c = round(popt[0], 3)
    r2 = round(r2_score(y, hack(x, popt[0])), 2)

    table.append([zone, h, c, r2])


writer = MarkdownTableWriter(table_name='Koppen Zone c values with fixed h',
                             headers=['Koppen Zone', 'h', 'c', 'R-squared'],
                             value_matrix=table)

writer.dump('task-5a.md')
