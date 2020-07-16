import numpy as np
import pymysql
from functools import cmp_to_key
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sklearn.decomposition import PCA
from music.audio.calcmfcc import *
from music.audio.download import *
from music.dispose.cluster import *


# 数据库操作cursor
conn = pymysql.connect(host="localhost", user="root", password="root", database="tiktok_video")
cursor = conn.cursor()


# 遍历文件夹的所有文件，并存储在一个列表中
def get_filelist(dir):
    files=os.listdir(dir)
    files.sort(key=cmp_to_key(lambda x,y: int(x.split(".")[0]) - int(y.split(".")[0])))  # 按文件名的值排序
    file_list=[]
    for file_name in files:
        if(file_name!='.DS_Store'):
            file_list.append(os.path.join(dir, file_name))
    return file_list

# 根据id看这个音乐的长度
def check_length(vid):
    sql="SELECT music_duration FROM Video WHERE id='%s';" %(vid)
    cursor.execute(sql)
    length = cursor.fetchone()
    return length[0]   # 返回的总是个元组 好烦

#给音乐上标签
def category(vids,labels):
    if len(vids)!=len(labels):
        print("错误输入")
    else:
        for i in range(len(vids)):
            sql="update Video set category='%s' where id='%s';" %(labels[i],vids[i])
            cursor.execute(sql)
            conn.commit()


if __name__ == '__main__':
    # 先下载全部音频 已经下过的会自动跳过
    # print("正在下载全部音频...")
    # sql = "SELECT id,music_url FROM Video"
    # cursor.execute(sql)
    # infos = cursor.fetchall()
    # for info in infos:
    #     download(info[0], info[1])
    # print("全部音频已经下载完毕")

    file_list=get_filelist("music/wav/")     # 得到所有wav音频

    # 根据音频长度分成4类， 0-10s || 10-30s || 30-60s || >60s
    first_length=[]
    second_length=[]
    third_length=[]
    forth_length=[]

    first_reocrd=[]
    second_record=[]
    third_record=[]
    forth_record=[]

    all_length=[]
    all_record=[]

    row_record = []
    for i in range(0,len(file_list)):      # i+1即为id
        mfcc_feat=np.load("music/mfcc_backup/"+str(i+1)+".npy")   # 读取已经保存好的nparray
        row=mfcc_feat.shape[0]
        row_record.append(row)

    min_row=min(row_record)

    for i in range(0,len(file_list)):      # i+1即为id
    #     id = i + 1
    #     (rate, sig) = wav.read(file_list[id-1])
    #     print("正在获取第"+str(id)+"个音频的MFCC系数矩阵...")
    #     mfcc_feat = calcMFCC_delta_delta(sig, rate)    # 获得此音频的MFCC系数,n*39的矩阵
    #     print("已获得第"+str(id)+"个音频的MFCC系数矩阵！")
    #
    #     backup_path="music/mfcc_backup/"+str(id)+".npy"
    #     if not os.path.exists(backup_path):  # 文件不存在的话
    #         np.save(backup_path,mfcc_feat)    # 保存nparray 节省调参后的时间
    #         print(str(id)+".npy已保存！")
    #     else:
    #         print("发现"+str(id)+".npy已存在！")


        mfcc_feat=np.load("music/mfcc_backup/"+str(i+1)+".npy")   # 读取已经保存好的nparray

        # 使用sklearn中的PCA
        # pca = PCA(n_components=10)      # 降成10*39的矩阵
        # resize_matrix = pca.fit_transform(np.transpose(mfcc_feat))
        # resize_matrix = np.transpose(resize_matrix)
        # resize_matrix = resize_matrix.flatten()   # 再拉成一维

        # length=check_length(i+1)    # 第i个音频就是表中id为i+1的视频的bgm
        # if 0<=length<=10:
        #     first_length.append(resize_matrix)
        #     first_reocrd.append(i+1)
        # elif 11<=length<=30:
        #     second_length.append(resize_matrix)
        # elif 31<=length<=60:
        #     third_length.append(resize_matrix)
        # else:
        #     forth_length.append(resize_matrix)

        mfcc_feat = mfcc_feat[:min_row]

        resize_matrix = mfcc_feat.flatten()

        all_length.append(resize_matrix)
        all_record.append(i + 1)


    kmeans_labels, kmeans_cluster_centers_ = k_means(all_length,10)
    # kmeans_labels, kmeans_cluster_centers_ = k_means(first_length,9)

    category(all_record,kmeans_labels)



    conn.close()