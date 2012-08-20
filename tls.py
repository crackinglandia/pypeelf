#Boa:Frame:tls
#
#   Description:
#       TLS Viewer/Editor
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

__revision__ = "$Id: tls.py 280 2009-10-27 00:51:57Z reversing $"

import wx

from app import pedata
from app.common import hex_up

def create(parent):
    return tls(parent)

[wxID_TLS, wxID_TLSCALL_BACK_TABLE_VA, wxID_TLSCHARACTERISTICS, 
 wxID_TLSDATA_BLOCK_END_VA, wxID_TLSDATA_BLOCK_START_VA, 
 wxID_TLSINDEX_VARIABLE_VA, wxID_TLSOK, wxID_TLSSAVE, 
 wxID_TLSSIZE_OF_ZERO_FILL, wxID_TLSTLS_INFORMATION, 
 wxID_TLS_CALLBACK_TABLE_VA, wxID_TLS_CHARACTERISTICS, 
 wxID_TLS_DATA_BLOCK_END_VA, wxID_TLS_DATA_BLOCK_START_VA, 
 wxID_TLS_INDEX_VARIABLE_VA, wxID_TLS_SIZE_OF_ZERO_FILL, 
] = [wx.NewId() for _init_ctrls in range(16)]

class tls(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_TLS, name='tls', parent=prnt,
              pos=wx.Point(490, 330), size=wx.Size(380, 229),
              style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER, title='TLS Table')
        
        self.SetClientSize(wx.Size(364, 193))

        self.tls_information = wx.StaticBox(id=wxID_TLSTLS_INFORMATION,
              label='TLS Information', name='tls_information', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(264, 176), style=0)

        self.data_block_start_va = wx.StaticText(id=wxID_TLSDATA_BLOCK_START_VA,
              label='DataBlockStartVA', name='data_block_start_va', parent=self,
              pos=wx.Point(16, 40), size=wx.Size(85, 13), style=0)

        self.data_block_end_va = wx.StaticText(id=wxID_TLSDATA_BLOCK_END_VA,
              label='DataBlockEndVA', name='data_block_end_va', parent=self,
              pos=wx.Point(16, 64), size=wx.Size(79, 13), style=0)

        self.index_variable_va = wx.StaticText(id=wxID_TLSINDEX_VARIABLE_VA,
              label='IndexVariableVA', name='index_variable_va', parent=self,
              pos=wx.Point(16, 88), size=wx.Size(80, 13), style=0)

        self.call_back_table_va = wx.StaticText(id=wxID_TLSCALL_BACK_TABLE_VA,
              label='CallbackTableVA', name='call_back_table_va', parent=self,
              pos=wx.Point(16, 112), size=wx.Size(79, 13), style=0)

        self.size_of_zero_fill = wx.StaticText(id=wxID_TLSSIZE_OF_ZERO_FILL,
              label='SizeOfZeroFill', name='size_of_zero_fill', parent=self,
              pos=wx.Point(16, 136), size=wx.Size(66, 13), style=0)

        self.characteristics = wx.StaticText(id=wxID_TLSCHARACTERISTICS,
              label='Characteristics', name='characteristics', parent=self,
              pos=wx.Point(16, 160), size=wx.Size(72, 13), style=0)

        self.ok = wx.Button(id=wxID_TLSOK, label='OK', name='ok', parent=self,
              pos=wx.Point(280, 16), size=wx.Size(75, 23), style=0)

        self.save = wx.Button(id=wxID_TLSSAVE, label='Save', name='save',
              parent=self, pos=wx.Point(280, 40), size=wx.Size(75, 23),
              style=0)

        self._data_block_start_va = wx.TextCtrl(id=wxID_TLS_DATA_BLOCK_START_VA,
              name='_data_block_start_va', parent=self, pos=wx.Point(120, 32),
              size=wx.Size(100, 21), style=0, value='')

        self._data_block_end_va = wx.TextCtrl(id=wxID_TLS_DATA_BLOCK_END_VA,
              name='_data_block_end_va', parent=self, pos=wx.Point(120, 56),
              size=wx.Size(100, 21), style=0, value='')

        self._index_variable_va = wx.TextCtrl(id=wxID_TLS_INDEX_VARIABLE_VA,
              name='_index_variable_va', parent=self, pos=wx.Point(120, 80),
              size=wx.Size(100, 21), style=0, value='')

        self._callback_table_va = wx.TextCtrl(id=wxID_TLS_CALLBACK_TABLE_VA,
              name='_callback_table_va', parent=self, pos=wx.Point(120, 104),
              size=wx.Size(100, 21), style=0, value='')

        self._size_of_zero_fill = wx.TextCtrl(id=wxID_TLS_SIZE_OF_ZERO_FILL,
              name='_size_of_zero_fill', parent=self, pos=wx.Point(120, 128),
              size=wx.Size(100, 21), style=0, value='')

        self._characteristics = wx.TextCtrl(id=wxID_TLS_CHARACTERISTICS,
              name='_characteristics', parent=self, pos=wx.Point(120, 152),
              size=wx.Size(100, 21), style=0, value='')

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.save.Bind(wx.EVT_BUTTON, self.OnSaveButton, id=wxID_TLSSAVE)
        
    def __init__(self, parent):
        self.__pe = parent.Parent.peInstance
        self._fp = parent.Parent.get_loaded_file()

        self.__parentDirectory = parent
        
        self._init_ctrls(parent)
        
        self.loadTlsInfo()
    
    def loadTlsInfo(self):
        tlsStruct = pedata.getTlsStruct(self.__pe)
        
        self._data_block_start_va.SetValue(hex_up(tlsStruct.StartAddressOfRawData))
        self._data_block_end_va.SetValue(hex_up(tlsStruct.EndAddressOfRawData))
        self._index_variable_va.SetValue(hex_up(tlsStruct.AddressOfIndex))
        self._callback_table_va.SetValue(hex_up(tlsStruct.AddressOfCallBacks))
        self._size_of_zero_fill.SetValue(hex_up(tlsStruct.SizeOfZeroFill))
        self._characteristics.SetValue(hex_up(tlsStruct.Characteristics))

    def OnClose(self, event):
        self.__parentDirectory.Show()
        self.Destroy()
        
    def OnSaveButton(self, event):
        sVa = int(self._data_block_start_va.GetValue(), 16)
        eVa = int(self._data_block_end_va.GetValue(), 16)
        iVa = int(self._index_variable_va.GetValue(), 16)
        cVa = int(self._callback_table_va.GetValue(), 16)
        sZf = int(self._size_of_zero_fill.GetValue(), 16)
        cHa = int(self._characteristics.GetValue(), 16)
        
        tlsStruct = pedata.getTlsStruct(self.__pe)
        
        tlsStruct.StartAddressOfRawData = sVa
        tlsStruct.EndAddressOfRawData = eVa
        tlsStruct.AddressOfIndex = iVa
        tlsStruct.AddressOfCallBacks = cVa
        tlsStruct.SizeOfZeroFill = sZf
        tlsStruct.Characteristics = cHa
        
        try:
            self.__pe.write(self._fp)
        except IOError, e:
            raise str(e)
        