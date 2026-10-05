import pymecht as pmt
import numpy as np
from math import sqrt
import os.path
#from scipy.stats import multivariate_normal
from gmmtools import *
import pickle
import pandas as pd
from sklearn.decomposition import PCA

class Stress_transform:
    def __init__(self, stress_dias, stress_sys):
        self.stress_dias = stress_dias
        self.stress_sys = stress_sys
        self.s1_pca = PCA(n_components=1)
        self.s2_pca = PCA(n_components=3)
        self.s1_pca.fit(self.stress_dias)
        self.s2_pca.fit(self.stress_sys)
        print(np.sum(self.s1_pca.explained_variance_ratio_))
        print(np.sum(self.s2_pca.explained_variance_ratio_))
        self.s1_t, self.s2_t = self.transform()
        
    def transform(self,s1=None, s2=None):
        if s1 is None:
            s1 = self.stress_dias
        if s2 is None:
            s2 = self.stress_sys
        s1_t = self.s1_pca.transform(s1)
        s2_t = self.s2_pca.transform(s2)
        return np.exp(s1_t/1000), np.exp(s2_t/1000)
        
    def i_transform(self, s1_t, s2_t):
        s1_t = np.atleast_2d(s1_t)
        s2_t = np.atleast_2d(s2_t)
        s1 = self.s1_pca.inverse_transform(np.log(s1_t)*1000)
        s2 = self.s2_pca.inverse_transform(np.log(s2_t)*1000)
        return s1, s2
    
class cal_compliance:
    def __init__(self,sample):
        self.sample = sample

    def __call__(self, params, props):
        try:
            p_dias, pp, A_dias,dist = props
            p_sys = p_dias + pp
            A_sys = A_dias*(dist*1e-3*(p_sys-p_dias) + 1)
            Rdias = np.sqrt(A_dias/np.pi)
            Rsys = np.sqrt(A_sys/np.pi)
            pressure = np.array([p_dias,p_sys])
            #print(params, props, Rdias, Rsys)
            #print(self.sample.__class__,isinstance(self.sample,pmt.TubeInflation))
            #pmt.specify_two_fibers(self.sample,angle=params['phi'],degrees=True,verbose=False)
            angle_rad = np.deg2rad(params['phi'])
            vec = [np.array([0,np.cos(angle_rad), np.sin(angle_rad)]), np.array([0,np.cos(-angle_rad), np.sin(-angle_rad)])]
            models = self.sample._mat_model.models
            for m in models:
                m.fiber_dirs = vec
            _params = params.copy()
            _params['Ri'] = params['Ri']*2*np.pi/(2*np.pi-params['omega'])
            #rad = self.sample.force_controlled(self.deltap,_params,x0=params['Ri'])
            _params['mu_0'] = 1.
            _params['k1_1'] = 0.
            p11 = self.sample.disp_controlled(Rdias,_params)
            p21 = self.sample.disp_controlled(Rsys,_params)
            _params['mu_0'] = 0.
            _params['k1_1'] = 1.
            p12 = self.sample.disp_controlled(Rdias,_params)
            p22 = self.sample.disp_controlled(Rsys,_params)
            A = np.array([[p11,p12],[p21,p22]])
            x = np.linalg.solve(A,pressure) #gives the values of mu and k1 in mm-Hg
            #print(Rdias, Rsys, x)
            _params['mu_0'] = x[0]
            _params['k1_1'] = x[1]
            xi,stress_dias = self.sample.cauchy_stress(Rdias,_params,n=10,pressure=p_dias)
            xi,stress_sys = self.sample.cauchy_stress(Rsys,_params,n=10,pressure=p_sys)
            stress_dias = np.array([np.diag(s) for s in stress_dias]).T.flatten() #in mm-Hg
            stress_sys  = np.array([np.diag(s) for s in stress_sys]).T.flatten() #in mm-Hg
            return np.append(np.append(x,stress_dias/p_dias), stress_sys/p_sys)
        except:
            return np.array([np.nan]*62)

if __name__ ==  '__main__':
    tissue = pmt.MatModel('nh','goh')
    artery = pmt.TubeInflation(tissue,disp_measure='radius',force_measure='pressure')
    params = artery.parameters
    params['phi'] = pmt.Param(54.5,0,90)
    param_file = 'params-asc.csv'
    if os.path.isfile(param_file):
        params.read(param_file)
    else:
        params.save(param_file)
    rand_param = pmt.RandomParameters(params)
    print(params)
    print(rand_param)
    sim = cal_compliance(artery)
    nsamples = 2**18
    param_samples = rand_param.sample(nsamples,'sobol')
    #sample diastolic radius and distensibility
    #rv = multivariate_normal([15, 1], [[2.0, 0.3], [0.3, 0.2]]) #synthetic distribution
    #prop_samples = rv.rvs(nsamples) #diastolic radius and distensibility
    
    ######### Use GMM fitted to biobank data #############
    with open("../ukbb-work/instance-2-ao/create-gmms/gmm_asc.pkl", "rb") as f:
        gmm = pickle.load(f)
    
    prop_samples = gmm.samples(nsamples, condition=False)
    
    ######################################################
    
    from p_tqdm import p_map
    results_all = p_map(sim,param_samples,prop_samples,num_cpus=4)
    #sim(param_samples[0],prop_samples[0])
    #results_all = np.array([sim(x) for x in param_samples])
    #finite_results = np.all(np.isfinite(results_all),axis=1)

    results_all = np.array(results_all)
    #outfile = 'results/mc-results4'
    #from pathlib import Path
    #Path(os.path.dirname(outfile)).mkdir(parents=True, exist_ok=True)
    #np.savez(outfile,param_samples=param_samples,finite_results=finite_results,results=results_all)
    df1 = pd.DataFrame(param_samples)
    df1 = df1.drop('mu_0',axis=1)
    df1 = df1.drop('k1_1',axis=1)
    df2 = pd.DataFrame(prop_samples, columns=['DBP','PP','Area','Dist'])
    df3 = pd.DataFrame({
    "mu_0": results_all[:, 0],
    "k1_1": results_all[:, 1],
    "stress_dias": list(results_all[:, 2:32]),
    "stress_sys": list(results_all[:,32:62])})
    df_all = pd.concat((df1,df2,df3),axis=1)
    df_all.to_pickle('results.pkl')
    
    valid = (df_all['mu_0']>0)*(df_all['k1_1']>0)
    df_val = df_all[valid].copy()
    df_val = df_val.dropna()

    print(len(df_val), len(df_all), len(df_val)/len(df_all))

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
        
    cols = ['DBP','PP', 'Area', 'Dist'] + [c for c in df_val.columns if '_t_' in c]
    df1 = df_val[cols]

    gmm_stress = GMM_Custom(df1)
    gmm_stress.fit()
    
    gmm_stress.reduce(condition=['DBP','PP', 'Area', 'Dist'])
    
    with open("gmm_stress.pkl", "wb") as f:
        pickle.dump(gmm_stress, f)
    with open("stress_transform.pkl","wb") as f:
        pickle.dump(stress_transform,f)
