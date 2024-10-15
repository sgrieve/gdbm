import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from glob import glob
from sklearn.metrics import r2_score


def hack(x, h, k):
    return k * (x ** h)


koppen_zones = ['A', 'C', 'D', 'B']
titles = ['Tropical', 'Temperate', 'Cold', 'Arid']

filenames = ['HigherArea_data.csv', 'LowerArea_data.csv', 'onlyLGM_data.csv',
             'onlyTectonic_data.csv', 'removeErg.csv',
             'removeTectonic_data.csv', 'removeLGM_data.csv', 'small_data.csv']

filenames = ['HigherArea_data.csv', 'LowerArea_data.csv', 'onlyLGM_data.csv',
             'onlyTectonic_data.csv', 'removeErg.csv',
             'removeTectonic_data.csv', 'removeLGM_data.csv', 'small_data.csv']

for f in filenames:

    data = pd.read_csv(f)

    print('\n{}\n'.format(f))

    # Koppen zone filtering
    for i in range(4):

        selection = data[data['river_id'].str.startswith(koppen_zones[i])]

        x = selection['area']
        y = selection['total_leng']

        popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])
        print(koppen_zones[i], titles[i], round(popt[0],3))


    # Now need to repeat for aridity classes

    hyper_arid = data.loc[(data['AI_median'] <= 0.03)]
    arid = data.loc[(data['AI_median'] > 0.03) & (data['AI_median'] <= 0.2)]
    semi_arid = data.loc[(data['AI_median'] > 0.2) & (data['AI_median'] <= 0.5)]
    dry_sh = data.loc[(data['AI_median'] > 0.5) & (data['AI_median'] <= 0.65)]
    humid = data.loc[(data['AI_median'] > 0.65)]

    ai_classes = [hyper_arid, arid, semi_arid, dry_sh, humid]
    ai_class_names = ["hyper_arid", "arid", "semi_arid", "dry_sh", "humid"]

    for i, ai_class in enumerate(ai_classes):
        x = ai_class['area']
        y = ai_class['total_leng']

        popt, pcov = curve_fit(hack, x, y, bounds=([0.3, 1.3], [0.9, 4]), p0=[0.6, 1.4])
        print(ai_class_names[i], round(popt[0],3))
