#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 23:06:27 2019

Train ai with features.

@author: me
"""

import _pickle
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
import numpy as np
from sklearn.model_selection import train_test_split

features = np.load("sign_features.npy")
target = np.load("sign_target.npy")

bad = np.load("false_features.npy")
good = np.load("right_features.npy")

bad = bad[np.random.choice(len(bad),len(good),replace=False),:]
features = np.concatenate((features,bad,good), axis=0)
target = np.concatenate((target,np.zeros(len(bad)),np.ones(len(good))))

num_one = np.count_nonzero(target)
print("Number of arrows ", num_one)
print("Number of non arrows ",len(target)-num_one)

x_train, x_test, y_train, y_test = train_test_split(features,target,test_size=0.1)

kernel = 1.0 * RBF(1.0)
#gpc = GaussianProcessClassifier(kernel=kernel, random_state=0).fit(features, target)
gpc = GaussianProcessClassifier(kernel=kernel, random_state=0).fit(x_train, y_train)

score = gpc.score(x_train,y_train)
print("Accuracy of training data: ",score)
print('Accuracy on the testing subset:',format(gpc.score(x_test,y_test)))

with open("sign_ai.pkl","wb") as f:
    _pickle.dump(gpc,f)

print("done")
