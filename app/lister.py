#Boa:Frame:structure_lister
#
#   Description: 
#       Section Lister
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

__revision__ = "$Id: lister.py 298 2010-02-26 20:43:24Z reversing $"

import wx

def create(parent):
    return structure_lister(parent)

[wxID_STRUCTURE_LISTER, wxID_STRUCTURE_LISTERLISTER, 
] = [wx.NewId() for _init_ctrls in range(2)]

class structure_lister(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_STRUCTURE_LISTER,
              name='structure_lister', parent=prnt, pos=wx.Point(413, 265),
              size=wx.Size(548, 364), style=wx.DEFAULT_FRAME_STYLE,
              title='Structure Lister')
        self.SetClientSize(wx.Size(532, 328))

        self.lister = wx.TextCtrl(id=wxID_STRUCTURE_LISTERLISTER, name='lister',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(520, 312), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER,
              value='')

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __init__(self, parent):
        self._init_ctrls(parent)

        self.parent = parent
        
        self.show_section_header()
        
    def OnClose(self, event):
        self.parent.Show()
        self.Destroy()
        
    def show_section_header(self):
        sections = self.get_pe_instance().sections
        
        for i in range(self.get_pe_instance().FILE_HEADER.NumberOfSections):
            self.lister.WriteText(str(sections[i]) + "\n\n")
    
    def get_pe_instance(self):
        return self.parent.Parent.get_pe_instance()
    