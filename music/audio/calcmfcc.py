# coding=utf-8
# 计算每一帧的MFCC系数

import numpy
from .sigprocess import audio2frame
from .sigprocess import pre_emphasis
from .sigprocess import spectrum_power
from scipy.fftpack import dct


def calcMFCC_delta_delta(signal, samplerate=16000, win_length=0.025, win_step=0.01, cep_num=13, filters_num=26,
                         NFFT=512, low_freq=0, high_freq=None, pre_emphasis_coeff=0.97, cep_lifter=22,
                         appendEnergy=True):
    '''计算13个MFCC+13个一阶微分系数+13个加速系数,一共39个系数
    '''
    feat = calcMFCC(signal, samplerate, win_length, win_step, cep_num, filters_num, NFFT, low_freq, high_freq,
                    pre_emphasis_coeff, cep_lifter, appendEnergy)  # 首先获取13个一般MFCC系数
    result1 = derivate(feat)
    result2 = derivate(result1)
    result3 = numpy.concatenate((feat, result1), axis=1)
    result = numpy.concatenate((result3, result2), axis=1)
    return result


def calcMFCC_delta(signal, samplerate=16000, win_length=0.025, win_step=0.01, cep_num=13, filters_num=26, NFFT=512,
                   low_freq=0, high_freq=None, pre_emphasis_coeff=0.97, cep_lifter=22, appendEnergy=True):
    '''计算13个MFCC+13个一阶微分系数
    '''
    feat = calcMFCC(signal, samplerate, win_length, win_step, cep_num, filters_num, NFFT, low_freq, high_freq,
                    pre_emphasis_coeff, cep_lifter, appendEnergy)  # 首先获取13个一般MFCC系数
    result = derivate(feat)  # 调用derivate函数
    result = numpy.concatenate((feat, result), axis=1)
    return result


def derivate(feat, big_theta=2, cep_num=13):
    '''计算一阶系数或者加速系数的一般变换公式
    参数说明:
    feat:MFCC数组或者一阶系数数组
    big_theta:公式中的大theta，默认取2
    '''
    result = numpy.zeros(feat.shape)  # 结果
    denominator = 0  # 分母
    for theta in numpy.linspace(1, big_theta, big_theta):
        denominator = denominator + theta ** 2
    denominator = denominator * 2  # 计算得到分母的值
    for row in numpy.linspace(0, feat.shape[0] - 1, feat.shape[0]):
        tmp = numpy.zeros((cep_num,))
        numerator = numpy.zeros((cep_num,))  # 分子
        for t in numpy.linspace(1, cep_num, cep_num):
            a = 0
            b = 0
            s = 0
            row=int(row)
            t=int(t)
            for theta in numpy.linspace(1, big_theta, big_theta):
                theta=int(theta)
                if (t + theta) > cep_num:
                    a = 0
                else:
                    a = feat[row][t + theta - 1]
                if (t - theta) < 1:
                    b = 0
                else:
                    b = feat[row][t - theta - 1]
                s += theta * (a - b)
            numerator[t - 1] = s
        tmp = numerator * 1.0 / denominator
        result[row] = tmp
    return result


def calcMFCC(signal, samplerate=16000, win_length=0.025, win_step=0.01, cep_num=13, filters_num=26, NFFT=512,
             low_freq=0, high_freq=None, pre_emphasis_coeff=0.97, cep_lifter=22, appendEnergy=True):
    '''计算13个MFCC系数
    参数含义：
    signal:原始音频信号，一般为.wav格式文件
    samplerate:抽样频率，这里默认为16KHz
    win_length:窗长度，默认即一帧为25ms
    win_step:窗间隔，默认情况下即相邻帧开始时刻之间相隔10ms
    cep_num:倒谱系数的个数，默认为13
    filters_num:滤波器的个数，默认为26
    NFFT:傅立叶变换大小，默认为512
    low_freq:最低频率，默认为0
    high_freq:最高频率
    pre_emphasis_coeff:预加重系数，默认为0.97
    cep_lifter:倒谱的升个数？？
    appendEnergy:是否加上能量，默认加
    '''

    feat, energy = fbank(signal, samplerate, win_length, win_step, filters_num, NFFT, low_freq, high_freq,
                         pre_emphasis_coeff)
    feat = numpy.log(feat)
    feat = dct(feat, type=2, axis=1, norm='ortho')[:, :cep_num]  # 进行离散余弦变换,只取前13个系数
    feat = lifter(feat, cep_lifter)
    if appendEnergy:
        feat[:, 0] = numpy.log(energy)  # 只取2-13个系数，第一个用能量的对数来代替
    return feat


def fbank(signal, samplerate=16000, win_length=0.025, win_step=0.01, filters_num=26, NFFT=512, low_freq=0,
          high_freq=None, pre_emphasis_coeff=0.97):
    '''计算音频信号的MFCC
    参数说明：
    samplerate:采样频率
    win_length:窗长度
    win_step:窗间隔
    filters_num:梅尔滤波器个数
    NFFT:FFT大小
    low_freq:最低频率
    high_freq:最高频率
    pre_emphasis_coeff:预加重系数
    '''

    high_freq = high_freq or samplerate / 2  # 计算音频样本的最大频率
    signal = pre_emphasis(signal, pre_emphasis_coeff)  # 对原始信号进行预加重处理
    frames = audio2frame(signal, win_length * samplerate, win_step * samplerate)  # 得到帧数组
    spec_power = spectrum_power(frames, NFFT)  # 得到每一帧FFT以后的能量谱
    energy = numpy.sum(spec_power, 1)  # 对每一帧的能量谱进行求和
    energy = numpy.where(energy == 0, numpy.finfo(float).eps, energy)  # 对能量为0的地方调整为eps，这样便于进行对数处理
    fb = get_filter_banks(filters_num, NFFT, samplerate, low_freq, high_freq)  # 获得每一个滤波器的频率宽度
    feat = numpy.dot(spec_power, fb.T)  # 对滤波器和能量谱进行点乘
    feat = numpy.where(feat == 0, numpy.finfo(float).eps, feat)  # 同样不能出现0
    return feat, energy


def log_fbank(signal, samplerate=16000, win_length=0.025, win_step=0.01, filters_num=26, NFFT=512, low_freq=0,
              high_freq=None, pre_emphasis_coeff=0.97):
    '''计算对数值
    参数含义：同上
    '''
    feat, energy = fbank(signal, samplerate, win_length, win_step, filters_num, NFFT, low_freq, high_freq,
                         pre_emphasis_coeff)
    return numpy.log(feat)


def ssc(signal, samplerate=16000, win_length=0.025, win_step=0.01, filters_num=26, NFFT=512, low_freq=0, high_freq=None,
        pre_emphasis_coeff=0.97):
    '''
    待补充
    '''
    high_freq = high_freq or samplerate / 2
    signal = pre_emphasis(signal, pre_emphasis_coeff)
    frames = audio2frame(signal, win_length * samplerate, win_step * samplerate)
    spec_power = spectrum_power(frames, NFFT)
    spec_power = numpy.where(spec_power == 0, numpy.finfo(float).eps, spec_power)  # 能量谱
    fb = get_filter_banks(filters_num, NFFT, samplerate, low_freq, high_freq)
    feat = numpy.dot(spec_power, fb.T)  # 计算能量
    R = numpy.tile(numpy.linspace(1, samplerate / 2, numpy.size(spec_power, 1)), (numpy.size(spec_power, 0), 1))
    return numpy.dot(spec_power * R, fb.T) / feat


def hz2mel(hz):
    '''把频率hz转化为梅尔频率
    参数说明：
    hz:频率
    '''
    return 2595 * numpy.log10(1 + hz / 700.0)


def mel2hz(mel):
    '''把梅尔频率转化为hz
    参数说明：
    mel:梅尔频率
    '''
    return 700 * (10 ** (mel / 2595.0) - 1)


def get_filter_banks(filters_num=20, NFFT=512, samplerate=16000, low_freq=0, high_freq=None):
    '''计算梅尔三角间距滤波器，该滤波器在第一个频率和第三个频率处为0，在第二个频率处为1
    参数说明：
    filers_num:滤波器个数
    NFFT:FFT大小
    samplerate:采样频率
    low_freq:最低频率
    high_freq:最高频率
    '''
    # 首先，将频率hz转化为梅尔频率，因为人耳分辨声音的大小与频率并非线性正比，所以化为梅尔频率再线性分隔
    low_mel = hz2mel(low_freq)
    high_mel = hz2mel(high_freq)
    # 需要在low_mel和high_mel之间等间距插入filters_num个点，一共filters_num+2个点
    mel_points = numpy.linspace(low_mel, high_mel, filters_num + 2)
    # 再将梅尔频率转化为hz频率，并且找到对应的hz位置
    hz_points = mel2hz(mel_points)
    # 我们现在需要知道这些hz_points对应到fft中的位置
    bin = numpy.floor((NFFT + 1) * hz_points / samplerate)
    # 接下来建立滤波器的表达式了，每个滤波器在第一个点处和第三个点处均为0，中间为三角形形状
    fbank = numpy.zeros([filters_num, NFFT // 2 + 1])     # python3中的/结果是float 不能和整数相加 得用//
    for j in range(0, filters_num):
        for i in range(int(bin[j]), int(bin[j + 1])):
            fbank[j, i] = (i - bin[j]) / (bin[j + 1] - bin[j])
        for i in range(int(bin[j + 1]), int(bin[j + 2])):
            fbank[j, i] = (bin[j + 2] - i) / (bin[j + 2] - bin[j + 1])
    return fbank


def lifter(cepstra, L=22):
    '''升倒谱函数
    参数说明：
    cepstra:MFCC系数
    L：升系数，默认为22
    '''
    if L > 0:
        nframes, ncoeff = numpy.shape(cepstra)
        n = numpy.arange(ncoeff)
        lift = 1 + (L / 2) * numpy.sin(numpy.pi * n / L)
        return lift * cepstra
    else:
        return cepstra