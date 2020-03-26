#!/home/will/.pyenv/shims/python

from dice import roll
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import PercentFormatter

roll_to_test = 'd20'
num_rolls = 1000
fig, axs = plt.subplots(1, 2, constrained_layout=True)
fig.suptitle('{} Rolls of {}'.format(num_rolls, roll_to_test))
N = [0,0]
bins = [0,0]
patches = [0,0]
fracs = [0,0]
print("Beginning first roll...")
rolls = np.array(roll('{{{},{}}}'.format(roll_to_test, num_rolls)))
print("Done with first roll!")
d = np.diff(np.unique(rolls)).min()
left_of_first_bin = rolls.min() - float(d)/2
right_of_last_bin = rolls.max() + float(d)/2
plt.ion()
while True:
    for i in (0, 1):
        axs[i].cla()
    axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
    axs[0].set_ylabel('Occurences')
    axs[1].set_ylabel('Percent of Occurences')
    locator = MaxNLocator(integer=True, nbins=21)
    for i in (0, 1):
        axs[i].xaxis.set_major_locator(locator)
        axs[i].set_xlabel('Roll')
    N[0], bins[0], patches[0] = axs[0].hist(rolls,
        np.arange(left_of_first_bin, right_of_last_bin + d, d))
    N[1], bins[1], patches[1] = axs[1].hist(rolls,
        np.arange(left_of_first_bin, right_of_last_bin + d, d), density=True)
    for i in (0, 1):
        fracs[i] = N[i] / N[i].max()
        norm = colors.Normalize(fracs[i].min(), fracs[i].max())
        for frac, patch in zip(fracs[i], patches[i]):
            color = plt.cm.viridis(norm(frac))
            patch.set_facecolor(color)
    print("Drawing plot...")
    plt.pause(0.0001)
    print("Generating more data...")
    rolls = np.array(roll('{{{},{}}}'.format(roll_to_test, num_rolls)))
    print("Done generating data!")
    input("Press enter to plot new data...")
