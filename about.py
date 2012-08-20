#!/usr/bin/env python
#
#   Description:
#       About window
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

__revision__ = "$Id: about.py 164 2009-08-22 18:34:57Z reversing $"

import wx
from wx.lib.wordwrap import wordwrap

def About(class_instance):
    licenseText = (
"Permission is hereby granted, free of charge, to any person obtaining a copy"
"of this software and associated documentation files (the 'Software'), to deal"
"in the Software without restriction, including without limitation the rights"
"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell"
"copies of the Software, and to permit persons to whom the Software is"
"furnished to do so, subject to the following conditions:"
"The above copyright notice and this permission notice shall be included in"
"all copies or substantial portions of the Software."
"THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR"
"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,"
"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE"
"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"
"LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,"
"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN"
"THE SOFTWARE.")

    info = wx.AboutDialogInfo()
    info.Name = "PyPEELF - Multi-Platform Binary Editor"
    info.Version = "1.0"
    info.Copyright = "Copyright (c) 2009 Nahuel Cayetano Riva <nahuelriva@gmail.com>"
    info.Description = wordwrap(
                        "PyPEELF is a multi-platform binary editor. PyPEELF lets you"
                        "view and edit PE32, PE32+ and ELF binary files.",
                        450, wx.ClientDC(class_instance))
    info.Website = ("http://crackinglandia.blogspot.com", "PyPEELF Home Page")
    info.Developers = ["Nahuel Cayetano Riva (nahuelriva@gmail.com)", "Matias Bordese (mbordese@gmail.com)"]
    info.License = wordwrap(licenseText, 650, wx.ClientDC(class_instance))
    info.SetDocWriters(["Jacob Soo (Jacob.soo@gmail.com)"])
    info.SetArtists(["Jacob Soo (Jacob.soo@gmail.com)"])
    
    wx.AboutBox(info)
    
