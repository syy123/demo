# -*- coding: utf-8 -*-

import numpy as np
import math

#没有导频，只有数据    
def zheng_channel(B_number,Fs,n,delay,power,fm,s):
    #添加高斯噪声
    mu = 0  # 均值
    sigma = 0.1  # 标准差
    s11 = np.random.normal(mu, sigma, len(s))  # 最后的size=10000怎么选取
    y_out = np.zeros(len(s))    
    fs = 100 #采样频率
    Ns = len(s)
    M = 32
    for i in range(0, int(n)):
        r = zheng(fs, fm, Ns, M)
        e = np.abs(r)
        m = np.zeros(int(delay[i]))
        y_in = list(m) + list(s[:len(s) - len(m)])
        for k in range(0, len(s)):
            y_out[k] = y_out[k] + e[k] * y_in[k] * (10 ** (power[i] / 10.0))
    channel_out1 = y_out + s11  #信道输出 
    channel_out = channel_out1[20*Fs:(20+B_number)*Fs]
    
    #分离实部，虚部
    channel_out_real = []
    channel_out_imag = []
    channel_out_complex = []
    print 'c',len(channel_out),len(channel_out)/Fs
    for i in range(len(channel_out)/Fs/2):
        channel_out_real += list(channel_out[i*Fs : (i+1)*Fs])
        channel_out_imag += list(channel_out[(i+1)*Fs : (i+2)*Fs])
        i += 2
    print 're',len(channel_out_real),len(channel_out_imag)
    for j in range(len(channel_out_imag)):
        channel_out_complex.append(complex(channel_out_real[j], channel_out_imag[j]))    
    print 'com',len(channel_out_complex)
    
    spec = spectrum(channel_out_complex,Fs)  #频谱
    demo_data_out = demodulate(channel_out_real,channel_out_imag,B_number,Fs)   #星座图
    sf = doppler(fm,Fs)   #多普勒频移
    
    #概率密度函数，相位
    angle=np.zeros(len(r))
    for i in range(0,len(r)):
        angle[i]=math.atan2(np.imag(r[i]),np.real(r[i]))
    #自相关函数    
    rt=np.correlate(r,r,"full")
    t1=np.linspace(-10,10,len(rt))
    
    return channel_out_complex,spec[0],demo_data_out[0],sf,e,angle,t1,spec[1],demo_data_out[1],rt # 信道输出
  
def zheng(fs, fm, Ns, M):
    N = 4 * M + 2
    c1 = []
    c2 = []
    f = []
    bata = []
    alpha = []
    s = 2 * np.pi * np.random.rand(M) / N
    for n in range(1, M + 1):      
        bata.append(np.pi * n / M)
        alpha.append((2 * np.pi * n - np.pi) / N + s[n - 1])
        c1.append(2 * np.cos(bata[n - 1]))
        c2.append(2 * np.sin(bata[n - 1]))  
        f.append(fm * np.cos(alpha[n - 1]))
    c1.append(1 / np.sqrt(2) * np.cos(np.pi / 4))
    c2.append(1 / np.sqrt(2) * np.sin(np.pi / 4)) 
    f.append(fm)
    angle = 2 * np.pi * np.random.rand(M + 1)
   
    x1 = []
    r = []
    x2 = []
    w = []
    for k in range(Ns):
        ts = 1.0 / fs
        t = k * ts       
        for j in range(len(c1)):           
            w.append(np.cos(2 * np.pi * f[j] * t + angle[j]))
    w0 = np.array(w)
    w0 = w0.reshape(-1, M + 1)
    for n in range(Ns): 
        x1.append(2 / np.sqrt(N) * np.dot(c1, w0[n]))    
        x2.append(-2 / np.sqrt(N) * np.dot(c2, w0[n]))
        r.append(np.complex(x1[n], x2[n]))
    return r #rayli_envelope瑞利仿真器产生的信号包络

#频谱
def spectrum(data, Fs):
    N = len(data)  
    yfr = np.fft.fft(data,N)
    yfr = np.fft.fftshift(yfr)
    yfr = np.abs(yfr)
    freqs = np.linspace(-0.5*Fs,0.5*Fs,N)
    return freqs,yfr
    
#星座图
def demodulate(real_data,imag_data,B_number,Fs):
    data_real_out = []
    data_imag_out = []

    for i in range(Fs/2, len(imag_data), Fs):
        data_real_out.append(real_data[i])
        data_imag_out.append(imag_data[i])
    #a = self.modulateReal[15.0*self.Fs:(self.number*self.Fs/self.div)+5.0*self.Fs:self.Fs]
    #b = self.modulateImage[15.0*self.Fs:(self.number*self.Fs/self.div)+5.0*self.Fs:self.Fs]  
    return data_real_out,data_imag_out
    
def doppler(fm,Fs):
    fm = fm*Fs
    f = np.arange(1, 2*fm, 1, np.float)
    y=np.zeros(2*fm-1,np.float)
    for j in range(0,2*fm-1):
        y[j]=0.5/(np.pi*math.sqrt(1-((f[j]-fm)/fm)**2)) #多普勒功率谱（基带）
    sf=y
    return sf    
        
    
    
    
    
    
    
    
    
    
    
    
    
