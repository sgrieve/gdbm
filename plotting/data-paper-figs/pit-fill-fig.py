import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

data = '../../dems/11_0_deltas.csv'

plt.rcParams['font.family'] = 'sans-serif'

deltas = pd.read_csv(data)

pc = np.percentile(deltas['d'], 98)

plt.figure(figsize=(5.2, 3.9))

plt.hist(deltas['d'], bins=20, density=False, edgecolor='k', linewidth=0.5)
max_count = plt.gca().get_ylim()[1] + 100000  # Constant is to create headroom at top of plot

plt.vlines(pc, 0, max_count, linewidth=1, color='k', edgecolor='k', linestyle='--',label='98th percentile')

plt.xlabel('Vertical change (m)')
plt.ylabel('Density')

plt.yscale('log')
plt.xlim(0, 18)
plt.ylim(ymax=max_count)

plt.errorbar(x=7.25, y=100000, xerr=2.25, c='k', linewidth=0.5, capsize=4,
             capthick=0.5)

# Dummy data to make a cleaner legend
plt.plot([7.25, 7.8], [100000, 100000], c='k', linewidth=0.5,
         label='SRTM vertical error range')

plt.legend()

plt.tight_layout()


plt.savefig('pit-fill.pdf')
