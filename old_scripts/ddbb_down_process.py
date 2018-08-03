#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:11:05 2018


This file allows to get database and convert to RR intervals

This is a temporary script file.
"""
import wfdb
import os

#get database from physionet

#%% Database Physionet https://www.physionet.org/physiobank/database/nsr2db/

#create a folder



cwd = os.getcwd()
dl_dir = os.path.join(cwd, 'nsr2db')

if  not(os.path.isdir(dl_dir)):
    print("Downloading nsr2db")
# Download all the WFDB content
    wfdb.dl_database('nsr2db', dl_dir=dl_dir)

    print("Downloading nsr2db ended")

else:
    print("Database already downloaded")


#%% Database Physionet https://www.physionet.org/physiobank/database/excluded/
    
cwd = os.getcwd()
dl_dir = os.path.join(cwd, 'excluded')

if  not(os.path.isdir(dl_dir)):
    print("Downloading excluded")
# Download all the WFDB content
    wfdb.dl_database('excluded', dl_dir=dl_dir)

    print("Downloading excluded ended")

else:
    print("Database already downloaded")
    
#%% Database Physionet https://www.physionet.org/physiobank/database/nsrdb/
    
cwd = os.getcwd()
dl_dir = os.path.join(cwd, 'nsrdb')

if  not(os.path.isdir(dl_dir)):
    print("Downloading nsrdb")
# Download all the WFDB content
    wfdb.dl_database('nsrdb', dl_dir=dl_dir)

    print("Downloading nsrdb ended")

else:
    print("Database already downloaded")
    