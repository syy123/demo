# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 21:39:31 2016

@author: Administrator
"""
import wx
#from config import *
from Configure import *
from Head import *
from SliderBox import *
from wx.lib.pubsub import Publisher 
import numpy as np
import math

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from matplotlib.widgets import SpanSelector

from QPSK import QPSK
from AWGN import AWGN

class Channelsink(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent,-1)
        self.CreateSizers()
        self.CreateElementForLeftSizer()
        self.CreateElementForRightSizer()
        self.AddElementForLeftSizer()
        self.AddElementForRightSizer()
        self.ConfigSizersLayout()
        
    def CreateSizers(self):     #创建每个模块
        self.TopSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_vsizer = wx.BoxSizer(wx.VERTICAL)
        self.right_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sub_left_visizer = wx.BoxSizer(wx.VERTICAL)
        self.sub_right_visizer = wx.BoxSizer(wx.VERTICAL)
           
    def AddElementForLeftSizer(self):   #创建每个模块
        self.left_vsizer.Add(self.BalanceBox, 0, wx.ALL|wx.EXPAND,3)
        #self.left_vsizer.Add(self.InfoBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.CodeBox, 0, wx.ALL|wx.EXPAND, 2)
        self.left_vsizer.Add(self.FilterBox, 0, wx.ALL|wx.EXPAND, 2)
        self.left_vsizer.Add(self.ModuBox, 0, wx.ALL|wx.EXPAND, 2)
        self.left_vsizer.Add(self.ChannelBox, 0, wx.ALL|wx.EXPAND, 2)
        self.left_vsizer.Add(self.RayparaBox, 0, wx.ALL|wx.EXPAND, 2)
        self.left_vsizer.Add(self.BalanceparaBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.FigureBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.ButtonBox, 0, wx.ALL|wx.EXPAND,3)
        
    def AddElementForRightSizer(self):
        self.sub_left_visizer.Add(self.leftUpNavigation, 0, wx.ALL|wx.EXPAND)
        self.sub_left_visizer.Add(self.leftUpCanvas, 1, wx.ALL|wx.EXPAND)
        self.sub_left_visizer.Add(self.leftDownCanvas, 1, wx.ALL|wx.EXPAND)
        self.sub_right_visizer.Add(self.rightUpNavigation, 0, wx.ALL|wx.EXPAND)
        self.sub_right_visizer.Add(self.rightUpCanvas, 1, wx.ALL|wx.EXPAND)
        self.sub_right_visizer.Add(self.rightDownCanvas, 1, wx.ALL|wx.EXPAND)
        
    def ConfigSizersLayout(self):
        self.right_hsizer.Add(self.sub_left_visizer, 1, wx.EXPAND, 5)
        self.right_hsizer.Add(self.sub_right_visizer, 1, wx.EXPAND, 5)
        self.TopSizer.Add(self.left_vsizer,1.5, wx.EXPAND, 5)
        self.TopSizer.Add(self.right_hsizer, 4, wx.EXPAND, 5)
        self.SetSizer(self.TopSizer)
        self.Layout()
        
    def CreateElementForLeftSizer(self): #调用函数，不需要布局 
        self.CreateCodeBox()
        self.CreateFilterBox()
        self.CreateModuBox()
        self.CreateChannelBox()
        self.CreateRayparaBox()
        self.CreateBalanceBox()
        self.CreateBalanceparaBox()
        self.CreateFigureBox()
        self.CreateButtonBox()
        #self.CreateInfoBox()
                        
    def CreateElementForRightSizer(self):  #创建模块，无需布局
        self.leftUpFigure = Figure(figsize = (3.6, 3.7))
        self.leftUpAxes = self.leftUpFigure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.leftUpCanvas = FigureCanvas(self, -1, self.leftUpFigure)
        self.leftUpNavigation = NavigationToolbar(self.leftUpCanvas)
        
        self.leftDownFigure = Figure(figsize = (3.6, 3.7))
        self.leftDownAxes = self.leftDownFigure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.leftDownCanvas = FigureCanvas(self, -1, self.leftDownFigure)
        #self.leftDownNavigation = NavigationToolbar(self.leftDownCanvas)
        
        self.rightUpFigure = Figure(figsize = (3.6, 3.7))
        self.rightUpAxes = self.rightUpFigure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.rightUpCanvas = FigureCanvas(self, -1, self.rightUpFigure)
        self.rightUpNavigation = NavigationToolbar(self.rightUpCanvas)
 
        self.rightDownFigure = Figure(figsize = (3.6, 3.7))
        self.rightDownAxes = self.rightDownFigure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.rightDownCanvas = FigureCanvas(self, -1, self.rightDownFigure)
        #self.rightDownNavigation = NavigationToolbar(self.rightDownCanvas)
    '''   
    def CreateInfoBox(self):
        self.InfoBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,"信道状态"),wx.VERTICAL)
        self.InfoBox.Add(self.codetext,0,wx.EXPAND|wx.ALL,5)
        self.InfoBox.Add(self.filtertext,0,wx.EXPAND|wx.ALL,5)
        self.InfoBox.Add(self.modutext,0,wx.EXPAND|wx.ALL,5)
        self.InfoBox.Add(self.channeltext,0,wx.EXPAND|wx.ALL,5)
        self.InfoBox.Add(self.noisetext,0,wx.EXPAND|wx.ALL,3)
        self.InfoBox.Add(self.pathtext,0,wx.EXPAND|wx.ALL,3)
        self.InfoBox.Add(self.delaytext,0,wx.EXPAND|wx.ALL,3)
        self.InfoBox.Add(self.powertext,0,wx.EXPAND|wx.ALL,3)
    '''    
    def CreateCodeBox(self):
        self.codetext=wx.StaticText(self, -1, u"码源数量：20")
        #self.codetext.SetForegroundColour('white')
        #self.codetext.SetBackgroundColour('gray')
        
        self.CodeBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,""),wx.HORIZONTAL)
        self.CodeBox.Add((50,10))
        self.CodeBox.Add(self.codetext,0,wx.EXPAND|wx.ALL,5)
        
    def CreateFilterBox(self):
        self.filtertext=wx.StaticText(self, -1, u"升余弦滚降系数：0.5")
        #self.filtertext.SetForegroundColour('white')
        #self.filtertext.SetBackgroundColour('gray')
        
        self.FilterBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,""),wx.HORIZONTAL)
        self.FilterBox.Add((50,10))
        self.FilterBox.Add(self.filtertext,0,wx.EXPAND|wx.ALL,5)
         
    def CreateModuBox(self):
        self.modutext=wx.StaticText(self, -1, u"调制方式：QPSK")
        
        self.ModuBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,""),wx.HORIZONTAL)
        self.ModuBox.Add((50,10))
        self.ModuBox.Add(self.modutext,0,wx.EXPAND|wx.ALL,5)

    def CreateChannelBox(self):
        self.channeltext=wx.StaticText(self, -1, u"信道模型：瑞利信道")
        
        self.ChannelBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,""),wx.HORIZONTAL)
        self.ChannelBox.Add((50,10))
        self.ChannelBox.Add(self.channeltext,0,wx.EXPAND|wx.ALL,5)
        
    def CreateRayparaBox(self):
        self.noisetext=wx.StaticText(self, -1, u"噪声功率：0.5dB")
        self.pathtext=wx.StaticText(self, -1, u"多径数目：3")
        self.delaytext=wx.StaticText(self, -1, u"时延：[0 , 1 , 3]")
        self.powertext=wx.StaticText(self, -1, u"衰减：[-1 , -2 , -3]")
        
        sizer1=wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add((50,10))
        sizer1.Add(self.noisetext,0,wx.ALL|wx.EXPAND,2)
        
        sizer2=wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add((50,10))
        sizer2.Add(self.pathtext,0,wx.ALL|wx.EXPAND,2)
        
        sizer3=wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add((50,10))
        sizer3.Add(self.delaytext,0,wx.ALL|wx.EXPAND,2)
        
        sizer4=wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add((50,10))
        sizer4.Add(self.powertext,0,wx.ALL|wx.EXPAND,2)
        
        self.RayparaBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"瑞利信道参数"),wx.VERTICAL)
        self.RayparaBox.Add(sizer1,0,wx.EXPAND|wx.ALL,2)
        self.RayparaBox.Add(sizer2,0,wx.EXPAND|wx.ALL,2)
        self.RayparaBox.Add(sizer3,0,wx.EXPAND|wx.ALL,2)
        self.RayparaBox.Add(sizer4,0,wx.EXPAND|wx.ALL,2)
        
        
    def CreateBalanceBox(self):
        self.Balance= wx.Choice(self, -1,choices = GetBalanceBoxList())
        
        self.BalanceBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"均衡算法"),wx.VERTICAL)
        self.BalanceBox.Add(self.Balance,0,wx.EXPAND|wx.ALL,5)
        
    def CreateBalanceparaBox(self):
        self.step=wx.StaticText(self,-1,u"步长",style=wx.ALIGN_CENTER)
        self.stepslider=wx.Slider(self,-1,10,5,50,style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)#sizer
        self.stepslider.SetTickFreq(5, 1)   #设置刻度
        self.steptext=wx.TextCtrl(self,-1,"0.1")
        self.stepslider.Bind(wx.EVT_SLIDER, self.OnStepSliderMove)
        
        self.tap = wx.StaticText(self, -1, u"抽头个数:")
        self.tapIn = wx.TextCtrl(self, -1, "500",size = (118,20),style=wx.TE_PROCESS_ENTER)
        
        self.pilot = wx.StaticText(self, -1, u"导频长度:")
        self.politIn = wx.TextCtrl(self, -1, "8000",size = (118,20),style=wx.TE_PROCESS_ENTER)
        
        sizer1=wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add((35,10))
        sizer1.Add(self.tap,0,wx.ALL|wx.EXPAND,3)
        sizer1.Add(self.tapIn,0,wx.ALL|wx.EXPAND,3)
        
        sizer2=wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add((35,10))
        sizer2.Add(self.pilot,0,wx.ALL|wx.EXPAND,3)
        #sizer2.Add((24,10))
        sizer2.Add(self.politIn,0,wx.ALL|wx.EXPAND,3)
        
        self.BalanceparaBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"均衡器参数"),wx.VERTICAL)
        self.BalanceparaBox.Add(self.step,0,wx.ALL|wx.EXPAND,2)
        self.BalanceparaBox.Add(self.stepslider,0,wx.ALL|wx.EXPAND,2)
        self.BalanceparaBox.Add(self.steptext,0,wx.ALL|wx.EXPAND,2)
        self.BalanceparaBox.Add(sizer1,0,wx.ALL|wx.EXPAND,2)
        self.BalanceparaBox.Add(sizer2,0,wx.ALL|wx.EXPAND,2)
    def OnStepSliderMove(self, event):
        self.steptext.SetValue(str(float(self.stepslider.GetValue())/100))
      
    def CreateFigureBox(self):
        self.figure=wx.CheckListBox(self,-1,size= (70,70),choices=GetBalancefigureBoxList())
        
        self.FigureBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"图形显示"),wx.VERTICAL)
        self.FigureBox.Add(self.figure,0,wx.EXPAND|wx.ALL,5)
        
    def CreateButtonBox(self):
        self.startbutton=wx.Button(self,-1,u"启动")
        self.showbutton=wx.Button(self,-1,u"显示")
        self.Bind(wx.EVT_BUTTON,self.OnClickStart,self.startbutton)
        self.Bind(wx.EVT_BUTTON,self.OnClickShow,self.showbutton)
        
        self.ButtonBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"按钮"),wx.HORIZONTAL)
        self.ButtonBox.Add((30,10))
        self.ButtonBox.Add(self.startbutton,0,wx.EXPAND|wx.ALL,3)
        self.ButtonBox.Add((30,10))
        self.ButtonBox.Add(self.showbutton,0,wx.EXPAND|wx.ALL,3)
    def OnClickStart(self,event):
        pass
    def OnClickShow(self,event):
        pass