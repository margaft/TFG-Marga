#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:04:22 2018

@author: obarquero
"""

import numpy as np
from HolterData import HolterData
from HRT import HRT
from HRV import HRV
import os
import glob


def get_HRV_HRT_matrix_for_patient(ruta, ident):
    """
    Create a X matrix with all the values extracted from a 24-hour Holter recording associate to
    one patient, and their correspondent Y_TS, Y_TO matrixes with the TS and TO values calculated.
    """
    
    rr_3min_valid = []
    rr_3min_valid_corrected = []
    lab_3min_valid = []
    pos_3min_valid = []
    tachs_all_cond_valid = []
    V_pos_tachs_all_cond_valid = [] 
    name = ruta.split('.')[0]
    ident = ident
    
    #Extract the data from the file
    hd = HolterData()
    pat = hd.read_holter_file(ruta)
    
    #We saved the RR intervals and the labels of each one
    rr = pat['RRInt']
    labels = pat['Labels']
       
    #We calculate the parameters of Heart Turbulence 
    print("HRT")
    hrt = HRT(rr, labels)
    hrt_pat = hrt.fill_HRT()
    #We saved the valid tachogramas and their positions
    tachs_all_cond = hrt_pat['tachograms_ok']
    V_pos_tachs_all_cond = hrt_pat['v_pos_tachs_ok']
    
    #And with the periods of 3 minutes before each tachogram along with their positions
    rr_3min_all = hrt_pat['RR_before_V']
    pos_rr_3min_all = hrt_pat['pos_RR_bef_V']    

    #Of all the segments of 3 minutes, we only want those corresponding to the valid tachograms
    #To do this we go through all 3-min segments of RR-intervals before each VPC,
    #and we keep the valid tachograms already corrected (with their corresponding positions and associated labels)
    #and their corresponding 3-min segment of RR previous(with their corresponding positions and associated labels)
    ii = 0
    hrv = HRV()
    for rr_3min,pos_3min,tach,V_pos_tach in zip(rr_3min_all,pos_rr_3min_all,tachs_all_cond,V_pos_tachs_all_cond):
        
       # print ii," de ",len(rr_3min_all)
        
        ii = ii + 1
        
        lab_3min = labels[pos_3min[0]:pos_3min[1]] #get the labels for the actual 3 min seg
        hrv = HRV()
        ind_not_N_beats = hrv.artifact_ectopic_detection(rr_3min, lab_3min, 0.2)
        
        if hrv.is_valid(ind_not_N_beats):
            
            #correction
            rr_corrected = hrv.artifact_ectopic_correction(rr_3min, ind_not_N_beats)
            
            rr_3min_valid.append(rr_3min)
            rr_3min_valid_corrected.append(rr_corrected)
            
            lab_3min_valid.append(lab_3min)
            pos_3min_valid.append(pos_3min)
            
            tachs_all_cond_valid.append(tach)
            V_pos_tachs_all_cond_valid.append(V_pos_tach)
            
            
    #Once we have the 3-minute segments of RR for the corrected tachograms, 
    #we calculate the HRV variables for those segments
    
    #save all variables
    hrv_pat = dict()
    hrv_pat['AVNN'] = []
    hrv_pat['NN50'] = []
    hrv_pat['PNN50'] = []
    hrv_pat['RMSSD'] = []
    hrv_pat['SDNN'] = []
    hrv_pat['SDSD'] = []
    hrv_pat['HRVTriangIndex'] = []
    hrv_pat['logIndex'] = []
    hrv_pat['TINN'] =[]
    
    #spectral indices
    hrv_pat['Ptot'] = []
    hrv_pat['Pulf'] = []
    hrv_pat['Pvlf'] = []
    hrv_pat['Plf'] = []
    hrv_pat['Phf'] = []
    hrv_pat['lfhf_ratio'] = []
    print("HRV corrected ok. Start HRV indexes computing")
    
    for rr_3min in rr_3min_valid_corrected:
        hrv_pat_aux = hrv.load_HRV_variables(rr_3min)
    
        for k in hrv_pat.keys():
            hrv_pat[k].append(hrv_pat_aux[k])
    
    
    #We join the RR segment of 3 minutes together with the corrected valid tachogram associated for each 
    #and save it in a list
    list_rr3_and_tach = []
    for i in range(len(rr_3min_valid_corrected)):
        list_rr3_and_tach.append(list(rr_3min_valid_corrected[i]) + list(tachs_all_cond_valid[i]))
    
    #get the TS,TO,for the valid tachograms according to HRV filtering criteria   
    ts = []
    to = []
    
    for v_pos in hrt_pat['v_pos_tachs_ok']:
        if v_pos in V_pos_tachs_all_cond_valid:
            idx = hrt_pat['v_pos_tachs_ok'].index(v_pos)
            ts.append(hrt_pat['TS'][idx])
            to.append(hrt_pat['TO'][idx])
    
    #get CI and CP and SCL or the valid tachograms according to HRV filtering criteria        
    ci = []  
    cp = []
    scl = []
    
    for tach in tachs_all_cond_valid:
        ci.append(tach[5])
        cp.append(tach[6])
        scl.append(np.mean(tach[:5]))
        
    #Get y_TS and y_TO matrix    
    y_TS = np.array(ts)
    y_TO = np.array(to)
    
    #We save the name associated with each column in labels
    etiquetas = [ident, name]
    for elem in hrv_pat.keys():
        etiquetas.append(elem)
    others = ['scl','ci','cp','ts','to','ts_a','to_a']
    for elem in others:
        etiquetas.append(elem)
    
    #Get X matrix 
    #Get only spectral indices
    
    spectra_idx_keys = ['Ptot', 'Pulf', 'Pvlf', 'Plf', 'Phf', 'lfhf_ratio']
    X = np.array([hrv_pat[l] for l in spectra_idx_keys]).T
    
        
    #We repeat the unique values
    idents = [ident]*len(scl)
    names = [name]*len(scl)
    ts_a = [hrt_pat['TS_average']]*len(scl)
    to_a = [hrt_pat['TO_average']]*len(scl)
    
    #Converted to vector column
    idents_array = np.array(idents)[:,np.newaxis]
    names_array = np.array(names)[:,np.newaxis]
    scl_array = np.array(scl)[:,np.newaxis]
    ci_array = np.array(ci)[:,np.newaxis]
    cp_array = np.array(cp)[:,np.newaxis]
    to_array = np.array(to)[:,np.newaxis]
    ts_array = np.array(ts)[:,np.newaxis]
    to_a_array = np.array(to_a)[:,np.newaxis]
    ts_a_array = np.array(ts_a)[:,np.newaxis]
    
    X = np.concatenate((idents_array, names_array, X, scl_array, ci_array, cp_array, to_array, ts_array, to_a_array, ts_a_array),axis= 1)        
    labels = etiquetas
    return X,y_TS,y_TO,labels

#%%

#get path for ddbb
cwd = os.getcwd()
ddbb_dir = os.path.join(cwd,'ddbb_panda')
os.chdir(ddbb_dir)
for i,file in enumerate(glob.glob("*.txt")):
    
    #counter
    print(ddbb_dir)
    print(i)
    X,y_TS,y_TO,labels = get_HRV_HRT_matrix_for_patient(file,i+1) 
    if i == 0:
                
        X_all = np.array(X)
        y_TS_all = np.array(y_TS)
        y_TO_all = np.array(y_TO)
    
    else:
    
        X_all = np.concatenate((X_all,np.array(X)))
        y_TS_all = np.concatenate((y_TS_all,np.array(y_TS)))        
        y_TO_all = np.concatenate((y_TO_all,np.array(y_TO))) 
    
    
    
