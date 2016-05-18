
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 21:33:11 2016

@author: Administrator
"""
from scipy.stats import rayleigh
import numpy as np;
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 
class RayChannelFigure():
    
    def __init__(self, panel):
        #类raychannelfigure是在panel的基础上编写的,导入panel-数据就有了
        self.panel = panel;  
        self.init_data();  
        self.init_dictonary();

    def draw_ray_channel_figure(self):
        self.panel.Figure.clear()
        for i in range(7):
            if self.panel.images[i]:
                self.panel.Axes = self.panel.Figure.add_subplot(self.panel.m,self.panel.n,self.panel.images[i])
                self.panel.Axes.set_title(self.title[i],fontproperties=font)
                self.function[i]()
                self.panel.Axes.set_xlabel(self.xLable[i],fontproperties=font)
                self.panel.Axes.grid()
                self.panel.Canvas.draw()
        
    def draw_time_data(self):
        self.panel.Axes.plot(self.yData[0],self.xData[0])
    def draw_freq_data(self):
        self.panel.Axes.plot(self.xData[1],self.yData[1])
    def draw_planisphere(self):
        self.panel.Axes.scatter(self.xData[2], self.yData[2])
        self.panel.Axes.plot([-2.0,2],[0,0],'b:',[0,0],[-2.0,2],'b:')
    def draw_doppler(self):
        self.panel.Axes.plot(self.xData[3])  #self.yData[3],
    def draw_envelope(self):
        self.panel.Axes.hist(self.xData[4], self.yData[4])
    def draw_phase(self):
        self.panel.Axes.hist(self.xData[5])
    def draw_correlate(self):
        self.panel.Axes.plot(self.xData[6], self.yData[6])
        
    def init_dictonary(self):
        
        self.xData = {  
                0: self.xData0,1: self.xData1,  
                2: self.xData2,3: self.xData3,
                4: self.xData4,5: self.xData5,
                6: self.xData6}
            
        self.yData = { 
                0: self.yData0,
                1: self.yData1,  
                2: self.yData2,
                #3: self.yData3,
                4: self.yData4,
                6: self.yData6
               }
                
        self.title = {  
                0: self.title0,1: self.title1,  
                2: self.title2,3: self.title3,
                4: self.title4,5: self.title5,
                6: self.title6
                }
                
        self.xLable = {  
                0: self.xLable0,1: self.xLable1, 
                2: self.xLable2,3: self.xLable3,
                4: self.xLable4,5: self.xLable5,
                6: self.xLable6
                }
                
        self.function = {
                0: self.draw_time_data,1: self.draw_freq_data, 
                2: self.draw_planisphere,3: self.draw_doppler,
                4: self.draw_envelope,5: self.draw_phase,
                6: self.draw_correlate
                }
                
    def init_data(self):
        self.xData0 = self.panel.result_ray[0]
        self.xData1 = self.panel.result_ray[1]
        self.xData2 = self.panel.result_ray[2]
        self.xData3 = self.panel.result_ray[3]
        self.xData4 = self.panel.result_ray[4]
        self.xData5 = self.panel.result_ray[5]
        self.xData6 = self.panel.result_ray[6]
        self.yData0 = np.linspace(0, 1.0*self.panel.number/self.panel.rate/self.panel.div, len(self.xData0))
        self.yData1 = self.panel.result_ray[7]
        self.yData2 = self.panel.result_ray[8]
        self.yData4 = 128
        self.yData6 = self.panel.result_ray[9]
        self.title0 = u'瑞利信道时域波形'
        self.title1 = u'瑞利信道频谱图'
        self.title2 = u'星座图(瑞利信道)'
        self.title3 = u'多普勒功率谱'
        self.title4 = u'瑞利概率密度函数'
        self.title5 = u'信号相位波形'
        self.title6 = u'瑞利信道自相关函数'
        self.xLable0 = "time / s"
        self.xLable1 = "frequency / Hz"
        self.xLable2 = ""
        self.xLable3 = "frequency / Hz"
        self.xLable4 = ""
        self.xLable5 = ""
        self.xLable6 = ""
    