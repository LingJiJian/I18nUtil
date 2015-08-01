#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 扫描中文工具
# author B-y 342854406@qq.com

import os
import wx
import lk

class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, "Language Trans Util", size = (500, 305))
    panel = wx.Panel(self)

    wx.StaticText(panel,-1,u"扫描目录:",(10,10))
    self.input_indir = wx.TextCtrl(panel, -1,"", pos=(80, 10),size=(330,22))
    self.btnIn = wx.Button(panel,label=u"浏览", pos=(410,5),size=(70,22))
    self.btnIn.Bind(wx.EVT_BUTTON,self.onBtnInDir)

    wx.StaticText(panel,-1,u"输出目录:",(10,35))
    self.input_outdir = wx.TextCtrl(panel, -1,"", pos=(80, 35),size=(330,22))
    self.btnOut = wx.Button(panel,label=u"浏览", pos=(410,30),size=(70,22))
    self.btnOut.Bind(wx.EVT_BUTTON,self.onBtnOutDir)

    self.text_log = wx.TextCtrl(panel,-1,"",pos=(10,65),size=(470,170),style=wx.TE_MULTILINE)

    self.btnRun = wx.Button(panel,label=u"运行",pos=(410,240),size=(70,22))
    self.btnRun.Bind(wx.EVT_BUTTON,self.onBtnRun)

    lk.FileManager().setLogCallFuc(self.onLogRefresh)

  def onBtnInDir(self, event):
  	wildcard = "Lua source (*.lua)|*.lua|All files (*.*)|*.*"
        dialog = wx.DirDialog(None, "Choose a directory", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
          self.input_indir.SetValue(dialog.GetPath())
          lk.FileManager().setInDir(dialog.GetPath())
          dialog.Destroy()

  def onBtnOutDir(self,event):
  	wildcard = "Lua source (*.lua)|*.lua|All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Save i18n file", os.getcwd(),"", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
          self.input_outdir.SetValue(dialog.GetPath())
          lk.FileManager().setOutDir(dialog.GetPath())
          dialog.Destroy()

  def onBtnRun(self,event):
    self.onLogRefresh({"isBegin":True})
    lk.FileManager().run()
    

  def onLogRefresh(self,data):
    if data.get("isFinish",False):
      self.text_log.SetValue(u"扫描完成!")
    elif data.get("isBegin",False):
      self.text_log.SetValue(u"正在扫描...")
  	
class App(wx.App):
  def __init__(self,redirect=False,filename=None):
  	wx.App.__init__(self,redirect,filename)

  def OnInit(self):
    self.frame = MyFrame()
    self.frame.Show()
    return True


if __name__ == '__main__':
  app = App()
  app.MainLoop()

