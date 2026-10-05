import pandas as pd
import numpy as np
from gmmtools import *
from StressTransform import *
import pickle

df = pd.read_pickle('results.pkl')

if 'PP' in df.columns:
    df['SBP'] = df['DBP'] + df['PP']
else:
    df['PP'] = df['SBP'] - df['DBP']

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

stress_transform = Stress_transform(s1,s2)
_,m = np.shape(stress_transform.s1_t)
for i in range(m):
    df_val['s1_t_'+str(i)] = stress_transform.s1_t[:,i]

_,m = np.shape(stress_transform.s2_t)
for i in range(m):
    df_val['s2_t_'+str(i)] = stress_transform.s2_t[:,i]

#_,m = np.shape(stress_transform.s_comb_t)
#for i in range(m):
#    df_val['s_t_'+str(i)] = stress_transform.s_comb_t[:,i]

cols = ['DBP','SBP', 'Area', 'Dist'] + [c for c in df_val.columns if '_t_' in c]
df1 = df_val[cols]

gmm_stress = GMM_Custom(df1)
gmm_stress.fit()
gmm_stress.reduce(condition=['DBP','SBP', 'Area', 'Dist'])

with open("gmm_stress.pkl", "wb") as f:
    pickle.dump(gmm_stress, f)
with open("stress_transform.pkl","wb") as f:
    pickle.dump(stress_transform,f)
