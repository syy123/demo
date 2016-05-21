# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 21:39:31 2016

@author: Administrator
"""

import wx
import numpy as np
import matplotlib
matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from Configure import *

class ChannelSink(wx.Panel):
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
        self.right_vsizer = wx.BoxSizer(wx.VERTICAL)
           
    def AddElementForLeftSizer(self):   #创建每个模块
        self.left_vsizer.Add(self.BalanceBox, 0, wx.ALL|wx.EXPAND,3)
        #self.left_vsizer.Add(self.InfoBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.BalanceparaBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.FigureBox, 1, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.ButtonBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.showBox, 1, wx.ALL|wx.EXPAND,3)
        
    def AddElementForRightSizer(self):
        self.right_vsizer.Add(self.Navigation, 0, wx.ALL|wx.EXPAND)
        self.right_vsizer.Add(self.StaticText, 0, wx.ALL | wx.EXPAND);
        self.right_vsizer.Add(self.Canvas, 1, wx.ALL|wx.EXPAND)
        
    def ConfigSizersLayout(self):
        self.TopSizer.Add(self.left_vsizer, 1, wx.ALL|wx.EXPAND, 3)
        self.TopSizer.Add(self.right_vsizer,4, wx.ALL|wx.EXPAND, 3)
        self.SetSizer(self.TopSizer)
        self.Layout()
        
    def CreateElementForLeftSizer(self): #调用函数，不需要布局 
        self.CreateBalanceBox()
        self.CreateBalanceparaBox()
        self.CreateFigureBox()
        self.CreateButtonBox()
        #self.CreateInfoBox()
        self.CreateNoteBoxForRightSizer()                
    def CreateElementForRightSizer(self):  #创建模块，无需布局
        self.Figure = Figure(figsize = (4, 4))
        self.axes = self.Figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.Canvas = FigureCanvas(self, -1, self.Figure)
        self.Navigation = NavigationToolbar(self.Canvas) 
        self.Canvas.mpl_connect('motion_notify_event', self.CanvasOnMouseMove)
        self.StaticText = wx.StaticText(self, -1, label = 'Mouse Location')
    def CanvasOnMouseMove(self, event):
        ex=event.xdata   
        ey=event.ydata   
        if ex and ey:
            self.StaticText.SetLabel('(%s, %s)' % (ex, ey))
            
    def CreateNoteBoxForRightSizer(self):
        self.showBox = wx.StaticBoxSizer(wx.StaticBox(self,-1,u'状态显示'),wx.VERTICAL)
        self.DisplayText=wx.TextCtrl(self,-1,"",size=(35,-1),style=wx.TE_MULTILINE)
        self.DisplayText.AppendText(u"请配置参数...\n")
        self.showBox.Add(self.DisplayText, 1, wx.EXPAND|wx.ALL, 2)
        
        
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
        self.politIn = wx.TextCtrl(self, -1, "80",size = (118,20),style=wx.TE_PROCESS_ENTER)
        
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
        self.FigureBox.Add(self.figure,1,wx.EXPAND|wx.ALL,5)
        
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

class NewFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "frame", size = (800, 600))
        self.newPanel = Channelsink(self)
if __name__ == '__main__':
    app = wx.PySimpleApp()
    NewFrame(None).Show(True)
    app.MainLoop()