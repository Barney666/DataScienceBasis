import os
import requests
from pydub import AudioSegment

# 下载mp3格式音频
def download(vid,mp3_url):
    try:
        if mp3_url is None:
            print('参数错误')
            return None
        file_name = str(vid)+".mp3"      # 以vid作为音频名字 方便之后聚类完贴标签
        save_url = os.path.abspath('.')+'/music/original/'
        file_path = os.path.join(save_url, file_name)
        if not os.path.exists(file_path):   # 文件不存在的话
            # 读取MP3资源
            res = requests.get(mp3_url, stream=True)
            print('开始写入文件：', file_path)
            # 打开本地文件夹路径file_path，以二进制流方式写入，保存到本地
            with open(file_path, 'wb') as fd:
                for chunk in res.iter_content():
                    fd.write(chunk)
            print(file_name + ' 成功下载！')
            convert(file_path)
        else:
            print(file_path+"已存在！")
    except Exception as e:
        print('程序错误:'+str(e))


# 把mp3格式的文件转成wav
# TODO: 有的没法转 商业成曲是加密的mp3文件
def convert(src):
    print('开始转换文件：'+src)
    dst = src.replace("original","wav").replace("mp3","wav")    # 目标文件

    # 如果没转化过
    if os.path.exists(dst)==False:
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
    print('成功转成'+dst)