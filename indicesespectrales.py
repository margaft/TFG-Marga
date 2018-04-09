# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 10:35:33 2018

@author: Margaft
"""

import numpy as np
from scipy.interpolate import interp1d

#Función que calcula los índices espectrales de una serie temporal de intervalo rr
#Duración 5 minutos o más.
#t tiempos de vector de raw rr, es decir, el tiempo original en mseg. Si no
#pasado, se calculará a partir de series temporales de intervalos rr.

def interp_to_psd(rr, t, fs, method):
    nargin=0;
    if nargin == 1:
        t = np.cumsum(rr)/1000;
        fs = 4; #Hz
        method = 'spline';
    elif nargin < 3:
        fs = 4;
        method = 'spline';

    ts = 1/fs;
    t_new = t[1]:t[end]:ts;
    #Interpolacion
    rr_interp = interp1d(t, rr, t_new, method);


def main_spectral(rr,t = None,duration=5):
    if t == None:
        t = np.cumsum(rr)/1000;

#Interpolación
    
    rr_interpolated_4_hz = interp_to_psd(rr,t, 0, 0);
    

main_spectral(rrtxt)












