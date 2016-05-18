# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 21:55:14 2016

@author: zmy
"""

from Head import *;

def GetmoduChoicBoxList():
    return [QPSKname(),modu_othername()]
def QPSKname():
    return 'QPSK';
def modu_othername():
    return u'单频载波'
def GetChannelChoicBoxList():
    return [SosBoxName(),SmithBoxName(), OtherName()];
def SmithBoxName():
    return 'Smith Channel';    
def SosBoxName():
    return 'SOS channel';
def OtherName():
    return u'高斯信道';

def GetAWGNimage():
    return 'image/AWGN.png';
        
def GetRayimage():
    return 'image/ray.png';
    
def GetStartImageLocation():
    return 'startImage/Image.png';
    
def GetChannelfigureBoxList():
    return [u'信道时域波形',u'信道频谱',u'星座图',u'多普勒频谱',u'瑞利概率密度函数',
            u'瑞利信道相位',u'瑞利信道自相关函数'];
    
def GetBalanceBoxList():
    return [u'NLMS均衡算法',u'RLS均衡算法'];
    
def GetBalancefigureBoxList():
    return [u"均衡器导频部分比较(实部虚部)",u"导频-均方误差",
            u"原始数据与均衡输出比较(实部虚部)",u"原始数据与均衡输出-实部比较",
            u"原始数据与均衡输出-虚部比较",u"数据部分-均方误差(不含导频)",
            u"信道输入数据的星座图",u"信道输出数据的星座图",u"均衡器输出数据的星座图"]

def GetSimthBoxName():
    return 'Smith Channel';   
def GetSosBoxName():
    return 'SOS channel';
def OtherBoxName():
    return 'LMS'
def GetPoundNumberBoxName():
    return 'PoundNumber';
def GetRaisedBoxName():
    return 'Raised Cosine Filter';
def GetLMSBoxName():
    return 'LMS'
def GetMultiPathBoxName():
    return 'MultiPath'

