# -*- coding: utf-8 -*-
"""
Created on Jul 2020

@author: daniel
preparition: pip3 install githubdl
             get token from GitHub
             replace github_token in data_processing.py line26
             info:http://githubdl.seso.io/
"""
import numpy as np
import matplotlib.pyplot as plt
import data_processing
# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
# =============================================================================
# Load data
data_processing.download_data(download = False) #read preparition
data_processing.Process_data(process = False)
(CaseNum,Data) = data_processing.load_data()
data_processing.dailycasePlot(CaseNum, plot = False)

np.random.shuffle(Data)
sep = int(0.7*np.size(Data,0))
train_data = Data[:sep]
test_data = Data[sep:]
# =============================================================================
# Model
tf_input = tf.placeholder(tf.int32, [None,6], "input")
tfx = tf_input[:, :5]
tfy = tf_input[:, 5]

