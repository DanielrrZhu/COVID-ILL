# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:46:51 2020

@author: danie
preparition: pip3 install githubdl
             get token from GitHub
             info:http://githubdl.seso.io/
"""
import numpy as np
import pandas as pd
import githubdl
import os
import csv
import shutil 
import copy

# =============================================================================

def download_data(download=True):
    # download data from the Johns Hopkins University COVID-19 dataset
    # https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports_us
      githubdl.dl_dir("https://github.com/CSSEGISandData/COVID-19",
                "csse_covid_19_data", github_token="-------")
      
# =============================================================================

def Process_data(process = True):
          
    cwd = os.getcwd()
    if os.path.exists('ProcessedData.txt')==1:
        os.remove('ProcessedData.txt')
    os.chdir('csse_covid_19_data\csse_covid_19_daily_reports_us')
    filePath = os.getcwd()
    fileNames = os.listdir(filePath)
    del(fileNames[-1])
    fileNum = len(fileNames)
    
    if os.path.exists('ProcessedData.txt')==1:
        print('ProcessedData.txt already exist')
    fp = open('ProcessedData.txt','w')
    info = ['Date   Confirmed_Case\n']
    fp.writelines(info)
    
    for i in range(fileNum):
        with open(fileNames[i],'r') as csvfile:
            Raw_data = csv.reader(csvfile)
            rows= [row for row in Raw_data]
        data=np.array(rows)
    #    print(data)
        for line in data:
            if line[0]=='Illinois':
                Date = fileNames[i]
                Date = Date[0:-4]
                Confirmed_Case = line[5]
                info = [Date,'   ',Confirmed_Case,'\n']
                fp.writelines(info)
    
    fp.close()
    shutil.move('ProcessedData.txt',cwd)
    os.chdir(cwd)
    print(os.getcwd())
    
# =============================================================================
    
def load_data(load = True):
    Raw = pd.read_table("ProcessedData.txt",sep='   ', header=0)
    CaseNum=Raw.drop(columns=['Date'])
    CaseNum=np.array(CaseNum)
    DateNum = len(CaseNum)
    data=np.zeros((DateNum-5,6),dtype=int)
    
    for i in range(DateNum-5):
        data[i,0]=copy.deepcopy(CaseNum[i])
        data[i,1]=copy.deepcopy(CaseNum[i+1])
        data[i,2]=copy.deepcopy(CaseNum[i+2])
        data[i,3]=copy.deepcopy(CaseNum[i+3])
        data[i,4]=copy.deepcopy(CaseNum[i+4])
        data[i,5]=copy.deepcopy(CaseNum[i+5])
    return(data)
# =============================================================================
download_data()
Process_data()
Data = load_data()