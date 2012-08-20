#
#   Description:
#       Main ELF Viewer/Editor Window
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

__revision__ = "$Id: pypeelf_elf.py 300 2010-02-26 23:14:48Z reversing $"

import wx
import sys

import  wx.lib.mixins.listctrl  as  listmix

def create(parent):
    return ELFMainDialog(parent)

[wxID_ELF_EDITOR, wxID_ELF_TREE_STRUCTURE, wxID_ELF_LISTCTRL] = [wx.NewId() for _init_ctrls in range(3)]

listctrldata = {
1 : ("Hey!", "You can edit", "me!"),
2 : ("Try changing the contents", "by", "clicking"),
3 : ("in", "a", "cell"),
4 : ("See how the length columns", "change", "?"),
5 : ("You can use", "TAB,", "cursor down,"),
6 : ("and cursor up", "to", "navigate"),
}

class ELFListCtrlStructure(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin,  listmix.TextEditMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.populate()
        listmix.TextEditMixin.__init__(self)
        
    def populate(self):
        # for normal, simple columns, you can add them like this:
        self.InsertColumn(0, "Column 1")
        self.InsertColumn(1, "Column 2")
        self.InsertColumn(2, "Column 3")
        self.InsertColumn(3, "Len 1", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(4, "Len 2", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(5, "Len 3", wx.LIST_FORMAT_RIGHT)

        items = listctrldata.items()
        for key, data in items:
            index = self.InsertStringItem(sys.maxint, data[0])
            self.SetStringItem(index, 1, data[1])
            self.SetStringItem(index, 2, data[2])
            self.SetItemData(index, key)

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, 100)

        self.currentItem = 0


    def SetStringItem(self, index, col, data):
        if col in range(3):
            wx.ListCtrl.SetStringItem(self, index, col, data)
            wx.ListCtrl.SetStringItem(self, index, 3+col, str(len(data)))
        else:
            try:
                datalen = int(data)
            except:
                return

            wx.ListCtrl.SetStringItem(self, index, col, data)

            data = self.GetItem(index, col-3).GetText()
            wx.ListCtrl.SetStringItem(self, index, col-3, data[0:datalen])
    
class ELFMainDialog(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_ELF_EDITOR, name='elf_dlg',
              parent=prnt, pos=wx.Point(438, 298), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title='[PyPEELF v1.0 - ELF Editor]')
        
        self.Centre()
        self.SetClientSize(wx.Size(384, 214))

        self.com_tree = wx.TreeCtrl(id=wxID_ELF_TREE_STRUCTURE, name='elf_structure',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(300, 384),
              style=wx.TR_HAS_BUTTONS)
        
        self.list = ELFListCtrlStructure(self, wxID_ELF_LISTCTRL,
                         style=wx.LC_REPORT
                         | wx.BORDER_NONE
                         | wx.LC_SORT_ASCENDING
                         )

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.parent = parent
    
    def OnClose(self, event):
        self.parent.Show()
        self.Destroy()
        