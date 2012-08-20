#Boa:Frame:resource_viewer
#
#   Description:
#       Resource Viewer/Editor
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

__revision__ = "$Id: resources.py 167 2009-08-22 21:49:33Z reversing $"

import wx

def create(parent):
    return resource_viewer(parent)

[wxID_RESOURCE_VIEWER] = [wx.NewId() for _init_ctrls in range(1)]

class resource_viewer(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_RESOURCE_VIEWER, name='resource_viewer',
              parent=prnt, pos=wx.Point(438, 298), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title='Resource Viewer')
        
        self.Centre()
        self.SetClientSize(wx.Size(384, 214))

    def __init__(self, parent):
        self._init_ctrls(parent)
