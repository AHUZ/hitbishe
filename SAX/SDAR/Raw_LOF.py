# !/usr/bin/env python
# -*-coding:utf-8-*-

import os
import sys
import numpy
import random
from numpy import array, sum, sqrt
import time
from sklearn.metrics import roc_auc_score, euclidean_distances
from sklearn.preprocessing import scale, StandardScaler
from bitarray import bitarray
from matplotlib import pyplot as plt
from LocalOutlierFactor import *

data = numpy.loadtxt('../../dataSets/ionosphere', delimiter=',')
labels = data[:, -1]
data = data[:, :-1]

rows, cols = data.shape
for i in range(rows):
    data[i] = scale(data[i])


# 计算距离矩阵
dist_matrix = euclidean_distances(data)

# 表示方法用在LOF中
d_nlist, d_n = find_kdist(dist_matrix)
rd_matrix = reach_distance(d_nlist, dist_matrix)
lr_vector = lr_density(d_n, rd_matrix)
lof = lo_factor(d_n, lr_vector)

auc = roc_auc_score(labels, lof)

if auc < 0.5:
    print 1-auc
else:
    print auc