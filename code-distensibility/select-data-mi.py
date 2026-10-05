import numpy as np
import pandas as pd
from gmmtools import * 

#Import Data
df = pd.read_pickle('original-appended-data.pkl')

#col_subset = ['Sex', 'Age when attended assessment centre | Instance 2', 'Body surface area | Instance 2', 'Diastolic brachial blood pressure | Instance 2', 'Ascending aorta minimum area | Instance 2', 'Ascending aorta distensibility | Instance 2', 'Descending aorta minimum area | Instance 2', 'Descending aorta distensibility | Instance 2']
#df1 = df[col_subset]
#df1.columns = ['Sex', 'Age', 'Bod_Sur', 'DBP', 'Asc_D_Area', 'Asc_Dist', 'Dsc_D_Area', 'Dsc_Dist']

#dict1 = {
#'Diastolic brachial blood pressure | Instance 2':'DBP',
#'Ascending aorta minimum area | Instance 2': 'Asc_D_Area',
#'Ascending aorta distensibility | Instance 2': 'Asc_Dist'}
dict1 = {'Sex': 'Sex',
         'Age when attended assessment centre | Instance 2': 'Age',
         'Body surface area | Instance 2': 'Bod_Sur',
         'Height | Instance 2': 'height',
         'Weight | Instance 2': 'weight',
         'Systolic brachial blood pressure | Instance 2': 'SBP',
         'Diastolic brachial blood pressure | Instance 2':'DBP',
         'Ascending aorta minimum area | Instance 2': 'Asc_D_Area',
         'Ascending aorta distensibility | Instance 2': 'Asc_Dist',
         'Descending aorta minimum area | Instance 2': 'Dsc_D_Area',
         'Descending aorta distensibility | Instance 2': 'Dsc_Dist',
         }
df1 = df[dict1.keys()]
df1.columns = dict1.values()
df1 = df1.dropna()
df1['PP'] = df1['SBP'] - df1['DBP']
df1['Sex'] = df1['Sex'].replace({'Female': 1, 'Male': 0})

mi_df = MI_data_matrix(df1, ['Sex'])

mask = np.zeros_like(mi_df, dtype=bool)
np.fill_diagonal(mask,True)
mi_df[mask] = np.nan

pd.to_pickle(mi_df, 'MI.pkl')
pd.options.display.float_format = "{:,.2f}".format
print(mi_df)

fname = 'mi-npeet'
fname0 = fname
i=1
import os
while os.path.exists(fname0+'.html'):
    fname0 = fname + str(i)
    i+= 1
print('Writing', fname0 + '.html')
(mi_df
.style
.background_gradient(cmap='Grays', axis=None, vmin=0, vmax=0.9)
.highlight_null(color='#f1f1f1')  # Color NaNs grey
.format(precision=2)).to_html(fname0+'.html',convert_css=True)

ii = (['Asc_D_Area'],['height'],['Bod_Sur'])
print(*ii, CMI_data(df1, *ii))
ii = (['Asc_D_Area'],['weight'],['Bod_Sur'])
print(*ii, CMI_data(df1, *ii))
ii = (['Asc_D_Area'],['Bod_Sur'],['height','weight'])
print(*ii, CMI_data(df1, *ii))
ii = (['Asc_Dist'],['Bod_Sur'],['height','weight'])
print(*ii, CMI_data(df1, *ii))
ii = (['Asc_Dist'],['weight'],['Bod_Sur'])
print(*ii, CMI_data(df1, *ii))
ii = (['Asc_Dist'],['height'],['Bod_Sur'])
print(*ii, CMI_data(df1, *ii))
ii = (['Asc_Dist'],['Bod_Sur'],['height'])
print(*ii, CMI_data(df1, *ii))
ii = (['Asc_Dist'],['Bod_Sur'],['weight'])
print(*ii, CMI_data(df1, *ii))
