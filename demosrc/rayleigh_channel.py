#!/bin/env python
# -*- coding: cp936 -*-
import numpy as np
import math

#���ж��������ݴ���û�е�Ƶ
def RAYLEIGH(B_number,Fs,n,delay,power,fdts,s):
    #print "Rayleigh"
    # ʱ�Ʋ���
    q0 = delay[n - 1]
    n1 = delay[n - 1] + len(s)
            
    y_in = np.zeros(n1)
    
    for i in range(0, len(s)):
        y_in[q0] = s[i]
        q0 = q0 + 1
    y_out = np.zeros(len(s))

    fm = fdts*Fs  # ��������Ƶ��
    for i in range(0, int(n)):
        f = np.arange(1, 2*fm, 1, np.float)
        y = np.zeros(2*fm-1, np.float)
        for j in range(0, 2*fm-1):
            y[j] = 0.5 / (np.pi * math.sqrt(1 - ((f[j] - fm) / fm) ** 2))  # �����չ����ף�������
        sf = np.zeros(len(s))
        sf1 = y  # �������˲�����Ƶ��
        q1 = -fm 
        for j in range(0, 2*fm-1):
            sf[q1] = y[j]
            q1 = q1 + 1
        x1 = np.random.randn(len(s))
        x2 = np.random.randn(len(s))
        nc1 = np.zeros(len(s), np.complex)
        nc2 = np.zeros(len(s), np.complex)
        nc = np.zeros(len(s))
        for k in range(0, len(s)):
            nc1[k] = np.complex(x1[k], x2[k])
            nc2 = np.fft.ifft(np.fft.fft(nc1) * np.sqrt(sf))  # ͬ�����
            nc = nc2.real
        x3 = np.random.randn(len(s))
        x4 = np.random.randn(len(s))
        ns1 = np.zeros(len(s), np.complex)
        ns2 = np.zeros(len(s), np.complex)
        ns = np.zeros(len(s))
        for k in range(0, len(s)):
            ns1[k] = np.complex(x3[k], x4[k])
            ns2 = np.fft.ifft(np.fft.fft(ns1) * np.sqrt(sf))  # ��������
            ns = ns2.real
        r0 = np.zeros(len(s), np.complex)
        for k in range(0, len(s)):
            r0[k] = np.complex(nc[k], ns[k])
        r = np.zeros(len(s))   
        for k in range(0, len(s)):
            r[k] = np.abs(r0[k])  # �����źŷ�ֵ
        m = delay[n - 1] - delay[i]
        for k in range(0, len(s)):
            y_out[k] = y_out[k] + r[k] * y_in[m + k] * (10 ** (power[i] * 0.1))
    # AWGN�ŵ�
    mu = 0  # ��ֵ
    sigma = 0.5  # ��׼��
    s11 = np.random.normal(mu, sigma, len(s))  
    channel_out = y_out + s11
    
    channel_out = channel_out[20*Fs:(20+B_number)*Fs]
    
    #����ʵ�����鲿
    channel_out_real = []
    channel_out_imag = []
    channel_out_complex = []

    for i in range(len(channel_out)/Fs/2):
        channel_out_real += list(channel_out[i*Fs : (i+1)*Fs])
        channel_out_imag += list(channel_out[(i+1)*Fs : (i+2)*Fs])
        i += 2
   
    for j in range(len(channel_out_imag)):
        channel_out_complex.append(complex(channel_out_real[j], channel_out_imag[j]))    
    
    spec = spectrum(channel_out,Fs)  #Ƶ��
    demo_data_out = demodulate(channel_out_real,channel_out_imag,B_number,Fs)   #����ͼ
    sf = doppler(fdts,Fs)   #������Ƶ��
    
    #�����ܶȺ�������λ
    angle=np.zeros(len(r0))
    for i in range(0,len(r0)):
        angle[i]=math.atan2(np.imag(r0[i]),np.real(r0[i]))
    #����غ���    
    rt=np.correlate(r0,r0,"full")
    t1=np.linspace(-10,10,len(rt))
    #channel = [channel_out_real,channel_out_imag]
    return channel_out,spec[0],demo_data_out[0],sf,r,angle,t1,spec[1],demo_data_out[1],rt # �ŵ����
#Ƶ��
def spectrum(data, Fs):
    N = len(data)  
    yfr=np.fft.fft(data,N)
    yfr = np.fft.fftshift(yfr)
    yfr = np.abs(yfr)
    freqs = np.linspace(-0.5*Fs,0.5*Fs,N)
    return freqs,yfr
    
#���������ͼ
def demodulate(real_data,imag_data,B_number,Fs):
    data_real_out = []
    data_imag_out = []
    for i in range(Fs/2, len(imag_data), Fs):
        data_real_out.append(real_data[i])
        data_imag_out.append(imag_data[i])
    return data_real_out,data_imag_out
    
def doppler(fm,Fs):
    fm = fm*Fs
    f = np.arange(1, 2*fm, 1, np.float)
    y=np.zeros(2*fm-1,np.float)
    for j in range(0,2*fm-1):
        y[j]=0.5/(np.pi*math.sqrt(1-((f[j]-fm)/fm)**2)) #�����չ����ף�������
    sf=y
    return sf    
        
    
    
    
    
    