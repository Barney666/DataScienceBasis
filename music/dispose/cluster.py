import os, codecs
import shutil
import matplotlib.pyplot as plt
import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist


def k_means(features, cluster_nums, randomState=True):

    input_x = np.array(features)
    print('数据维数', input_x.shape)

    # k-means聚类
    kmeans = KMeans(n_clusters=cluster_nums, max_iter=50000000)
    kmeans.fit(input_x)
    label_pred = kmeans.labels_

    # # 绘制k-means结果
    # x0 = input_x[label_pred == 0]
    # x1 = input_x[label_pred == 1]
    # x2 = input_x[label_pred == 2]
    # x3 = input_x[label_pred == 3]
    # x4 = input_x[label_pred == 4]
    # x5 = input_x[label_pred == 5]
    # x6 = input_x[label_pred == 6]
    # x7 = input_x[label_pred == 7]
    # x8 = input_x[label_pred == 8]
    # x9 = input_x[label_pred == 9]
    # plt.figure(2)
    # plt.scatter(x0[:, 0], x0[:, 1], c="red", marker='o', label='label0')
    # plt.scatter(x1[:, 0], x1[:, 1], c="green", marker='*', label='label1')
    # plt.scatter(x2[:, 0], x2[:, 1], c="blue", marker='+', label='label2')
    # plt.scatter(x3[:, 0], x3[:, 1], c="black", marker='p', label='label3')
    # plt.scatter(x4[:, 0], x4[:, 1], c="green", marker='d', label='label4')
    # plt.scatter(x5[:, 0], x5[:, 1], c="yellow", marker='8', label='label5')
    # plt.scatter(x6[:, 0], x6[:, 1], c="cyan", marker='s', label='labe6')
    # plt.scatter(x7[:, 0], x7[:, 1], c="magenta", marker='D', label='label7')
    # plt.scatter(x8[:, 0], x8[:, 1], c="blue", marker='<', label='label8')
    # plt.scatter(x9[:, 0], x9[:, 1], c="red", marker='|', label='label9')
    # plt.xlabel('petal length')
    # plt.ylabel('petal width')
    # plt.legend(loc=2)
    # plt.show()

    # mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    # plt.plot(kmeans.cluster_centers_)
    # plt.plot(kmeans.labels_)
    # plt.show()
    return kmeans.labels_, kmeans.cluster_centers_

# def main():
#     path_filenames = get_file_name("/Users/barney/Desktop/1/")
#
#     labels, cluster_centers = knn_detect(path_filenames, 2)
#     # labels, cluster_centers = knn_detect(path_filenames, 3)
#     # labels, cluster_centers = knn_detect(path_filenames, 6)
#
#     res_dict = res_fit(path_filenames, labels)
#     # save('./', 'knn_res.txt', res_dict)
#     # save('./','cluster.txt',res_dict)
#     # save('./', 'cluster_3.txt', res_dict)
#     # painter(labels,cluster_centers,result,input_x)
#
#