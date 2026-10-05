import numpy as np
import pickle
from matplotlib import pyplot as plt
from gmmtools import *
from StressTransform import *

import matplotlib as mpl

mpl.rcParams.update({
    # --- Font ---
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],  # or Arial if available

})

#load the created gmm's
with open("./fitted-models/gmm_stress.pkl", "rb") as f:
    gmm_stress = pickle.load(f)
    
with open("./fitted-models/stress_transform.pkl", "rb") as f:
    stress_transform = pickle.load(f)
    
gmm_stress.reduce(condition=['DBP','SBP', 'Area', 'Dist'])

t = np.linspace(0,1,10)

def plot(mean, high, low, ax, ltype, alpha):
    ax[0].plot(t,mean[0,:10],color='red', linestyle=ltype)
    ax[0].fill_between(t,high[0,:10],low[0,:10],color='red', alpha=alpha)
    ax[1].plot(t,mean[0,10:20],color='blue', linestyle=ltype)
    ax[1].fill_between(t,high[0,10:20],low[0,10:20],color='blue', alpha=alpha)
    ax[2].plot(t,mean[0,20:],color='green', linestyle=ltype)
    ax[2].fill_between(t,high[0,20:],low[0,20:],color='green', alpha=alpha)
    #ax.set_ylabel('Normalised stress [-]')
    #ax.set_xlabel('Normalised thickness [-]')

def plot3(axs,vals):
    dbp, sbp, D_dias, dist = vals 
    A_dias = np.pi*(D_dias/2)**2
    rad_dias = np.sqrt(A_dias/np.pi)
    A_sys = A_dias*(dist*1e-3*(sbp-dbp) + 1)
    rad_sys = np.sqrt(A_sys/np.pi)

    gmm_stress.reduce(condition=['DBP','SBP', 'Area', 'Dist'],x_cond=[dbp, sbp, A_dias, dist])
    dbp *= 0.1333224
    sbp *= 0.1333224
    dbp, sbp = 1, 1

    m, high, low = gmm_stress.mean_std(reduced=True)
    s1_mean_cond, s2_mean_cond = stress_transform.i_transform(m)
    high1, high2 = stress_transform.i_transform(high)
    low1, low2 = stress_transform.i_transform(low)
    #if high is less than low, switch
    switch = high1<low1
    high1[switch], low1[switch] = low1[switch], high1[switch]

    switch = high2<low2
    high2[switch], low2[switch] = low2[switch], high2[switch]

    t_low,t_high = 1.6, 3.32
    t_mean = (t_low+t_high)*0.5
    #laplace law calculation
    def laplace_stress(p,r,t_low,t_high):
        s1 = p*(r+t_low/2.)/t_low
        s2 = p*(r+t_high/2.)/t_high
        return (s1+s2)/2., s1, s2
    lap_s1_mean, lap_s1_low, lap_s1_high = laplace_stress(dbp, rad_dias, t_low, t_high)
    lap_s2_mean, lap_s2_low, lap_s2_high = laplace_stress(sbp, rad_sys, t_low, t_high)
    plot(s1_mean_cond*dbp,high1*dbp,low1*dbp,axs,'--', 0.2)
    plot(s2_mean_cond*sbp,high2*sbp,low2*sbp,axs,'-', 0.4)
    axs[0].tick_params(top=True, right=True, direction='in')
    axs[1].tick_params(top=True, right=True, direction='in')
    axs[2].tick_params(top=True, right=True, direction='in')


fig, axs4 = plt.subplots(4,3, figsize=(9,10*0.8), layout="constrained", sharex=True, sharey='col')

all_vals = [[65, 130, 35, 2],
            [80, 130, 40, 3] ,
            [55, 120, 30, 4],
            [75, 150, 30, 1]]
#all_vals = [[80, 120, 30, 2.5],
#            [80, 140, 20, 2.5] ,
#            [80, 120, 40, 3.5],
#            [80, 120, 40, 1]]

for axs,vals in zip(axs4,all_vals):
    plot3(axs,vals)

from matplotlib.ticker import AutoMinorLocator, MultipleLocator
for ax in axs4[:,0]:
    ax.set_ylabel('Normalised stress [-]')
    ax.set_yticks([-1,0])
    #ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.tick_params(which='both',top=True, right=True, direction='in')
for ax in axs4[:,1]:
    ax.set_ylim(0,100)
for ax in axs4[-1]:
    ax.set_xlabel('Normalised position [-]')
    #ax.set_xlim(15,45)
    #ax.set_ylim(0,9)

import string

labels = list(string.ascii_lowercase)

for i, ax in enumerate(axs4[:,0]):
    ax.text(0.02, 0.95, f"({labels[i]})",
            transform=ax.transAxes,
            fontsize=12,
            va='top', ha='left')

# get figure coordinates of first row axes
fig.canvas.draw()  # ensure positions are updated

col_centers = []
for j in range(axs4.shape[1]):
    pos = axs4[0, j].get_position()
    x_center = 0.5 * (pos.x0 + pos.x1)
    col_centers.append(x_center)

# --- Column titles (second row) ---
col_titles = ["Radial", "Circumferential", "Longitudinal"]

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

plt.savefig('stresses-grid2.pdf', bbox_inches='tight')
plt.close()
