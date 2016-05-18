#!/bin/env python
# -*- coding: cp936 -*-
from random import randint
import numpy as np
import math

def QPSK(t1):
    fc0=10           
    ml=2
    nb=100                    #input("the length of the array:")
    delta=1/200               #T/200
    fs=200                    #1/delta
    #t1=np.arange(0,50,0.005)  #终值是nb-delta，步长为delta
    #基带信号产生
    data=[]
    for i in range(0,100):         #nb=100
        data.append(randint(0,1))
    #将基带信号变成对应波形信号
    data0=np.zeros(20000)
    k0=0
    for j in range(0,100):       #循环nb=100
        for i in range(0,200):   #循环200次
            data0[k0]=data[j]
            k0=k0+1
    b=2
    datanrz=np.dot(data,b)-1  #极性码
    data1=np.zeros(20000)     #将极性码变成对应的波形信号
    k1=0
    for j in range(0,100):     #循环nb=100
        for i in range(0,200):   #循环200次
            data1[k1]=datanrz[j]
            k1=k1+1
    #串并转换，将奇偶位数据分开
    idata=datanrz[::2]
    qdata=datanrz[1::2]
    #QPSK信号调制
    #I路信号
    ich=np.zeros(10000)
    k2=0
    for j in range(0,50):          #range中不包括终值
        for i in range(0,200):     #向idata中插入200个数
            ich[k2]=idata[j]
            k2=k2+1
    idata1=[]
    a=np.cos(t1*20*np.pi)*math.sqrt(2)
    idata1=ich*a
    #Q路信号
    qch=np.zeros(10000)
    k3=0
    for j in range(0,50):
        for i in range(0,200):
            qch[k3]=qdata[j]
            k3=k3+1
    qdata1=[]
    b=np.sin(t1*20*np.pi)*math.sqrt(2)
    qdata1=qch*b
    #调制信号s
    s=idata1+qdata1
    return data0,s
  
