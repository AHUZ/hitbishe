# !/usr/bin/env python
# -*-coding:utf-8-*-


import numpy
import time
from math import log
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import scale, StandardScaler
from bitarray import bitarray
from matplotlib import pyplot as plt


data = numpy.loadtxt('../dataSets/wafer', delimiter=',')
labels = data[:, 0].astype('int')
data = data[:, 1:]

print labels
# exit()

rows, cols = data.shape

win_size = 9
k = 2


begin = time.clock()
dist_matrix = numpy.zeros((rows, rows))

# find local density
densityVector = numpy.zeros(rows)
dist_cutoff = 8
for i in range(rows):
    for j in range(rows):
        if i == j:
            continue
        dist_matrix[i, j] = numpy.linalg.norm(data[i] - data[j])
        densityVector[i] += numpy.e ** (-(dist_matrix[i, j] / dist_cutoff)**2)

sortedIndex = numpy.argsort(-densityVector)

# find the nn distance of higher local density
distanceVector = numpy.array([float('inf')] * rows)
nnVector = numpy.array([0] * rows)
for i in range(1, rows):
    for j in sortedIndex[:i]:
        if distanceVector[sortedIndex[i]] > dist_matrix[sortedIndex[i], j]:
            distanceVector[sortedIndex[i]] = dist_matrix[sortedIndex[i], j]
            nnVector[sortedIndex[i]] = j

distanceVector[sortedIndex[0]] = max(distanceVector)

# calculating the multiply of the local density and nn distance
density_dist = numpy.argsort(-(densityVector * distanceVector))

clusters = numpy.array([-2] * rows)
# for i in range(k):
#     clusters[density_dist[i]] = i + 1
clusters[density_dist[0]] = 1
clusters[density_dist[1]] = -1
# print clusters

for i in range(rows):
    if clusters[sortedIndex[i]] == -2:
        clusters[sortedIndex[i]] = clusters[nnVector[sortedIndex[i]]]

print clusters
# exit()

# for i in range(rows):
#     if labels[i] == 1:

print 'Precision: %f' % precision_score(labels, clusters, average='macro')
print 'Recall: %f' % recall_score(labels, clusters, average='macro')
print 'F1: %f' % f1_score(labels, clusters, average='macro')
print 'Cost: %f' % (time.clock() - begin)

# f_obj = open('cluster.txt', 'w')
# f_obj.write('density-peak')
# f_obj.write('Precision: %f\n' % precision_score(labels, clusters))
# f_obj.write('Recall: %f\n' % recall_score(labels, clusters))
# f_obj.write('F1: %f\n\n\n\n' % f1_score(labels, clusters))