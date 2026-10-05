import pandas as pd
from gmmtools import * 
import pickle

#Import Data
df = pd.read_pickle('original-appended-data.pkl')
dict1 = {'Sex': 'Sex',
         'Age when attended assessment centre | Instance 2': 'Age',
         'Body surface area | Instance 2': 'Bod_Sur',
         'Diastolic brachial blood pressure | Instance 2':'DBP',
         'Systolic brachial blood pressure | Instance 2':'SBP',
         'Ascending aorta minimum area | Instance 2': 'Asc_D_Area',
         'Ascending aorta distensibility | Instance 2': 'Asc_Dist'}
df1 = df[dict1.keys()]
df1.columns = dict1.values()
df1 = df1.dropna()

df_fem = df1[df1['Sex']=='Female'].copy()
df_fem.drop('Sex', axis=1, inplace=True)
df_mal = df1[df1['Sex']=='Male'].copy()
df_mal.drop('Sex', axis=1, inplace=True)

gmm_mal = GMM_Custom(df_mal)
gmm_fem = GMM_Custom(df_fem)

gmm_mal.fit()
gmm_fem.fit()

with open("../fitted-models/gmm_asc_mal.pkl", "wb") as f:
    pickle.dump(gmm_mal, f)
with open("../fitted-models/gmm_asc_fem.pkl", "wb") as f:
    pickle.dump(gmm_fem, f)

dict1 = {'Sex': 'Sex',
         'Age when attended assessment centre | Instance 2': 'Age',
         'Body surface area | Instance 2': 'Bod_Sur',
         'Diastolic brachial blood pressure | Instance 2':'DBP',
         'Systolic brachial blood pressure | Instance 2':'SBP',
         'Descending aorta minimum area | Instance 2': 'Dsc_D_Area',
         'Descending aorta distensibility | Instance 2': 'Dsc_Dist'}
df1 = df[dict1.keys()]
df1.columns = dict1.values()
df1 = df1.dropna()

df_fem = df1[df1['Sex']=='Female'].copy()
df_fem.drop('Sex', axis=1, inplace=True)
df_mal = df1[df1['Sex']=='Male'].copy()
df_mal.drop('Sex', axis=1, inplace=True)

gmm_mal = GMM_Custom(df_mal)
gmm_fem = GMM_Custom(df_fem)

gmm_mal.fit()
gmm_fem.fit()

with open("../fitted-models/gmm_dsc_mal.pkl", "wb") as f:
    pickle.dump(gmm_mal, f)
with open("../fitted-models/gmm_dsc_fem.pkl", "wb") as f:
    pickle.dump(gmm_fem, f)
