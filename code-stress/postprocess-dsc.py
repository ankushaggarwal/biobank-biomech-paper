import pandas as pd
import numpy as np
from gmmtools import *
from StressTransform import *
import pickle

df = pd.read_pickle('results-dsc.pkl')

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
 0.710667547065836 ,
#Area + Dist
 0.891569674269475 ,
#Area + thick
 0.9990365305409289 ,
#Area + Dist + thick
 0.9416149280674588 ,
],
#========================================
#========================================
#With max longitudinal stress at DBP
[
#Area
 0.014035486362389202 ,
#Area + Dist
 0.07232164587286447 ,
#Area + thick
 0.015325539294154932 ,
#Area + Dist + thick
 0.07243933280338838 ,
],
#========================================
#========================================
#With max circumferential stress at SBP
[
#Area
 0.6344236075387273 ,
#Area + Dist
 0.7072547238210395 ,
#Area + thick
 0.7511572815048632 ,
#Area + Dist + thick
 0.7220289738124339 ,
],
#========================================
#========================================
#With max longitudinal stress at SBP
[
#Area
 0.041161657861362784 ,
#Area + Dist
 0.08835719654128919 ,
#Area + thick
 0.043651736457842774 ,
#Area + Dist + thick
 0.08847647032742169 ,
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
.format(precision=2)).to_latex('stress-dsc-mi.tex',convert_css=True)

