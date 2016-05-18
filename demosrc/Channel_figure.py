# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 16:21:39 2016

@author: Administrator
"""

class Figure_wave():
    def __init__(self,*result,figure_type,x_amount,y_amount,title,image_amount,xLabel):
        self.result = result   #绘图数据
        self.figure_type = figure_type   #图形类型：折线图，直方图，星座图
        self.x_amount = x_amount   #图形分布
        self.y_amount = y_amount
        self.title = title
        self.xLabel = xLabel   #x轴单位
        self.image_amount = image_amount   #图形是否被选中
        #self.figure_num = len(self.images)
    
    def draw_figure(self):
        self.Figure.clear()
        #for i in range(self.figure_num):
        if self.images[self.image_amount]:
            self.Axes.clear() 
            self.Axes = self.Figure.add_subplot(self.x_amount,self.y_amount,self.images[self.figure_num])
            self.Axes.set_title(self.title)
            if figure_type == 0:
                self.Axes.plot(self.result[0],self.result[1])
                self.Axes.set_xlabel(self.xLabel)
            elif figure_type == 1:
                self.Axes.scatter(self.result[0],self.result[1])
                self.Axes.plot([-2.0,2],[0,0],'b:',[0,0],[-2.0,2],'b:')
            elif figure_type == 2:
                self.Axes.hist(self.result[0],self.result[1])
            self.Axes.grid()
        