import pandas as pd
from gmmtools import * 
import pickle

with open("../fitted-models/gmm_asc_mal.pkl", "rb") as f:
    gmm_mal = pickle.load(f)

with open("../fitted-models/gmm_asc_fem.pkl", "rb") as f:
    gmm_fem = pickle.load(f)

gmm_mal.verbose = False
gmm_fem.verbose = False

x1 = CMI_gmms([gmm_mal,gmm_fem],['Asc_D_Area'],['Age','Bod_Sur'])
x2 = CMI_gmms_MC([gmm_mal,gmm_fem],['Asc_D_Area'],['Age','Bod_Sur'],
                 nsamples=200_000,
                 random_state=0)
print("Ascending: CMI between male/female Asc_D_Area (given age and BSA) is:")
print(x1,x2)


x1 = CMI_gmms([gmm_mal,gmm_fem],['Asc_Dist'],['Age','Bod_Sur'])
x2 = CMI_gmms_MC([gmm_mal,gmm_fem],['Asc_Dist'],['Age','Bod_Sur'],
                 nsamples=200_000,
                 random_state=0)
print("Ascending: CMI between male/female Asc_Dist (given age and BSA) is:")
print(x1,x2)

with open("../fitted-models/gmm_dsc_mal.pkl", "rb") as f:
    gmm_mal = pickle.load(f)

with open("../fitted-models/gmm_dsc_fem.pkl", "rb") as f:
    gmm_fem = pickle.load(f)

gmm_mal.verbose = False
gmm_fem.verbose = False

x1 = CMI_gmms([gmm_mal,gmm_fem],['Dsc_D_Area'],['Age','Bod_Sur'])
x2 = CMI_gmms_MC([gmm_mal,gmm_fem],['Dsc_D_Area'],['Age','Bod_Sur'],
                 nsamples=200_000,
                 random_state=0)
print("Descending: CMI between male/female Dsc_D_Area (given age and BSA) is:")
print(x1,x2)

x1 = CMI_gmms([gmm_mal,gmm_fem],['Dsc_Dist'],['Age','Bod_Sur'])
x2 = CMI_gmms_MC([gmm_mal,gmm_fem],['Dsc_Dist'],['Age','Bod_Sur'],
                 nsamples=200_000,
                 random_state=0)
print("Descending: CMI between male/female Dsc_Dist (given age and BSA) is:")
print(x1,x2)
