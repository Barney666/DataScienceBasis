import matplotlib.pyplot as plt
import librosa.display
import numpy as np
from pydub import AudioSegment

'''
提取音乐频谱并可视化
'''

# 1秒=1000毫秒
SECOND = 1000
# 音乐文件
AUDIO_PATH = 'music/original/edf69476c8d6d8c045914add64decb85.mp3'


def split_music(begin, end, filepath):
    # 导入音乐
    song = AudioSegment.from_mp3(filepath)

    # 取begin秒到end秒间的片段
    song = song[begin * SECOND: end * SECOND]

    # 存储为临时文件做备份
    temp_path = filepath.replace("original","backup")
    song.export(temp_path)

    return temp_path


music, sr = librosa.load(split_music(0, 1, AUDIO_PATH))

# 进一步放大，比如说0.9秒到1秒之间的频谱：
n0 = 9000
n1 = 10000

music = np.array([mic for mic in music if mic > 0])
# 宽高比为14:5的图
plt.figure(figsize=(14, 5))
plt.plot(music[n0:n1])
plt.grid()
plt.show()

