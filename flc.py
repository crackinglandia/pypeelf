#Boa:Frame:flc
#
#   Description:
#       File Location Calculator
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

__revision__ = "$Id: flc.py 236 2009-09-23 01:27:37Z reversing $"

import wx

from app import pedata
from app.common import hex_up, get_hex_bytes

def create(parent):
    return flc(parent)

[wxID_FLC, wxID_FLCADDITIONAL_INFORMATION, wxID_FLCADDRESSES, wxID_FLCBYTES, 
 wxID_FLCCONVERT, wxID_FLCHEXEDIT, wxID_FLCOFFSET, wxID_FLCRVA, 
 wxID_FLCSECTION, wxID_FLCVA, wxID_FLC_BYTES, wxID_FLC_OFFSET, wxID_FLC_RVA, 
 wxID_FLC_SECTION, wxID_FLC_VA, 
] = [wx.NewId() for _init_ctrls in range(15)]

class flc(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FLC, name='flc', parent=prnt,
              pos=wx.Point(457, 381), size=wx.Size(363, 236),
              style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER,
              title='[ File Location Calculator ]')
        self.SetClientSize(wx.Size(347, 200))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.addresses = wx.StaticBox(id=wxID_FLCADDRESSES, label='Addresses',
              name='addresses', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(248, 100), style=0)

        self.additional_information = wx.StaticBox(id=wxID_FLCADDITIONAL_INFORMATION,
              label='Additional Information', name='additional_information',
              parent=self, pos=wx.Point(8, 112), size=wx.Size(248, 80),
              style=0)

        self.convert = wx.Button(id=wxID_FLCCONVERT, label='Convert',
              name='convert', parent=self, pos=wx.Point(264, 16),
              size=wx.Size(75, 23), style=0)

        self.hexedit = wx.Button(id=wxID_FLCHEXEDIT, label='Hex Edit',
              name='hexedit', parent=self, pos=wx.Point(264, 168),
              size=wx.Size(75, 23), style=0)

        self.section = wx.StaticText(id=wxID_FLCSECTION, label='Section',
              name='section', parent=self, pos=wx.Point(24, 136),
              size=wx.Size(36, 13), style=0)

        self.bytes = wx.StaticText(id=wxID_FLCBYTES, label='Bytes',
              name='bytes', parent=self, pos=wx.Point(24, 160), size=wx.Size(28,
              13), style=0)

        self._va = wx.TextCtrl(id=wxID_FLC_VA, name='_va', parent=self,
              pos=wx.Point(144, 24), size=wx.Size(100, 21), style=0, value='')

        self._rva = wx.TextCtrl(id=wxID_FLC_RVA, name='_rva', parent=self,
              pos=wx.Point(144, 48), size=wx.Size(100, 21), style=0, value='')

        self._offset = wx.TextCtrl(id=wxID_FLC_OFFSET, name='_offset',
              parent=self, pos=wx.Point(144, 72), size=wx.Size(100, 21),
              style=0, value='')

        self._section = wx.TextCtrl(id=wxID_FLC_SECTION, name='_section',
              parent=self, pos=wx.Point(144, 136), size=wx.Size(100, 21),
              style=0, value='')

        self._bytes = wx.TextCtrl(id=wxID_FLC_BYTES, name='_bytes', parent=self,
              pos=wx.Point(88, 160), size=wx.Size(156, 21), style=0, value='')

        self.va = wx.Button(id=wxID_FLCVA, label='VA', name='va', parent=self,
              pos=wx.Point(32, 24), size=wx.Size(75, 23), style=wx.NO_BORDER)

        self.rva = wx.Button(id=wxID_FLCRVA, label='RVA', name='rva',
              parent=self, pos=wx.Point(32, 48), size=wx.Size(75, 23), style=wx.NO_BORDER)

        self.offset = wx.Button(id=wxID_FLCOFFSET, label='Offset',
              name='offset', parent=self, pos=wx.Point(32, 72), size=wx.Size(75,
              23), style=wx.NO_BORDER)

        # we do not have an hex editor rigth now so we must hide this button.
        self.hexedit.Enable(False)
        self.hexedit.Hide()
        
        self._va.Enable(False)
        self._offset.Enable(False)
        
        self.va.Bind(wx.EVT_BUTTON, self.OnVAButton, id=wxID_FLCVA)
        self.offset.Bind(wx.EVT_BUTTON, self.OnOffsetButton, id=wxID_FLCOFFSET)
        self.rva.Bind(wx.EVT_BUTTON, self.OnRVAButton, id=wxID_FLCRVA)
        self.convert.Bind(wx.EVT_BUTTON, self.OnConvertButton, id=wxID_FLCCONVERT)
        
    def __init__(self, parent):
        self._init_ctrls(parent)

        self._pe = parent.peInstance
        self.parentDlg = parent
        
    def OnClose(self, event):
        self.parentDlg.Restore()
        self.Destroy()

    def OnVAButton(self, event):
        self._va.Enable(True)
        self._offset.Enable(False)
        self._rva.Enable(False)
        
        self._CleanCtrls()
        
    def OnOffsetButton(self, event):
        self._offset.Enable(True)
        self._rva.Enable(False)
        self._va.Enable(False)
        
        self._CleanCtrls()
        
    def OnRVAButton(self, event):
        self._rva.Enable(True)
        self._offset.Enable(False)
        self._va.Enable(False)

        self._CleanCtrls()
        
    def OnConvertButton(self, event):
        
        if self._rva.IsEnabled():
            self._ConvertFromRVA()
        elif self._offset.IsEnabled():
            self._ConvertFromOffset()
        else:
            self._ConvertFromVA()
    
    def _ConvertFromRVA(self):
        rva = self._rva.GetValue()
        if not rva:
            rva = 0
        else:
            rva = int(rva, 16)
        
        try:
            offset = pedata.fromRvaToOffset(self._pe, rva)
            va = rva + self._pe.OPTIONAL_HEADER.ImageBase
            
            idx = pedata.guess_section_from_rva(self._pe, rva)
            if idx == -1:
                section = "Header"
            else:
                section = self._pe.sections[idx].Name
                
            bytes = get_hex_bytes(self._pe.get_data(rva, 16))
            
            self.PrintDataInCtrls(rva, va, offset, section, bytes)
            
        except Exception, e:
            #import traceback
            #traceback.print_exc()
            self._ShowError(e)

    def _ConvertFromOffset(self):
        offset = self._offset.GetValue()
        
        if not offset:
            offset = 0
        else:
            offset = int(offset, 16)

        try:
            if not offset < self._pe.sections[0].PointerToRawData:
                rva = self._pe.get_rva_from_offset(offset)
            else:
                rva = offset
                
            va = rva + self._pe.OPTIONAL_HEADER.ImageBase
            
            idx = pedata.guess_section_from_rva(self._pe, rva)
            if idx == -1:
                section = "HEADER"
            else:
                section = self._pe.sections[idx].Name
            
            bytes = get_hex_bytes(self._pe.get_data(rva, 16))
            
            self.PrintDataInCtrls(rva, va, offset, section, bytes)
            
        except Exception, e:
            self._ShowError(e)
            
    def _ConvertFromVA(self):
        va = self._va.GetValue()
        if not va:
            va = 0
        else:
            va = int(va, 16)
            
        try:
            rva = va - self._pe.OPTIONAL_HEADER.ImageBase
            offset = pedata.fromRvaToOffset(self._pe, rva)

            idx = pedata.guess_section_from_rva(self._pe, rva)
            if idx == -1:
                section = "HEADER"
            else:
                section = self._pe.sections[idx].Name

            bytes = get_hex_bytes(self._pe.get_data(rva, 16))
            
            self.PrintDataInCtrls(rva, va, offset, section, bytes)
            
        except Exception, e:
            self._ShowError(e)
    
    def PrintDataInCtrls(self, rva, va, offset, section, bytes):
        to_len = 8
        
        if self.parentDlg.Parent._PE64:
            to_len = 16
            
        self._rva.SetValue(hex_up(rva, to_len))
        self._va.SetValue(hex_up(va, to_len))
        self._offset.SetValue(hex_up(offset, to_len))
        self._section.SetValue(section)
        self._bytes.SetValue(bytes)
        
    def _CleanCtrls(self):
        self._rva.SetValue("")
        self._va.SetValue("")
        self._offset.SetValue("")
        self._section.SetValue("")
        self._bytes.SetValue("")
        
    def _ShowError(self, e):
        wx.MessageBox(str(e), "Error", wx.ICON_ERROR)
        