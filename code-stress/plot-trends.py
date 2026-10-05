import numpy as np
from gmmtools import *
import pickle
from StressTransform import *
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import matplotlib as mpl
mpl.rcParams.update({
    # --- Font ---
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],  # or Arial if available
})

with open("trend-results.pkl", "rb") as f:
    results = pickle.load(f)
    
def plot3(xlabel,axs, val, sc1, sl1, sc2, sl2):
    #axs[0].plot(sc1,sl1,'--',color='k')
    #axs[0].plot(sc2,sl2,'-',color='k')
    axs[0].plot(val,sc1,'--',color='blue')
    axs[0].plot(val,sc2,'-',color='blue')
    axs[1].plot(val,sl1,'--',color='green')
    axs[1].plot(val,sl2,'-',color='green')
    axs[0].set_ylabel('Maximum stress [-]')
    axs[0].set_xlabel(xlabel)
    axs[1].set_xlabel(xlabel)
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(2))
    axs[1].yaxis.set_minor_locator(AutoMinorLocator(2))
    axs[0].tick_params(top=True, right=True, direction='in')
    axs[1].tick_params(top=True, right=True, direction='in')
    axs[0].tick_params(which='minor', right=True, direction='in')
    axs[1].tick_params(which='minor', right=True, direction='in')



fig, axs = plt.subplots(4,2,figsize=(7,8),layout="constrained",sharex='row',sharey='col')

plot3('DBP [mmHg]',axs[0],*results['dbp'])
plot3('SBP [mmHg]', axs[1],*results['sbp'])
plot3('Diameter [mm]', axs[2],*results['dia'])
plot3('Distensibility [$10^{-3}$ mmHg$^{-1}$]', axs[3],*results['dist'])
axs[-1,0].set_ylim(bottom=0)
axs[-1,1].set_ylim(bottom=0)

import string

labels = list(string.ascii_lowercase)

for i, ax in enumerate(axs[:,0]):
    ax.text(0.02, 0.95, f"({labels[i]})",
            transform=ax.transAxes,
            fontsize=12,
            va='top', ha='left')


# get figure coordinates of first row axes
fig.canvas.draw()  # ensure positions are updated

col_centers = []
for j in range(axs.shape[1]):
    pos = axs[0, j].get_position()
    x_center = 0.5 * (pos.x0 + pos.x1)
    col_centers.append(x_center)

# --- Column titles (second row) ---
col_titles = ["Circumferential", "Longitudinal"]

for x, title in zip(col_centers, col_titles):
    fig.text(x, 1.02, title, ha='center', va='top', fontsize=12)

from matplotlib.lines import Line2D

# Create dummy handles (no data needed, just style)
legend_elements = [
    Line2D([0], [0], linestyle = '--', color='black', label='Diastolic'),
    Line2D([0], [0], linestyle = '-', color='black', label='Systolic'),
]

# Create legend from dummy handles
#legend = ax.legend(handles=legend_elements, loc='center', frameon=True, ncol=2)

fig.legend(
    handles=legend_elements,
    loc='lower center',
    ncol=2,                      # spread horizontally
    frameon=True,
    bbox_to_anchor=(0.5, -0.05)  # adjust vertical position
)

plt.savefig('stress-trends.pdf', bbox_inches='tight')
#plt.savefig('stress-trends.png', dpi=300, bbox_inches='tight')
#plt.show()
plt.close()
