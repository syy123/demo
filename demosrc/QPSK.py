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
    #t1=np.arange(0,50,0.005)  #��ֵ��nb-delta������Ϊdelta
    #�����źŲ���
    data=[]
    for i in range(0,100):         #nb=100
        data.append(randint(0,1))
    #�������źű�ɶ�Ӧ�����ź�
    data0=np.zeros(20000)
    k0=0
    for j in range(0,100):       #ѭ��nb=100
        for i in range(0,200):   #ѭ��200��
            data0[k0]=data[j]
            k0=k0+1
    b=2
    datanrz=np.dot(data,b)-1  #������
    data1=np.zeros(20000)     #���������ɶ�Ӧ�Ĳ����ź�
    k1=0
    for j in range(0,100):     #ѭ��nb=100
        for i in range(0,200):   #ѭ��200��
            data1[k1]=datanrz[j]
            k1=k1+1
    #����ת��������żλ���ݷֿ�
    idata=datanrz[::2]
    qdata=datanrz[1::2]
    #QPSK�źŵ���
    #I·�ź�
    ich=np.zeros(10000)
    k2=0
    for j in range(0,50):          #range�в�������ֵ
        for i in range(0,200):     #��idata�в���200����
            ich[k2]=idata[j]
            k2=k2+1
    idata1=[]
    a=np.cos(t1*20*np.pi)*math.sqrt(2)
    idata1=ich*a
    #Q·�ź�
    qch=np.zeros(10000)
    k3=0
    for j in range(0,50):
        for i in range(0,200):
            qch[k3]=qdata[j]
            k3=k3+1
    qdata1=[]
    b=np.sin(t1*20*np.pi)*math.sqrt(2)
    qdata1=qch*b
    #�����ź�s
    s=idata1+qdata1
    return data0,s
  
