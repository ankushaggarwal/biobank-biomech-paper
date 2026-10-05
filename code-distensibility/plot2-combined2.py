import pandas as pd
import pickle
from matplotlib import pyplot as plt
import numpy as np

import matplotlib as mpl

mpl.rcParams.update({
    # --- Font ---
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],  # or Arial if available

})

results_df = pd.read_pickle('results_df.pkl')
ages = np.linspace(45,80,21) #covers almost all of the range in the data
BSAs = np.linspace(1.2,2.8,21) #covers almost all of the range in the data
DBPs = np.linspace(50,90,21) #covers almost all of the range in the data
SBPs = np.linspace(90,130,21) #covers almost all of the range in the data

area2dia = lambda a: np.sqrt(a/np.pi)*2
figsize = (4*3,2.67*4)
fig, axs = plt.subplots(4,3,figsize=figsize,layout="constrained")

# add space at the bottom for the legend
#fig.subplots_adjust(bottom=0.12)

def plot_mix(line, cross, contour, color, ltype, ax):
    ax.plot(area2dia(line[:,0]), line[:,1], ltype, color=color)
    ax.plot(area2dia(cross[:,0]), cross[:,1], 'x', color=color)
    for x in [elem for sublist1 in contour for sublist2 in sublist1 for elem in sublist2]:
        ax.plot(x[:,0], x[:,1],ltype,color=color)

def plot4(i1,i2,i3,i4, ax):
    for i in [i1,i2,i3,i4]:
        line, cross, contour = results_df.loc[i,'line'], results_df.loc[i,'cross'], results_df.loc[i,'contour']
        if i==i1:
            plot_mix(line, cross, contour, 'blue', '-', ax)
        elif i==i2:
            plot_mix(line, cross, contour, 'red', '-', ax)
        elif i==i3:
            plot_mix(line, cross, contour, 'blue', '--', ax)
        elif i==i4:
            plot_mix(line, cross, contour, 'red', '--', ax)

    ax.tick_params(top=True, right=True, direction='in')
    ax.set_xlabel('Diameter [mm]')
    ax.set_ylabel(r'Distensibility [$10^{-3}$ mmHg$^{-1}$]')
    ax.set_xlim(left=15,right=45)
    ax.set_ylim(bottom=0, top=5.5)

def plot_vary(i1,i2,i3,i4,array,xlabel,ax,ax2):
    for i in [i1,i2,i3,i4]:
        line = results_df.loc[i,'line']
        if i==i1:
            ax.plot(array, area2dia(line[:,0]), '-', color = 'blue')
        elif i==i2:
            ax.plot(array, area2dia(line[:,0]), '-', color = 'red')
        elif i==i3:
            ax.plot(array, area2dia(line[:,0]), '--', color = 'blue')
        elif i==i4:
            ax.plot(array, area2dia(line[:,0]), '--', color = 'red')

    ax.tick_params(top=True, right=True, direction='in')
    ax2.tick_params(top=True, right=True, direction='in')
    ax.set_ylabel('Diameter [mm]')
    ax.set_ylim(bottom=18, top=38)
    #ax.set_xlim(left = np.min(array), right = np.max(array))
    ax.autoscale(enable=True, axis='x', tight=False)
    ax.set_xlabel(xlabel)
    #ax.yaxis.set_ticks_position('left')
    
    #twin axis for distensibility
    #ax2 = ax.twinx()
    for i in [i1,i2,i3,i4]:
        line = results_df.loc[i,'line']
        if i==i1:
            ax2.plot(array, line[:,1], '-' , color = 'blue')
        elif i==i2:
            ax2.plot(array, line[:,1], '-' , color = 'red')
        elif i==i3:
            ax2.plot(array, line[:,1], '--', color = 'blue')
        elif i==i4:
            ax2.plot(array, line[:,1], '--', color = 'red')

    ax2.set_ylabel(r'Distensibility [$10^{-3}$ mmHg$^{-1}$]')
    ax2.set_ylim(bottom=0, top=5.5)
    ax2.set_xlabel(xlabel)

####################################################################################################
# w.r.t. age
####################################################################################################
plot4(0,1,2,3,axs[0,0])
axs[0,0].annotate("",
             xy=(38, 1),
             xycoords='data',
             xytext=(32, 4),
             textcoords='data',
             arrowprops=dict(arrowstyle= '->',
                             lw=1.5,
                             ls='-')
           )
axs[0,0].annotate("Age",
             xy=(37, 2.8),
             xycoords='data',
             horizontalalignment="center",
            verticalalignment='top',
             textcoords='data',
           )

plot_vary(0,1,2,3, ages, 'Age [years]',axs[0,1],axs[0,2])
####################################################################################################
# w.r.t. BSA
####################################################################################################
plot4(4,5,6,7,axs[1,0])
axs[1,0].annotate("",
             xy=(38, 2.5),
             xycoords='data',
             xytext=(28, 2.7),
             textcoords='data',
             arrowprops=dict(arrowstyle= '->',
                             lw=1.5,
                             ls='-')
           )
axs[1,0].annotate("BSA",
             xy=(33, 3.2),
             xycoords='data',
             horizontalalignment="center",
            verticalalignment='top',
             textcoords='data',
           )

plot_vary(4,5,6,7, BSAs, 'BSA [m$^2$]',axs[1,1],axs[1,2])

####################################################################################################
# w.r.t. DBPs 
####################################################################################################
plot4(8,9,10,11,axs[2,0])
#plt.savefig('vary-DBP.pdf')
#plt.close()

axs[2,0].annotate("",
             xy=(35, 2.5),
             xycoords='data',
             xytext=(30, 2.5),
             textcoords='data',
             arrowprops=dict(arrowstyle= '<->',
                             lw=1.5,
                             ls='-')
           )
axs[2,0].annotate("DBP",
             xy=(32.5, 3.),
             xycoords='data',
             horizontalalignment="center",
            verticalalignment='top',
             textcoords='data',
           )
plot_vary(8,9,10,11, DBPs, 'DBP [mmHg]',axs[2,1],axs[2,2])

####################################################################################################
# w.r.t. SBPs 
####################################################################################################
plot4(12,13,14,15,axs[3,0])
#plt.savefig('vary-SBP.pdf')
#plt.close()

axs[3,0].annotate("",
             xy=(36.5, 1),
             xycoords='data',
             xytext=(36.5, 3.5),
             textcoords='data',
             arrowprops=dict(arrowstyle= '->',
                             lw=1.5,
                             ls='-')
           )
axs[3,0].annotate("SBP",
             xy=(38, 2.25),
             xycoords='data',
             horizontalalignment="center",
            verticalalignment='top',
             textcoords='data',
           )

plot_vary(12,13,14,15, SBPs, 'SBP [mmHg]',axs[3,1], axs[3,2])
#plt.close()
import string

labels = list(string.ascii_lowercase)

for i, ax in enumerate(axs[:,0]):
    ax.text(0.02, 0.95, f"({labels[i]})",
            transform=ax.transAxes,
            fontsize=12,
            va='top', ha='left')

from matplotlib.lines import Line2D

# Create dummy handles (no data needed, just style)
legend_elements = [
    Line2D([0], [0], color='blue', label='Females'),
    Line2D([0], [0], color='red', label='Males'),
    Line2D([0], [0], color='black', linestyle='-', label='Ascending'),
    Line2D([0], [0], color='black', linestyle='--', label='Descending'),
]

# Create legend from dummy handles
#legend = ax.legend(handles=legend_elements, loc='center', frameon=True, ncol=2)


fig.legend(
    handles=legend_elements,
    loc='lower center',
    ncol=2,                      # spread horizontally
    frameon=True,
    bbox_to_anchor=(0.5, -0.07)  # adjust vertical position
)

# Save
#fig.savefig("dummy_legend.pdf")

plt.savefig('combined-all2.pdf', bbox_inches='tight')
plt.close()
