#Boa:Frame:extra_info
#
#   Description:
#       Extra info window
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

__revision__ = "$Id: extra_info.py 199 2009-08-30 23:43:20Z reversing $"

import wx
import os

from app import compute_hash
from app import signaturesdb

def create(parent):
    return extra_info(parent)

[wxID_EXTRA_INFO, wxID_EXTRA_INFOEXTRA_INFO, 
] = [wx.NewId() for _init_ctrls in range(2)]

class extra_info(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_EXTRA_INFO, name='extra_info',
              parent=prnt, pos=wx.Point(466, 295), size=wx.Size(479, 317),
              style=wx.DEFAULT_FRAME_STYLE, title='Extra Information')
        self.SetClientSize(wx.Size(463, 281))

        self.extra_info = wx.ListBox(choices=[], id=wxID_EXTRA_INFOEXTRA_INFO,
              name='extra_info', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(463, 281), style=0)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __init__(self, parent):
        self._init_ctrls(parent)

        self.parentDlg = parent
        self.lFile = parent.get_loaded_file()
        self._pe = parent.peInstance
        
        self.LoadExtraInfo()
        
    def OnClose(self,event):
        self.parentDlg.Restore()
        self.Destroy()
    
    def LoadExtraInfo(self):
        self.extra_info.Append("Loading file information...please wait")
        self.extra_info.Append("Filename: %s" % os.path.basename(self.lFile))
        self.extra_info.Append("File Size: %d bytes" % os.stat(self.lFile )[6])
        
        if self.parentDlg.isx86:
            self.extra_info.Append("Microsoft Portable Executable (x86)")
        else:
            if self.parentDlg.isIA64:
                self.extra_info.Append("Microsoft Portable Executable (x64)")
        
        try:
            fd = open(self.lFile , "rb")
            fz = os.stat(self.lFile )[6]
            
            self.extra_info.Append("Compiler/Packer:", str(signaturesdb.getSignature(self._pe)))
            
            # here, we calculate the file MD5, SHA-1, and CRC-32 hashes
            self.extra_info.Append("CRC-32: %s" % hex(abs(compute_hash.computeCRC32Hash(fd, fz))).replace("0x", "").upper())
            self.extra_info.Append("MD5: %s" % compute_hash.computeMd5Hash(fd).upper())
            self.extra_info.Append("SHA-1: %s" % compute_hash.computeSha512Hash(fd).upper())
            fd.close()
        except IOError:
            wx.MessageBox("Error: Unable to open the file %s in read mode" % self.lFile)
