import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from glob import glob
from sklearn.metrics import r2_score


def hack(x, h, k):
    return k * (x ** h)


files = glob('*_data.csv')

tmp = []
for f in files:
    tmp.append(pd.read_csv(f))

data = pd.concat(tmp)

data = data.loc[data['pit_length_proportion']  < 0.01]
data = data.loc[data['straightness_proportion']  < 0.01]


x = data['Area']
y = data['FlowLength']
gc = data['Gravelius_coefficient']

popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])
print('h', round(popt[0],3))
print('n', len(x))
print('median A', round((np.median(x) / 1000000),1))
print('median L', round((np.median(y) / 1000),1))
print('median GC', round((np.median(gc)),3))


# koppen_zones = ['A', 'C', 'D', 'B']
# titles = ['Tropical', 'Temperate', 'Cold', 'Arid']
#
# # Koppen zone filtering
# for i in range(4):
#     print('\n', koppen_zones[i], titles[i])
#     selection = data[data['RiverName'].str.startswith(koppen_zones[i])]
#
#     x = selection['Area']
#     y = selection['FlowLength']
#     gc = selection['Gravelius_coefficient']
#
#     popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])
#     print('h', round(popt[0],3))
#     print('n', len(x))
#     print('median A', round((np.median(x) / 1000000),1))
#     print('median L', round((np.median(y) / 1000),1))
#     print('median GC', round((np.median(gc)),3))


hyper_arid = data.loc[(data['ai_median'] <= 0.03)]
arid = data.loc[(data['ai_median'] > 0.03) & (data['ai_median'] <= 0.2)]
semi_arid = data.loc[(data['ai_median'] > 0.2) & (data['ai_median'] <= 0.5)]
dry_sh = data.loc[(data['ai_median'] > 0.5) & (data['ai_median'] <= 0.65)]
humid = data.loc[(data['ai_median'] > 0.65)]

ai_classes = [hyper_arid, arid, semi_arid, dry_sh, humid]
ai_class_names = ["hyper_arid", "arid", "semi_arid", "dry_sh", "humid"]

for i, ai_class in enumerate(ai_classes):

    print('\n', ai_class_names[i])
    x = ai_class['Area']
    y = ai_class['FlowLength']
    gc = ai_class['Gravelius_coefficient']

    popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])
    print('n', len(x))
    print('median L', round((np.median(y) / 1000),1))
    print('median A', round((np.median(x) / 1000000),1))
    print('median GC', round((np.median(gc)),3))
    print('h', round(popt[0],3))
