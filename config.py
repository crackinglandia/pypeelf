#Boa:Frame:options
#
#   Description:
#       This is the configuration window for PyPEELF
#   Author:
#       +NCR/CRC! [ReVeRsEr] (nriva)
#
# Copyright (c) 2009 Nahuel Cayetano Riva <nahuelriva@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__revision__ = "$Id: config.py 230 2009-09-21 21:28:49Z mbordese $"

import wx
import os, sys

from app import config_parser

def create(parent):
    return options(parent)

[wxID_OPTIONS, wxID_OPTIONSPIDS, wxID_OPTIONSTASKLIST, 
 wxID_OPTIONS_PID_CHOICE, 
] = [wx.NewId() for _init_ctrls in range(4)]

class options(wx.Frame):
    def _init_ctrls(self, prnt):
        self.option_list = ["Hexadecimal", "Decimal"]
        
        wx.Frame.__init__(self, id=wxID_OPTIONS, name='options', parent=prnt,
              pos=wx.Point(462, 278), size=wx.Size(236, 146),
              style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER, title='PyPEELF - Options')
        
        self.SetClientSize(wx.Size(220, 110))

        self.tasklist = wx.StaticBox(id=wxID_OPTIONSTASKLIST, label='TaskList',
              name='tasklist', parent=self, pos=wx.Point(8, 0),
              size=wx.Size(200, 100), style=0)

        self._pid_choice = wx.Choice(choices=self.option_list, id=wxID_OPTIONS_PID_CHOICE,
              name='_pid_choice', parent=self, pos=wx.Point(88, 24),
              size=wx.Size(72, 21), style=0)

        self.pids = wx.StaticText(id=wxID_OPTIONSPIDS, label='Show PID in:',
              name='pids', parent=self, pos=wx.Point(16, 24), size=wx.Size(62,
              13), style=0)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self._pid_choice.Bind(wx.EVT_CHOICE, self.OnTaskListChoice, id=wxID_OPTIONS_PID_CHOICE)
        
        self.path = os.path.join(os.path.dirname(__file__), "config/config.cfg")
        
        self.config.open_config_file(self.path)
        default_ch = self.config.get_task_list_section()
        self._pid_choice.SetStringSelection(default_ch)
        
    def __init__(self, parent):
        self.config = config_parser.ConfigFileParser()
        self._init_ctrls(parent)
        self.parentDlg = parent
        
    def OnClose(self, event):
        self.config.write_config()
        self.parentDlg.Restore()
        self.Destroy()
    
    def OnTaskListChoice(self, event):
        self.config.open_config_file(self.path)
        if event.GetString() == self.option_list[0]:
            self.config.set_task_list_section(self.option_list[0].lower())
        else:
            self.config.set_task_list_section(self.option_list[1].lower())
            