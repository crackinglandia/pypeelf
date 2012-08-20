#Boa:Frame:edit_export_item
#
#   Description:
#       A module to edit exports
#   Author:
#       +NCR/CRC! [ReVeRsEr]
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

__revision__ = "$Id: edit_exports.py 293 2009-12-21 03:16:55Z reversing $"

import wx

from struct import unpack
from app.common import hex_up, toInt

def create(parent):
    return edit_export_item(parent)

[wxID_EDIT_EXPORT_ITEM, wxID_EDIT_EXPORT_ITEMCANCEL, 
 wxID_EDIT_EXPORT_ITEMFUNCTION_NAME, wxID_EDIT_EXPORT_ITEMITEM_INFO, 
 wxID_EDIT_EXPORT_ITEMNAME_ORDINAL, wxID_EDIT_EXPORT_ITEMNAME_RVA, 
 wxID_EDIT_EXPORT_ITEMOK, wxID_EDIT_EXPORT_ITEMRVA, 
 wxID_EDIT_EXPORT_ITEM_FUNCTION_NAME, wxID_EDIT_EXPORT_ITEM_NAME_ORDINAL, 
 wxID_EDIT_EXPORT_ITEM_NAME_RVA, wxID_EDIT_EXPORT_ITEM_RVA, 
] = [wx.NewId() for _init_ctrls in range(12)]

class edit_export_item(wx.Dialog):
    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id=wxID_EDIT_EXPORT_ITEM,
              name='edit_export_item', parent=prnt, pos=wx.Point(367, 470),
              size=wx.Size(482, 172), style=wx.DEFAULT_FRAME_STYLE,
              title='[ Edit Export Item ]')
        
        self.SetClientSize(wx.Size(466, 136))

        self.item_info = wx.StaticBox(id=wxID_EDIT_EXPORT_ITEMITEM_INFO,
              label='Export Item Information', name='item_info', parent=self,
              pos=wx.Point(8, 0), size=wx.Size(360, 128), style=0)

        self.rva = wx.StaticText(id=wxID_EDIT_EXPORT_ITEMRVA, label='RVA',
              name='rva', parent=self, pos=wx.Point(24, 24), size=wx.Size(21,
              13), style=0)

        self.name_ordinal = wx.StaticText(id=wxID_EDIT_EXPORT_ITEMNAME_ORDINAL,
              label='Name Ordinal', name='name_ordinal', parent=self,
              pos=wx.Point(24, 48), size=wx.Size(65, 13), style=0)

        self.name_rva = wx.StaticText(id=wxID_EDIT_EXPORT_ITEMNAME_RVA,
              label='Name RVA', name='name_rva', parent=self, pos=wx.Point(24,
              72), size=wx.Size(51, 13), style=0)

        self.function_name = wx.StaticText(id=wxID_EDIT_EXPORT_ITEMFUNCTION_NAME,
              label='Function Name', name='function_name', parent=self,
              pos=wx.Point(24, 96), size=wx.Size(72, 13), style=0)

        self._rva = wx.TextCtrl(id=wxID_EDIT_EXPORT_ITEM_RVA, name='_rva',
              parent=self, pos=wx.Point(256, 24), size=wx.Size(100, 21),
              style=0, value='')

        self._name_ordinal = wx.TextCtrl(id=wxID_EDIT_EXPORT_ITEM_NAME_ORDINAL,
              name='_name_ordinal', parent=self, pos=wx.Point(256, 48),
              size=wx.Size(100, 21), style=0, value='')

        self._name_rva = wx.TextCtrl(id=wxID_EDIT_EXPORT_ITEM_NAME_RVA,
              name='_name_rva', parent=self, pos=wx.Point(256, 72),
              size=wx.Size(100, 21), style=0, value='')

        self._function_name = wx.TextCtrl(id=wxID_EDIT_EXPORT_ITEM_FUNCTION_NAME,
              name='_function_name', parent=self, pos=wx.Point(112, 96),
              size=wx.Size(244, 21), style=0, value='')

        self.ok = wx.Button(id=wxID_EDIT_EXPORT_ITEMOK, label='OK', name='ok',
              parent=self, pos=wx.Point(384, 8), size=wx.Size(75, 23), style=0)

        self.cancel = wx.Button(id=wxID_EDIT_EXPORT_ITEMCANCEL, label='Cancel',
              name='cancel', parent=self, pos=wx.Point(384, 32),
              size=wx.Size(75, 23), style=0)

        self.cancel.Bind(wx.EVT_BUTTON, self.OnClose)
        self.ok.Bind(wx.EVT_BUTTON, self.OnSaveButton)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __init__(self, parent):
        self.parent = parent
        
        self._init_ctrls(parent)
        
        self.loadData()
        
    def OnClose(self, event):
        self.parent.Show()
        self.Destroy()
    
    def OnSaveButton(self, event):
        rva = toInt(self._rva.GetValue())
        name_ordinal = toInt(self._name_ordinal.GetValue())
        func_name = self._function_name.GetValue()
        name_rva = toInt(self._name_rva.GetValue())
        
        old_ordinal = self.parent.getCurrentItemData()["Ordinal"]
        
        f = self.parent.getPeInstance().DIRECTORY_ENTRY_EXPORT.symbols[old_ordinal]
        
        f.name = func_name
        f.ordinal = name_ordinal
        f.rva = rva

        data = self.parent.getCurrentItemData()
        p = self.parent.getPeInstance()
        e = p.DIRECTORY_ENTRY_EXPORT.struct

        raw_data = p.get_data(e.AddressOfNames, 4 * e.NumberOfNames)

        addr_of_names = list()
        
        for i in range(0, len(raw_data), 4):
            addr_of_names.append(unpack("<L", raw_data[i:i+4])[0])
            
        p.set_dword_at_rva(addr_of_names[data["Ordinal"]], name_rva)
        
        try:
            self.parent.getPeInstance().write(self.parent.getFp())
        except IOError, e:
            wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
        
    def loadData(self):
        data = self.parent.getCurrentItemData()

        self._rva.SetValue(hex_up(data["RVA"]))
        self._name_ordinal.SetValue(hex_up(data["Ordinal"], 4))
        self._function_name.SetValue(data["Name"])

        p = self.parent.getPeInstance()
        e = p.DIRECTORY_ENTRY_EXPORT.struct

        raw_data = p.get_data(e.AddressOfNames, 4 * e.NumberOfNames)

        addr_of_names = list()
        
        for i in range(0, len(raw_data), 4):
            addr_of_names.append(unpack("<L", raw_data[i:i+4])[0])
            
        self._name_rva.SetValue(hex_up(addr_of_names[data["Ordinal"] - 1]))
        