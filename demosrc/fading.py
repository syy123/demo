# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math as math
from numpy import fft
from scipy import fftpack
from scipy import special
import matplotlib.pyplot as pl
from matplotlib import rcParams
from scipy.stats import rayleigh
import commbase as cb

#font = FontProperties(fname=r"c:\windows\fonts\stzhongs.ttf", size=14)

channel_in = []
Fs = 0

def get_value(obj):
    global channel_in
    global Fs
    channel_in = obj.channel_in
    Fs = obj.Fs
    
def flat_fader_Clarke(maxIter, fDTs, K = 0, pathCount = 50, seed = None):
    '''
    该程序利用clarke模型来产生单径的平坦型瑞利衰落信道
    输入变量说明：
      fDTs：归一化最大多普勒频移（使用采样频率归一化）
      K：   莱斯因子，该值为0表示瑞利衰落，否则生成莱斯衰落，
            物理含义是LOS路径与其他NLOS路径的功率之比
      N：   散射路径数目
      seed：随机数种子，该值为0将采用机器时间最为随机数种子
    '''
    np.random.seed(seed)
    scale_sin = math.sqrt(2.0/pathCount)
    f_nlos = math.sqrt(1/(K+1))
    f_los = math.sqrt(K/(K+1))
    phi = 2 * math.pi * np.random.random_sample(pathCount) - math.pi
    theta_los = 2 * math.pi * np.random.random_sample() - math.pi
    phi_los = 2 * math.pi * np.random.random_sample() - math.pi
    count = 0
    while count < maxIter:
        Hi = 0
        Hq = 0
        for path_idx in range(pathCount):
            alpha = 2 * math.pi * np.random.random_sample() - math.pi
            Hi += math.cos(2*math.pi*fDTs*count*math.cos(alpha) + phi[path_idx])
            Hq += math.sin(2*math.pi*fDTs*count*math.cos(alpha) + phi[path_idx])
        Hi = scale_sin * Hi
        Hq = scale_sin * Hq

        if K > 0:
            Ri = math.cos(2*math.pi*fDTs*count*math.sin(theta_los) + phi_los)
            Rq = math.sin(2*math.pi*fDTs*count*math.sin(theta_los) + phi_los)
            yield complex(f_nlos*Hi + f_los*Ri, f_nlos*Hq + f_los*Rq)
        else:
            yield complex(Hi, Hq)
        count += 1

def flat_fader_Xiao(maxIter, fDTs, K = 0, pathCount = 10, seed = None):
    '''
    该程序利用改进的jakes模型来产生单径的平坦型瑞利衰落信道
    Yahong R.Zheng and Chengshan Xiao "
    Improved Models for the Generation of Multiple Uncorrelated Rayleigh Fading Waveforms" 
    IEEE Commu letters, Vol.6, NO.6, JUNE 2002
    输入变量说明：
      fDTs：归一化最大多普勒频移（使用采样频率归一化）
      K：   莱斯因子，该值为0表示瑞利衰落，否则生成莱斯衰落，
            物理含义是LOS路径与其他NLOS路径的功率之比
      N：   散射路径数目，参见参考文献的公式(1)，
      seed：随机数种子，该值为0将采用机器时间最为随机数种子
    '''
    np.random.seed(seed)
    scale_sin = math.sqrt(2.0/pathCount)
    f_nlos = math.sqrt(1/(K+1))
    f_los = math.sqrt(K/(K+1))
    phi = 2 * math.pi * np.random.random_sample(pathCount) - math.pi
    psi = 2 * math.pi * np.random.random_sample(pathCount) - math.pi
    theta_los = 2 * math.pi * np.random.random_sample() - math.pi
    phi_los = 2 * math.pi * np.random.random_sample() - math.pi
    count = 0
    while count < maxIter:
        Hi = 0
        Hq = 0
        for path_idx in range(pathCount):
            theta = 2 * math.pi * np.random.random_sample() - math.pi
            alpha = (2*math.pi*(path_idx+1) - math.pi + theta)/(4*pathCount)
            Hi += math.cos(2*math.pi*fDTs*count*math.cos(alpha) + phi[path_idx])
            Hq += math.cos(2*math.pi*fDTs*count*math.sin(alpha) + psi[path_idx])
        Hi = scale_sin * Hi
        Hq = scale_sin * Hq

        if K > 0:
            Ri = math.cos(2*math.pi*fDTs*count*math.cos(theta_los) + phi_los)
            Rq = math.sin(2*math.pi*fDTs*count*math.cos(theta_los) + phi_los)
            yield complex(f_nlos*Hi + f_los*Ri, f_nlos*Hq + f_los*Rq)
        else:
            yield complex(Hi, Hq)
        count += 1

def flat_fader_RWP(maxIter, fDTs, K = 0, pathCount = 8, seed = None):
    """
    依据参考文献A Compact Rayleigh and Rician Fading Simulator Based on
    Random Walking Processes》描述的方法产生平坦衰落
    fDTs：归一化最大多普勒频移（使用采样频率归一化）
    K：   莱斯因子，该值为0表示瑞利衰落，否则生成莱斯衰落，
          物理含义是LOS路径与其他NLOS路径的功率之比
    N：   散射路径数目，参见参考文献的公式(1)，
    seed：随机数种子，该值为0将采用机器时间最为随机数种子
    """
    np.random.seed(seed)
    delta = math.pow(0.00125*fDTs, 1.1) # delta approximated from Table 2
    theta = 2 * math.pi * np.random.random_sample() - math.pi
    scale_sin = math.sqrt(2.0/pathCount)
    f_nlos = math.sqrt(1/(K+1))
    f_los = math.sqrt(K/(K+1))
    phi = 2 * math.pi * np.random.random_sample(pathCount) - math.pi
    psi = 2 * math.pi * np.random.random_sample(pathCount) - math.pi
    theta_los = 2 * math.pi * np.random.random_sample() - math.pi
    phi_los = 2 * math.pi * np.random.random_sample() - math.pi
    count = 0
    while count < maxIter:
        Hi = 0
        Hq = 0
        for path_idx in range(pathCount):
            alpha = (2*math.pi*(path_idx+1) - math.pi + theta)/(4*pathCount)
            phi_ = 2 * math.pi * np.random.random_sample() - math.pi
            psi_ = 2 * math.pi * np.random.random_sample() - math.pi
            Hi += math.cos(2*math.pi*fDTs*count*math.cos(alpha) + phi[path_idx])
            Hq += math.cos(2*math.pi*fDTs*count*math.sin(alpha) + psi[path_idx])
        Hi = scale_sin * Hi
        Hq = scale_sin * Hq

        if K > 0:
            Ri = math.cos(2*math.pi*fDTs*count*math.cos(theta_los) + phi_los)
            Rq = math.sin(2*math.pi*fDTs*count*math.cos(theta_los) + phi_los)
            yield complex(f_nlos*Hi + f_los*Ri, f_nlos*Hq + f_los*Rq)
        else:
            yield complex(Hi, Hq)

        count += 1
        theta += delta*np.random.random_sample()
        if theta >= math.pi:
            theta = math.pi
            delta = -delta

        if theta <= -math.pi:
            theta = -math.pi
            delta = -delta

def autocorrelation(x, lags):
    '''
    #计算lags阶以内的自相关系数，返回lags个值，将序列均值、标准差视为不变
    '''
    n = len(x)
    x = np.array(x)
    v = x.var()
    x = x - x.mean()
    r = np.correlate(x,x,'full')[n-1:n+lags-1]/(v*(np.arange(n-1,n-1-lags,-1)))
    return r

def crosscorrelation(x, y, lags):
    '''
    #计算lags阶以内的自相关系数，返回lags个值，将序列均值、标准差视为不变
    '''
    n = len(x)
    x = np.array(x)
    y = np.array(y)
    v = x.std() * y.std()
    x = x - x.mean()
    y = y - y.mean()
    r = np.correlate(x,y,'full')[n-1:n+lags-1]/(v*(np.arange(n-1,n-1-lags,-1)))
    return r

maxIter = channel_in
fDTs    = 10
K       = 100
rl = list()
for i in flat_fader_RWP(maxIter, fDTs):
    rl.append(i)

rr = list()
for i in flat_fader_RWP(maxIter, fDTs, K):
    rr.append(i)

rli = [i.real for i in rl]
rlq = [i.imag for i in rl]
rlm = [abs(i) for i in rl]
rrm = [abs(i) for i in rr]
'''
rcParams['font.family'] = 'STZhongSong'
rcParams['axes.titlesize'] = 20
'''
pl.subplot(221)
pl.title(u"平坦衰落幅度,$f_DT_s=%f$" % fDTs)
pl.semilogy(rlm, label=u'瑞利衰落仿真')
pl.semilogy(rrm, label=u'莱斯衰落仿真($K=100$)')
pl.legend()

pl.subplot(224)
pl.title(u"瑞利衰落仿真的相关统计特性")
ref = special.j0([2*np.pi*fDTs*m for m in range(maxIter//10)])#2*np.pi*fDTs*range(maxIter))
acf_i = autocorrelation(rli, maxIter//10)
acf_q = autocorrelation(rlq, maxIter//10)
ccf = crosscorrelation(rli, rlq, maxIter//10)
pl.plot(acf_i, label=u'I分量自相关ACF')
pl.plot(acf_q, label=u'Q分量自相关ACF')
pl.plot(ccf, label=u'IQ分量互相关CCF')
pl.plot(ref, label=u'0阶第一类贝塞尔函数')
pl.legend()

pl.subplot(222)
pl.title(u"单频正弦波通过瑞利仿真信道后的频谱")
fff,fspe = cb.Spectrum(rl, 1)    #ts??? 对频谱的影响？
pl.plot(fff,fspe, label=u'幅度')
pl.legend()

pl.subplot(223)
pl.title("pdf")
x = np.linspace(rayleigh.ppf(0), rayleigh.ppf(0.9999), 500)
pl.plot(x, rayleigh.pdf(x), 'r-', lw=5, alpha=0.6, label=u'瑞利分布')
p,t2 = np.histogram(rlm, bins=100, range=(rayleigh.ppf(0), rayleigh.ppf(0.9999)), normed=True)
t2 = (t2[:-1] + t2[1:])/2
pl.stem(t2, p) # 绘制统计所得到的概率密度  , label=u'仿真信道'
pl.legend()
'''
pl.subplot(224)
pl.title("CDF")
pl.plot(x, rayleigh.cdf(x), 'r-',  lw=5, alpha=0.6, label=u'理论模型')
pl.stem(t2, np.add.accumulate(p)*(t2[1]-t2[0]))
#, lw=5, label=u'仿真信道'
pl.legend()
'''
pl.show()
