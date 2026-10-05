import pandas as pd
from gmmtools import * 
import pickle

#Import Data
df = pd.read_pickle('original-appended-data.pkl')
dict1 = {'Diastolic brachial blood pressure | Instance 2':'DBP',
         'Systolic brachial blood pressure | Instance 2':'SBP',
         'Ascending aorta minimum area | Instance 2': 'Area',
         'Ascending aorta distensibility | Instance 2': 'Dist'}
df1 = df[dict1.keys()]
df1.columns = dict1.values()
df1 = df1.dropna()
df1['PP'] = df1['SBP']-df1['DBP']
df1 = df1.drop('SBP',axis=1)
df1 = df1[df1['PP']>=10]
df1 = df1[['DBP','PP','Area','Dist']]

gmm = GMM_Custom(df1)
gmm.fit()
gmm.data = None

dict2 = {'Diastolic brachial blood pressure | Instance 2':'DBP',
         'Systolic brachial blood pressure | Instance 2':'SBP',
         'Descending aorta minimum area | Instance 2': 'Area',
         'Descending aorta distensibility | Instance 2': 'Dist'}
df2 = df[dict2.keys()]
df2.columns = dict2.values()
df2 = df2.dropna()
df2['PP'] = df2['SBP']-df2['DBP']
df2 = df2.drop('SBP',axis=1)
df2 = df2[df2['PP']>=10]
df2 = df2[['DBP','PP','Area','Dist']]

gmm2 = GMM_Custom(df2)
gmm2.fit()
gmm2.data = None

with open("gmm_asc.pkl", "wb") as f:
    pickle.dump(gmm, f)
with open("gmm_dsc.pkl", "wb") as f:
    pickle.dump(gmm2, f)
