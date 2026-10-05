import numpy as np
from sklearn.decomposition import PCA

class Stress_transform:
    def __init__(self, stress_dias, stress_sys):
        self.stress_dias = stress_dias
        self.stress_sys = stress_sys
        self.n1, self.n2 = 2, 4
        self.s1_pca = PCA(n_components=self.n1)
        self.s2_pca = PCA(n_components=self.n2)
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
        
    def i_transform(self, s_comb_t):
        s1_t, s2_t = s_comb_t[...,:self.n1], s_comb_t[...,self.n1:]
        s1_t = np.atleast_2d(s1_t)
        s2_t = np.atleast_2d(s2_t)
        s1 = self.s1_pca.inverse_transform(np.log(s1_t)*1000)
        s2 = self.s2_pca.inverse_transform(np.log(s2_t)*1000)
        return s1, s2

