# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 21:33:11 2016

@author: Administrator
"""

import wx
from Configure import *
import numpy as np

import matplotlib
matplotlib.use("WXAgg");
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas;  
from matplotlib.figure import Figure;
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar;

from AWGN import AWGN
from zheng_channel import *
from rayleigh_channel import * 
from Gauss_Channel_Figure import *
from Ray_Channel_Figure import *
from ChannelSource import *
from new_interface import *
#显示中文字体，不用修改文件
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 

channel_in = []
signal = []
Fs = 0
B_number = 0
rate = 0
div = 0
def get_value(obj):
    global channel_in
    global Fs
    global B_number
    global rate
    global signal
    global div
    signal = obj.signal
    channel_in = obj.channel_in
    Fs = obj.Fs
    B_number = obj.number
    rate = obj.rate
    div = obj.div
class Channel(wx.Panel):
    def __init__(self, parent):
        
        wx.Panel.__init__(self,parent,id=-1)
        
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
        self.left_vsizer.Add(self.choiceBox, 0, wx.ALL|wx.EXPAND, 3)
        self.left_vsizer.Add(self.NoteBox,1 , wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.AWGNBox,0 , wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.RayBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.ShiftBox, 0, wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.FigureBox,0 , wx.ALL|wx.EXPAND,3)
        self.left_vsizer.Add(self.ButtonBox, 0, wx.ALL|wx.EXPAND,3)
        #self.left_vsizer.Hide(self.AWGNBox)
        #self.left_vsizer.Hide(self.RayBox)
        #self.left_vsizer.Hide(self.ShiftBox)
        
    def AddElementForRightSizer(self):
        self.right_vsizer.Add(self.Navigation, 0, wx.ALL|wx.EXPAND)
        self.right_vsizer.Add(self.Canvas, 1, wx.ALL|wx.EXPAND)
       
    def ConfigSizersLayout(self):
        self.TopSizer.Add(self.left_vsizer,1, wx.EXPAND, 5)
        self.TopSizer.Add(self.right_vsizer, 4, wx.EXPAND, 5)
        #self.SetSizer(self.TopSizer)
        #self.Layout()
        self.SetSizerAndFit(self.TopSizer)
        self.TopSizer.SetSizeHints(self)
    def CreateElementForLeftSizer(self): #调用函数，不需要布局 
        self.CreateChoiceBox()
        self.CreateNoteBox()
        self.CreateAWGNBox()
        self.CreateRayBox()
        self.CreateShiftBox()
        self.CreateButtonBox()
        self.CreateFigureBox()                
        
    def CreateElementForRightSizer(self):  #创建模块，无需布局
        self.Figure = Figure(figsize = (4,4))
        self.Axes = self.Figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.Canvas = FigureCanvas(self, -1, self.Figure)
        self.Navigation = NavigationToolbar(self.Canvas)
        #self.CreateNoteBoxForRightSizer()

    def CreateChoiceBox(self):
        self.choiceBox = wx.ComboBox(self, -1,u"信道类型",choices = GetChannelChoicBoxList())

    def CreateNoteBox(self):
        self.Note=wx.StaticBox(self,-1,u"信道公式")
        self.NoteBox=wx.StaticBoxSizer(self.Note,wx.VERTICAL)
       
    def CreateAWGNBox(self):  #滑块
        self.noise=wx.StaticText(self,-1,u"信噪比:")
        self.noiseslider=wx.Slider(self,-1,10,1,20,style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)#sizer
        self.noiseslider.SetTickFreq(1, 1)   #设置刻度
        self.noisetext=wx.TextCtrl(self,-1,"1.0")
        self.noiseslider.Bind(wx.EVT_SLIDER, self.OnSliderMove)
        self.noise_in=1.0
        
        sizer1=wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add((25,10))
        sizer1.Add(self.noise,0,wx.ALL|wx.EXPAND,2)
        sizer1.Add((24,10))
        sizer1.Add(self.noisetext,0,wx.ALL|wx.EXPAND,2)
        
        self.AWGNBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"AWGN信道"),wx.VERTICAL)
        self.AWGNBox.Add(self.noiseslider,0,wx.ALL|wx.EXPAND,2)
        self.AWGNBox.Add(sizer1,0,wx.ALL|wx.EXPAND,2)
    def OnSliderMove(self, event):
        self.noise_in=float((self.noiseslider.GetValue())/10.0)
        self.noisetext.SetValue(str(float(1.0/(self.noise_in))))
    
    def CreateRayBox(self):
        self.pathsum=wx.StaticText(self,-1,u"多径数目:    ")
        self.pathtext=wx.SpinCtrl(self,-1,"",size = (130,20), style=wx.SP_WRAP)
        self.pathtext.SetRange(1,15)
        self.pathtext.SetValue(1)
        
        self.delaylabel = wx.StaticText(self, -1, u"相对时延:    ")
        self.delayIn = wx.TextCtrl(self, -1, "0",size = (130,20),style=wx.TE_PROCESS_ENTER)
        self.delayIn.SetToolTipString(u"用英文符号','隔开输入，以回车结束输入")
        self.delay_time_label = wx.StaticText(self, -1, u"绝对时延(s):")
        self.delay_time=wx.TextCtrl(self,-1,"1.0", size = (130,20))
        self.powerlabel = wx.StaticText(self, -1, u"衰减(dBw):  ")
        self.powerIn = wx.TextCtrl(self, -1,"-1", size = (130,20),style=wx.TE_PROCESS_ENTER)
        self.powerIn.SetToolTipString(u"用英文符号','隔开输入")
        self.delayIn.Bind(wx.EVT_TEXT_ENTER,self.OnText)
        self.powerIn.Bind(wx.EVT_TEXT_ENTER,self.OnText1)
    
        #布局
        sizer1=wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add((25,10))
        sizer1.Add(self.pathsum,0,wx.ALL|wx.EXPAND,3)
        sizer1.Add(self.pathtext,0,wx.ALL|wx.EXPAND,3)
        
        sizer2=wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add((25,10))
        sizer2.Add(self.delaylabel,0,wx.ALL|wx.EXPAND,3)
        #sizer2.Add((24,10))
        sizer2.Add(self.delayIn,0,wx.ALL|wx.EXPAND,3)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add((25,10))
        sizer4.Add(self.delay_time_label, 0, wx.ALL|wx.EXPAND,3)
        sizer4.Add(self.delay_time, 0, wx.ALL|wx.EXPAND,3)
        
        
        sizer3=wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add((25,10))
        sizer3.Add(self.powerlabel,0,wx.ALL|wx.EXPAND,3)
        #sizer3.Add((24,10))
        sizer3.Add(self.powerIn,0,wx.ALL|wx.EXPAND,3)
        
        self.RayBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"rayleigh信道"),wx.VERTICAL)
        self.RayBox.Add(sizer1,0,wx.EXPAND|wx.ALL,3) 
        self.RayBox.Add(sizer2,0,wx.EXPAND|wx.ALL,3) 
        self.RayBox.Add(sizer4,0,wx.EXPAND|wx.ALL,3)
        self.RayBox.Add(sizer3,0,wx.EXPAND|wx.ALL,3)
    def OnText(self,event):
        self.delayIn.GetValue()
        print self.delayIn
        self.delay = (self.delayIn.GetValue()).split(',')
        self.Delay = []
        for i in range(self.pathtext.GetValue() ):
            self.Delay.append(float(self.delay[i])/Fs)
        self.Delay_time = str(self.Delay)
        self.Delay_time.split('[')
        self.Delay_time.split(']')
        self.delay_time.SetValue(str(self.Delay_time))
    def OnText1(self,event):
        self.powerIn.GetValue()
    
    def CreateShiftBox(self):
        self.shift=wx.StaticText(self,-1,u"多普勒频移(Hz):")
        self.shiftIn=wx.TextCtrl(self,-1,u"500",size = (103,20), style=wx.TE_PROCESS_ENTER)
        self.shiftIn.SetToolTipString(u"按回车键结束输入")
        self.shiftIn.Bind(wx.EVT_TEXT_ENTER, self.NorShiftIn)
        
        self.norshift=wx.StaticText(self,-1,u"归一化多普勒频移(fDTs):")
        self.norshiftIn=wx.TextCtrl(self,-1,'', size = (103,20))
        
        self.ShiftBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"多普勒效应"),wx.VERTICAL)
             
        self.subBox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.subBox1.Add(self.shift, 0, wx.EXPAND|wx.ALL,2)
        self.subBox1.Add(self.shiftIn,0,wx.EXPAND|wx.ALL,2)
        
        self.subBox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.subBox2.Add(self.norshift, 0, wx.EXPAND|wx.ALL,2)
        self.subBox2.Add(self.norshiftIn,0,wx.EXPAND|wx.ALL,2)
        self.ShiftBox.Add(self.subBox1,0,wx.EXPAND|wx.ALL,2)
        self.ShiftBox.Add(self.subBox2,0,wx.EXPAND|wx.ALL,2) 
        
    def NorShiftIn(self, event):
        self.norshiftIn.SetValue(str(float(self.shiftIn.GetValue())/Fs))
        event.Skip()
        
    def CreateButtonBox(self):
        self.startbutton=wx.Button(self,-1,u"启动")
        self.Bind(wx.EVT_BUTTON,self.OnClickStart,self.startbutton)
        self.configbutton = wx.Button(self, -1, u"图形显示")
        self.configbutton.Bind(wx.EVT_BUTTON, self.OnConfig)
        
        self.ButtonBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u""),wx.HORIZONTAL)
        self.ButtonBox.Add((50,10))
        self.ButtonBox.Add(self.startbutton,0,wx.EXPAND|wx.ALL,5)
        self.ButtonBox.Add(self.configbutton,0,wx.EXPAND|wx.ALL,5)
        
    def CreateFigureBox(self):
        self.figurechoice=wx.CheckListBox(self,-1,size= (100,100),choices=GetChannelfigureBoxList())
        self.figurechoice.SetToolTipString(u"最多选择四幅图形")
        self.figurechoice.Bind(wx.EVT_CHECKLISTBOX, self.FigureShow)
        #将绘图选择界面中的每次改变连接到函数上
    
        self.FigureBox=wx.StaticBoxSizer(wx.StaticBox(self,-1,u"图形显示"),wx.VERTICAL)
        self.FigureBox.Add(self.figurechoice,0,wx.EXPAND|wx.ALL,5)
    def FigureShow(self,event):
        self.count=0
      
        self.images_number=len(GetChannelfigureBoxList())  #所选图像的总数
        self.images=np.zeros(self.images_number,int)
        
        for i in range(self.images_number):
            if self.figurechoice.IsChecked(i):
                self.count=self.count+1
                self.images[i]=self.count
        
    def OnClickStart(self, event):
        self.number = B_number
        self.rate = rate
        self.fm = self.shiftIn.GetValue()
        self.div = div
        img1 = wx.Image(GetAWGNimage(),wx.BITMAP_TYPE_ANY)
        img2 = wx.Image(GetRayimage())
        if self.choiceBox.GetLabelText() == u"信道类型":
            retCode = wx.MessageBox(u"请选择信道类型。", u"错误提示",
                            wx.OK | wx.ICON_EXCLAMATION)
        elif self.count == 0:
            retCode = wx.MessageBox(u"请选择要显示的图像。", u"错误提示",
                            wx.OK | wx.ICON_EXCLAMATION)
        elif self.norshiftIn == 0:
            retCode = wx.MessageBox(u"请输入归一化多普勒频移。", u"错误提示",
                            wx.OK | wx.ICON_EXCLAMATION)
        elif self.count > 4:
            retCode = wx.MessageBox(u"最多选择四幅图像，请重新选择。", u"错误提示",
                            wx.OK | wx.ICON_EXCLAMATION)
        elif self.choiceBox.GetLabelText() == OtherName():
            #显示信道公式
            self.NoteBox.Clear()
            img1 = img1.Scale(self.NoteBox.GetSize()[0]-15,self.NoteBox.GetSize()[1]-25)
            sb1 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(img1))
            self.NoteBox.Add(sb1)     
            self.Fit()
            self.left_vsizer.Layout()
            
            sigma0=self.noise_in
            self.ret_awgn = AWGN(B_number,Fs,sigma0,signal)
            self.result = self.ret_awgn
            self.plotAWGN(self)
            #wx.CallAfter(Publisher().sendMessage, "update_awgn", ret_awgn)
        else:
            #显示信道公式
            self.NoteBox.Clear()
            img2 = img2.Scale(self.NoteBox.GetSize()[0]-15,self.NoteBox.GetSize()[1]-25)
            sb1 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(img2))
            self.NoteBox.Add(sb1)
            self.Fit()
            self.left_vsizer.Layout()     
            #配置每条路径参数
            self.delay = (self.delayIn.GetValue()).split(',')
            self.Delay = []
            for i in range(self.pathtext.GetValue() ):
                self.Delay.append(int(self.delay[i]))
            self.power = (self.powerIn.GetValue()).split(',')
            self.Power = []
            for i in range(self.pathtext.GetValue() ):
                self.Power.append(int(self.power[i]))
         
            n = int(self.pathtext.GetValue())
            fdts = int(self.shiftIn.GetValue())/Fs   #多普勒频移
            
            if self.choiceBox.GetLabelText() == SosBoxName():
                self.ray_out = zheng_channel(B_number,Fs,n,self.Delay,self.Power,fdts,channel_in)
            elif self.choiceBox.GetLabelText() == SmithBoxName():
                self.ray_out = RAYLEIGH(B_number,Fs,n,self.Delay,self.Power,fdts,channel_in)
            self.result_ray = self.ray_out
            self.plotRAY(self)
            #wx.CallAfter(Publisher().sendMessage, "update_ray", self.ray_out)
        
    def OnConfig(self,event):    #图形显示按钮绑定的函数，传递参数
        if self.count > 4:
            retCode = wx.MessageBox(u"最多选择四幅图像，请重新选择。", u"错误提示",
                            wx.OK | wx.ICON_EXCLAMATION)
        elif self.choiceBox.GetLabelText() == OtherName():
            self.result = self.ret_awgn
            self.plotAWGN(self)
        else:
            self.result_ray = self.ray_out
            self.plotRAY(self)
    
    def plotAWGN(self,event):
        self.gaussFigure = GaussChannelFigure(self)  #类实例化
        self.gaussFigure.draw_gauss_channel_figure()
        
    def plotRAY(self,event):
        #分配图形位置
        if self.count < 4:
            self.m=1
            self.n=self.count
            self.drawRAY()
        else:
            self.m=2
            self.n=2
            self.drawRAY()
             
    def drawRAY(self):
        self.rayFigure = RayChannelFigure(self); 
        self.rayFigure.draw_ray_channel_figure()
class NewFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "frame", size = (800, 600))
        self.newPanel = Channel(self)
if __name__ == '__main__':
    app = wx.PySimpleApp()
    NewFrame(None).Show(True)
    app.MainLoop()    
