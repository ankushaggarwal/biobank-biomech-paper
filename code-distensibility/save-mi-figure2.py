import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

mi_df = pd.read_pickle('MI.pkl')
pd.options.display.float_format = "{:,.2f}".format
print(mi_df)
mi_df2 = mi_df.drop(['Sex','height','weight','PP'],axis=0).drop(['Sex','height','weight','PP'],axis=1)
print(mi_df2)
mi_df3 = mi_df2.rename(columns={'Bod_Sur':'BSA', 'Asc_D_Area':'Asc $\Adias$', 'Asc_Dist': 'Asc $\dist$', 'Dsc_D_Area': 'Dsc $\Adias$', 'Dsc_Dist': 'Dsc $\dist$'}, index={'Bod_Sur':'BSA', 'Asc_D_Area':'Asc $\Adias$', 'Asc_Dist': 'Asc $\dist$', 'Dsc_D_Area': 'Dsc $\Adias$', 'Dsc_Dist': 'Dsc $\dist$'})
#reorder
mi_df3 = mi_df3.iloc[[0,1,3,2,4,5,6,7],[0,1,3,2,4,5,6,7]]
#set the "non-significant mi to nan (0.01 selected through 1000 random permutations, which gives an MI of 0.01 for p-value of <0.001)
mi_df3[mi_df3 < 0.01] = np.nan
mi_df3
(mi_df3
.style
.background_gradient(cmap='YlOrRd', axis=None, vmin=0, vmax=0.7)
.highlight_null(color='#f1f1f1')  # Color NaNs grey
.format(precision=2)).to_latex('mi-npeet4.tex',convert_css=True)

