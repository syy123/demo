# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:48:00 2016

@author: Administrator
"""
import numpy
import numpy as np
from random import randint
def binarysource(N):
    binarydata=[]
    for i in range(N):
        binarydata.append(randint(0,1))
    return binarydata



def Raised_cosine_time(a, x, fs):
    #label = '\begin{displaymath}c^{2}=a^{2}+b^{2}\end{displaymath}'
    #label = r'$h(t)=S_a(\pi t/T_b)\frac{cos(\alpha\pi t/T_b)}{1-(2\alpha t/T_b)^2}$'
    label =  r'$h(t)=S_a(\pi t/T_b)\frac{cos(\alpha\pi t/T_b)}{1-(2\alpha t/T_b)^2}$'
    func = (numpy.sin(numpy.pi * x* fs) / (numpy.pi * x*fs)) * (numpy.cos(a * numpy.pi * x*fs) / (1 - 4 * a **2 * x ** 2 *fs**2))
    return label,func
def Partial_Response_Time_Func(Type,x,fs):        
    if Type == 1:
        label = r'$g(t)=S_a(\frac{\pi t}{T_b})+2S_a(\frac{\pi (t-T_b)}{T_b})+S_a(\frac{\pi (t-2T_b)}{T_b})$'
        func = numpy.sin(numpy.pi*x*fs)/(numpy.pi*x*fs)+2*numpy.sin(numpy.pi*fs*(x-1.0/fs))/(numpy.pi*fs*(x-1.0/fs))+numpy.sin(numpy.pi*fs*(x-2.0/fs))/(numpy.pi*fs*(x-2.0/fs))
    elif Type == 2:
        label = r'$g(t)=2S_a(\frac{\pi t}{T_b})+S_a(\frac{\pi (t-T_b)}{T_b})-S_a(\frac{\pi (t-2T_b)}{T_b})$'
        func = 2*numpy.sin(numpy.pi*x*fs)/(numpy.pi*x*fs)+numpy.sin(numpy.pi*fs*(x-1.0/fs))/(numpy.pi*fs*(x-1.0/fs))-numpy.sin(numpy.pi*fs*(x-2.0/fs))/(numpy.pi*fs*(x-2.0/fs))
    elif Type == 3:
        label = r'$g(t)=S_a(\frac{\pi t}{T_b})-S_a(\frac{\pi (t-T_b)}{2T_b})$'
        func = 1*numpy.sin(numpy.pi*x*fs)/(numpy.pi*x*fs)-numpy.sin(numpy.pi*fs*(x-2.0/fs))/(numpy.pi*fs*(x-2.0/fs))
    elif Type == 4:
        label = r'$g(t)=-S_a(\frac{\pi t}{T_b})+2S_a(\frac{\pi (t-2T_b)}{T_b})-S_a(\frac{\pi (t-4T_b)}{T_b})$'
        func =(-1)*numpy.sin(numpy.pi*x*fs)/(numpy.pi*x*fs)+2*numpy.sin(numpy.pi*fs*(x-2.0/fs))/(numpy.pi*fs*(x-2.0/fs))-numpy.sin(numpy.pi*fs*(x-4.0/fs))/(numpy.pi*fs*(x-4.0/fs))
    else:
        label = r'$g(t)=S_a(\frac{\pi t}{T_b})+S_a(\frac{\pi (t-T_b)}{T_b})$'
        func = numpy.sin(numpy.pi*x*fs)/(numpy.pi*x*fs)+numpy.sin(numpy.pi*fs*(x-1.0/fs))/(numpy.pi*fs*(x-1.0/fs))
    return label, func
def Gauss_Time_Distribution(sigma, x, fs):
    label =r'$g(t)=\frac{1}{\sqrt{2\pi {\sigma}^2}}e^{-\frac{t^2}{2{\sigma}^2}}$'
    #label = u'高斯'
    func = 1.0 / (numpy.sqrt(2 * numpy.pi) * sigma) * numpy.exp(-(x ** 2*fs**2) / (2 * sigma ** 2))
    return label, func
   
def Impulse_time(case, a, x, Fs, fs, Type1, sigma, Type2, ratio):
    if case == 0:
        label,impulse = Raised_cosine_time(a, x, fs)
    elif case == 1:
        label,impulse = Partial_Response_Time_Func(Type1,x,fs)
    elif case == 2:
        label,impulse = Gauss_Time_Distribution(sigma, x, fs)
    else:
        label,impulse = Code_time(Type2,x,Fs, fs,ratio)
    return label,impulse

def DoConvolution(leftData, rightData):
    return numpy.convolve(leftData, rightData);
def Single_NRZ(x, fs):   
    func = numpy.zeros(len(x))
    for i in range(len(x)):
        if (x[i]<=1.0/fs)and(x[i]>=0) :
            func[i] = 1
        else:
            func[i] = 0
    return func
def Double_NRZ(x, fs):
    func = numpy.zeros(len(x))
    for i in range(len(x)):
        if (x[i]<1.0/fs)and(x[i]>0) :
            func[i] = 1
        else:
            func[i] = -1
    return func
def Single_RZ(x,Fs,fs,ratio):
    func = numpy.zeros(len(x))
    for i in range(len(x)):
        if (x[i]<=1.0*ratio/Fs/fs)and(x[i]>=0) :
            func[i] = 1                  
        else:
            func[i] = 0
    return func  
def Double_RZ(x,fs,ratio):
    func = numpy.zeros(len(x))
    for i in range(len(x)):
        if (x[i]<=1.0*ratio/16/fs)and(x[i]>=0) :
            func[i] = 1                  
        else:
            func[i] = -1
    return func  
def Code_time(case, x, Fs, fs,ratio):
    if case == 0:
        label = u'非归零矩形脉冲'
        code = Single_NRZ(x,fs)
    elif case == 1:
        label = u'归零矩形脉冲'
        code = Single_RZ(x,Fs, fs,ratio)
    return label,code  
    

def ModulateType(modulatetype, number, sample):
    if modulatetype == 0:
        div = 1
        realsignal,imagesignal = CreatePskBinary(number, sample)
    elif modulatetype == 1:
        div = 2
        realsignal,imagesignal = CreateQpskBinary(number, sample)
    else:
        div = 4
        realsignal,imagesignal = CreateQamBinary(number, sample)
    return realsignal, imagesignal,div

def CreatePskBinary(number, sample):
    data=binarysource(number)
    A=[]
    B=[]
    for i in range(len(data)):
        if(data[i]==0):
            A.append(-1)
            for j in range(sample-1):
                A.append(0)
            B.append(0)
            for j in range(sample-1):
                B.append(0)
        else:
            A.append(1)
            for j in range(sample-1):
                A.append(0)
            B.append(0)
            for j in range(sample-1):
                B.append(0)
    return A,B

def CreateQpskBinary(number, sample):
    randomNumber=binarysource(number)
    RealArray = [];
    ImageArray = [];
    ArrayLength = 0;
    m = 1.0/np.sqrt(2)
    if (len(randomNumber) % 2 == 1):
        ArrayLength = len(randomNumber) - 1;
    elif (len(randomNumber) % 2 == 0):
        ArrayLength = len(randomNumber);            
    for i in range(0, ArrayLength, 2):
        CurrentData = randomNumber[i] * 2 + randomNumber[i + 1];
        if (CurrentData == 0):
            RealNumber = -1*m;
            ImageNumber = -1*m;
        elif (CurrentData == 1):
            RealNumber = -1*m;
            ImageNumber = 1*m;
        elif (CurrentData == 2):
            RealNumber = 1*m;
            ImageNumber = -1*m;
        elif (CurrentData == 3):
            RealNumber = 1*m;
            ImageNumber = 1*m;               
        for j in range(1):
            RealArray.append(RealNumber);
            ImageArray.append(ImageNumber);
        for j in range(1, sample):
            RealArray.append(0);
            ImageArray.append(0);                               
    return RealArray, ImageArray

def CreateQamBinary(number,sample):
    data=binarysource(number)
    A=[]
    B=[]
    m=1.0/np.sqrt(10)
    i=0
    while(i<number):
        if((data[i]==0)and(data[i+1]==0)and(data[i+2]==0)and(data[i+3]==0)):
            A.append(3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(3*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==0)and(data[i+1]==0)and(data[i+2]==0)and(data[i+3]==1)):
            A.append(1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(3*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==0)and(data[i+1]==0)and(data[i+2]==1)and(data[i+3]==1)):
            A.append(-1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(3*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==0)and(data[i+1]==0)and(data[i+2]==1)and(data[i+3]==0)):
            A.append(-3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(3*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==0)and(data[i+1]==1)and(data[i+2]==1)and(data[i+3]==0)):
            A.append(-3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==0)and(data[i+1]==1)and(data[i+2]==1)and(data[i+3]==1)):

            A.append(-1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==0)and(data[i+1]==1)and(data[i+2]==0)and(data[i+3]==1)):
            A.append(1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==0)and(data[i+1]==1)and(data[i+2]==0)and(data[i+3]==0)):
            A.append(3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==1)and(data[i+2]==0)and(data[i+3]==0)):
            
            A.append(3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==1)and(data[i+2]==0)and(data[i+3]==1)):
            A.append(1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==1)and(data[i+2]==1)and(data[i+3]==1)):
            A.append(-1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==1)and(data[i+2]==1)and(data[i+3]==0)):
            A.append(-3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-1*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==0)and(data[i+2]==1)and(data[i+3]==0)):
            A.append(-3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-3*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==0)and(data[i+2]==1)and(data[i+3]==1)):
            A.append(-1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-3*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==0)and(data[i+2]==0)and(data[i+3]==1)):
            A.append(1*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-3*m)
            for j in range(sample-1):
                B.append(0)
        elif((data[i]==1)and(data[i+1]==0)and(data[i+2]==0)and(data[i+3]==0)):
            A.append(3*m)
            for j in range(sample-1):
                A.append(0)
            B.append(-3*m)
            for j in range(sample-1):
                B.append(0)
        i=i+4
    return A,B

'''频谱函数'''
def spectrum(A, Fs, fs):
    N = len(A)
    y = A[:N]
    yfr=np.fft.fft(y,N)
    yfr = np.fft.fftshift(np.abs(yfr))/Fs/fs
    freqs = np.linspace(-0.5*Fs*fs,0.5*Fs*fs,N)
    #yfpr = np.abs(yfr)
    return freqs,yfr

def modulate(a,b,t,Fc):
    #t = numpy.linspace(-10.0/fs, (1.0*number/div/fs)+(10.0/fs), len(a))
    idata=a*np.cos(2*np.pi*Fc*t)
    qdata=b*np.sin(2*Fc*t*np.pi-0.5*np.pi)
    y=(idata+qdata)
    return y,idata,qdata
    
