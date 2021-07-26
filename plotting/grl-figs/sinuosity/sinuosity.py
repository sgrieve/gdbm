import math
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import seaborn as sns
from seaborn.categorical import _ViolinPlotter

class MyVPlot(_ViolinPlotter):
    '''
    https://gist.github.com/mpharrigan/a4375afa71d560dbdf3a0d96552a1cd5
    '''
    def draw_quartiles(self, ax, data, support, density, center, split=False):
        """Draw the quartiles as lines at width of density."""
        q25, q50, q75 = np.percentile(data, [25, 50, 75])
        self.draw_to_density(ax, center, q50, support, density, split,
                             linewidth=self.linewidth*0.75, )


def my_violinplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
                  bw="scott", cut=2, scale="area", scale_hue=True, gridsize=100,
                  width=.8, inner="box", split=False, dodge=True, orient=None,
                  linewidth=None, color=None, palette=None, saturation=.75,
                  ax=None, **kwargs):
    plotter = MyVPlot(x, y, hue, data, order, hue_order,
                      bw, cut, scale, scale_hue, gridsize,
                      width, inner, split, dodge, orient, linewidth,
                      color, palette, saturation)
    if ax is None:
        ax = plt.gca()

    plotter.plot(ax)
    return ax


def get_n(data, i):
    return '\n $n={}$'.format(len(data[i]))

reach = 300
zones = ['A', 'B', 'C', 'D',]
plots = []

for i, z in enumerate(zones):
    x = []
    files = glob('../../../Results/{0}*/{0}*_river*.csv'.format(z))
    print(z)
    for filename in files:
        data = np.genfromtxt(filename, delimiter=',')
        data_length = len(data[:,1])
        if data_length > reach:
            for start, end in zip(range(0, data_length - 1, reach), range(reach, data_length, reach)):
                length = np.abs(data[:, 5] - np.max(data[:, 5]))

                top = (data[start][0], data[start][1])
                bottom = (data[end][0], data[end][1])

                flow_length = data[end, 5] - data[start, 5]
                euc_dist = math.hypot(bottom[0] - top[0], bottom[1] - top[1]) * 30
                x.append(flow_length/euc_dist)
    plots.append(x)

plots.append(sum(plots, []))

ax = my_violinplot(data=plots, inner='quartile', palette=['b','r','g','purple','grey'])

# Manually set the median line to white to match the other violin plots in the supplement
for i in range(5):
    ax.lines[i].set_color('w')

plt.plot([3.6, 3.6], [0, 7], 'k--')
plt.ylim(0,7)




labels = ['Tropical{}'.format(get_n(plots, 0)),
          'Arid{}'.format(get_n(plots, 1)),
          'Temperate{}'.format(get_n(plots, 2)),
          'Cold{}'.format(get_n(plots, 3)),
          'All{}'.format(get_n(plots, 4))]

plt.xticks([0, 1, 2, 3, 4], labels)
plt.ylabel('Sinuosity ratio')

plt.savefig('Sinuosity.eps')
plt.savefig('Sinuosity.png')
