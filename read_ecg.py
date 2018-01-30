#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 20:17:20 2018

@author: obarquero
"""

#Read bitalino ECG. See https://www.youtube.com/watch?v=a8VSeygQWkc

import numpy as np
import matplotlib.pyplot as plt

sigs = np.loadtxt('./data/opensignals_Oscar_2017-10-17_12-27-32.txt')

fs = 1000. #1Khz sampling frequency

# There is a need to specify the channel. It is indicated in the header file
ecg= sigs[:,5]

t = np.arange(len(ecg))/fs

plt.plot(t,ecg)