# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:17:55 2016

@author: Administrator
"""
import wx
from Configure import *

class SliderBox():
    def __init__(self, parent, id, textName, defaultValue, startValue, endValue, precision, divisor):
        self.staticText = wx.StaticText(parent, id, textName)  #文本框
        self.slider = wx.Slider(parent, id, defaultValue, startValue, endValue, 
                                style = wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)
        #self.slider.Disable()
        self.slider.SetTickFreq(precision, 1)
        self.textCtrl = wx.TextCtrl(parent, id, str(float(self.slider.GetValue())/divisor))
        self.textCtrl.SetEditable(False)
        