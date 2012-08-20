#!/usr/bin/env python

#Boa:App:PyPeElf
#
#   Description:
#       PyPEELF application
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

__revision__ = "$Id: PyPeElfMain.py 298 2010-02-26 20:43:24Z reversing $"

import wx

import pypeelf_maindlg

modules ={u'pypeelf_maindlg': [1, 'Main frame of Application', u'pypeelf_maindlg.py']}

class PyPeElfApp(wx.App):
    def OnInit(self):
        self.main = pypeelf_maindlg.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = PyPeElfApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
