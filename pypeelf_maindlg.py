#
#   Description:
#       PyPEELF Main Window
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

__revision__ = "$Id: pypeelf_maindlg.py 299 2010-02-26 22:47:30Z reversing $"

import wx
import os

import tasks
import about
import pefile
import pypeelf_pe
import pypeelf_elf
import config

from app import bae
from app import config_parser
from external import elf32

def create(parent):
    return PyPEELFMainDlg(parent)

[wxID_MAINPYPEELFDLG] = [wx.NewId() for _init_ctrls in range(1)]

[wxID_EXITMENU_ITEM, wxID_FILEMENU_ITEM, wxID_HELPMENU_ITEM, wxID_ABOUTMENU_ITEM,
 wxID_TOOLMENU_TASK_ITEM, wxID_OPTIONSMENU_ITEM, wxID_TOOLMENU_BREAK_ITEM
] = [wx.NewId() for _init_coll_FILE_Items in range(7)]


class FileDropTarget(wx.FileDropTarget):
    """This object implements Drop Target functionality for files"""
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Frame reference"""
        # Initialize the wsFileDropTarget Object
        wx.FileDropTarget.__init__(self)
        # Store the Object Reference for dropped files
        self.frame = obj

    def OnDropFiles(self, x, y, filenames):
        """ Implement File Drop """
        if filenames:
            self.frame.open_file(filenames[0])


class PyPEELFMainDlg(wx.Frame):
    
    def _init_menuBar_items(self, parent):
        FileMenu = wx.Menu()
        FileMenu.Append(wxID_FILEMENU_ITEM,'&Open...', "Open a file...")
        FileMenu.Append(wxID_EXITMENU_ITEM, '&Exit', "Exit from PyPEELF")
        parent.Append(FileMenu, "File")

        ToolsMenu = wx.Menu()
        ToolsMenu.Append(wxID_TOOLMENU_TASK_ITEM, "&Task List", "Task List Viewer")
        ToolsMenu.Append(wxID_TOOLMENU_BREAK_ITEM, "&Break & Enter", "Break and Enter")
        parent.Append(ToolsMenu, "Tools")
        
        OptionsMenu = wx.Menu()
        OptionsMenu.Append(wxID_OPTIONSMENU_ITEM, "&Task List Options ...", "Task List Options")
        parent.Append(OptionsMenu, "Options")
        
        HelpMenu = wx.Menu()
        HelpMenu.Append(wxID_HELPMENU_ITEM, "&Help", "Help")
        HelpMenu.Append(wxID_ABOUTMENU_ITEM, "&About", "About PyPEELF v1.0")
        parent.Append(HelpMenu, "Help")
        
        self.Bind(wx.EVT_MENU, self.OnTaskMenuItem, id=wxID_TOOLMENU_TASK_ITEM)
        self.Bind(wx.EVT_MENU, self.OnOpenMenuItem, id=wxID_FILEMENU_ITEM)
        self.Bind(wx.EVT_MENU, self.OnExitMenuItem, id=wxID_EXITMENU_ITEM)
        self.Bind(wx.EVT_MENU, self.OnHelpMenuItem, id=wxID_HELPMENU_ITEM)
        self.Bind(wx.EVT_MENU, self.OnAboutMenuItem, id=wxID_ABOUTMENU_ITEM)
        self.Bind(wx.EVT_MENU, self.OnOptionsMenuItem, id=wxID_OPTIONSMENU_ITEM)
        self.Bind(wx.EVT_MENU, self.OnBreakAndEnterMenuItem, id=wxID_TOOLMENU_BREAK_ITEM)
        
    def _init_utils(self):
        self.menuBar = wx.MenuBar()

        self._init_menuBar_items(self.menuBar)

    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_MAINPYPEELFDLG, name='', parent=prnt,
              pos=wx.Point(532, 305), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER, title='[PyPEELF v1.0] - Open Source Multi-Platform and Multi-Format Binary Editor')
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self._loadFoxImage()
        
        self.CenterOnScreen()
        self.SetClientSize(wx.Size(488, 488))

        self.CreateStatusBar()
        
        self._init_utils()

    def __init__(self, parent):
        self._isPE = False
        self._PE32 = False
        self._PE64 = False
        self._ELF32 = False
        self._ELF64 = False
        self.peInstance = None
        self.Errors = list()

        self._init_ctrls(parent)
        self.SetMenuBar(self.menuBar)

        # Create a File Drop Target object
        fdt = FileDropTarget(self)
        # Link the Drop Target Object to the Text Control
        self.SetDropTarget(fdt)


    def opj(self, path):
        ## from wxPython Docs and Demos:
        ## http://downloads.sourceforge.net/wxpython/wxPython-demo-2.8.10.1.tar.bz2
        """Convert paths to the platform-specific separator"""
        st = apply(os.path.join, tuple(path.split('/')))
        # HACK: on Linux, a leading / gets lost...
        if path.startswith('/'):
            st = '/' + st
        return st

    def _loadFoxImage(self):
        #imagePath = path = os.path.join(os.path.dirname(__file__), "PyPeElf.png")
        pngImage = wx.Image(self.opj("gfx/pypeelf_logo_little.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        panel = wx.Panel(self, -1)
        
        wx.StaticBitmap(panel, -1, pngImage, (10, 10), (pngImage.GetWidth(), pngImage.GetHeight()))
        return panel
    
    def OnBreakAndEnterMenuItem(self, event):
        bae.BreakAtEP()
        
    def OnOptionsMenuItem(self, event):
        optDlg = config.create(self)
        optDlg.Show()
        self.Hide()
        
    def OnClose(self, event):
        self.Destroy()

    def OnTaskMenuItem(self, event):
        taskDlg = tasks.create(self)
        taskDlg.Show()

    def OnOpenMenuItem(self, event):
        filters = 'Executable Files (*.exe)|*.exe|Dinamyc Libraries (*dll)|*.dll|Out Files(*out)|*.out|So Files(*so)|*.so|All files (*.*)|*.*'

        dialog = wx.FileDialog ( None, message = 'Select file....', wildcard = filters, style = wx.OPEN | wx.MULTIPLE )

        if dialog.ShowModal() == wx.ID_OK:
            file_path = str(dialog.GetPaths()[0])
            self.open_file(file_path)

    def open_file(self, filename):
        if self.isPE(filename):
            pedlg = pypeelf_pe.create(self)
            pedlg._load_file(filename)
            pedlg.Show()
        elif self.isELF(filename):
            elfdlg = pypeelf_elf.create(self)
            elfdlg.Show()
        else:
            wx.MessageBox("Invalid format of file!", "File Format Error", wx.ICON_ERROR)
            return
        self.Hide()

    def isELF(self, f):
        elf = elf32.elf32_file.parse_stream(open(f, "rb"))
        if elf.identifier.magic == "\x7fELF":
            return True
        return False
    
    def isPE(self, f):
        try:
            self.peInstance = pefile.PE(f, fast_load = True)
            self._isPE = True
            
            if self.peInstance.PE_TYPE == 0x10b:
                self._PE32 = True
            elif self.peInstance.PE_TYPE == 0x20b:
                self._PE64 = True
            else:
                self.Errors.append((0xC001, "Invalid PE_TYPE"))
                return
        except pefile.PEFormatError, e:
            self.Errors.append((0xC002, e.value))
            #wx.MessageBox(e.value, "Pe Format Error", wx.ICON_ERROR)
        return self._isPE
    
    def isPE32(self):
        return self._PE32
    
    def isPE64(self):
        return self._PE64
    
    def isELF32(self):
        return self._ELF32
    
    def isELF64(self):
        return self._ELF64
        
    def OnExitMenuItem(self, event):
        self.OnClose(event)
        
    def OnHelpMenuItem(self, event):
        event.Skip()
    
    def OnAboutMenuItem(self, event):
        about.About(self)