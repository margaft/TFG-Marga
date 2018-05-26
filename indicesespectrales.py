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

def Welch_Periodogram(rr, fs = 4., window = 'hamming', nperseg = 256, noverlap = len('hamming')/2, nfft  = 1024):
    rr = rr - np.mean(rr)
    rr = signal.detrend(rr)
    
    f, p = signal.welch(rr, fs, window = window, nperseg = nperseg, noverlap = noverlap, nfft = nfft)
    #f, p = signal.welch(rr, fs, window = 'hanning', nperseg = 256, noverlap = 128, nfft  = 1024)
    
    
    return f, p #p: densidad espectral de potencia
                #f: vector frecuencia
             
#def spectral_indices(Pxx, f, duration = 5):
#    
#    if duration == 5:
#        indVlf = f <= 0.04
#        indUlf = []
#    elif duration >= 5:
#        indUlf = f <= 0.003
#        indVlf = f > 0.003 & f <= 0.04;
#        
#    ind = f <= 0.4
#    indLf = np.bitwise_and(f > 0.04, f <= 0.15)
#    indHf = np.bitwise_and(f > 0.15, f <= 0.4)
#    
#    df = f[2]
#    
#    #Cálculo de la potencia total
#    Ptot = df * sum(Pxx[ind])
#    
#    #Cálculo potencia en la banda ULF
#    if len(indUlf) == 0:
#        Pulf = df*sum(Pxx[indUlf]) #En ms^2
#    else:
#        Pulf = [];
#        
#    #Cálculo potencia en la banda VLF
#    Pvlf = df*sum(Pxx[indVlf]); 
#    
#    #Cálculo potencia en la banda LF
#    Plf = df*sum(Pxx[indLf]);
#    
#    #Cálculo potencia en la banda HF
#    Phf = df*sum(Pxx[indHf]);
#    
#    #Cáculo del ratio LF/HF
#    lfhf_ratio = Plf/Phf;
#     
#    return Ptot, Pulf, Pvlf, Plf, Phf, lfhf_ratio

def main_interp(rr, t = None, duration = 5):
    if t == None:
        t = np.cumsum(rr)/1000.

    #Interpolación
    
    rr_interpolated_4_hz, t_new = interp_to_psd(rr,t)
    
    return rr_interpolated_4_hz, t_new

def main_welch(rr, t = None, duration = 5):
    f, Pxx = Welch_Periodogram(rr_interpolated_4_hz,  4., 'hamming', 256, 128, 1024)
    
    return f, Pxx

#def main_spectral_indices(rr, t = None, duration = 5):
#    
#    Ptot, Pulf, Pvlf, Plf, Phf, lfhf_ratio = spectral_indices(Pxx, f, duration = 5.)
#    
#    return Ptot, Pulf, Pvlf, Plf, Phf, lfhf_ratio

plt.close('all')
rr = np.loadtxt('rr.txt')
t = np.cumsum(rr)/1000.
plt.plot(t,rr)

rr_interpolated_4_hz, t_new = main_interp(rr)

f, Pxx = main_welch(rr_interpolated_4_hz)

#Ptot, Pulf, Pvlf, Plf, Phf, lfhf_ratio = main_spectral_indices(Pxx)

plt.figure()
plt.plot(f[f<0.5],Pxx[f<0.5])