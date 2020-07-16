#!usr/bin/env python
# encoding:utf-8
from __future__ import division


import math
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau



def pearsonrSim(x, y):
    '''
    皮尔森相似度
    '''
    return pearsonr(x, y)[0]


def spearmanrSim(x, y):
    '''
    斯皮尔曼相似度
    '''
    return spearmanr(x, y)[0]


def kendalltauSim(x, y):
    '''
    肯德尔相似度
    '''
    return kendalltau(x, y)[0]


def cosSim(x, y):
    '''
    余弦相似度计算方法
    '''
    tmp = sum(a * b for a, b in zip(x, y))
    non = np.linalg.norm(x) * np.linalg.norm(y)
    return round(tmp / float(non), 3)


def eculidDisSim(x, y):
    '''
    欧几里得相似度计算方法
    '''
    return math.sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))


def manhattanDisSim(x, y):
    '''
    曼哈顿距离计算方法
    '''
    return sum(abs(a - b) for a, b in zip(x, y))


def minkowskiDisSim(x, y, p):
    '''
    明可夫斯基距离计算方法
    '''
    sumvalue = sum(pow(abs(a - b), p) for a, b in zip(x, y))
    tmp = 1 / float(p)
    return round(sumvalue ** tmp, 3)


def MahalanobisDisSim(x, y):
    '''
    马氏距离计算方法
    '''
    npvec1, npvec2 = np.array(x), np.array(y)
    npvec = np.array([npvec1, npvec2])
    sub = npvec.T[0] - npvec.T[1]
    inv_sub = np.linalg.inv(np.cov(npvec1, npvec2))
    return math.sqrt(np.dot(inv_sub, sub).dot(sub.T))


def jaccardDisSim(x, y):
    '''
    杰卡德相似度计算
    '''
    res = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return res / float(union_cardinality)


if __name__ == '__main__':
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 0, 8, 9]
    print('pearsonrSim:', pearsonrSim(x, y))
    print('spearmanrSim:', spearmanrSim(x, y))
    print('kendalltauSim:', kendalltauSim(x, y))
    print('cosSim:', cosSim(x, y))
    print('eculidDisSim:', eculidDisSim(x, y))
    print('manhattanDisSim:', manhattanDisSim(x, y))
    print('minkowskiDisSim:', minkowskiDisSim(x, y, 2))
    print('MahalanobisDisSim:', MahalanobisDisSim(x, y))
    print('jaccardDisSim:', jaccardDisSim(x, y))
