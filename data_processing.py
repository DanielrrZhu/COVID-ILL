# -*- coding: utf-8 -*-
"""
Created on Jul 2020

@author: daniel
preparition: pip3 install githubdl
             get token from GitHub
             info:http://githubdl.seso.io/
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import githubdl
import os
import csv
import shutil 
import copy

# =============================================================================

def download_data(download=True):
    if download==1:
        # download data from the Johns Hopkins University COVID-19 dataset
        # https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports_us
          githubdl.dl_dir("https://github.com/CSSEGISandData/COVID-19",
                    "csse_covid_19_data", github_token="-------")
      
# =============================================================================

def Process_data(process = True):
    if process==1:
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
    return(CaseNum,data)
# =============================================================================
# ===============PLOT===============
def dailycasePlot(CaseNum, plot = True):
    if plot == 1:
        plt.close('all') 
        font1 = {'family' : 'Times New Roman',
        'weight' : 'normal',
        'size'   : 23,
        }
        
        figsize = 15,9
        figure, ax1 = plt.subplots(figsize=figsize)
        ax1.plot(range(0,len(CaseNum)), CaseNum, color="r", linestyle="-", marker="*", linewidth=1.0, 
                 label='Total case number')
        ax1.legend(loc=2,prop=font1)
        ax1.set_xlabel('Date since April 12',font1)
        ax1.set_ylabel('Confirmed Case in Illinois',font1)
        plt.tick_params(labelsize=23)
        
        CaseNum = CaseNum.T
        ax2 = ax1.twinx()
        Daily_NewCase = np.diff(CaseNum)
        l = np.arange(1, np.size(CaseNum,1), dtype=np.int)
        ax2.plot(l, Daily_NewCase.T, color="b", linestyle="-", marker="*", linewidth=1.0, 
                 label='Daily new case')
        ax2.legend(loc=2,bbox_to_anchor=(0,0.9),prop=font1)
        ax2.set_ylabel('Daily new case number',font1)
        
        plt.tick_params(labelsize=23)
        labels = ax1.get_xticklabels() + ax1.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        plt.show()
        plt.savefig('CaseSummary.png')
    
# =============================================================================
#download_data()
#Process_data()
#(CaseNum,Data) = load_data()
#dailycasePlot(CaseNum)
