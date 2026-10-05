import numpy as np
import pandas as pd
from gmmtools import *
from matplotlib import pyplot as plt

#Import Data
df = pd.read_pickle('original-appended-data.pkl')
dict1 = {'Sex': 'Sex',
         'Age when attended assessment centre | Instance 2': 'Age',
         'Body surface area | Instance 2': 'BSA',
         'Diastolic brachial blood pressure | Instance 2':'DBP',
         'Systolic brachial blood pressure | Instance 2':'SBP',
         'Ascending aorta minimum area | Instance 2': 'Area',
         'Ascending aorta distensibility | Instance 2': 'Dist',
         'Descending aorta minimum area | Instance 2': 'Area2',
         'Descending aorta distensibility | Instance 2': 'Dist2'}
df1 = df[dict1.keys()]
df1.columns = dict1.values()
df1 = df1.dropna()
df1 = df1[df1['Dist']<20]
df1['Dia'] = np.sqrt(df1['Area']/np.pi)*2
df1['Dia2'] = np.sqrt(df1['Area2']/np.pi)*2

#df_fem.drop('Sex', axis=1, inplace=True)
#df_mal = df1[df1['Sex']=='Male'].copy()
#df_mal.drop('Sex', axis=1, inplace=True)
#df_fem = df_fem[df_fem['Dist']<20]
#df_mal = df_mal[df_mal['Dist']<20]

import matplotlib as mpl

mpl.rcParams.update({
    # --- Font ---
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],  # or Arial if available
})

sample = df1.sample(n=1000, random_state=42)

import seaborn as sns
g = sns.pairplot(sample,hue='Sex',kind='kde',
                 height=1.5,aspect=1.2,
                 vars=['Age','BSA','DBP','SBP','Dia','Dist', 'Dia2', 'Dist2'],
                 palette=("blue","red"),
                 plot_kws={"alpha":0.9, "linewidths":0.95}
                 )
#g.map_lower(sns.kdeplot,alpha=0.5, linewidth=0.5)
#g.map_diag(sns.kdeplot)

sns.move_legend(g, "lower center", bbox_to_anchor=(0.5, -0.02), ncol=2, title=None)

#handles = g._legend_data.values()
#labels = g._legend_data.keys()
#g.fig.legend(handles=handles, labels=labels, loc='upper center', ncol=1)
#g.fig.legend(handles=handles, labels=labels, loc='lower center', ncol=2)
#g.fig.legend(handles=handles, labels=labels, loc='upper left', ncol=3)


# Define your custom labels (same order as columns in the pairplot)
custom_labels = ["Age", "BSA", "DBP", "SBP", r"Asc $D_{\text{dias}}$", r"Asc $\delta$", r"Dsc $D_{\text{dias}}$", r"Dsc $\delta$"]

# Set axis labels
for i, ax in enumerate(g.axes[-1, :]):  # bottom row → x labels
    ax.set_xlabel(custom_labels[i])

for i, ax in enumerate(g.axes[:, 0]):   # left column → y labels
    ax.set_ylabel(custom_labels[i])

g.axes[0,5].set_xlim(right=6)
g.axes[5,0].set_ylim(top=6)
g.axes[0,7].set_xlim(right=6)
g.axes[7,0].set_ylim(top=6)
g.axes[0,3].set_xlim(left=80)
g.axes[3,0].set_ylim(bottom=80)

plt.savefig('pairplot.png',dpi=100,bbox_inches='tight')
#plt.show()
plt.close()
