#Boa:Frame:bound_import
#
#   Description:
#       Bound Imports Viewer
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

__revision__ = "$Id: bound_imports.py 279 2009-10-25 23:53:06Z reversing $"

import wx
import time

from app.common import hex_up

def create(parent):
    return bound_import(parent)

[wxID_BOUND_IMPORT, wxID_BOUND_IMPORT_BOUND_IMPORTS, 
] = [wx.NewId() for _init_ctrls in range(2)]

class bound_import(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_BOUND_IMPORT, name='bound_import',
              parent=prnt, pos=wx.Point(491, 245), size=wx.Size(453, 304),
              style=wx.DEFAULT_FRAME_STYLE, title='Bound Import')
        self.SetClientSize(wx.Size(437, 268))

        self.Centre()
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self._bound_imports = wx.TreeCtrl(id=wxID_BOUND_IMPORT_BOUND_IMPORTS,
              name='_bound_imports', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(437, 268), style=wx.TR_HAS_BUTTONS)
        
    def __init__(self, parent):
        self.__pe = parent.Parent.peInstance
        self.__parentDirectory = parent
        self._init_ctrls(parent)
        
        self.populateTree(self._bound_imports)
        
    def OnClose(self, event):
        self.__parentDirectory.Show()
        self.Destroy()
    
    def populateTree(self, parent):
        root = parent.AddRoot("Bound Imports")
        parent.SetPyData(root, None)
        
        for entry in self.__pe.DIRECTORY_ENTRY_BOUND_IMPORT:
            child = parent.AppendItem(root, entry.name)
            parent.SetPyData(child, None)
            
            timeDateStampItem = parent.AppendItem(child, "TimeDateStamp: %sh [%s UTC]" % (hex_up(entry.struct.TimeDateStamp), time.asctime(time.gmtime(entry.struct.TimeDateStamp))))
            parent.SetPyData(timeDateStampItem, None)
            
            offsetModuleNameItem = parent.AppendItem(child, "OffsetModuleName: %sh" % hex_up(entry.struct.OffsetModuleName, 4))
            parent.SetPyData(offsetModuleNameItem, None)
            
            fowarderRefsItem = parent.AppendItem(child, "NumberOfModuleForwarderRefs: %sh / %s" % (hex_up(entry.struct.NumberOfModuleForwarderRefs, 4), entry.struct.NumberOfModuleForwarderRefs))
            parent.SetPyData(fowarderRefsItem, None)
            
        parent.Expand(root)
        