# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 21:33:30 2016

@author: Administrator
"""

import wx;
import numpy;
import wx.py.images as images;
import wx.lib.plot as wxPyPlot;
import matplotlib;
import random;
matplotlib.use("WXAgg");
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas;  
from matplotlib.figure import Figure;
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar;


def Rectangle():
    return u'矩形脉冲'
def RaisedCosineBoxName():
    return u'升余弦脉冲'
def PartialBoxName():
    return u'部分响应波形'
def GaussBoxName():
    return u'高斯脉冲'
def GetImpulseChoiceList():
    return [  RaisedCosineBoxName(),PartialBoxName(),GaussBoxName(), Rectangle()];
def PSKBoxName():
    return '2PSK'
def QPSKBoxName():
    return 'QPSK'
def QAMBoxName():
    return '16QAM'
def GetModulateChoiecList():
    return [PSKBoxName(), QPSKBoxName(), QAMBoxName()]
def GetCodeChoiceList():
    return [u'非归零矩形脉冲',u'归零矩形脉冲']
def GetFigureChoiceList():
    return [u'脉冲波形',u'脉冲频谱',u'调制信号波形',u'调制信号频谱',u'星座映射',u'眼图']  
def GetPartialTypeChoiceList():
    return [u'第一类部分响应波形',u'第二类部分响应波形',u'第三类部分响应波形',
            u'第四类部分响应波形',u'第五类部分响应波形']

class SliderBox():
    def __init__(self, parent, id, textName, defaultValue, startValue, endValue, precision, divisor):
        self.staticText = wx.StaticText(parent, id, textName)  #文本框
        self.slider = wx.Slider(parent, id, defaultValue, startValue, endValue, 
                                style = wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        #self.slider.Disable()
        self.slider.SetTickFreq(precision, 1)
        self.textCtrl = wx.TextCtrl(parent, id, str(float(self.slider.GetValue())/divisor))
        self.textCtrl.SetEditable(False)
           
