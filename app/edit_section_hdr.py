#Boa:Frame:edit_section_hdr

#
#   Description:
#       Edit Section Header Window
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

__revision__ = "$Id: edit_section_hdr.py 296 2010-02-09 22:48:44Z reversing $"

import wx

from app import set_section_flags
from app.common import hex_up, toInt

def create(parent):
    return edit_section_hdr(parent)

[wxID_EDIT_SECTION_HDR, wxID_EDIT_SECTION_HDRCANCEL, 
 wxID_EDIT_SECTION_HDRFLAGS, wxID_EDIT_SECTION_HDRNAME, 
 wxID_EDIT_SECTION_HDROK, wxID_EDIT_SECTION_HDRRAW_OFFSET, 
 wxID_EDIT_SECTION_HDRRAW_SIZE, wxID_EDIT_SECTION_HDRSECTION_HEADER, 
 wxID_EDIT_SECTION_HDRVIRTUAL_ADDRESS, wxID_EDIT_SECTION_HDRVIRTUAL_SIZE, 
 wxID_EDIT_SECTION_HDR_FLAGS, wxID_EDIT_SECTION_HDR_NAME, 
 wxID_EDIT_SECTION_HDR_RAW_OFFSET, wxID_EDIT_SECTION_HDR_RAW_SIZE, 
 wxID_EDIT_SECTION_HDR_VIRTUAL_ADDESS, wxID_EDIT_SECTION_HDR_VIRTUAL_SIZE, 
 wxID_EDIT_SECTION_HDR__FLAGS, 
] = [wx.NewId() for _init_ctrls in range(17)]

class edit_section_hdr(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_EDIT_SECTION_HDR,
              name='edit_section_hdr', parent=prnt, pos=wx.Point(459, 348),
              size=wx.Size(362, 218), style=wx.DEFAULT_FRAME_STYLE,
              title='[ Edit Section Header ]')
        self.SetClientSize(wx.Size(346, 182))

        self.section_header = wx.StaticBox(id=wxID_EDIT_SECTION_HDRSECTION_HEADER,
              label='Section Header', name='section_header', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(256, 176), style=0)

        self.save = wx.Button(id=wxID_EDIT_SECTION_HDROK, label='Save', name='save',
              parent=self, pos=wx.Point(264, 8), size=wx.Size(75, 23), style=0)

        self.cancel = wx.Button(id=wxID_EDIT_SECTION_HDRCANCEL, label='Cancel',
              name='cancel', parent=self, pos=wx.Point(264, 32),
              size=wx.Size(75, 23), style=0)

        self.name = wx.StaticText(id=wxID_EDIT_SECTION_HDRNAME, label='Name',
              name='name', parent=self, pos=wx.Point(16, 24), size=wx.Size(28,
              13), style=0)

        self.virtual_address = wx.StaticText(id=wxID_EDIT_SECTION_HDRVIRTUAL_ADDRESS,
              label='VirtualAddress', name='virtual_address', parent=self,
              pos=wx.Point(16, 48), size=wx.Size(70, 13), style=0)

        self.virtual_size = wx.StaticText(id=wxID_EDIT_SECTION_HDRVIRTUAL_SIZE,
              label='VirtualSize', name='virtual_size', parent=self,
              pos=wx.Point(16, 72), size=wx.Size(50, 13), style=0)

        self.raw_offset = wx.StaticText(id=wxID_EDIT_SECTION_HDRRAW_OFFSET,
              label='RawOffset', name='raw_offset', parent=self,
              pos=wx.Point(16, 96), size=wx.Size(53, 13), style=0)

        self.raw_size = wx.StaticText(id=wxID_EDIT_SECTION_HDRRAW_SIZE,
              label='RawSize', name='raw_size', parent=self, pos=wx.Point(16,
              120), size=wx.Size(41, 13), style=0)

        self.flags = wx.StaticText(id=wxID_EDIT_SECTION_HDRFLAGS, label='Flags',
              name='flags', parent=self, pos=wx.Point(16, 144), size=wx.Size(26,
              13), style=0)

        self._name = wx.TextCtrl(id=wxID_EDIT_SECTION_HDR_NAME, name='_name',
              parent=self, pos=wx.Point(120, 24), size=wx.Size(100, 21),
              style=0, value='')

        self._virtual_address = wx.TextCtrl(id=wxID_EDIT_SECTION_HDR_VIRTUAL_ADDESS,
              name='_virtual_addess', parent=self, pos=wx.Point(120, 48),
              size=wx.Size(100, 21), style=0, value='')

        self._virtual_size = wx.TextCtrl(id=wxID_EDIT_SECTION_HDR_VIRTUAL_SIZE,
              name='_virtual_size', parent=self, pos=wx.Point(120, 72),
              size=wx.Size(100, 21), style=0, value='')

        self._raw_offset = wx.TextCtrl(id=wxID_EDIT_SECTION_HDR_RAW_OFFSET,
              name='_raw_offset', parent=self, pos=wx.Point(120, 96),
              size=wx.Size(100, 21), style=0, value='')

        self._raw_size = wx.TextCtrl(id=wxID_EDIT_SECTION_HDR_RAW_SIZE,
              name='_raw_size', parent=self, pos=wx.Point(120, 120),
              size=wx.Size(100, 21), style=0, value='')

        self._flags = wx.TextCtrl(id=wxID_EDIT_SECTION_HDR_FLAGS, name='_flags',
              parent=self, pos=wx.Point(120, 144), size=wx.Size(100, 21),
              style=0, value='')

        self.__flags = wx.Button(id=wxID_EDIT_SECTION_HDR__FLAGS, label='...',
              name='__flags', parent=self, pos=wx.Point(224, 144),
              size=wx.Size(24, 23), style=0)

        self.cancel.Bind(wx.EVT_BUTTON, self.OnCancel, id=wxID_EDIT_SECTION_HDRCANCEL)
        self.save.Bind(wx.EVT_BUTTON, self.OnSave, id=wxID_EDIT_SECTION_HDROK)
        self.__flags.Bind(wx.EVT_BUTTON, self.OnFlags, id=wxID_EDIT_SECTION_HDR__FLAGS)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __init__(self, parent):
        self.parent = parent
        
        self._init_ctrls(parent)
        
        self.flags = None
        self.LoadSectionHdrInfo()
        
    def OnClose(self, event):
        self.parent.Show()
        self.Destroy()

    def OnCancel(self, event):
        self.OnClose(event)

    def OnSave(self, event):
        # function name is an unicode string
        function_name = self._name.GetValue()
        vs = toInt(self._virtual_size.GetValue())
        vo = toInt(self._virtual_address.GetValue())
        rs = toInt(self._raw_size.GetValue())
        ro = toInt(self._raw_offset.GetValue())
        flags = toInt(self._flags.GetValue())
        
        p = self.parent.get_pe_instance()
        
        section = p.sections[self.parent.get_section_index()]
        
        section.Characteristics = flags
        section.Name = str(function_name)
        section.Misc_VirtualSize = vs
        section.VirtualAddress = vo
        section.SizeOfRawData = rs
        section.PointerToRawData = ro
        
        try:
            p.write(self.parent.getFp())
        except IOError, e:
            wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
    
    def OnFlags(self, event):
        fDlg = set_section_flags.create(self)
        fDlg.Show()
        self.Hide()
        
    def LoadSectionHdrInfo(self):
        hdr_data = self.parent.get_section_hdr_data()
        
        self.set_section_flags(hdr_data["Characteristics"])
        
        self._name.SetValue(hdr_data["SectionName"])
        self._virtual_size.SetValue(hex_up(hdr_data["VirtualSize"]))
        self._virtual_address.SetValue(hex_up(hdr_data["VirtualOffset"]))
        self._raw_offset.SetValue(hex_up(hdr_data["RawOffset"]))
        self._raw_size.SetValue(hex_up(hdr_data["RawSize"]))
        self._flags.SetValue(hex_up(hdr_data["Characteristics"]))
    
    def set_section_flags(self, flags):
        self.flags = flags
    
    def get_section_flags(self):
        return self.flags
    