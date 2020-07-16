import json
import time
import requests
import re
import mitmproxy.http
import pymysql

'''
视频数据的处理【json格式】
'''
def response(flow: mitmproxy.http.HTTPFlow):
    # /usr/local/Cellar/mitmproxy/5.0.1_1/libexec/bin/python3.8 命令行运行只能在这个python下面 不知道为啥 只能手动导包了
    print('START!!!')

    url = 'https://api3-core-c-lf.amemv.com/aweme/v2/follow/feed/'
    # url = 'https://api3-core-c-lf.amemv.com/aweme/v1/aweme/post/'

    if str(flow.request.url).startswith(url):
        # data = json.loads(flow.response.text)
        # aweme_list = data['aweme_list']
        # # 遍历所有作品
        # for aweme in aweme_list:
        data_list = json.loads(flow.response.text)['data']
        for data in data_list:
            aweme=data['aweme']
            create_time = aweme["create_time"]
            now_time = int(time.time())
            nickname = aweme["author"]["nickname"]
            uid = aweme["author"]["uid"]
            sec_uid = aweme["author"]["sec_uid"]
            statistics = aweme["statistics"]
            comment_count=statistics["comment_count"]
            digg_count=statistics["digg_count"]
            download_count=statistics["download_count"]

            music = aweme["music"]
            music_author=music["author"]
            music_owner_nickname=music["owner_nickname"]
            music_title=music["title"]
            music_duration=music["duration"]
            music_url=music["play_url"]["uri"]
            music_original=music["is_original"]
            music_original_sound=music["is_original_sound"]

            video_dict = aweme['video']
            video_title = re.sub(r'[？.，,。！!\\/:*?"<>|#]', '', aweme['desc'])
            video_url = video_dict['download_addr']['url_list'][0]

            # 在个人信息网页https://www.iesdouyin.com/share/user/{uid}?sec_uid={sec_uid}分析js得知下面这个网址是查询其所有信息的
            self_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=' + sec_uid
            response = requests.get(url=self_url)
            fans = json.loads(response.text)['user_info']["follower_count"]

            print(create_time,now_time,nickname,uid,sec_uid,fans,comment_count,digg_count,download_count,music_author,music_owner_nickname,music_title,music_duration,music_url,music_original,music_original_sound ,video_title, video_url)

            # 连接database
            conn = pymysql.connect(host="localhost",user ="root", password ="root",database ="tiktok_video")
            # 得到一个可以执行SQL语句的光标对象，执行完毕返回的结果集默认以元组显示
            cursor = conn.cursor()
            # 定义要执行的SQL语句  【全都是%s python的string和mysql的string不是一个意思 不能有%d】
            sql = """INSERT INTO Video(create_time,now_time,nickname,uid,sec_uid,fans,comment_count,digg_count,download_count,music_author,music_owner_nickname,music_title,music_duration,music_url,music_original,music_original_sound ,video_title, video_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            values = (create_time, now_time, nickname, uid, sec_uid, fans, comment_count, digg_count, download_count, music_author, music_owner_nickname,music_title, music_duration, music_url, music_original, music_original_sound, video_title, video_url)
            # 执行SQL语句
            cursor.execute(sql, values)
            # 关闭光标对象
            cursor.close()
            # 提交到数据库！不提交数据库里没有
            conn.commit()
            # 关闭数据库连接
            conn.close()
