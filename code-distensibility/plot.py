import numpy as np
import pickle
import pandas as pd
from scipy.stats import norm
from matplotlib import pyplot as plt
from gmmtools import *

#load the created gmm's
with open("../create-gmms/gmm_asc_mal.pkl", "rb") as f:
    mal_asc_gmm = pickle.load(f)
with open("../create-gmms/gmm_asc_fem.pkl", "rb") as f:
    fem_asc_gmm = pickle.load(f)
with open("../create-gmms/gmm_dsc_mal.pkl", "rb") as f:
    mal_dsc_gmm = pickle.load(f)
with open("../create-gmms/gmm_dsc_fem.pkl", "rb") as f:
    fem_dsc_gmm = pickle.load(f)

gmms = [fem_asc_gmm, mal_asc_gmm, fem_dsc_gmm, mal_dsc_gmm]

for gmm in gmms[:2]:
    #gmm.verbose = False
    gmm.reduce(condition=['Asc_D_Area'], marginalise = ['Age', 'Bod_Sur', 'DBP', 'SBP'])

for gmm in gmms[2:]:
    #gmm.verbose = False
    gmm.reduce(condition=['Dsc_D_Area'], marginalise = ['Age', 'Bod_Sur', 'DBP', 'SBP'])

def get_dist(gmm,diams):
    all_means, all_lows, all_highs = [], [], []
    for dia in diams:
        area = np.pi*dia**2/4.
        gmm.update_reduced_gmm(x_cond = area)
        m, h, l = gmm.mean_std(reduced=True)
        all_means.append(m[0])
        all_highs.append(h[0])
        all_lows.append(l[0])

    return all_means, all_highs, all_lows

figsize = (8, 3)
fig, ax = plt.subplots(1, 2, figsize = figsize, layout = "constrained", sharex=True, sharey=True)

diams = np.linspace(20,40,30)
mean_dist, high_dist, low_dist = get_dist(fem_asc_gmm, diams)
ax[0].plot(diams,mean_dist, color='blue')
ax[0].fill_between(diams, high_dist, low_dist, alpha=0.3, color='blue')
ax[0].tick_params(top=True, right=True, direction='in')
#ax.semilogy()

mean_dist, high_dist, low_dist = get_dist(fem_dsc_gmm, diams)
ax[1].plot(diams,mean_dist, '--', color='blue')
ax[1].fill_between(diams, high_dist, low_dist, alpha=0.3, color='blue')
ax[1].tick_params(top=True, right=True, direction='in')

mean_dist, high_dist, low_dist = get_dist(mal_asc_gmm, diams)
ax[0].plot(diams,mean_dist, color='red')
ax[0].fill_between(diams, high_dist, low_dist, alpha=0.3, color='red')
ax[0].tick_params(top=True, right=True, direction='in')
#ax.semilogy()

mean_dist, high_dist, low_dist = get_dist(mal_dsc_gmm, diams)
ax[1].plot(diams,mean_dist, '--', color='red')
ax[1].fill_between(diams, high_dist, low_dist, alpha=0.3, color='red')
ax[1].tick_params(top=True, right=True, direction='in')

ax[0].set_ylabel(r'Distensibility [$10^{-3}$ mmHg$^{-1}$]')
ax[0].set_xlabel(r'Diameter [mm]')
ax[1].set_xlabel(r'Diameter [mm]')

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
    bbox_to_anchor=(0.5, -0.2)  # adjust vertical position
)

plt.savefig('diam-distens-marg.pdf', bbox_inches='tight')

for gmm in gmms[:2]:
    #gmm.verbose = False
    gmm.reduce(condition=['Age','Bod_Sur','DBP','SBP', 'Asc_D_Area'])

for gmm in gmms[2:]:
    #gmm.verbose = False
    gmm.reduce(condition=['Age','Bod_Sur','DBP','SBP', 'Dsc_D_Area'])

def get_dist(gmm,diams):
    all_means, all_lows, all_highs = [], [], []
    #gmm.verbose = False
    try:
        gmm.reduce(condition=['Age','Bod_Sur','DBP','SBP', 'Dsc_D_Area'])
    except:
        gmm.reduce(condition=['Age','Bod_Sur','DBP','SBP', 'Asc_D_Area'])
    mu = gmm.mean()
    for dia in diams:
        mu[-2] = np.pi*dia**2/4.
        gmm.update_reduced_gmm(x_cond = mu[:-1])
        m, h, l = gmm.mean_std(reduced=True)
        all_means.append(m[0])
        all_highs.append(h[0])
        all_lows.append(l[0])

    return all_means, all_highs, all_lows

figsize = (8, 3)
fig, ax = plt.subplots(1, 2, figsize = figsize, layout = "constrained", sharex=True, sharey=True)

diams = np.linspace(20,40,30)
mean_dist, high_dist, low_dist = get_dist(fem_asc_gmm, diams)
ax[0].plot(diams,mean_dist, color='blue')
ax[0].fill_between(diams, high_dist, low_dist, alpha=0.3, color='blue')
ax[0].tick_params(top=True, right=True, direction='in')
#ax.semilogy()

mean_dist, high_dist, low_dist = get_dist(fem_dsc_gmm, diams)
ax[1].plot(diams,mean_dist, '--', color='blue')
ax[1].fill_between(diams, high_dist, low_dist, alpha=0.3, color='blue')
ax[1].tick_params(top=True, right=True, direction='in')

mean_dist, high_dist, low_dist = get_dist(mal_asc_gmm, diams)
ax[0].plot(diams,mean_dist, color='red')
ax[0].fill_between(diams, high_dist, low_dist, alpha=0.3, color='red')
ax[0].tick_params(top=True, right=True, direction='in')
#ax.semilogy()

mean_dist, high_dist, low_dist = get_dist(mal_dsc_gmm, diams)
ax[1].plot(diams,mean_dist, '--', color='red')
ax[1].fill_between(diams, high_dist, low_dist, alpha=0.3, color='red')
ax[1].tick_params(top=True, right=True, direction='in')

ax[0].set_ylabel(r'Distensibility [$10^{-3}$ mmHg$^{-1}$]')
ax[0].set_xlabel(r'Diameter [mm]')
ax[1].set_xlabel(r'Diameter [mm]')

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
    bbox_to_anchor=(0.5, -0.2)  # adjust vertical position
)

plt.savefig('diam-distens-cond-mean.pdf', bbox_inches='tight')
