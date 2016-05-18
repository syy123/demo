#!/bin/env python
# -*- coding: cp936 -*-
import numpy as np
import math

def AWGN(B_number,Fs,sigma0,s):
    #AWGN信道
    mu=0         #均值
    sigma=np.sqrt(sigma0)     #标准差
    s11=np.random.normal(mu,sigma,len(s))  
    channel_out=s+s11
    
    channel_out_real = []
    channel_out_imag = []
    channel_out_complex = []
    for i in range(len(channel_out)/Fs/2):
        channel_out_real += list(channel_out[i*Fs : (i+1)*Fs])
        channel_out_imag += list(channel_out[(i+1)*Fs : (i+2)*Fs])
        i += 2
    print 're',len(channel_out_real),len(channel_out_imag)
    for j in range(len(channel_out_imag)):
        channel_out_complex.append(complex(channel_out_real[j], channel_out_imag[j])) 
    
    demo_out = demodulate(channel_out_real,channel_out_imag,B_number,Fs)        
    spec = spectrum(channel_out,Fs)
    
    return channel_out,demo_out[0],demo_out[1],spec[0],spec[1]  #后两个为星座图参数

def demodulate(real_data,imag_data,B_number,Fs):
    data_real_out = []
    data_imag_out = []
    for i in range(Fs/2, len(imag_data), Fs):
        data_real_out.append(real_data[i])
        data_imag_out.append(imag_data[i])
    return data_real_out,data_imag_out
#频谱
def spectrum(data,Fs):
    N = len(data)
    data = data[:N]
    yfr = np.fft.fft(data,N)
    yfr = np.fft.fftshift(yfr)/Fs
    #yfr = np.abs(yfr)
    freqs = np.linspace(-0.5*Fs,0.5*Fs,N)
    return freqs,yfr
'''    
def spectrum(A, Fs):
    N = len(A)
    y = A[:N]
    yfr=np.fft.fft(y,N)
    yfr = np.fft.fftshift(np.abs(yfr))/Fs
    freqs = np.linspace(-0.5*Fs*fs,0.5*Fs*fs,N)
    #yfpr = np.abs(yfr)
    return freqs,yfr
'''