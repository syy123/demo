# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 21:33:11 2016

@author: Administrator
"""

import numpy as np;


class GaussChannelFigure():
    
    def __init__(self, panel):
        self.panel = panel;
        self.initEventMethods()
        
    def draw_channel_time_wave(self):
        t1=np.arange(0,50,0.005)
        awgn=self.panel.result[2]
        #self.panel.Axes.clear() 
        self.panel.Axes = self.panel.Figure.add_subplot(1,self.panel.count,self.panel.images[0])
        self.panel.Axes.set_title(u'经过高斯信道的信号时域波形')
        self.panel.Axes.plot(t1,awgn)
        self.panel.Axes.set_xlabel(u"时间/s")
        self.panel.Axes.grid()
        self.panel.Canvas.draw()
        
    def draw_channel_freq(self):
        awgn = self.panel.result[2]
        N = len(awgn)
        yfr = np.fft.fft(awgn, N)
        yf = np.fft.fftshift(yfr)
        yfpr = np.abs(yf)/100

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
        #self.panel.Axes.plot([-2.0,2],[0,0],'b:',[0,0],[-2.0,2],'b:')
        #self.panel.Axes.axis([-2,2,-2,2])
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