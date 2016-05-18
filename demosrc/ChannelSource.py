# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 19:44:22 2016

@author: Administrator
"""
from config import *
from ChannelSourceFunction import *
from Channel_Source_Figure import *
import sys
from Channel import *
class ChannelSource(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)       
        self.CreateSizer()
        self.CreateElementForLeftSizer()
        self.CreateElementForRightSizer()
        self.AddElementForLeftSizer()
        self.AddElementForRightSizer()
        self.ConfigSizersLayout()
    def CreateSizer(self):
        self.TopSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_vsizer = wx.BoxSizer(wx.VERTICAL)
        self.right_vsizer = wx.BoxSizer(wx.VERTICAL)
        self.sub_vsizer = wx.BoxSizer(wx.VERTICAL)
    def CreateElementForLeftSizer(self):
        self.SymbolNumberBox()
        self.SymbolRateBox()
        self.SimpleBox()
        self.CarrierBox()
        self.EyeBox()
        self.ImpulseChoiceBox()
        self.CodeChoiceBox()
        self.RZRatioBox()
        self.RaisedCosineBox()
        self.PartialResponseBox()
        self.GausseFilterBox()
        self.ModulateChoiceBox()
        self.FigureShowBox()
        self.ButtonBox()
    def CreateElementForRightSizer(self):
        self.Figure = Figure(figsize = (4, 4))
        self.axes = self.Figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.Canvas = FigureCanvas(self, -1, self.Figure)
        self.Navigation = NavigationToolbar(self.Canvas) 
        self.Canvas.mpl_connect('motion_notify_event', self.CanvasOnMouseMove);
        self.StaticText = wx.StaticText(self, -1, label = 'Mouse Location');
        self.CreateNoteBoxForRightSizer()
    def CanvasOnMouseMove(self, event):
        ex=event.xdata   
        ey=event.ydata   
        if ex and ey:
            self.StaticText.SetLabel('(%s, %s)' % (ex, ey))
    def CreateNoteBoxForRightSizer(self):
        self.showBox = wx.StaticBoxSizer(wx.StaticBox(self,-1,u'状态显示'),wx.VERTICAL)
        self.DisplayText=wx.TextCtrl(self,-1,"",size=(35,-1),style=wx.TE_MULTILINE)
        self.DisplayText.AppendText(u"请配置参数...\n")
        self.showBox.Add(self.DisplayText,0,wx.EXPAND|wx.ALL,2)
    def AddElementForRightSizer(self):
        self.sub_vsizer.Add(self.Navigation, 0, wx.ALL|wx.EXPAND)
        self.sub_vsizer.Add(self.StaticText, 0, wx.ALL | wx.EXPAND);
        self.sub_vsizer.Add(self.Canvas, 1, wx.ALL|wx.EXPAND)
        self.right_vsizer.Add(self.sub_vsizer, 1, wx.ALL|wx.EXPAND)
        self.right_vsizer.Add(self.showBox, 0, wx.ALL|wx.EXPAND )
    def AddElementForLeftSizer(self):   
        self.left_vsizer.Add(self.symbolNumberBox, 0, wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.symbolRateBox, 0, wx.ALL|wx.EXPAND, 5)       
        self.left_vsizer.Add(self.sampleBox, 0, wx.ALL|wx.EXPAND, 5)     
        self.left_vsizer.Add(self.ImpulseChoiceSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.RaisedCosineSizer, 0,  wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.partialBox, 0,  wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.gaussBox, 0,  wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.CodeChoiceSizer, 0, wx.ALL|wx.EXPAND, 5) 
        self.left_vsizer.Add(self.rectRatioBox, 0,  wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.ModulateSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.carrierBox, 0, wx.ALL|wx.EXPAND, 5)        
        self.left_vsizer.Add(self.eyeBox, 0, wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.FigureSizer, 1, wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Add(self.buttonBox, 0, wx.ALL|wx.EXPAND, 5)
        self.left_vsizer.Hide(self.RaisedCosineSizer)
        self.left_vsizer.Hide(self.partialBox)
        self.left_vsizer.Hide(self.gaussBox)
        self.left_vsizer.Hide(self.CodeChoiceSizer)
        self.left_vsizer.Hide(self.rectRatioBox)

    def ConfigSizersLayout(self):
        self.TopSizer.Add(self.left_vsizer, 1, wx.ALL|wx.EXPAND, 3)
        self.TopSizer.Add(self.right_vsizer,4, wx.ALL|wx.EXPAND, 3)
        self.SetSizer(self.TopSizer)
        self.Layout()
    def SymbolNumberBox(self):
        self.staticSymbolNumBox = wx.StaticBox(self, -1, u"码元数量")
        self.symbolNumberBox = wx.StaticBoxSizer(self.staticSymbolNumBox, wx.VERTICAL)      
        self.NumberTextCtrl = wx.TextCtrl(self, -1, "100",style = wx.TE_PROCESS_ENTER)
        self.NumberTextCtrl.SetToolTipString(u"按回车键结束输入")
        self.NumberTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.TextNumber)
        self.symbolNumberBox.Add(self.NumberTextCtrl, 1, wx.ALL|wx.EXPAND, 5)    
    def SymbolRateBox(self):
        self.staticSymbolRateBox = wx.StaticBox(self, -1, u"码元速率(Baud)")
        self.symbolRateBox = wx.StaticBoxSizer(self.staticSymbolRateBox, wx.VERTICAL)
        self.RateTextCtrl = wx.TextCtrl(self, -1, "1", style = wx.TE_PROCESS_ENTER)
        self.RateTextCtrl.SetToolTipString(u"按回车键结束输入")
        self.RateTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.TextNumber)
        self.symbolRateBox.Add(self.RateTextCtrl, 1, wx.ALL|wx.EXPAND, 5)
    def SimpleBox(self):
        self.staticSampleBox = wx.StaticBox(self, -1, u"采样频率(Hz)")
        self.sampleBox = wx.StaticBoxSizer(self.staticSampleBox, wx.VERTICAL)
        self.SampleTextCtrl = wx.TextCtrl(self, -1, "20", style = wx.TE_PROCESS_ENTER)
        self.SampleTextCtrl.SetToolTipString(u"按回车键结束输入")
        self.SampleTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.TextNumber)
        self.sampleBox.Add(self.SampleTextCtrl, 1, wx.ALL|wx.EXPAND, 5)
    def CarrierBox(self):
        self.statiCarrierBox = wx.StaticBox(self, -1, u"载波频率(Hz)")
        self.carrierBox = wx.StaticBoxSizer(self.statiCarrierBox, wx.VERTICAL)
        self.CarrierTextCtrl = wx.TextCtrl(self, -1, "0", style = wx.TE_PROCESS_ENTER)
        self.CarrierTextCtrl.SetToolTipString(u"按回车键结束输入")
        self.CarrierTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.TextNumber)
        self.carrierBox.Add(self.CarrierTextCtrl, 1, wx.ALL|wx.EXPAND, 5)
    def EyeBox(self):
        self.staticEye = wx.StaticBox(self, -1, u"眼睛个数")
        self.eyeBox = wx.StaticBoxSizer(self.staticEye, wx.VERTICAL)
        self.EyeTextCtrl = wx.TextCtrl(self, -1, "6", style = wx.TE_PROCESS_ENTER)
        self.EyeTextCtrl.SetToolTipString(u"按回车键结束输入")
        self.EyeTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.TextNumber)
        self.eyeBox.Add(self.EyeTextCtrl, 1, wx.ALL|wx.EXPAND, 5)
    def TextNumber(self, event):
        self.number = int(self.NumberTextCtrl.GetValue())
        self.rate = int(self.RateTextCtrl.GetValue())
        self.fc = int(self.CarrierTextCtrl.GetValue())
        self.Fs = int(self.SampleTextCtrl.GetValue())
        self.eye_num = int(self.EyeTextCtrl.GetValue())
    def RZRatioBox(self):
        self.staticRatioBox = wx.StaticBox(self, -1, u"矩形脉冲")
        self.rectRatioBox = wx.StaticBoxSizer(self.staticRatioBox, wx.VERTICAL)
        self.ratioBox = SliderBox(self, -1, u"脉冲宽度", 5, 1, int(self.SampleTextCtrl.GetValue()), 1,1)
        self.ratioBox.slider.Bind(wx.EVT_SLIDER, self.OnRatioSlider)
        self.rectRatioBox.Add(self.ratioBox.staticText, 0, wx.CENTER)
        self.rectRatioBox.Add(self.ratioBox.slider, 1, wx.ALL|wx.EXPAND, 5)
        self.rectRatioBox.Add(self.ratioBox.textCtrl, 1, wx.ALL|wx.EXPAND, 5)
    def OnRatioSlider(self, event):
        self.ratioBox.textCtrl.SetValue(str(int(self.ratioBox.slider.GetValue())/1))
        event.Skip()
    def RaisedCosineBox(self):
        self.alphBox = SliderBox(self, -1, u"滚降系数", 0, 0, 10, 1, 10)      
        self.alphBox.slider.Bind(wx.EVT_SLIDER, self.OnAlphSlider)
        self.staticRaisedBox = wx.StaticBox(self, -1, u"升余弦脉冲")
        self.RaisedCosineSizer = wx.StaticBoxSizer(self.staticRaisedBox, wx.VERTICAL)
        self.RaisedCosineSizer.Add(self.alphBox.staticText, 0, wx.CENTER)
        self.RaisedCosineSizer.Add(self.alphBox.slider, 1, wx.ALL|wx.EXPAND, 5)
        self.RaisedCosineSizer.Add(self.alphBox.textCtrl, 1, wx.ALL|wx.EXPAND, 5)    
    def OnAlphSlider(self, event):
        self.alphBox.textCtrl.SetValue(str(float(self.alphBox.slider.GetValue()) / 10))
        self.alph = float(self.alphBox.slider.GetValue()) / 10          
        event.Skip()
    def PartialResponseBox(self):
        self.staticPartialBox = wx.StaticBox(self, -1, u"部分响应")
        self.partialBox = wx.StaticBoxSizer(self.staticPartialBox, wx.VERTICAL)
        self.typeChoice = wx.ComboBox(self, -1, u"必选", choices = GetPartialTypeChoiceList())
        self.typeChoice.SetStringSelection(u'第一类部分响应波形')
        self.typeChoice.Bind(wx.EVT_COMBOBOX, self.PartialType)
        self.partialBox.Add(self.typeChoice, 1, wx.ALL|wx.EXPAND, 5)
    def PartialType(self, event):
        self.frqlabel = [
                 r'$H(f)=2T_s cos\pi fT_s \, , \; |f| \leq \frac{1}{2T_s}$',
                 r'$H(f)=4T_s {cos}^2\pi fT_s \, , \; |f| \leq \frac{1}{2T_s}$',
                 r'$H(f)=2T_s cos\pi fT_s \sqrt{5-4cos2\pi f T_s}\, , \; |f| \leq \frac{1}{2T_s}$',
                 r'$H(f)=2T_s {sin}^2 2\pi fT_s \, , \; |f| \leq \frac{1}{2T_s}$',
                 r'$H(f)=4T_s {sin}^2 2\pi fT_s \, , \; |f| \leq \frac{1}{2T_s}$',                 
                 ]
        self.frqlab = self.frqlabel[self.typeChoice.GetSelection()]
        print 'type: ',self.typeChoice.GetSelection()
    def GausseFilterBox(self):
        self.staticGaussBox = wx.StaticBox(self, -1, u"高斯滤波")
        self.sigmaBox = SliderBox(self, -1, u"方差", 4, 1, 10, 1, 10)
        self.sigmaBox.slider.Bind(wx.EVT_SLIDER, self.OnSigmaSlider)
        self.gaussBox = wx.StaticBoxSizer(self.staticGaussBox, wx.VERTICAL)
        self.gaussBox.Add(self.sigmaBox.staticText, 0, wx.CENTER)
        self.gaussBox.Add(self.sigmaBox.slider, 1, wx.ALL|wx.EXPAND, 5)
        self.gaussBox.Add(self.sigmaBox.textCtrl, 1, wx.ALL|wx.EXPAND, 5)
    def OnSigmaSlider(self, event):
        self.sigmaBox.textCtrl.SetValue(str(float(self.sigmaBox.slider.GetValue())/10))
        self.sigma = float(self.sigmaBox.slider.GetValue())/10
        event.Skip()
    def ImpulseChoiceBox(self):
        self.impulseChoiceBox = wx.ComboBox(self, -1, u"必选", choices = GetImpulseChoiceList())
        self.staticImpulse = wx.StaticBox(self, -1, u"脉冲成型")
        self.ImpulseChoiceSizer = wx.StaticBoxSizer(self.staticImpulse, wx.VERTICAL)
        self.ImpulseChoiceSizer.Add(self.impulseChoiceBox, 1, wx.ALL|wx.EXPAND, 5)
        self.impulseChoiceBox.Bind(wx.EVT_COMBOBOX, self.ChoiceBoxSwitchFunc)
    def ChoiceBoxSwitchFunc(self, event):             
        if self.impulseChoiceBox.GetLabelText() == RaisedCosineBoxName():
            self.frqlab = r'$H(f)=\frac{T_s}{2}[1+sin\frac{T_s}{2 \alpha}(\frac{\pi}{T_s}-2 \pi f)] \, , \;  \frac{(1-\alpha)}{2T_s} \leq |f| \leq \frac{(1+\alpha)}{2T_s}$'
            self.left_vsizer.Show(self.RaisedCosineSizer)
            self.left_vsizer.Hide(self.partialBox)
            self.left_vsizer.Hide(self.gaussBox)
            self.left_vsizer.Hide(self.CodeChoiceSizer)
            self.left_vsizer.Hide(self.rectRatioBox)
            self.left_vsizer.Layout() #强制重绘
        elif self.impulseChoiceBox.GetLabelText() == PartialBoxName():  
            self.frqlab = r'$H(f)=2T_s cos\pi fT_s \, , \; |f| \leq \frac{1}{2T_s}$'
            self.left_vsizer.Show(self.partialBox)
            self.left_vsizer.Hide(self.RaisedCosineSizer)
            self.left_vsizer.Hide(self.gaussBox)
            self.left_vsizer.Hide(self.CodeChoiceSizer)
            self.left_vsizer.Hide(self.rectRatioBox)
            self.left_vsizer.Layout()
        elif self.impulseChoiceBox.GetLabelText() == GaussBoxName():
            self.frqlab = u'高斯脉冲频谱'
            self.left_vsizer.Show(self.gaussBox)
            self.left_vsizer.Hide(self.RaisedCosineSizer)
            self.left_vsizer.Hide(self.partialBox)
            self.left_vsizer.Hide(self.CodeChoiceSizer)
            self.left_vsizer.Hide(self.rectRatioBox)
            self.left_vsizer.Layout()
        else:
            self.frqlab = u'矩形脉冲频谱'
            self.left_vsizer.Show(self.CodeChoiceSizer)
            self.left_vsizer.Show(self.rectRatioBox)
            self.left_vsizer.Hide(self.RaisedCosineSizer)
            self.left_vsizer.Hide(self.partialBox)
            self.left_vsizer.Hide(self.gaussBox)
            self.left_vsizer.Layout()
            
    def CodeChoiceBox(self):
        self.codeChoiceBox = wx.ComboBox(self, -1, u"必选", choices = GetCodeChoiceList())
        self.codeChoiceBox.SetStringSelection(u'非归零矩形脉冲')
        self.staticCode = wx.StaticBox(self, -1, u"码型选择")
        self.CodeChoiceSizer = wx.StaticBoxSizer(self.staticCode, wx.VERTICAL)
        self.CodeChoiceSizer.Add(self.codeChoiceBox, 1, wx.ALL|wx.EXPAND, 5)
        self.codeChoiceBox.Bind(wx.EVT_COMBOBOX, self.Code)
    def Code(self, event):
        self.DisplayText.AppendText(self.codeChoiceBox.GetSelection())
        
    def ModulateChoiceBox(self):
        self.modulateChoiceBox = wx.ComboBox(self, -1, u"必选", choices = GetModulateChoiecList())
        self.modulateChoiceBox.SetStringSelection('2PSK')
        self.modulateChoiceBox.Bind(wx.EVT_COMBOBOX, self.ModulateChoice)
        self.staticModulate = wx.StaticBox(self, -1, u"调制方式")
        self.ModulateSizer = wx.StaticBoxSizer(self.staticModulate, wx.VERTICAL)
        self.ModulateSizer.Add(self.modulateChoiceBox, 1, wx.ALL|wx.EXPAND, 5)
    def ModulateChoice(self, event): 
        if self.modulateChoiceBox.GetCurrentSelection() == -1:
            self.DisplayText.AppendText(u"请选择调制方式...")
            retCode = wx.MessageBox(u'请选择调制方式!', u'错误提示', wx.OK|wx.ICON_EXCLAMATION)
    def FigureShowBox(self):
        self.figureChoiceBox = wx.CheckListBox(self, -1,  choices = GetFigureChoiceList())
        self.figureChoiceBox.Bind(wx.EVT_CHECKLISTBOX, self.FigureShow)
        self.staticFigure = wx.StaticBox(self, -1, u"图形显示")
        self.FigureSizer = wx.StaticBoxSizer(self.staticFigure, wx.VERTICAL)
        self.FigureSizer.Add(self.figureChoiceBox, 1, wx.ALL|wx.EXPAND, 5)
    def FigureShow(self, event):
        self.count=0     
        images_number=len(GetFigureChoiceList())  #所选图像的总数
        self.images=np.zeros(images_number,int)        
        for i in range(images_number):
            if self.figureChoiceBox.IsChecked(i):
                self.count=self.count+1
                self.images[i]=self.count
        
    def PlotConfig(self, event):
        if self.count > 4:
            self.DisplayText.AppendText(u"最多选择四幅图像，请重新选择...\n")
            retCode = wx.MessageBox(u'最多选择四幅图像，请重新选择!', u'错误提示', wx.OK|wx.ICON_EXCLAMATION)
        elif self.count < 4:
            self.n=1
            self.m=self.count
            self.Draw(self)
        else:
            self.m=2
            self.n=2  
            self.Draw(self)
        
    def Draw(self,event):
        self.Figure.clear()
        self.plotDate = ChannelSourceFigure(self)
        self.plotDate.draw_figure()       
    def ButtonBox(self):
        self.buttonBox = wx.BoxSizer(wx.VERTICAL)
        self.static = wx.StaticBox(self, -1, u" ")
        self.buttonBox = wx.StaticBoxSizer(self.static, wx.VERTICAL)
        self.starbutton = wx.Button(self, -1, u"开始")
        self.starbutton.SetToolTipString(u"开始运行")
        self.starbutton.Bind(wx.EVT_BUTTON, self.OnStart)
        self.buttonBox.Add(self.starbutton, 1, wx.ALL|wx.EXPAND, 5)
    def OnStart(self, event):  
        if self.impulseChoiceBox.GetCurrentSelection() == -1:
            self.DisplayText.AppendText(u"请选择脉冲成型方式...\n")  
            retCode = wx.MessageBox(u'请选择脉冲成型方式!', u'错误提示', wx.OK|wx.ICON_EXCLAMATION)
        else:
            self.number = int(self.NumberTextCtrl.GetValue())                    
            self.rate = int(self.RateTextCtrl.GetValue())
            self.Fs = int(self.SampleTextCtrl.GetValue()) 
            self.ratio = int(self.ratioBox.slider.GetValue())/1
            self.alph = float(self.alphBox.slider.GetValue()) / 10 
            self.sigma = float(self.sigmaBox.slider.GetValue())/10
            self.fc = int(self.CarrierTextCtrl.GetValue())
            self.x = numpy.arange(-10.0/self.rate,10.0/self.rate,1.0/self.Fs/self.rate)        
            self.impulsetype = self.impulseChoiceBox.GetSelection()       
            self.partialtype = self.typeChoice.GetSelection()
            self.codetype = self.codeChoiceBox.GetSelection()
            self.modulatetype = self.modulateChoiceBox.GetSelection()              
            self.label,self.impulse = Impulse_time(self.impulsetype, self.alph, self.x, self.Fs, 
                                                   self.rate, self.partialtype, self.sigma,self.codetype, self.ratio)
            self.f1,self.ImpulSpectrum = spectrum(self.impulse, self.Fs, self.rate)
            self.real,self.image, self.div = ModulateType(self.modulatetype, self.number, self.Fs)      
            self.modulateReal = DoConvolution(self.impulse, self.real)            
            self.modulateImage = DoConvolution(self.impulse, self.image)
            self.eye_num = int(self.EyeTextCtrl.GetValue())  
            self.x1 = numpy.linspace(-10.0/self.rate, (1.0*self.number/self.div/self.rate)+(10.0/self.rate), len(self.modulateReal))
            self.signal, self.Idata, self.Qdata = modulate(self.modulateReal, self.modulateImage, self.x1, self.fc)
            self.f2,self.Spectrum = spectrum(self.signal, self.Fs, self.rate)
            self.a = self.modulateReal[15.0*self.Fs:(self.number*self.Fs/self.div)+5.0*self.Fs:self.Fs]
            self.b = self.modulateImage[15.0*self.Fs:(self.number*self.Fs/self.div)+5.0*self.Fs:self.Fs]  
            self.DisplayText.AppendText(u"请等待...\n")                
            self.PlotConfig(self)
            self.channel_in = []  
            for i in range(len(self.modulateReal)/self.Fs):
                self.channel_in += list(self.modulateReal[i*self.Fs : (i+1)*self.Fs])
                self.channel_in += list(self.modulateImage[i*self.Fs : (i+1)*self.Fs])
            print len(self.modulateReal),len(self.modulateImage),len(self.channel_in)
            get_value(self);
class NewFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "frame", size = (800, 600))
        self.newPanel = ChannelSource(self)
if __name__ == '__main__':
    app = wx.PySimpleApp()
    NewFrame(None).Show(True)
    app.MainLoop()

