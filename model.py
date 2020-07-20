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
(CaseNum,Data_Load) = data_processing.load_data()
data_processing.dailycasePlot(CaseNum, plot = False)
# ========================================================================
No = np.arange(np.size(Data_Load,0))
Data = np.c_[No,Data_Load]
Data = np.array(Data, dtype='float32')

np.random.shuffle(Data)
sep = int(0.7*np.size(Data,0))
train_data = Data[:sep]
test_data = Data[sep:]
# ========================================================================
# Build network
tf_input = tf.placeholder(tf.float32, [None,7], "input")
tfx = tf_input[:, 1:6]
tfy = tf_input[:, 6]

l1 = tf.layers.dense(tfx, 128, tf.nn.relu, name="l1")
l2 = tf.layers.dense(l1, 128, tf.nn.relu, name="l2")
out = tf.layers.dense(l2, 1, name='l3')

loss = tf.reduce_mean(tf.square((tfy - out)))
accuracy = tf.metrics.accuracy(
        labels=tf.argmax(tfy, axis=1), prediction=tf.argmax(out, axis=1),
        )[1]

train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

sess = tf.Session() 
sess.run(tf.global_variables_initializer())
sess.run(tf.local_variables_initializer())

for t in range(4000):
    batch_index = np.random.randint(len(train_data), size=32)
    sess.run(train_step,{tf_input: train_data[batch_index]})
    
    if t%50 ==0:
        acc_, pred_, loss_ = sess.run([accuracy, out, loss],
                                      {tf_input: test_data})
        print("Step: %i" %t, "|Accurate: %.2f"%acc_,"|Loss: %.2f"%loss_,)