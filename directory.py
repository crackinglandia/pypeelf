#Boa:Frame:dirtableviewer
#
#   Description:
#       Directory Table Viewer
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

__revision__ = "$Id: directory.py 279 2009-10-25 23:53:06Z reversing $"

import wx
import sys
import os
import com
import imports
import exports
import debug
import bound_imports
import tls
import relocations

from pefile import DIRECTORY_ENTRY

from app import pedata
from app.common import hex_up

def create(parent):
    return dirtableviewer(parent)

[wxID_DIRTABLEVIEWER, wxID_DIRTABLEVIEWERAPLYCHANGES, 
 wxID_DIRTABLEVIEWERBASERELOC, wxID_DIRTABLEVIEWERBOUNDIMPORT, 
 wxID_DIRTABLEVIEWERCOM, wxID_DIRTABLEVIEWERCOPYRIGHT, wxID_DIRTABLEVIEWERDBG, 
 wxID_DIRTABLEVIEWERDEBUG, wxID_DIRTABLEVIEWEREXCEPTION, 
 wxID_DIRTABLEVIEWEREXIT, wxID_DIRTABLEVIEWEREXPORTS, 
 wxID_DIRTABLEVIEWEREXPORTTABLE, wxID_DIRTABLEVIEWERGLOBALPTR, 
 wxID_DIRTABLEVIEWERIMPORTADDRESSTABLE, wxID_DIRTABLEVIEWERIMPORTS, 
 wxID_DIRTABLEVIEWERIMPORTTABLE, wxID_DIRTABLEVIEWERLOADCONFIG, 
 wxID_DIRTABLEVIEWEROPTIONS, wxID_DIRTABLEVIEWERRESOURCE, 
 wxID_DIRTABLEVIEWERRSC, wxID_DIRTABLEVIEWERRVA, 
 wxID_DIRTABLEVIEWERRVA_AND_SIZE, wxID_DIRTABLEVIEWERSECURITY, 
 wxID_DIRTABLEVIEWERSIZE, wxID_DIRTABLEVIEWERTLS, wxID_DIRTABLEVIEWERTLSTABLE, 
 wxID_DIRTABLEVIEWERVIEW, wxID_DIRTABLEVIEWER_BASERELOC_RVA, 
 wxID_DIRTABLEVIEWER_BASERELOC_SIZE, wxID_DIRTABLEVIEWER_BOUNDIMPORT_RVA, 
 wxID_DIRTABLEVIEWER_BOUNDIMPORT_SIZE, wxID_DIRTABLEVIEWER_BOUND_IMPORTS, 
 wxID_DIRTABLEVIEWER_COM, wxID_DIRTABLEVIEWER_COM_RVA, 
 wxID_DIRTABLEVIEWER_COM_SIZE, wxID_DIRTABLEVIEWER_COPYRIGHT, 
 wxID_DIRTABLEVIEWER_COPYRIGHT_RVA, wxID_DIRTABLEVIEWER_COPYRIGHT_SIZE, 
 wxID_DIRTABLEVIEWER_DEBUG_RVA, wxID_DIRTABLEVIEWER_DEBUG_SIZE, 
 wxID_DIRTABLEVIEWER_EXCEPTION_RVA, wxID_DIRTABLEVIEWER_EXCEPTION_SIZE, 
 wxID_DIRTABLEVIEWER_EXPORTTABLE_RVA, wxID_DIRTABLEVIEWER_EXPORTTABLE_SIZE, 
 wxID_DIRTABLEVIEWER_GLOBALPTR_RVA, wxID_DIRTABLEVIEWER_GLOBALPTR_SIZE, 
 wxID_DIRTABLEVIEWER_IAT_RVA, wxID_DIRTABLEVIEWER_IAT_SIZE, 
 wxID_DIRTABLEVIEWER_IMPORTTABLE_RVA, wxID_DIRTABLEVIEWER_IMPORTTABLE_SIZE, 
 wxID_DIRTABLEVIEWER_LOADCONFIG_RVA, wxID_DIRTABLEVIEWER_LOADCONFIG_SIZE, 
 wxID_DIRTABLEVIEWER_RELOCS, wxID_DIRTABLEVIEWER_RESOURCE_RVA, 
 wxID_DIRTABLEVIEWER_RESOURCE_SIZE, wxID_DIRTABLEVIEWER_SECURITY_RVA, 
 wxID_DIRTABLEVIEWER_SECURITY_SIZE, wxID_DIRTABLEVIEWER_TLSTABLE_RVA, 
 wxID_DIRTABLEVIEWER_TLSTABLE_SIZE, 
] = [wx.NewId() for _init_ctrls in range(59)]

class dirtableviewer(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_DIRTABLEVIEWER, name='dirtableviewer',
              parent=prnt, pos=wx.Point(451, 273), size=wx.Size(497, 459),
              style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER, title='Directory Table Viewer')
        
        self.Centre()
        
        self.SetClientSize(wx.Size(481, 423))
        
        self._exporttable_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_EXPORTTABLE_RVA,
              name='_exporttable_rva', parent=self, pos=wx.Point(128, 64),
              size=wx.Size(88, 21), style=0, value='')

        self._importtable_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_IMPORTTABLE_RVA,
              name='_importtable_rva', parent=self, pos=wx.Point(128, 88),
              size=wx.Size(88, 21), style=0, value='')

        self.aplychanges = wx.Button(id=wxID_DIRTABLEVIEWERAPLYCHANGES,
              label='Apply Changes', name='aplychanges', parent=self,
              pos=wx.Point(376, 32), size=wx.Size(83, 23), style=0)

        self.rva_and_size = wx.StaticBox(id=wxID_DIRTABLEVIEWERRVA_AND_SIZE,
              label='', name='rva_and_size', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(344, 408), style=0)

        self.options = wx.StaticBox(id=wxID_DIRTABLEVIEWEROPTIONS,
              label='Options', name='options', parent=self, pos=wx.Point(360,
              8), size=wx.Size(112, 88), style=0)

        self.view = wx.StaticBox(id=wxID_DIRTABLEVIEWERVIEW, label='View',
              name='view', parent=self, pos=wx.Point(360, 96), size=wx.Size(112,
              320), style=0)

        self.exit = wx.Button(id=wxID_DIRTABLEVIEWEREXIT, label='Exit',
              name='exit', parent=self, pos=wx.Point(376, 64), size=wx.Size(83,
              23), style=0)

        self._resource_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_RESOURCE_RVA,
              name='_resource_rva', parent=self, pos=wx.Point(128, 112),
              size=wx.Size(88, 21), style=0, value='')

        self._exception_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_EXCEPTION_RVA,
              name='_exception_rva', parent=self, pos=wx.Point(128, 136),
              size=wx.Size(88, 21), style=0, value='')

        self._security_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_SECURITY_RVA,
              name='_security_rva', parent=self, pos=wx.Point(128, 160),
              size=wx.Size(88, 21), style=0, value='')

        self._basereloc_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_BASERELOC_RVA,
              name='_basereloc_rva', parent=self, pos=wx.Point(128, 184),
              size=wx.Size(88, 21), style=0, value='')

        self._debug_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_DEBUG_RVA,
              name='_debug_rva', parent=self, pos=wx.Point(128, 208),
              size=wx.Size(88, 21), style=0, value='')

        self._copyright_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_COPYRIGHT_RVA,
              name='_copyright_rva', parent=self, pos=wx.Point(128, 232),
              size=wx.Size(88, 21), style=0, value='')

        self._globalptr_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_GLOBALPTR_RVA,
              name='_globalptr_rva', parent=self, pos=wx.Point(128, 256),
              size=wx.Size(88, 21), style=0, value='')

        self._tlstable_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_TLSTABLE_RVA,
              name='_tlstable_rva', parent=self, pos=wx.Point(128, 280),
              size=wx.Size(88, 21), style=0, value='')

        self._loadconfig_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_LOADCONFIG_RVA,
              name='_loadconfig_rva', parent=self, pos=wx.Point(128, 304),
              size=wx.Size(88, 21), style=0, value='')

        self._boundimport_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_BOUNDIMPORT_RVA,
              name='_boundimport_rva', parent=self, pos=wx.Point(128, 328),
              size=wx.Size(88, 21), style=0, value='')

        self._iat_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_IAT_RVA,
              name='_iat_rva', parent=self, pos=wx.Point(128, 352),
              size=wx.Size(88, 21), style=0, value='')

        self.exports = wx.Button(id=wxID_DIRTABLEVIEWEREXPORTS, label='Exports',
              name='exports', parent=self, pos=wx.Point(376, 120),
              size=wx.Size(83, 23), style=0)

        self.imports = wx.Button(id=wxID_DIRTABLEVIEWERIMPORTS, label='Imports',
              name='imports', parent=self, pos=wx.Point(376, 152),
              size=wx.Size(83, 23), style=0)

        self.rsc = wx.Button(id=wxID_DIRTABLEVIEWERRSC, label='Resource',
              name='rsc', parent=self, pos=wx.Point(376, 184), size=wx.Size(83,
              23), style=0)

        self.dbg = wx.Button(id=wxID_DIRTABLEVIEWERDBG, label='Debug',
              name='dbg', parent=self, pos=wx.Point(376, 216), size=wx.Size(83,
              23), style=0)

        self.tls = wx.Button(id=wxID_DIRTABLEVIEWERTLS, label='TLS', name='tls',
              parent=self, pos=wx.Point(376, 248), size=wx.Size(83, 23),
              style=0)

        self.exporttable = wx.StaticText(id=wxID_DIRTABLEVIEWEREXPORTTABLE,
              label='Export Table', name='exporttable', parent=self,
              pos=wx.Point(16, 64), size=wx.Size(62, 13), style=0)

        self.importtable = wx.StaticText(id=wxID_DIRTABLEVIEWERIMPORTTABLE,
              label='Import Table', name='importtable', parent=self,
              pos=wx.Point(16, 88), size=wx.Size(62, 13), style=0)

        self.resource = wx.StaticText(id=wxID_DIRTABLEVIEWERRESOURCE,
              label='Resource', name='resource', parent=self, pos=wx.Point(16,
              112), size=wx.Size(46, 13), style=0)

        self.exception = wx.StaticText(id=wxID_DIRTABLEVIEWEREXCEPTION,
              label='Exception', name='exception', parent=self, pos=wx.Point(16,
              136), size=wx.Size(48, 13), style=0)

        self.security = wx.StaticText(id=wxID_DIRTABLEVIEWERSECURITY,
              label='Security', name='security', parent=self, pos=wx.Point(16,
              160), size=wx.Size(40, 13), style=0)

        self.basereloc = wx.StaticText(id=wxID_DIRTABLEVIEWERBASERELOC,
              label='Base Reloc', name='basereloc', parent=self,
              pos=wx.Point(16, 184), size=wx.Size(53, 13), style=0)

        self.debug = wx.StaticText(id=wxID_DIRTABLEVIEWERDEBUG, label='Debug',
              name='debug', parent=self, pos=wx.Point(16, 208), size=wx.Size(32,
              13), style=0)

        self.copyright = wx.StaticText(id=wxID_DIRTABLEVIEWERCOPYRIGHT,
              label='Copyright', name='copyright', parent=self, pos=wx.Point(16,
              232), size=wx.Size(48, 13), style=0)

        self.globalptr = wx.StaticText(id=wxID_DIRTABLEVIEWERGLOBALPTR,
              label='Globalptr', name='globalptr', parent=self, pos=wx.Point(16,
              256), size=wx.Size(44, 13), style=0)

        self.tlstable = wx.StaticText(id=wxID_DIRTABLEVIEWERTLSTABLE,
              label='TlsTable', name='tlstable', parent=self, pos=wx.Point(16,
              280), size=wx.Size(40, 13), style=0)

        self.loadconfig = wx.StaticText(id=wxID_DIRTABLEVIEWERLOADCONFIG,
              label='Load Config', name='loadconfig', parent=self,
              pos=wx.Point(16, 304), size=wx.Size(58, 13), style=0)

        self.boundimport = wx.StaticText(id=wxID_DIRTABLEVIEWERBOUNDIMPORT,
              label='Bound Import', name='boundimport', parent=self,
              pos=wx.Point(16, 328), size=wx.Size(66, 13), style=0)

        self.importaddresstable = wx.StaticText(id=wxID_DIRTABLEVIEWERIMPORTADDRESSTABLE,
              label='Import Address Table', name='importaddresstable',
              parent=self, pos=wx.Point(16, 352), size=wx.Size(104, 13),
              style=0)

        self.rva = wx.StaticText(id=wxID_DIRTABLEVIEWERRVA, label='RVA',
              name='rva', parent=self, pos=wx.Point(160, 40), size=wx.Size(21,
              13), style=0)

        self.size = wx.StaticText(id=wxID_DIRTABLEVIEWERSIZE, label='Size',
              name='size', parent=self, pos=wx.Point(272, 40), size=wx.Size(20,
              13), style=0)

        self._exporttable_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_EXPORTTABLE_SIZE,
              name='_exporttable_size', parent=self, pos=wx.Point(232, 64),
              size=wx.Size(100, 21), style=0, value='')

        self._importtable_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_IMPORTTABLE_SIZE,
              name='_importtable_size', parent=self, pos=wx.Point(232, 88),
              size=wx.Size(100, 21), style=0, value='')

        self._resource_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_RESOURCE_SIZE,
              name='_resource_size', parent=self, pos=wx.Point(232, 112),
              size=wx.Size(100, 21), style=0, value='')

        self._exception_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_EXCEPTION_SIZE,
              name='_exception_size', parent=self, pos=wx.Point(232, 136),
              size=wx.Size(100, 21), style=0, value='')

        self._security_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_SECURITY_SIZE,
              name='_security_size', parent=self, pos=wx.Point(232, 160),
              size=wx.Size(100, 21), style=0, value='')

        self._basereloc_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_BASERELOC_SIZE,
              name='_basereloc_size', parent=self, pos=wx.Point(232, 184),
              size=wx.Size(100, 21), style=0, value='')

        self._debug_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_DEBUG_SIZE,
              name='_debug_size', parent=self, pos=wx.Point(232, 208),
              size=wx.Size(100, 21), style=0, value='')

        self._copyright_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_COPYRIGHT_SIZE,
              name='_copyright_size', parent=self, pos=wx.Point(232, 232),
              size=wx.Size(100, 21), style=0, value='')

        self._globalptr_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_GLOBALPTR_SIZE,
              name='_globalptr_size', parent=self, pos=wx.Point(232, 256),
              size=wx.Size(100, 21), style=0, value='')

        self._tlstable_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_TLSTABLE_SIZE,
              name='_tlstable_size', parent=self, pos=wx.Point(232, 280),
              size=wx.Size(100, 21), style=0, value='')

        self._loadconfig_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_LOADCONFIG_SIZE,
              name='_loadconfig_size', parent=self, pos=wx.Point(232, 304),
              size=wx.Size(100, 21), style=0, value='')

        self._boundimport_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_BOUNDIMPORT_SIZE,
              name='_boundimport_size', parent=self, pos=wx.Point(232, 328),
              size=wx.Size(100, 21), style=0, value='')

        self._iat_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_IAT_SIZE,
              name='_iat_size', parent=self, pos=wx.Point(232, 352),
              size=wx.Size(100, 21), style=0, value='')

        self._bound_imports = wx.Button(id=wxID_DIRTABLEVIEWER_BOUND_IMPORTS,
              label='Bound Imports', name='_bound_imports', parent=self,
              pos=wx.Point(376, 280), size=wx.Size(83, 23), style=0)

        self._relocs = wx.Button(id=wxID_DIRTABLEVIEWER_RELOCS,
              label='Relocations', name='_relocs', parent=self,
              pos=wx.Point(376, 312), size=wx.Size(83, 23), style=0)
        
        self._copyright = wx.Button(id=wxID_DIRTABLEVIEWER_COPYRIGHT,
              label='Copyright', name='_copyright', parent=self,
              pos=wx.Point(376, 344), size=wx.Size(83, 23), style=0)

        self._com = wx.Button(id=wxID_DIRTABLEVIEWER_COM, label='COM',
              name='_com', parent=self, pos=wx.Point(376, 376), size=wx.Size(83,
              23), style=0)

        self.com = wx.StaticText(id=wxID_DIRTABLEVIEWERCOM, label='COM',
              name='com', parent=self, pos=wx.Point(16, 376), size=wx.Size(24,
              13), style=0)

        self._com_rva = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_COM_RVA,
              name='_com_rva', parent=self, pos=wx.Point(128, 376),
              size=wx.Size(88, 21), style=0, value='')

        self._com_size = wx.TextCtrl(id=wxID_DIRTABLEVIEWER_COM_SIZE,
              name='_com_size', parent=self, pos=wx.Point(232, 376),
              size=wx.Size(100, 21), style=0, value='')
        
        self.Bind(wx.EVT_BUTTON, self.OnRelocsButton, id=wxID_DIRTABLEVIEWER_RELOCS)
        self.Bind(wx.EVT_BUTTON, self.OnComButton, id=wxID_DIRTABLEVIEWER_COM)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_BUTTON, self.OnDebugButton, id=wxID_DIRTABLEVIEWERDBG)
        self.Bind(wx.EVT_BUTTON, self.OnBoundImportsButton, id=wxID_DIRTABLEVIEWER_BOUND_IMPORTS)
        self.Bind(wx.EVT_BUTTON, self.OnTLSButton, id=wxID_DIRTABLEVIEWERTLS)
        
        self.imports.Bind(wx.EVT_BUTTON, self.OnImportsButton, id=wxID_DIRTABLEVIEWERIMPORTS)
        self.exit.Bind(wx.EVT_BUTTON, self.OnExitButton,id=wxID_DIRTABLEVIEWEREXIT)
        self.aplychanges.Bind(wx.EVT_BUTTON, self.OnApplyChangesButton, id=wxID_DIRTABLEVIEWERAPLYCHANGES)
        self.exports.Bind(wx.EVT_BUTTON, self.OnExportsButton, id=wxID_DIRTABLEVIEWEREXPORTS)
        
    def __init__(self, parent):
        self.__pe = parent.peInstance
        self._fp = parent.get_loaded_file()
        
        self.parentWindow = parent
        self._init_ctrls(parent)
        self.loadDirectoryData()
    
    def OnComButton(self, event):
        if self.__pe.OPTIONAL_HEADER.DATA_DIRECTORY[14].VirtualAddress:
            comDlg = com.create(self)
            comDlg.Show()
            self.Hide()
        else:
            wx.MessageBox("Com Directory was not found!", "Error", wx.ICON_ERROR)
        
    def OnExitButton(self, event):
        self.Close()
        self.parentWindow.Show()

    def OnRelocsButton(self, event):
        dir = DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]
        self.__pe.parse_data_directories(directories = [dir])
        
        if hasattr(self.__pe, "DIRECTORY_ENTRY_BASERELOC"):
            relocsDialog = relocations.create(self)
            relocsDialog.Show()
            self.Hide()
        else:
            wx.MessageBox("Relocations Directory Was Not Found!", "Error", wx.ICON_ERROR)
            
    def OnImportsButton(self, event):
        dir = DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]
        self.__pe.parse_data_directories(directories = [dir])
        
        if hasattr(self.__pe, "DIRECTORY_ENTRY_IMPORT"):
            importsDialog = imports.create(self)
            importsDialog.Show()
            self.Hide()
        else:
            wx.MessageBox("Import Directory Table Was Not Found!", "Error", wx.ICON_ERROR)
            
    def OnBoundImportsButton(self, event):
        dir = DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT"]
        self.__pe.parse_data_directories(directories = [dir])
        
        if hasattr(self.__pe, "DIRECTORY_ENTRY_BOUND_IMPORT"):
            boundDialog = bound_imports.create(self)
            boundDialog.Show()
            self.Hide()
        else:
            wx.MessageBox("Bound Import Entry Was Not Found!", "Error", wx.ICON_ERROR)
            
    def OnDebugButton(self, event):
        dir = DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_DEBUG"]
        self.__pe.parse_data_directories(directories = [dir])
        
        if hasattr(self.__pe, "DIRECTORY_ENTRY_DEBUG"):
            debugDialog = debug.create(self)
            debugDialog.Show()
            self.Hide()
        else:
            wx.MessageBox("Debug Entry Was Not Found!", "Error", wx.ICON_ERROR)
    
    def OnTLSButton(self, event):
        dir = DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_TLS"]
        self.__pe.parse_data_directories(directories = [dir])
        
        if hasattr(self.__pe, "DIRECTORY_ENTRY_TLS"):
            tlsDialog = tls.create(self)
            tlsDialog.Show()
            self.Hide()
        else:
            wx.MessageBox("TLS Directory Was Not Found!", "Error", wx.ICON_ERROR)
            
    def OnExportsButton(self, event):
        dir = DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]
        self.__pe.parse_data_directories(directories = [dir])
        
        if hasattr(self.__pe, "DIRECTORY_ENTRY_EXPORT"):
            exportsDialog = exports.create(self)
            exportsDialog.Show()
            self.Hide()
        else:
            wx.MessageBox("Directory Entry Export Was Not Found!", "Error", wx.ICON_ERROR)
        
    def OnApplyChangesButton(self, event):
        dirTable = pedata.getDataDirectory(self.__pe)

        dirTable[0].VirtualAddress = int(self._exporttable_rva.GetValue(), 16)
        dirTable[0].Size = int(self._exporttable_size.GetValue(), 16)
        
        dirTable[1].VirtualAddress = int(self._importtable_rva.GetValue(), 16)
        dirTable[1].Size = int(self._importtable_size.GetValue(), 16)
        
        dirTable[2].VirtualAddress = int(self._resource_rva.GetValue(), 16)
        dirTable[2].Size = int(self._resource_size.GetValue(), 16)
        
        dirTable[3].VirtualAddress = int(self._exception_rva.GetValue(), 16)
        dirTable[3].Size = int(self._exception_size.GetValue(), 16)
        
        dirTable[4].VirtualAddress = int(self._security_rva.GetValue(), 16)
        dirTable[4].Size = int(self._security_size.GetValue(), 16)

        dirTable[5].VirtualAddress = int(self._basereloc_rva.GetValue(), 16)
        dirTable[5].Size = int(self._basereloc_size.GetValue(), 16)

        dirTable[6].VirtualAddress = int(self._debug_rva.GetValue(), 16)
        dirTable[6].Size = int(self._debug_size.GetValue(), 16)

        dirTable[7].VirtualAddress = int(self._copyright_rva.GetValue(), 16)
        dirTable[7].Size = int(self._copyright_size.GetValue(), 16)

        dirTable[8].VirtualAddress = int(self._globalptr_rva.GetValue(), 16)
        dirTable[8].Size = int(self._globalptr_size.GetValue(), 16)

        dirTable[9].VirtualAddress = int(self._tlstable_rva.GetValue(), 16)
        dirTable[9].Size = int(self._tlstable_size.GetValue(), 16)

        dirTable[10].VirtualAddress = int(self._loadconfig_rva.GetValue(), 16)
        dirTable[10].Size = int(self._loadconfig_size.GetValue(), 16)

        dirTable[11].VirtualAddress = int(self._boundimport_rva.GetValue(), 16)
        dirTable[11].Size = int(self._boundimport_size.GetValue(), 16)

        dirTable[12].VirtualAddress = int(self._iat_rva.GetValue(), 16)
        dirTable[12].Size = int(self._iat_size.GetValue(), 16)

        dirTable[14].VirtualAddress = int(self._com_rva.GetValue(), 16)
        dirTable[14].Size = int(self._com_size.GetValue(), 16)
        
        try:
            self.__pe.write(self._fp)
        except IOError, e:
            raise str(e)
        
    def OnClose(self, event):
        self.parentWindow.Show()
        self.Destroy()

    def loadDirectoryData(self):
        dirData = pedata.getDataDirectory(self.__pe)
        
        self._exporttable_rva.SetValue(hex_up(dirData[0].VirtualAddress))
        self._exporttable_size.SetValue(hex_up(dirData[0].Size))
        
        self._importtable_rva.SetValue(hex_up(dirData[1].VirtualAddress))
        self._importtable_size.SetValue(hex_up(dirData[1].Size))
        
        self._resource_rva.SetValue(hex_up(dirData[2].VirtualAddress))
        self._resource_size.SetValue(hex_up(dirData[2].Size))
        
        self._exception_rva.SetValue(hex_up(dirData[3].VirtualAddress))
        self._exception_size.SetValue(hex_up(dirData[3].Size))
        
        self._security_rva.SetValue(hex_up(dirData[4].VirtualAddress))
        self._security_size.SetValue(hex_up(dirData[4].Size))
        
        self._basereloc_rva.SetValue(hex_up(dirData[5].VirtualAddress))
        self._basereloc_size.SetValue(hex_up(dirData[5].Size))
        
        self._debug_rva.SetValue(hex_up(dirData[6].VirtualAddress))
        self._debug_size.SetValue(hex_up(dirData[6].Size))
        
        self._copyright_rva.SetValue(hex_up(dirData[7].VirtualAddress))
        self._copyright_size.SetValue(hex_up(dirData[7].Size))
        
        self._globalptr_rva.SetValue(hex_up(dirData[8].VirtualAddress))
        self._globalptr_size.SetValue(hex_up(dirData[8].Size))
        
        self._tlstable_rva.SetValue(hex_up(dirData[9].VirtualAddress))
        self._tlstable_size.SetValue(hex_up(dirData[9].Size))
        
        self._loadconfig_rva.SetValue(hex_up(dirData[10].VirtualAddress))
        self._loadconfig_size.SetValue(hex_up(dirData[10].Size))
        
        self._boundimport_rva.SetValue(hex_up(dirData[11].VirtualAddress))
        self._boundimport_size.SetValue(hex_up(dirData[11].Size))
        
        self._iat_rva.SetValue(hex_up(dirData[12].VirtualAddress))
        self._iat_size.SetValue(hex_up(dirData[12].Size))
        
        self._com_rva.SetValue(hex_up(dirData[14].VirtualAddress))
        self._com_size.SetValue(hex_up(dirData[14].Size))

