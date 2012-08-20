#Boa:Frame:dos_header
#
#   Description:
#       DOS HEADER Window
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

__revision__ = "$Id: dos_header.py 280 2009-10-27 00:51:57Z reversing $"

import wx

from app import pedata
from app.common import hex_up, toInt

def create(parent):
    return dos_header(parent)

[wxID_DOS_HEADER, wxID_DOS_HEADEREXIT, wxID_DOS_HEADERE_CBLP, 
 wxID_DOS_HEADERE_CP, wxID_DOS_HEADERE_CPARHDR, wxID_DOS_HEADERE_CRLC, 
 wxID_DOS_HEADERE_CS, wxID_DOS_HEADERE_CSUM, wxID_DOS_HEADERE_IP, 
 wxID_DOS_HEADERE_LFANEW, wxID_DOS_HEADERE_LFARLC, wxID_DOS_HEADERE_MAGIC, 
 wxID_DOS_HEADERE_MAXALLOC, wxID_DOS_HEADERE_MINALLOC, wxID_DOS_HEADERE_OEMID, 
 wxID_DOS_HEADERE_OEMINFO, wxID_DOS_HEADERE_OVNO, wxID_DOS_HEADERE_RES, 
 wxID_DOS_HEADERE_RES2, wxID_DOS_HEADERE_SP, wxID_DOS_HEADERE_SS, 
 wxID_DOS_HEADEROK, wxID_DOS_HEADERSTATICBOX1, wxID_DOS_HEADER_E_CBLP, 
 wxID_DOS_HEADER_E_CP, wxID_DOS_HEADER_E_CPARHDR, wxID_DOS_HEADER_E_CRLC, 
 wxID_DOS_HEADER_E_CS, wxID_DOS_HEADER_E_CSUM, wxID_DOS_HEADER_E_IP, 
 wxID_DOS_HEADER_E_LFANEW, wxID_DOS_HEADER_E_LFARLC, wxID_DOS_HEADER_E_MAGIC, 
 wxID_DOS_HEADER_E_MAXALLOC, wxID_DOS_HEADER_E_MINALLOC, 
 wxID_DOS_HEADER_E_OEMID, wxID_DOS_HEADER_E_OEMINFO, wxID_DOS_HEADER_E_OVNO, 
 wxID_DOS_HEADER_E_RES, wxID_DOS_HEADER_E_RES2, wxID_DOS_HEADER_E_SP, 
 wxID_DOS_HEADER_E_SS, 
] = [wx.NewId() for _init_ctrls in range(42)]

class dos_header(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_DOS_HEADER, name='dos_header',
              parent=prnt, pos=wx.Point(653, 298), size=wx.Size(529, 322),
              style=wx.DEFAULT_FRAME_STYLE, title='DOS Header')
        self.SetClientSize(wx.Size(513, 286))

        self.staticBox1 = wx.StaticBox(id=wxID_DOS_HEADERSTATICBOX1,
              label='DOS Header Information', name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(416, 272), style=0)

        self.e_magic = wx.StaticText(id=wxID_DOS_HEADERE_MAGIC, label='e_magic',
              name='e_magic', parent=self, pos=wx.Point(24, 32),
              size=wx.Size(40, 13), style=0)

        self.e_cblp = wx.StaticText(id=wxID_DOS_HEADERE_CBLP, label='e_cblp',
              name='e_cblp', parent=self, pos=wx.Point(24, 56), size=wx.Size(32,
              13), style=0)

        self.e_cp = wx.StaticText(id=wxID_DOS_HEADERE_CP, label='e_cp',
              name='e_cp', parent=self, pos=wx.Point(24, 80), size=wx.Size(24,
              13), style=0)

        self.e_crlc = wx.StaticText(id=wxID_DOS_HEADERE_CRLC, label='e_crlc',
              name='e_crlc', parent=self, pos=wx.Point(24, 104),
              size=wx.Size(29, 13), style=0)

        self.e_cparhdr = wx.StaticText(id=wxID_DOS_HEADERE_CPARHDR,
              label='e_cparhdr', name='e_cparhdr', parent=self, pos=wx.Point(24,
              128), size=wx.Size(50, 13), style=0)

        self.e_minalloc = wx.StaticText(id=wxID_DOS_HEADERE_MINALLOC,
              label='e_minalloc', name='e_minalloc', parent=self,
              pos=wx.Point(24, 152), size=wx.Size(50, 13), style=0)

        self.e_maxalloc = wx.StaticText(id=wxID_DOS_HEADERE_MAXALLOC,
              label='e_maxalloc', name='e_maxalloc', parent=self,
              pos=wx.Point(24, 176), size=wx.Size(54, 13), style=0)

        self.e_ss = wx.StaticText(id=wxID_DOS_HEADERE_SS, label='e_ss',
              name='e_ss', parent=self, pos=wx.Point(24, 200), size=wx.Size(23,
              13), style=0)

        self.e_sp = wx.StaticText(id=wxID_DOS_HEADERE_SP, label='e_sp',
              name='e_sp', parent=self, pos=wx.Point(24, 224), size=wx.Size(24,
              13), style=0)

        self.e_csum = wx.StaticText(id=wxID_DOS_HEADERE_CSUM, label='e_csum',
              name='e_csum', parent=self, pos=wx.Point(24, 248),
              size=wx.Size(37, 13), style=0)

        self.e_ip = wx.StaticText(id=wxID_DOS_HEADERE_IP, label='e_ip',
              name='e_ip', parent=self, pos=wx.Point(224, 40), size=wx.Size(21,
              13), style=0)

        self.e_cs = wx.StaticText(id=wxID_DOS_HEADERE_CS, label='e_cs',
              name='e_cs', parent=self, pos=wx.Point(224, 64), size=wx.Size(23,
              13), style=0)

        self.e_lfarlc = wx.StaticText(id=wxID_DOS_HEADERE_LFARLC,
              label='e_lfarlc', name='e_lfarlc', parent=self, pos=wx.Point(224,
              88), size=wx.Size(36, 13), style=0)

        self._e_magic = wx.TextCtrl(id=wxID_DOS_HEADER_E_MAGIC, name='_e_magic',
              parent=self, pos=wx.Point(112, 32), size=wx.Size(100, 21),
              style=0, value='')

        self._e_cblp = wx.TextCtrl(id=wxID_DOS_HEADER_E_CBLP, name='_e_cblp',
              parent=self, pos=wx.Point(112, 56), size=wx.Size(100, 21),
              style=0, value='')

        self._e_cp = wx.TextCtrl(id=wxID_DOS_HEADER_E_CP, name='_e_cp',
              parent=self, pos=wx.Point(112, 80), size=wx.Size(100, 21),
              style=0, value='')

        self._e_crlc = wx.TextCtrl(id=wxID_DOS_HEADER_E_CRLC, name='_e_crlc',
              parent=self, pos=wx.Point(112, 104), size=wx.Size(100, 21),
              style=0, value='')

        self._e_cparhdr = wx.TextCtrl(id=wxID_DOS_HEADER_E_CPARHDR,
              name='_e_cparhdr', parent=self, pos=wx.Point(112, 128),
              size=wx.Size(100, 21), style=0, value='')

        self._e_minalloc = wx.TextCtrl(id=wxID_DOS_HEADER_E_MINALLOC,
              name='_e_minalloc', parent=self, pos=wx.Point(112, 152),
              size=wx.Size(100, 21), style=0, value='')

        self._e_maxalloc = wx.TextCtrl(id=wxID_DOS_HEADER_E_MAXALLOC,
              name='_e_maxalloc', parent=self, pos=wx.Point(112, 176),
              size=wx.Size(100, 21), style=0, value='')

        self._e_ss = wx.TextCtrl(id=wxID_DOS_HEADER_E_SS, name='_e_ss',
              parent=self, pos=wx.Point(112, 200), size=wx.Size(100, 21),
              style=0, value='')

        self._e_sp = wx.TextCtrl(id=wxID_DOS_HEADER_E_SP, name='_e_sp',
              parent=self, pos=wx.Point(112, 224), size=wx.Size(100, 21),
              style=0, value='')

        self._e_csum = wx.TextCtrl(id=wxID_DOS_HEADER_E_CSUM, name='_e_csum',
              parent=self, pos=wx.Point(112, 248), size=wx.Size(100, 21),
              style=0, value='')

        self._e_ip = wx.TextCtrl(id=wxID_DOS_HEADER_E_IP, name='_e_ip',
              parent=self, pos=wx.Point(296, 40), size=wx.Size(100, 21),
              style=0, value='')

        self._e_cs = wx.TextCtrl(id=wxID_DOS_HEADER_E_CS, name='_e_cs',
              parent=self, pos=wx.Point(296, 64), size=wx.Size(100, 21),
              style=0, value='')

        self._e_lfarlc = wx.TextCtrl(id=wxID_DOS_HEADER_E_LFARLC,
              name='_e_lfarlc', parent=self, pos=wx.Point(296, 88),
              size=wx.Size(100, 21), style=0, value='')

        self.e_ovno = wx.StaticText(id=wxID_DOS_HEADERE_OVNO, label='e_ovno',
              name='e_ovno', parent=self, pos=wx.Point(224, 112),
              size=wx.Size(37, 13), style=0)

        self.e_res = wx.StaticText(id=wxID_DOS_HEADERE_RES, label='e_res',
              name='e_res', parent=self, pos=wx.Point(224, 136),
              size=wx.Size(28, 13), style=0)

        self.e_oemid = wx.StaticText(id=wxID_DOS_HEADERE_OEMID, label='e_oemid',
              name='e_oemid', parent=self, pos=wx.Point(224, 160),
              size=wx.Size(41, 13), style=0)

        self.e_oeminfo = wx.StaticText(id=wxID_DOS_HEADERE_OEMINFO,
              label='e_oeminfo', name='e_oeminfo', parent=self,
              pos=wx.Point(224, 184), size=wx.Size(51, 13), style=0)

        self.e_res2 = wx.StaticText(id=wxID_DOS_HEADERE_RES2, label='e_res2',
              name='e_res2', parent=self, pos=wx.Point(224, 208),
              size=wx.Size(34, 13), style=0)

        self.e_lfanew = wx.StaticText(id=wxID_DOS_HEADERE_LFANEW,
              label='e_lfanew', name='e_lfanew', parent=self, pos=wx.Point(224,
              232), size=wx.Size(45, 13), style=0)

        self._e_ovno = wx.TextCtrl(id=wxID_DOS_HEADER_E_OVNO, name='_e_ovno',
              parent=self, pos=wx.Point(296, 112), size=wx.Size(100, 21),
              style=0, value='')

        self._e_res = wx.TextCtrl(id=wxID_DOS_HEADER_E_RES, name='_e_res',
              parent=self, pos=wx.Point(296, 136), size=wx.Size(100, 21),
              style=0, value='')

        self._e_oemid = wx.TextCtrl(id=wxID_DOS_HEADER_E_OEMID, name='_e_oemid',
              parent=self, pos=wx.Point(296, 160), size=wx.Size(100, 21),
              style=0, value='')

        self._e_oeminfo = wx.TextCtrl(id=wxID_DOS_HEADER_E_OEMINFO,
              name='_e_oeminfo', parent=self, pos=wx.Point(296, 184),
              size=wx.Size(100, 21), style=0, value='')

        self._e_res2 = wx.TextCtrl(id=wxID_DOS_HEADER_E_RES2, name='_e_res2',
              parent=self, pos=wx.Point(296, 208), size=wx.Size(100, 21),
              style=0, value='')

        self._e_lfanew = wx.TextCtrl(id=wxID_DOS_HEADER_E_LFANEW,
              name='_e_lfanew', parent=self, pos=wx.Point(296, 232),
              size=wx.Size(100, 21), style=0, value='')

        self.ok = wx.Button(id=wxID_DOS_HEADEROK, label='OK', name='ok',
              parent=self, pos=wx.Point(432, 24), size=wx.Size(75, 23),
              style=0)

        self.exit = wx.Button(id=wxID_DOS_HEADEREXIT, label='Exit', name='exit',
              parent=self, pos=wx.Point(432, 56), size=wx.Size(75, 23),
              style=0)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.ok.Bind(wx.EVT_BUTTON, self.OnOKButton, id=wxID_DOS_HEADEROK)
        self.exit.Bind(wx.EVT_BUTTON, self.OnExitButton, id=wxID_DOS_HEADEREXIT)
        
    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self._pe = parent.peInstance
        self._fp = parent.get_loaded_file()
        self.parentDlg = parent
        
        self.loadDosHdrInfo()
    
    def OnExitButton(self, event):
        self.parentDlg.Show()
        self.Close()
        
    def OnClose(self, event):
        self.parentDlg.Restore()
        self.Destroy()
    
    def OnOKButton(self, event):
        dos_hd = self._pe.DOS_HEADER

        dos_hd.e_magic      = toInt(self._e_magic.GetValue())
        dos_hd.e_cblp       = toInt(self._e_cblp.GetValue())
        dos_hd.e_cp         = toInt(self._e_cp.GetValue())
        dos_hd.e_crlc       = toInt(self._e_crlc.GetValue())
        dos_hd.e_cparhdr    = toInt(self._e_cparhdr.GetValue())
        dos_hd.e_minalloc   = toInt(self._e_minalloc.GetValue())
        dos_hd.e_maxalloc   = toInt(self._e_maxalloc.GetValue())
        dos_hd.e_ss         = toInt(self._e_ss.GetValue())
        dos_hd.e_sp         = toInt(self._e_sp.GetValue())
        dos_hd.e_csum       = toInt(self._e_csum.GetValue())
        dos_hd.e_ip         = toInt(self._e_ip.GetValue())
        dos_hd.e_cs         = toInt(self._e_cs.GetValue())
        dos_hd.e_lfarlc     = toInt(self._e_lfarlc.GetValue())
        dos_hd.e_ovno       = toInt(self._e_ovno.GetValue())
        dos_hd.e_res        = str(self._e_res.GetValue())
        dos_hd.e_oemid      = toInt(self._e_oemid.GetValue())
        dos_hd.e_oeminfo    = toInt(self._e_oeminfo.GetValue())
        dos_hd.e_res2       = str(self._e_res2.GetValue())
        dos_hd.e_elfanew    = toInt(self._e_lfanew.GetValue())
            
        try:
            self._pe.write(self._fp)
        except IOError, e:
            raise str(e)
        
    def loadDosHdrInfo(self):
        dos_header = pedata.getDosHeader(self._pe)
        
        self._e_magic.SetValue(hex_up(dos_header.e_magic, 4))
        self._e_cblp.SetValue(hex_up(dos_header.e_cblp, 1))
        self._e_cp.SetValue(hex_up(dos_header.e_cp, 1))
        self._e_crlc.SetValue(hex_up(dos_header.e_crlc, 1))
        self._e_cparhdr.SetValue(hex_up(dos_header.e_cparhdr, 1))
        self._e_minalloc.SetValue(hex_up(dos_header.e_minalloc, 1))
        self._e_maxalloc.SetValue(hex_up(dos_header.e_maxalloc, 4))
        self._e_ss.SetValue(hex_up(dos_header.e_ss, 1))
        self._e_sp.SetValue(hex_up(dos_header.e_sp, 1))
        self._e_csum.SetValue(hex_up(dos_header.e_csum, 1))
        self._e_ip.SetValue(hex_up(dos_header.e_ip, 1))
        self._e_cs.SetValue(hex_up(dos_header.e_cs, 1))
        self._e_lfarlc.SetValue(hex_up(dos_header.e_lfarlc, 1))
        self._e_ovno.SetValue(hex_up(dos_header.e_ovno, 1))
        self._e_res.SetValue(str(dos_header.e_res))
        self._e_oemid.SetValue(hex_up(dos_header.e_oemid, 1))
        self._e_oeminfo.SetValue(hex_up(dos_header.e_oeminfo, 1))
        self._e_res2.SetValue(str(dos_header.e_res2))
        self._e_lfanew.SetValue(hex_up(dos_header.e_lfanew, 1))
        