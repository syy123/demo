# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:53:10 2016

@author: WB
"""
#[u'脉冲波形',u'脉冲频谱',u'调制信号波形',u'调制信号频谱',u'星座映射',u'眼图'] 
from matplotlib.font_manager import FontProperties
#import matplotlib.pyplot as plt
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
import numpy as np
class ChannelSourceFigure():
    def __init__(self, panel):
        self.panel = panel
        self.init_dict()       
    def init_dict(self):
        self.xdata = {
                0: self.panel.x,
                1: self.panel.f1,
                2: self.panel.x1,
                3: self.panel.f2,
                4: self.panel.a
        }
        self.ydata = {
                0: self.panel.impulse,
                1: self.panel.ImpulSpectrum,
                2: [self.panel.Idata, self.panel.Qdata, self.panel.signal],
                3: self.panel.Spectrum,
                4: self.panel.b          
        }
        self.label = {
                0: self.panel.label,
                1: self.panel.frqlab,
                2: [u"实部", u"虚部", u"实-虚"],
                3: "",
                4: ""
                        
        }
        self.title = {
                0: u"脉冲信号时域波形",
                1: u"脉冲频谱",
                2: u"调制信号时域波形",
                3: u"调制信号频谱",
                4: u"星座图"         
        }
        self.xLabel = {
                0: u"时间/s",
                1: u"频率/Hz",
                2: u"时间/s",
                3: u"频率/Hz",
                4: ""
                
        }
        self.function = {
                0: self.draw_impulse_data,
                1: self.draw_impufreq_data,
                2: self.draw_modutale_data,
                3: self.draw_modufreq_data,
                4: self.draw_planisphere
        }
    
    def draw_impulse_data(self):
        self.panel.axes.plot(self.xdata[0], self.ydata[0], label = self.label[0])
        self.panel.axes.legend(loc = 'lower right', prop = font)  
    def draw_impufreq_data(self):
        self.panel.axes.plot(self.xdata[1], self.ydata[1], label = self.label[1]) 
        self.panel.axes.legend(loc = 'upper right', prop = font)
    def draw_modutale_data(self):
        self.panel.axes.plot(self.xdata[2], self.ydata[2][0], 'b', label = self.label[2][0] )
        self.panel.axes.plot(self.xdata[2], self.ydata[2][1], 'r', label = self.label[2][1] )
        #self.panel.axes.plot(self.xdata[2], self.ydata[2][2], 'k', label = self.label[2][2] )
        self.panel.axes.legend(loc = 1, prop=font)
    def draw_modufreq_data(self):
        self.panel.axes.plot(self.xdata[3], self.ydata[3])
    def draw_planisphere(self):
        self.panel.axes.scatter(self.xdata[4], self.ydata[4])
        self.panel.axes.plot([-2.0,2],[0,0],'b:',[0,0],[-2.0,2],'b:')
    def draw_figure(self):        
        for i in range(5):
            if self.panel.images[i]:
                self.panel.axes = self.panel.Figure.add_subplot(self.panel.m,self.panel.n,self.panel.images[i])
                self.panel.axes.set_title(self.title[i], fontproperties=font)
                self.function[i]()
                self.panel.axes.set_xlabel(self.xLabel[i], fontproperties=font)
                self.panel.axes.grid()
                self.panel.Canvas.draw()
        if self.panel.images[5]:
            self.panel.axes = self.panel.Figure.add_subplot(self.panel.m,self.panel.n,self.panel.images[5])
            self.panel.eye = np.zeros(self.panel.Fs*self.panel.eye_num)
            self.t = np.arange(0, self.panel.eye_num, 1.0/self.panel.Fs)
            for k in range(10,self.panel.number/self.panel.div):
                self.panel.eye = self.panel.modulateReal[k*self.panel.Fs:(k+self.panel.eye_num)*self.panel.Fs]
                self.panel.axes.plot(self.t,self.panel.eye,'b')
                self.panel.axes.hold(True)
            self.panel.axes.grid(True)
            self.panel.axes.set_title(u"基带信号实部眼图", fontproperties=font)
            self.panel.Canvas.draw()