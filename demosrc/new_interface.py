# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 16:47:48 2016

@author: Administrator
"""

import wx
from ChannelSource import *
from Channel import *
from Channelsink import *

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title = u"无线通信系统")
        #self.statusBar = self.CreateStatusBar() 
if __name__ == '__main__':
    app = wx.App(False)
    
    frame = MyFrame()
    nb = wx.Notebook(frame)
    nb.AddPage(ChannelSource(nb),u'信源')
    nb.AddPage(Channel(nb), u"信道")
    nb.AddPage(Channelsink(nb), u"信宿")
    
    frame.Show()
    app.MainLoop()
    pass
