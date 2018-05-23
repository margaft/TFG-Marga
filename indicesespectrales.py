# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 10:35:33 2018
@author: Margaft
"""

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy import signal

#Función que calcula los índices espectrales de una serie temporal de intervalo rr
#Duración 5 minutos o más.
#t tiempos de vector de raw rr, es decir, el tiempo original en mseg. Si no
#pasado, se calculará a partir de series temporales de intervalos rr.

def interp_to_psd(rr, t = None, fs = 4., method = 'cubic'):
    
  

    ts = 1/fs #sampling frequency
    
    t_new = np.arange(t[0],t[-1],ts) #nuevo vector para la interpolacion
    #Interpolacion
    f = interp1d(t, rr, kind = method) #crea el objeto para interpolar
    
    #ahora realizamos la interpolación realmente
    rr_interp = f(t_new)
    
    return rr_interp,t_new

def Welch_Periodogram(rr, fs = 4., window = 'hanning', nperseg = 256, noverlap = 128, nfft  = 1024):
    rr = rr - np.mean(rr)
    rr = signal.detrend(rr)
    
    p, f = signal.welch(rr, fs, window = window, nperseg = nperseg, noverlap = noverlap, nfft = nfft)
    #p, f = signal.welch(rr, fs, window = 'hanning', nperseg = 256, noverlap = 128, nfft  = 1024)
    
    
    return p,f

def main_spectral(rr, t = None, duration = 5):
    if t == None:
        t = np.cumsum(rr)/1000.

    #Interpolación
    
   # rr_interpolated_4_hz,t_new = interp_to_psd(rr,t)
    
   # return rr_interpolated_4_hz, t_new

    f, Pxx = Welch_Periodogram(rr,  4., 'hanning', 256, 128, 1024)
    
    return Pxx, f

plt.close('all')
rr = np.load('rr_example.npy')
t = np.cumsum(rr)/1000.
plt.plot(t,rr)
#rr_interpolated_4_hz, t_new = main_spectral(rr)

Pxx, f = main_spectral(rr)

plt.figure()
plt.plot(f[f<0.5],Pxx[f<0.5])
