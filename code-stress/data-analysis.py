import pandas as pd
import numpy as np
import pickle
from matplotlib import pyplot as plt

df = pd.read_pickle('results.pkl')

df['SBP'] = df['DBP'] + df['PP']

def t_def(Ri,t,A_def,omega,lambdaZ):
   k = 2*np.pi/(2*np.pi-omega)
   Ro = Ri + t
   ri = np.sqrt(A_def/np.pi)
   ro = np.sqrt((Ro**2-Ri**2)/k/lambdaZ + ri**2)
   return ro-ri

df['thick_dias'] = t_def(df['Ri'], df['thick'], df['Area'], df['omega'], df['lambdaZ'])
df['thick_dias'].describe()

df['Area_sys'] =(df['Dist']*1e-3*(df['SBP']-df['DBP'])+1)*df['Area']
df['thick_sys'] = t_def(df['Ri'], df['thick'], df['Area_sys'], df['omega'], df['lambdaZ'])

valid = (df['mu_0']>0)*(df['k1_1']>0)
df_val = df[valid].copy()
df_val = df_val.dropna()

print(len(df_val), len(df), len(df_val)/len(df))

s1 = df_val['stress_dias']
s1 = np.array(list(s1))

s2 = df_val['stress_sys']
s2 = np.array(list(s2))

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
    mean1 = s1.mean(axis=0)
    mean2 = s2.mean(axis=0)
    sd1   = s1.std(axis=0)
    sd2   = s2.std(axis=0)
    low1, high1 = mean1-sd1, mean1+sd1
    low2, high2 = mean2-sd2, mean2+sd2

    plot(mean1,high1,low1,axs,'--', 0.2)
    plot(mean2,high2,low2,axs,'-', 0.4)
    axs[0].tick_params(top=True, right=True, direction='in')
    axs[1].tick_params(top=True, right=True, direction='in')
    axs[2].tick_params(top=True, right=True, direction='in')


import matplotlib as mpl

mpl.rcParams.update({
    # --- Font ---
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],  # or Arial if available

})

fig,axs = plt.subplots(1,3, figsize=(9,3*0.8), layout="constrained", sharex = True)
plot3(axs)
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
axs[0].set_ylabel('Normalised stress [-]')
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
plt.savefig('stresses-data.pdf', bbox_inches='tight')
plt.close()

### MI and correlation calculations

s1_c_max = np.max(s1[:,10:20],axis=1)
s1_l_max = np.max(s1[:,20:],axis=1)
s2_c_max = np.max(s2[:,10:20],axis=1)
s2_l_max = np.max(s2[:,20:],axis=1)

cols = ['DBP','SBP', 'Area', 'Dist', 'thick_dias']
df2 = df_val[cols]
df2['s1_c_max'] = s1_c_max
df2['s1_l_max'] = s1_l_max
df2['s2_c_max'] = s2_c_max
df2['s2_l_max'] = s2_l_max

from npeet import entropy_estimators as ee

def comb_ee(y):
    x = df2['Area'].to_numpy().reshape(-1,1)
    print('#Area\n',ee.mi(x,y,k=5),',')

    x = df2[['Area','Dist']].to_numpy()
    print('#Area + Dist\n', ee.mi(x,y,k=5),',')

    x = df2[['Area','thick_dias']].to_numpy()
    print('#Area + thick\n',ee.mi(x,y,k=5),',')

    x = df2[['Area','Dist','thick_dias']].to_numpy()
    print('#Area + Dist + thick\n',ee.mi(x,y,k=5),',')

print('#========================================')
print('#With max circumferential stress at DBP\n[')
y = df2['s1_c_max'].to_numpy().reshape(-1,1)
comb_ee(y)
print('],\n#========================================')

print('#========================================')
print('#With max longitudinal stress at DBP\n[')
y = df2['s1_l_max'].to_numpy().reshape(-1,1)
comb_ee(y)
print('],\n#========================================')

print('#========================================')
print('#With max circumferential stress at SBP\n[')
y = df2['s2_c_max'].to_numpy().reshape(-1,1)
comb_ee(y)
print('],\n#========================================')

print('#========================================')
print('#With max longitudinal stress at SBP\n[')
y = df2['s2_l_max'].to_numpy().reshape(-1,1)
comb_ee(y)
print('],\n#========================================')

stress_mi = [
#========================================
#With max circumferential stress at DBP
[
#Area 
0.5439863086507329,
#Area + Dist 
0.7590547212468572,
#Area + thick 
0.762037255316671,
#Area + Dist + thick 
0.8509103486418993,
],
#========================================
#========================================
#With max longitudinal stress at DBP
[
#Area 
0.06808626318827392,
#Area + Dist 
0.10374670683356911,
#Area + thick 
0.1590021515379645,
#Area + Dist + thick 
0.16306421322548764,
],
#========================================
#========================================
#With max circumferential stress at SBP
[
#Area 
0.49421215410769076,
#Area + Dist 
0.6259524488258364,
#Area + thick 
0.5820640338386153,
#Area + Dist + thick 
0.6572108824352846,
],
#========================================
#========================================
#With max longitudinal stress at SBP
[
#Area 
0.1409258863738918,
#Area + Dist 
0.17187763293495287,
#Area + thick 
0.1810114943894157,
#Area + Dist + thick 
0.1959351645290309,
],
#========================================
]

stress_mi_df = pd.DataFrame(np.array(stress_mi).T)
stress_mi_df.columns = ['Max circ. stress', 'Max long. stress', 'Max circ. stress', 'Max long. stress']
stress_mi_df.index = ['Size', 'Size + Dist', 'Size + thickness', 'Size + Dist + thickness']

names = [['Diastolic', 'Diastolic', 'Systolic', 'Systolic'],['Max circ. stress', 'Max long. stress', 'Max circ. stress', 'Max long. stress']]
stress_mi_df.columns = pd.MultiIndex.from_arrays(names, names=["Time","Direction"])

pd.options.display.float_format = "{:,.2f}".format
(stress_mi_df
.style
.background_gradient(cmap='YlOrRd', axis=None, vmin=0, vmax=1.1)
.highlight_null(color='#f1f1f1')  # Color NaNs grey
.format(precision=2)).to_latex('stress-asc-mi.tex',convert_css=True)

df2.corr()
# Output is:
#             DBP   SBP  Area  Dist  thick_dias  s1_c_max  s1_l_max  s2_c_max  s2_l_max
#DBP         1.00  0.50  0.23 -0.12       -0.08      0.09      0.04      0.01      0.05
#SBP         0.50  1.00  0.16 -0.55       -0.10      0.25     -0.03      0.22      0.06
#Area        0.23  0.16  1.00 -0.36       -0.37      0.62      0.10      0.50      0.33
#Dist       -0.12 -0.55 -0.36  1.00        0.20     -0.52      0.05     -0.39     -0.10
#thick_dias -0.08 -0.10 -0.37  0.20        1.00     -0.58     -0.24     -0.43     -0.36
#s1_c_max    0.09  0.25  0.62 -0.52       -0.58      1.00      0.28      0.55      0.46
#s1_l_max    0.04 -0.03  0.10  0.05       -0.24      0.28      1.00     -0.01      0.73
#s2_c_max    0.01  0.22  0.50 -0.39       -0.43      0.55     -0.01      1.00      0.40
#s2_l_max    0.05  0.06  0.33 -0.10       -0.36      0.46      0.73      0.40      1.00
#

stress_corr = df2.corr(method='spearman').iloc[2:5,5:]
stress_corr.index = ['Size','Dist','Thickness']
names = [['Diastolic', 'Diastolic', 'Systolic', 'Systolic'],['Max circ. stress', 'Max long. stress', 'Max circ. stress', 'Max long. stress']]
stress_corr.columns = pd.MultiIndex.from_arrays(names, names=["Time","Direction"])

pd.options.display.float_format = "{:,.2f}".format
(stress_corr
.style
.background_gradient(cmap='coolwarm', axis=None, vmin=-1, vmax=1)
.highlight_null(color='#f1f1f1')  # Color NaNs grey
.format(precision=2)).to_latex('stress-asc-corr.tex',convert_css=True)


x = df2['Dist'].to_numpy().reshape(-1,1)
z = df2[['Area','thick_dias']].to_numpy()
y = df2['s1_c_max'].to_numpy().reshape(-1,1)

#CMI between stress and distensibiliy, given area and thickness
ee.cmi(x,y,z)
# Output is 0.24688351527897312

y = df2['s2_c_max'].to_numpy().reshape(-1,1)
ee.cmi(x,y,z)
# Output is 0.1450335976270752

df_val['lap_stress_dias'] = np.sqrt(df_val['Area']/np.pi)/df_val['thick_dias']
df_val['lap_stress_sys'] = np.sqrt(df_val['Area_sys']/np.pi)/df_val['thick_sys']

cols = ['DBP','SBP', 'Area', 'Dist', 'thick_dias', 'lap_stress_dias', 'lap_stress_sys']
df3 = df_val[cols]
#df3.corr()
stress_corr = df3.corr(method='spearman').iloc[2:5,5:]
stress_corr.index = ['Size','Dist','Thickness']
stress_corr.columns = ['Mean diastolic stress', 'Mean systolic stress'] 

pd.options.display.float_format = "{:,.2f}".format
(stress_corr
.style
.background_gradient(cmap='coolwarm', axis=None, vmin=-1, vmax=1)
.highlight_null(color='#f1f1f1')  # Color NaNs grey
.format(precision=2)).to_latex('stress-asc-corr2.tex',convert_css=True)
