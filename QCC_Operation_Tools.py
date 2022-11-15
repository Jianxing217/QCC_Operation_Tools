  # -*- coding: utf-8 -*-
import wx
import subprocess
import _thread  
from six import with_metaclass
from QCC_Operation_Tools.WX_GUI import MyFrame1


if __name__ == '__main__':
  ex = wx.App() 
  WX_GUI = MyFrame1(None) 
#  thread.start_new_thread(WX_GUI.gauge_process,(filename,))
  WX_GUI.Show()
  ex.MainLoop()
