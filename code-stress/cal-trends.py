import numpy as np
from gmmtools import *
import pickle
from StressTransform import *

with open("../fitted-models/gmm_stress.pkl", "rb") as f:
    gmm_stress = pickle.load(f)
    
with open("./fitted-models/stress_transform.pkl", "rb") as f:
    stress_transform = pickle.load(f)
    
results = {}
smax_c1, smax_l1, smax_c2, smax_l2 = [], [], [], []
gmm_stress.reduce(condition=['DBP'],marginalise=['SBP', 'Area', 'Dist'])
DBPs = np.linspace(50,90,15)
for dbp in DBPs:
    gmm_stress.update_reduced_gmm(dbp)
    m,high,low = gmm_stress.mean_std(reduced=True)
    mean1, mean2 = stress_transform.i_transform(m)
    smax_c1.append(np.max(mean1[0,10:20]))
    smax_l1.append(np.max(mean1[0,20:]))
    smax_c2.append(np.max(mean2[0,10:20]))
    smax_l2.append(np.max(mean2[0,20:]))

results['dbp'] = [DBPs, 
                  np.array(smax_c1), np.array(smax_l1), 
                  np.array(smax_c2), np.array(smax_l2)]

smax_c1, smax_l1, smax_c2, smax_l2 = [], [], [], []
gmm_stress.reduce(condition=['SBP'],marginalise=['DBP', 'Area', 'Dist'])
SBPs = np.linspace(90,130,15)
for sbp in SBPs:
    gmm_stress.update_reduced_gmm(sbp)
    m,high,low = gmm_stress.mean_std(reduced=True)
    mean1, mean2 = stress_transform.i_transform(m)
    smax_c1.append(np.max(mean1[0,10:20]))
    smax_l1.append(np.max(mean1[0,20:]))
    smax_c2.append(np.max(mean2[0,10:20]))
    smax_l2.append(np.max(mean2[0,20:]))

results['sbp'] = [SBPs, 
                  np.array(smax_c1), np.array(smax_l1), 
                  np.array(smax_c2), np.array(smax_l2)]

smax_c1, smax_l1, smax_c2, smax_l2 = [], [], [], []
gmm_stress.reduce(condition=['Area'],marginalise=['DBP', 'SBP', 'Dist'])

dias = np.linspace(25,40,15)
areas = np.pi*(dias/2)**2
for a in areas:
    gmm_stress.update_reduced_gmm(a)
    m,high,low = gmm_stress.mean_std(reduced=True)
    mean1, mean2 = stress_transform.i_transform(m)
    smax_c1.append(np.max(mean1[0,10:20]))
    smax_l1.append(np.max(mean1[0,20:]))
    smax_c2.append(np.max(mean2[0,10:20]))
    smax_l2.append(np.max(mean2[0,20:]))

results['dia'] = [dias, 
                  np.array(smax_c1), np.array(smax_l1), 
                  np.array(smax_c2), np.array(smax_l2)]

smax_c1, smax_l1, smax_c2, smax_l2 = [], [], [], []
gmm_stress.reduce(condition=['Dist'],marginalise=['DBP', 'SBP', 'Area'])

DISTs = np.linspace(1,3,15)
for d in DISTs:
    gmm_stress.update_reduced_gmm(d)
    m,high,low = gmm_stress.mean_std(reduced=True)
    mean1, mean2 = stress_transform.i_transform(m)
    smax_c1.append(np.max(mean1[0,10:20]))
    smax_l1.append(np.max(mean1[0,20:]))
    smax_c2.append(np.max(mean2[0,10:20]))
    smax_l2.append(np.max(mean2[0,20:]))

results['dist'] = [DISTs, 
                  np.array(smax_c1), np.array(smax_l1), 
                  np.array(smax_c2), np.array(smax_l2)]

with open("trend-results.pkl","wb") as f:
    pickle.dump(results,f)
