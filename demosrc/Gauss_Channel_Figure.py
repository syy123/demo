
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 21:33:11 2016

@author: Administrator
"""

import numpy as np;
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 
class GaussChannelFigure():
    
    def __init__(self, panel):
        self.panel = panel;
        self.init_data();
        self.init_dictonary();

    def draw_gauss_channel_figure(self):
        self.panel.Figure.clear()
        for i in range(3):
            if self.panel.images[i]:
                self.panel.Axes = self.panel.Figure.add_subplot(self.panel.count,1,self.panel.images[i])
                self.panel.Axes.set_title(self.title[i],fontproperties=font)
                self.function[i]()
                self.panel.Axes.set_xlabel(self.xLable[i],fontproperties=font)
                self.panel.Axes.grid()
                self.panel.Canvas.draw()
        
    def draw_time_data(self):
        self.panel.Axes.plot(self.xData[0],self.yData[0])  
        
    def draw_freq_data(self):
        self.panel.Axes.plot(self.xData[1], self.yData[1])
        
    def draw_planisphere(self):
        self.panel.Axes.scatter(self.xData[2], self.yData[2])
        self.panel.Axes.plot([-2.0,2],[0,0],'b:',[0,0],[-2.0,2],'b:')
        
    def init_dictonary(self):  
        self.xData = {  
                0: self.xData0,  
                1: self.xData1,  
                2: self.xData2}
                
        self.yData = {  
                0: self.yData0,  
                1: self.yData1,  
                2: self.yData2}
                
        self.title = {  
                0: self.title0,  
                1: self.title1,  
                2: self.title2}
                
        self.xLable = {  
                0: self.xLable0,  
                1: self.xLable1, 
                2: self.xLable2}
                
        self.function = {
                0: self.draw_time_data,  
                1: self.draw_freq_data, 
                2: self.draw_planisphere}
                
    def init_data(self):
        self.yData0 = self.panel.result[0]
        self.xData0 = np.linspace(0, 1.0*self.panel.number/self.panel.rate/self.panel.div, len(self.yData0))
        self.yData1 = self.panel.result[4]
        self.xData1 = self.panel.result[3]
        self.xData2 = self.panel.result[1]
        self.yData2 = self.panel.result[2]
        self.title0 = u'高斯信道时域波形'
        self.title1 = u'高斯信道频谱图'
        self.title2 = u'星座图(AWGN)'
        self.xLable0 = "time / s"
        self.xLable1 = "frequency / f"
        self.xLable2 =  ""
        #freqs = np.linspace(-0.5*Fs*fs,0.5*Fs*fs,N)
        #yfpr = np.abs(yfr)

'''

    def draw_data(self, index):
        if index == 2:
            self.panel.Axes.scatter(self.xData[index], self.yData[index])
        else:
            self.panel.Axes.plot(self.xData[index], self.yData[index])
    
    def draw_channel_time_wave(self):
        t1=np.arange(0,50,0.005)
        awgn=self.panel.result[2]
        self.panel.Axes = self.panel.Figure.add_subplot(1,self.panel.count,self.panel.images[0])
        self.panel.Axes.set_title(u'经过高斯信道的信号时域波形')
        self.panel.Axes.plot(t1,awgn)
        self.panel.Axes.set_xlabel(u"时间/s")
        self.panel.Axes.grid()
        self.panel.Canvas.draw()
        
    def draw_channel_freq(self):
        

        self.panel.frequency = np.linspace(-10.0,10.0,len(yfpr))
        self.panel.Axes = self.panel.Figure.add_subplot(1, self.panel.count, self.panel.images[1])
        self.panel.Axes.plot(self.panel.frequency,yfpr)
        self.panel.Axes.set_title(u'经过高斯信道的信号频谱图')
        self.panel.Axes.set_xlabel(u"频率/f")
        self.panel.Axes.grid()
        self.panel.Canvas.draw()
        
    def draw_star(self):
        awgn_ichsum=self.panel.result[4]
        awgn_qchsum=self.panel.result[5]
        self.panel.Axes = self.panel.Figure.add_subplot(1,self.panel.count,self.panel.images[2])
        self.panel.Axes.set_title(u'星座图(AWGN)')
        self.panel.Axes.scatter(awgn_ichsum, awgn_qchsum)
        self.panel.Axes.grid()
        self.panel.Canvas.draw()        
    
    def initEventMethods(self):  
        self.EventMethods = {  
                0: self.draw_channel_time_wave,  
                1: self.draw_channel_freq,  
                2: self.draw_star}
                
    def drawAWGN(self):
        self.panel.Figure.clear()
        for i in range(3):
            if self.panel.images[i]:
                self.EventMethods[i]()
                '''