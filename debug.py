#Boa:Frame:debug
#
#   Description:
#       Debug Viewer/Editor
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

__revision__ = "$Id: debug.py 279 2009-10-25 23:53:06Z reversing $"

import wx
import sys

from app import pedata
from app.common import hex_up

def create(parent):
    return debug(parent)

[wxID_DEBUG, wxID_DEBUGDEBUG_LIST, 
] = [wx.NewId() for _init_ctrls in range(2)]

class debug(wx.Frame):
    def _init_coll_debugList_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Characteristics', width=90)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='TimeDateStamp', width=200)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Major Version', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Minor Version', width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT,
              heading='Type', width=-1)
        parent.InsertColumn(col=5, format=wx.LIST_FORMAT_LEFT,
              heading='Size Of Data', width=-1)
        parent.InsertColumn(col=6, format=wx.LIST_FORMAT_LEFT,
              heading='Address Of Raw Data', width=-1)
        parent.InsertColumn(col=7, format=wx.LIST_FORMAT_LEFT,
              heading='Pointer To Raw Data', width=-1)
        
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_DEBUG, name='debug', parent=prnt,
              pos=wx.Point(428, 335), size=wx.Size(705, 207),
              style=wx.DEFAULT_FRAME_STYLE, title='Debug')
        
        self.Centre()
        
        self.SetClientSize(wx.Size(689, 171))

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.debug_list = wx.ListView(id=wxID_DEBUGDEBUG_LIST,
              name='debug_list', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(689, 171), style=wx.LC_SINGLE_SEL | wx.LC_REPORT | wx.LC_SORT_ASCENDING)

        self._init_coll_debugList_Columns(self.debug_list)

        self.debug_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnDebugListItemSelected, id=wxID_DEBUGDEBUG_LIST)

    def __init__(self, parent):
        self.__pe = parent.Parent.peInstance
        self._parentDirectory = parent
        self._init_ctrls(parent)
        self.loadDebugInfo()

    def OnClose(self, parent):
        self._parentDirectory.Show()
        self.Destroy()
        
    def loadDebugInfo(self):
        dbg_info = pedata.getDebugDirectory(self.__pe)
        
        for entry in dbg_info:
            addrOfRawData = entry.struct.AddressOfRawData
            
            index = self.debug_list.InsertStringItem(sys.maxint, hex_up(addrOfRawData))
            
            mjVersion = entry.struct.MajorVersion
            miVersion = entry.struct.MinorVersion
            Charact = entry.struct.Characteristics
            ptrToRawData = entry.struct.PointerToRawData
            _type = entry.struct.Type
            timeDateStamp = entry.struct.TimeDateStamp
            sizeOfData = entry.struct.SizeOfData
            
            self.debug_list.SetStringItem(index, 0, hex_up(Charact))
            self.debug_list.SetStringItem(index, 1, hex_up(timeDateStamp))
            self.debug_list.SetStringItem(index, 2, hex_up(mjVersion, 4))
            self.debug_list.SetStringItem(index, 3, hex_up(miVersion, 4))
            self.debug_list.SetStringItem(index, 4, hex_up(_type, 4))
            self.debug_list.SetStringItem(index, 5, hex_up(sizeOfData))
            self.debug_list.SetStringItem(index, 6, hex_up(addrOfRawData))
            self.debug_list.SetStringItem(index, 7, hex_up(ptrToRawData))
            
    def OnDebugListItemSelected(self, event):
        event.Skip()
        