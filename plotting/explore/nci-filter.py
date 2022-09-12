import pandas as pd
from os.path import basename

zones = ['../../Results/Af_data.csv', '../../Results/Am_data.csv',
         '../../Results/Dw_data.csv', '../../Results/BSh_data.csv',
         '../../Results/C_data.csv', '../../Results/B_data.csv',
         '../../Results/BWk_data.csv', '../../Results/D_data.csv',
         '../../Results/Cw_data.csv', '../../Results/BWh_data.csv',
         '../../Results/Cf_data.csv', '../../Results/BSk_data.csv',
         '../../Results/A_data.csv', '../../Results/Cs_data.csv',
         '../../Results/Ds_data.csv', '../../Results/Df_data.csv',
         '../../Results/Aw_data.csv']

params = ['straightness_proportion', 'pit_length_proportion']
values = [0.01]

for value in values:
    for filename in zones:
        print(filename)
        data = pd.read_csv(filename)

        nci_s = data.where((data[params[0]] < value) & (data[params[1]] < value))
        removed = nci_s.dropna()
        removed.to_csv('{}_filtered.csv'.format(filename[:-4]), index=False)
