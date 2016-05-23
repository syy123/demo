#-*- encoding: utf-8 -*-
'''
Created on 2016年1月27日
@author: Administrator
'''

import numpy as np
import pylab as pl
import nlms_numpy
import zheng_channel as SOS
import rayleigh_channel as smith

from Impulse_Forming import *
import math

def plot_converge(y, u, label=""):
    size = len(u)  # len(u) = 10000, len(y) = 10255
    avg_number = 200  # 每avg_number个取样点计算上一次误差的乘方的平均值
    e = np.power(y[:size] - u, 2)  # e = (y[] - u) ^ 2
    tmp = e[:int(size / avg_number) * avg_number]
    tmp.shape = -1, avg_number  # shape原来是(10000,), 现在是(50, 200)
    avg = np.average(tmp, axis=1)  # 在指定的轴上求加权平均，tmp是(50, 200),其结果是(50,)个平均数。
    pl.plot(np.linspace(0, size, len(avg)), avg, linewidth=2.0, label=label)

def get_complex(re, im):
    complex_data = []
    for i in range(len(re)):
        complex_data.append(complex(re[i], im[i]))
    return complex_data
    
def signal_equation__channel_process_complex(n,delay,power,flag): #,moduflag
    D = 128  # 延时
    
    ImpulseObject = ImpulseForming(20, 80, 50, -4, 4, 0.5, 5);
    pilot_length = ImpulseObject.PilotNumber * ImpulseObject.pixelNumber;
    data_length = ImpulseObject.PulseNumber * ImpulseObject.pixelNumber;
    print "pilot_length = " + str(pilot_length)
    print "data_length = " + str(data_length)
    
   
    UserBinaryData, UserRealY, UserImageY, PilotUserComplexData =  ImpulseObject.PilotUserComplexDataForChannel();
    
    # 创建复数导频+数据
    pilot_add_data_complex = PilotUserComplexData; 
    
    pilot_complex = pilot_add_data_complex[:pilot_length] # 分离导频和数据
    data_complex = pilot_add_data_complex[pilot_length:]
    
    # 导频和数据复数变成实数
    pilot_add_data = []
    for i in range(len(pilot_add_data_complex)):
        pilot_add_data.append(pilot_add_data_complex[i].real)
        pilot_add_data.append(pilot_add_data_complex[i].imag)
                                                        
    pilot = pilot_add_data[:2 * pilot_length]# 导频部分虚实混合
    data = pilot_add_data[2 * pilot_length:] # 数据部分虚实混合
    
    delay_add_zero = np.zeros(D, np.float64) # 在导频前补零的数量
        
    pilot = list(delay_add_zero) + pilot # 导频延时在前补零
 
    data_real_in = []
    data_imag_in = []
    for i in range(len(data_complex)):
        data_real_in.append(data_complex[i].real)
        data_imag_in.append(data_complex[i].imag)
    
    print "len(pilot + delay) = " + str(len(pilot))
    print "len(pilot_add_data) = " + str(len(pilot_add_data))
    
    # 导频和数据过信道
        
    d = pilot[:-D]  # 前
    x = pilot[D:]  # 后channel_in
    print "len(d) = " + str(len(d))
    print "len(x) = " + str(len(x))
    
    pilot_data = channel_in
    if flag==0:
        channelarray_out= SOS.zheng_channel(n,delay,power,pilot_data) # 过信道
        print len(pilot_add_data)
    else:
        channelarray_out= smith.RAYLEIGH(n,delay,power,pilot_data)
    # 测试信道输出长度
    channel_out=channelarray_out[0]
    print "len(channel_out) = " + str(len(channel_out))
    
    h = np.zeros(500, np.float64) # 自适应滤波器长度  抽头个数
    channel_out += np.random.standard_normal(len(channel_out)) * 0 # 加噪声
    
    pilot_out = channel_out[:len(d)]
    data_out = channel_out[len(d):]
    
    print "len(pilot_out) = " + str(len(pilot_out))
    print "len(data_out) = " + str(len(data_out))
    
    # channel_out为参照信号，d为目标信号，h为自适应滤波器的初值，step_size = 0.5为更新系数
    # u = nlms_numpy.nlms(channel_out, d, h, 0.5)
    u, h = nlms_numpy.nlms(pilot_out, d, h, 0.1)   #步长
    
    eq_out = np.convolve(data_out, h)  # 均衡器输出

    eq_out = eq_out[D : D + len(data_out)]
    
    # 信道输出后将data_out变回复数
    data_real_out = []
    data_imag_out = []
    data_complex_out = []
    for i in range(0, len(data_out), 2):
        data_real_out.append(data_out[i])
        data_imag_out.append(data_out[i + 1])
        data_complex_out.append(complex(data_real_out[-1], data_imag_out[-1]))
        
    # 均衡器输出后将eq_out变回复数
    eq_real_out = []
    eq_imag_out = []
    eq_complex_out = []
    for i in range(0, len(eq_out), 2):
        eq_real_out.append(eq_out[i])
        eq_imag_out.append(eq_out[i + 1])
        eq_complex_out.append(complex(data_real_out[-1], data_imag_out[-1]))
    
    ImpulseObject.BinaryJudgement(eq_real_out, eq_imag_out, UserBinaryData);
    
    data_real_in_map = data_real_in[::100] # 每隔100个点取一个数
    data_imag_in_map = data_imag_in[::100]
    
    data_real_out_map = data_real_out[::100]
    data_imag_out_map = data_imag_out[::100]
   
    eq_real_out_map = eq_real_out[::100]
    eq_imag_out_map = eq_imag_out[::100]
    
    #多普勒频谱
    sf=1 
    
    r0=channelarray_out[1]
    angle=np.zeros(len(r0))
    for i in range(0,len(r0)):
        angle[i]=math.atan2(np.imag(r0[i]),np.real(r0[i]))
        
    rt=np.correlate(r0,r0,"full")
    t1=np.linspace(-10,10,len(rt))
    
    channel_out = channelarray_out[0]
    #频谱
    '''
    Fs = 200
    N = len(data_modu)  
    yfr = np.fft.fft(data_modu,N)
    yfr = np.fft.fftshift(yfr)/N
    freqs = np.linspace(-0.5*Fs,0.5*Fs,N)
    yfpr = np.abs(yfr)
    
    N = len(channel_out)
    yfr = np.fft.fft(channel_out,N)
    yfpr0 = np.fft.fftshift(np.abs(yfr))
    print yfpr0
    yfpr = np.zeros(len(yfpr0))
    for i in range(len(yfpr0)):
        yfpr[i] = np.dot(yfpr0[i],yfpr0[i])
  
    print yfpr
    '''
    def spectrum(A, Fs):
        N = len(A)  
        yfr=np.fft.fft(A,N)
        yfr = np.fft.fftshift(yfr)
        yfpr = np.abs(yfr)
        freqs = np.linspace(-0.5*Fs,0.5*Fs,N)
        return freqs,yfpr
   
    yfr = np.fft.fft(channel_out)
    yfr = np.fft.fftshift(yfr)
    yfpr = np.abs(yfr)
    return channelarray_out[0],freqs,data_real_out_map,sf,channelarray_out[2],angle,t1,yfpr,data_imag_out_map,rt,eq_out,eq_real_out, eq_imag_out,data,data_real_in,data_imag_in,data_real_in_map,data_imag_in_map,eq_real_out_map,eq_imag_out_map
    
