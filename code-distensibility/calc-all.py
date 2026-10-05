import numpy as np
import pickle
import pandas as pd
from scipy.stats import norm
from matplotlib import pyplot as plt
from scipy import interpolate
from gmmtools import *

#load the created gmm's
with open("../fitted-models/gmm_asc_mal.pkl", "rb") as f:
    mal_asc_gmm = pickle.load(f)
with open("../fitted-models/gmm_asc_fem.pkl", "rb") as f:
    fem_asc_gmm = pickle.load(f)
with open("../fitted-models/gmm_dsc_mal.pkl", "rb") as f:
    mal_dsc_gmm = pickle.load(f)
with open("../fitted-models/gmm_dsc_fem.pkl", "rb") as f:
    fem_dsc_gmm = pickle.load(f)

gmms = [fem_asc_gmm, mal_asc_gmm, fem_dsc_gmm, mal_dsc_gmm]
name_gmms = ['Female AAo', 'Male AAo', 'Female DAo', 'Male DAo']

area2dia = lambda a: np.sqrt(a/np.pi)*2

def plot_mean_contour(gmm, cond_values, ax, contour=False):
    gmm.update_reduced_gmm(x_cond = cond_values)
    mean = gmm.mean(reduced=True)
    if contour is True:
        x,y,z,l = gmm.contour_levels_from_percentiles(percentiles = [0.2])
        #create contour line
        cs = plt.contour(area2dia(x), y,  z, levels=l)
        #print(mean)
        #plt.plot(area2dia(mean[0]), mean[1], 'x', color='black')
        #plt.close()
        return mean, cs.allsegs
    return mean 

results = {'case':[], 'line': [], 'cross': [], 'contour':[]}

def plot_mix(line, cross, contour, color, ltype, ax):
    ax.plot(area2dia(line[:,0]), line[:,1],ltype,color=color)
    ax.plot(area2dia(cross[:,0]), cross[:,1],'x',color=color)
    for x in [elem for sublist1 in contour for sublist2 in sublist1 for elem in sublist2]:
        ax.plot(x[:,0], x[:,1],ltype,color=color)

####################################################################################################
# w.r.t. age
####################################################################################################
for gmm in gmms:
    #gmm.verbose = False
    gmm.reduce(condition=['Age'], marginalise = ['Bod_Sur', 'DBP', 'SBP'])

ages = np.linspace(45,80,21)
for gmm, name in zip(gmms, name_gmms):
    fig, ax = plt.subplots(1,1)
    all_means = []
    all_contours = []
    contour_means = []
    for i,age in enumerate(ages):
        if i%10 == 0:
            res1, res2 = plot_mean_contour(gmm, age, ax, contour = True)
            all_means.append(res1)
            all_contours.append(res2)
            contour_means.append(res1)
        else:
            all_means.append(plot_mean_contour(gmm, age, ax, contour = False))
    all_means = np.array(all_means)
    contour_means = np.array(contour_means)
    plt.close()
    results['case'].append(name+' w.r.t. age')
    results['line'].append(all_means)
    results['cross'].append(contour_means)
    results['contour'].append(all_contours)

#results_df = pd.DataFrame.from_dict(results)
#
#fig, ax = plt.subplots(1,1)
#for i in range(len(results_df)):
#    line, cross, contour = results_df.loc[i,'line'], results_df.loc[i,'cross'], results_df.loc[i,'contour']
#    if i==0:
#        plot_mix(line, cross, contour, 'red', '-', ax)
#    elif i==1:
#        plot_mix(line, cross, contour, 'blue', '-', ax)
#    elif i==2:
#        plot_mix(line, cross, contour, 'red', '--', ax)
#    elif i==3:
#        plot_mix(line, cross, contour, 'blue', '--', ax)
#plt.show()

####################################################################################################
# w.r.t. BSA
####################################################################################################
for gmm in gmms:
    #gmm.verbose = False
    gmm.reduce(condition=['Bod_Sur'], marginalise = ['Age', 'DBP', 'SBP'])

BSAs = np.linspace(1.2,2.8,21) #covers almost all of the range in the data
for gmm, name in zip(gmms, name_gmms):
    fig, ax = plt.subplots(1,1)
    all_means = []
    all_contours = []
    contour_means = []
    for i,bsa in enumerate(BSAs):
        if i%10 == 0:
            res1, res2 = plot_mean_contour(gmm, bsa, ax, contour = True)
            all_means.append(res1)
            all_contours.append(res2)
            contour_means.append(res1)
        else:
            all_means.append(plot_mean_contour(gmm, bsa, ax, contour = False))
    all_means = np.array(all_means)
    contour_means = np.array(contour_means)
    plt.close()
    results['case'].append(name+' w.r.t. BSA')
    results['line'].append(all_means)
    results['cross'].append(contour_means)
    results['contour'].append(all_contours)

#results_df = pd.DataFrame.from_dict(results)
#
#fig, ax = plt.subplots(1,1)
#for i in range(4,len(results_df)):
#    line, cross, contour = results_df.loc[i,'line'], results_df.loc[i,'cross'], results_df.loc[i,'contour']
#    if i==4:
#        plot_mix(line, cross, contour, 'red', '-', ax)
#    elif i==5:
#        plot_mix(line, cross, contour, 'blue', '-', ax)
#    elif i==6:
#        plot_mix(line, cross, contour, 'red', '--', ax)
#    elif i==7:
#        plot_mix(line, cross, contour, 'blue', '--', ax)
#plt.show()

####################################################################################################
# w.r.t. DBPs 
####################################################################################################
for gmm in gmms:
    #gmm.verbose = False
    gmm.reduce(condition=['DBP'], marginalise = ['Age', 'Bod_Sur', 'SBP'])

DBPs = np.linspace(50,90,21) #covers almost all of the range in the data
for gmm, name in zip(gmms, name_gmms):
    fig, ax = plt.subplots(1,1)
    all_means = []
    all_contours = []
    contour_means = []
    for i,dbp in enumerate(DBPs):
        if i%10 == 0:
            res1, res2 = plot_mean_contour(gmm, dbp, ax, contour = True)
            all_means.append(res1)
            all_contours.append(res2)
            contour_means.append(res1)
        else:
            all_means.append(plot_mean_contour(gmm, dbp, ax, contour = False))
    all_means = np.array(all_means)
    contour_means = np.array(contour_means)
    plt.close()
    results['case'].append(name+' w.r.t. DBP')
    results['line'].append(all_means)
    results['cross'].append(contour_means)
    results['contour'].append(all_contours)

#results_df = pd.DataFrame.from_dict(results)
#
#fig, ax = plt.subplots(1,1)
#for i in range(4,len(results_df)):
#    line, cross, contour = results_df.loc[i,'line'], results_df.loc[i,'cross'], results_df.loc[i,'contour']
#    if i==8:
#        plot_mix(line, cross, contour, 'red', '-', ax)
#    elif i==9:
#        plot_mix(line, cross, contour, 'blue', '-', ax)
#    elif i==10:
#        plot_mix(line, cross, contour, 'red', '--', ax)
#    elif i==11:
#        plot_mix(line, cross, contour, 'blue', '--', ax)
#plt.show()

####################################################################################################
# w.r.t. SBPs 
####################################################################################################
for gmm in gmms:
    #gmm.verbose = False
    gmm.reduce(condition=['SBP'], marginalise = ['Age', 'Bod_Sur', 'DBP'])

SBPs = np.linspace(90,140,21) #covers almost all of the range in the data
for gmm, name in zip(gmms, name_gmms):
    fig, ax = plt.subplots(1,1)
    all_means = []
    all_contours = []
    contour_means = []
    for i,sbp in enumerate(SBPs):
        if i%10 == 0:
            res1, res2 = plot_mean_contour(gmm, sbp, ax, contour = True)
            all_means.append(res1)
            all_contours.append(res2)
            contour_means.append(res1)
        else:
            all_means.append(plot_mean_contour(gmm, sbp, ax, contour = False))
    all_means = np.array(all_means)
    contour_means = np.array(contour_means)
    plt.close()
    results['case'].append(name+' w.r.t. SBP')
    results['line'].append(all_means)
    results['cross'].append(contour_means)
    results['contour'].append(all_contours)

#results_df = pd.DataFrame.from_dict(results)
#
#fig, ax = plt.subplots(1,1)
#for i in range(4,len(results_df)):
#    line, cross, contour = results_df.loc[i,'line'], results_df.loc[i,'cross'], results_df.loc[i,'contour']
#    if i==12:
#        plot_mix(line, cross, contour, 'red', '-', ax)
#    elif i==13:
#        plot_mix(line, cross, contour, 'blue', '-', ax)
#    elif i==14:
#        plot_mix(line, cross, contour, 'red', '--', ax)
#    elif i==15:
#        plot_mix(line, cross, contour, 'blue', '--', ax)
#plt.show()

results_df = pd.DataFrame.from_dict(results)
pd.to_pickle(results_df, 'results_df.pkl')
