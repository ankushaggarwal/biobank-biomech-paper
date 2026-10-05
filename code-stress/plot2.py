import numpy as np
from gmmtools import *
import pickle
from StressTransform import *
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib as mpl
mpl.rcParams.update({
    # --- Font ---
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],  # or Arial if available
})

t = np.linspace(0,1,10)
def plot(mean, high, low, ax, ltype, alpha):
    ax[0].plot(t,mean[:10],color='red', linestyle=ltype)
    ax[0].fill_between(t,high[:10],low[:10],color='red', alpha=alpha)
    ax[1].plot(t,mean[10:20],color='blue', linestyle=ltype)
    ax[1].fill_between(t,high[10:20],low[10:20],color='blue', alpha=alpha)
    ax[2].plot(t,mean[20:],color='green', linestyle=ltype)
    ax[2].fill_between(t,high[20:],low[20:],color='green', alpha=alpha)
    #ax.set_ylabel('Normalised stress [-]')
    #ax.set_xlabel('Normalised thickness [-]')

def plot3(axs):
    #calculate and plot the stresses for the conditioned values
    m,high,low = gmm_stress.mean_std(reduced=True)
    mean1, mean2 = stress_transform.i_transform(m)
    high1, high2 = stress_transform.i_transform(high)
    low1, low2 = stress_transform.i_transform(low)

    mean1 = mean1.flatten()
    mean2 = mean2.flatten()
    low1 = low1.flatten()
    high1 = high1.flatten()
    low2 = low2.flatten()
    high2 = high2.flatten()

    #if high is less than low, switch
    switch = high1<low1
    high1[switch], low1[switch] = low1[switch], high1[switch]

    switch = high2<low2
    high2[switch], low2[switch] = low2[switch], high2[switch]

    plot(mean1,high1,low1,axs,'--', 0.2)
    plot(mean2,high2,low2,axs,'-', 0.4)
    axs[0].tick_params(top=True, right=True, direction='in')
    axs[1].tick_params(top=True, right=True, direction='in')
    axs[2].tick_params(top=True, right=True, direction='in')

def plot_settings(fname):
    fig,axs = plt.subplots(1,3, figsize=(9,3*0.8), layout="constrained", sharex = True)
    plot3(axs)
    from matplotlib.ticker import AutoMinorLocator, MultipleLocator
    axs[0].set_ylabel('Noramlised stress [-]')
    axs[0].set_yticks([-1,0])
    #ax.yaxis.set_minor_locator(MultipleLocator(5))
    axs[0].yaxis.set_minor_locator(AutoMinorLocator(5))
    axs[0].tick_params(which='both',top=True, right=True, direction='in')
    #ax.set_ylim(0,100)
    for ax in axs:
        ax.set_xlabel('Normalised position [-]')
        #ax.set_xlim(15,45)
        #ax.set_ylim(0,9)

    # get figure coordinates of first row axes
    fig.canvas.draw()  # ensure positions are updated

    col_centers = []
    for j in range(3):
        pos = axs[j].get_position()
        x_center = 0.5 * (pos.x0 + pos.x1)
        col_centers.append(x_center)

    # --- Column titles (second row) ---
    col_titles = ["Radial", "Circumferential", "Longitudinal"]

    for x, title in zip(col_centers, col_titles):
        fig.text(x, 1.065, title, ha='center', va='top', fontsize=12)

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
        bbox_to_anchor=(0.5, -0.15)  # adjust vertical position
    )
    #plt.show()
    plt.savefig(fname, bbox_inches='tight')
    plt.close()

with open("./fitted-models/gmm_stress.pkl", "rb") as f:
    gmm_stress = pickle.load(f)
    
with open("./fitted-models/stress_transform.pkl", "rb") as f:
    stress_transform = pickle.load(f)
    
gmm_stress.reduce(condition=['DBP','PP', 'Area', 'Dist'])
plot_settings('stresses_conditional.pdf')

gmm_stress.reduce(marginalise=['DBP','PP', 'Area', 'Dist'])
plot_settings('stresses_marginal.pdf')
