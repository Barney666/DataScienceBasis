# coding=utf-8

from proto import python_proto_pb2
import mitmproxy.http

'''
解析抖音推荐视频请求的一个接口返回的protobuf格式数据
'''

def response(flow: mitmproxy.http.HTTPFlow):
    print('START!!!')
    url = 'https://api3-core-c-lf.amemv.com/aweme/v2/feed/'

    if str(flow.request.url).startswith(url):
        data = flow.response.content
        # data = json.loads(flow.response.text)
        video = python_proto_pb2.Video()
        # filename='/Users/barney/PycharmProjects/DataScienceBasis/protobufData'
        # buf = bytearray(os.path.getsize(filename))
        # with open(filename, 'rb') as f:
        #     f.readinto(buf)
        #     print(buf)
        # f.close()
        # string=''
        # file=open(filename,'r')
        # string=file.read()
        # file.close()
        # print(string.encode('utf-8'))
        video.ParseFromString(data)
        # video.ParseFromString(string.encode('utf-8'))
        print(video.aweme_list)