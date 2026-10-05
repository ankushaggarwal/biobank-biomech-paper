import numpy as np
import pickle
import pandas as pd
from scipy.stats import norm
from matplotlib import pyplot as plt
from gmmtools import *
from scipy import interpolate

import matplotlib as mpl

mpl.rcParams.update({
    # --- Font ---
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],  # or Arial if available

})

#load the created gmm's
with open("../fitted-models/gmm_asc_mal.pkl", "rb") as f:
    mal_asc_gmm = pickle.load(f)
with open("../fitted-models/gmm_asc_fem.pkl", "rb") as f:
    fem_asc_gmm = pickle.load(f)
with open("../fitted-models/gmm_dsc_mal.pkl", "rb") as f:
    mal_dsc_gmm = pickle.load(f)
with open("../fitted-models/gmm_dsc_fem.pkl", "rb") as f:
    fem_dsc_gmm = pickle.load(f)

gmms = [fem_asc_gmm, mal_asc_gmm, fem_dsc_gmm, mal_dsc_gmm]
name_gmms = ['Female AAo', 'Male AAo', 'Female DAo', 'Male DAo']

#for gmm in gmms:
#    gmm.reduce(condition=['Age','Bod_Sur','DBP','SBP'])

area2dia = lambda a: np.sqrt(a/np.pi)*2

def plot(gmm, ax):
    percentiles = np.linspace(0.9,0.1,9)
    X,Y,Z,levels = gmm.contour_levels_from_percentiles(percentiles,log=False)
    cs = ax.contour(area2dia(X), Y, Z, levels = levels,linewidths=1)
    fmt = {level: f"{p:.1f}" for level,p in zip(levels[::2],percentiles[::2])}
    #ax.clabel(cs, levels=levels[::2], fmt=fmt,fontsize=8) #makes it too cluttered
    ax.tick_params(top=True, right=True, direction='in')
    return

def plot4(axs,vals):
    for gmm in gmms:
        gmm.reduce(condition=['Age','Bod_Sur','DBP','SBP'],x_cond=vals)

    for ax,gmm in zip(axs,gmms):
        plot(gmm,ax)

fig, axs4 = plt.subplots(4,4, figsize=(10,10*0.8), layout="constrained", sharex=True, sharey=True)

all_vals = [[65,1.2,80,120],
            [45,1.2,80,120],
            [75,1.8,80,120],
            [65,1.2,80,150]]

for axs,vals in zip(axs4,all_vals):
    plot4(axs,vals)

for ax in axs4[:,0]:
    ax.set_ylabel(r'Dist [$10^{-3}$ mmHg$^{-1}$]')
for ax in axs4[-1]:
    ax.set_xlabel(r'Diameter [mm]')
    ax.set_xlim(15,45)
    ax.set_ylim(0,9)

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
col_titles = ["Females", "Males", "Females", "Males"]

for x, title in zip(col_centers, col_titles):
    fig.text(x, 1.02, title, ha='center', va='top', fontsize=12)

# --- Column group titles (top row) ---
fig.text((col_centers[0]+col_centers[1])*0.5, 1.05, "Ascending", ha='center', va='top', fontsize=12)
fig.text((col_centers[2]+col_centers[3])*0.5, 1.05, "Descending", ha='center', va='top', fontsize=12)

plt.savefig('contours.pdf', bbox_inches='tight')
plt.close()
