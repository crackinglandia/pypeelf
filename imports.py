#Boa:Frame:iat_viewer
#
#   Description:
#       Import Table Viewer
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

__revision__ = "$Id: imports.py 282 2009-11-06 16:56:36Z mbordese $"

import wx
import sys

from app import pedata
from app.common import hex_up
from wx.lib.anchors import LayoutAnchors

def create(parent):
    return iat_viewer(parent)

[wxID_IAT_VIEWER, wxDLL_LIST, wxFUNCTION_LIST, wxID_IMPORT_VIEWERTASKSTATUS 
] = [wx.NewId() for _init_ctrls in range(4)]

[wxID_IMPORTS_EDIT, wxID_IMPORTS_REFRESH, 
] = [wx.NewId() for _init_coll_ImportsContextMenu in range(2)]

[wxID_DLL_EDIT, wxID_DLL_ADD_IMPORT, wxID_DLL_KILL_IID, wxID_DLL_KILL_OFT, wxID_DLL_REFRESH 
] = [wx.NewId() for _init_coll_DllsContextMenu in range(5)]

class iat_viewer(wx.Frame):
    def _init_coll_DllsContextMenu(self, parent):
        parent.Append(help='', id=wxID_DLL_EDIT,
              kind=wx.ITEM_NORMAL, text='Edit')
        parent.Append(help='', id=wxID_DLL_ADD_IMPORT,
              kind=wx.ITEM_NORMAL, text='Add import...')
        parent.Append(help='', id=wxID_DLL_KILL_IID,
              kind=wx.ITEM_NORMAL, text='Kill ImageImportDescriptor')
        parent.Append(help='', id=wxID_DLL_KILL_OFT,
              kind=wx.ITEM_NORMAL, text='Kill OriginalFirstThunk')
        parent.Append(help='', id=wxID_DLL_REFRESH,
              kind=wx.ITEM_NORMAL, text='Refresh...')

        self.Bind(wx.EVT_MENU, self.OnDllEdit, id=wxID_DLL_EDIT)
        self.Bind(wx.EVT_MENU, self.OnDllAddImport, id=wxID_DLL_ADD_IMPORT)
        self.Bind(wx.EVT_MENU, self.OnDllKillIID, id=wxID_DLL_KILL_IID)
        self.Bind(wx.EVT_MENU, self.OnDllKillOFT, id=wxID_DLL_KILL_OFT)
        self.Bind(wx.EVT_MENU, self.OnDllRefresh, id=wxID_DLL_REFRESH)

    def _init_coll_ImportsContextMenu(self, parent):
        parent.Append(help='', id=wxID_IMPORTS_EDIT,
              kind=wx.ITEM_NORMAL, text='Edit')
        parent.Append(help='', id=wxID_IMPORTS_REFRESH,
              kind=wx.ITEM_NORMAL, text='Refresh...')
        
        self.Bind(wx.EVT_MENU, self.OnImportsEdit, id=wxID_IMPORTS_EDIT)
        self.Bind(wx.EVT_MENU, self.OnImportsRefresh, id=wxID_IMPORTS_REFRESH)

    def _init_coll_dllList_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Dll Name', width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='Original First Thunk', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Time Date Stamp', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Fowarder Chain', width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT,
              heading='Name', width=-1)
        parent.InsertColumn(col=5, format=wx.LIST_FORMAT_LEFT,
              heading='First Thunk', width=-1)

    def _init_coll_functionList_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Thunk RVA', width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='Thunk Offset', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Thunk Value', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Hint', width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT, heading='Api Name',
              width=-1)

    def _init_coll_taskStatus_Fields(self, parent):
        parent.SetFieldsCount(6)

        parent.SetStatusText(number=0, text='Number of Dlls:')
        parent.SetStatusText(number=1, text='%d' % self.getNumberOfDlls())
        parent.SetStatusText(number=2, text='Total Number of Functions:')
        parent.SetStatusText(number=3, text='%d' % self.getNumberOfFunctions())
        
        parent.SetStatusWidths([100, 40, 140, 40, 250, 40])
        
    def _init_utils(self):
        self.dllContextMenu = wx.Menu(title='Dlls List Options')
        self._init_coll_DllsContextMenu(self.dllContextMenu)
        
        self.importsContextMenu = wx.Menu(title='Function List Options')
        self._init_coll_ImportsContextMenu(self.importsContextMenu)
        
        
    def _custom_inits(self, parent):
        self.taskListSizer.Add(self.dllList, 2, wx.EXPAND)
        self.taskListSizer.Add(self.functionList, 2, wx.EXPAND)
        
    def _init_sizers(self):
        self.taskListSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.SetSizer(self.taskListSizer)
        
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_IAT_VIEWER, name='iat_viewer',
              parent=prnt, pos=wx.Point(439, 269), size=wx.Size(548, 352),
              style=wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE,
              title='Import Table Viewer')
        
        self.Centre()
        
        self._init_utils()
        
        self.SetClientSize(wx.Size(600, 400))
        self.SetMinSize(wx.Size(500, 250))
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.dllList = wx.ListCtrl(id=wxDLL_LIST,
              name='dllList', parent=self, pos=wx.Point(0, 144),
              size=wx.Size(600, 200),
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        
        self.dllList.SetConstraints(LayoutAnchors(self.dllList, True, True, True, True))
        
        self._init_coll_dllList_Columns(self.dllList)

        self.dllList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OndllListItemSelected, id=wxDLL_LIST)
        
        self.dllList.Bind(wx.EVT_RIGHT_DOWN, self.OnDllListRightDown)
        
        self.taskStatus = wx.StatusBar(id=wxID_IMPORT_VIEWERTASKSTATUS,
              name='taskStatus', parent=self, style=0)
        
        self._init_coll_taskStatus_Fields(self.taskStatus)
        
        self.SetStatusBar(self.taskStatus)

        self.functionList = wx.ListCtrl(id=wxFUNCTION_LIST,
              name='importList', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(600, 200),
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
        
        self._init_coll_functionList_Columns(self.functionList)
        
        self.functionList.Bind(wx.EVT_RIGHT_DOWN, self.OnImportsListRightDown)

        self._init_sizers()

    def __init__(self, parent):
        self.parentDirectory = parent
        
        self.__pe = self.parentDirectory.Parent.peInstance
        
        self._init_ctrls(parent)
        self._custom_inits(parent)
        self.loadDlls(self.__pe)
        
    def OnClose(self, event):
        self.parentDirectory.Show()
        self.Destroy()

    def OnImportsListRightDown(self, event):
        x = event.GetX()
        y = event.GetY()

        item, flags = self.functionList.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.functionList.Select(item)

        position = event.GetPosition() + self.functionList.GetPosition()
        self.PopupMenu(self.importsContextMenu, position)

    def OnDllListRightDown(self, event):
        x = event.GetX()
        y = event.GetY()
        item, flags = self.dllList.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.dllList.Select(item)

        self.PopupMenu(self.dllContextMenu, event.GetPosition())

    def OndllListItemSelected(self, event):
        self.functionList.DeleteAllItems()
        item_id = self.dllList.GetFirstSelected()
        item = self.dllList.GetItem(item_id, 0)
        dll = item.GetText()
        
        import_list = pedata.getImports(pedata.getDllInstance(self.__pe, dll))
        idx = 0
        
        self.taskStatus.SetStatusText(number=4, text='Total Number of Functions in %s:' % dll)
        self.taskStatus.SetStatusText(number=5, text='%d' % len(import_list))
        
        for imprt in import_list:
            
            if imprt.import_by_ordinal:
                api_name = "Ordinal: %dh / %dd " % (imprt.ordinal, imprt.ordinal)
            else:
                api_name = imprt.name
            
            index = self.functionList.InsertStringItem(sys.maxint, str(idx))
            thunk_rva = imprt.thunk_rva
            thunk_offset = imprt.thunk_offset
            thunk_value = self.__pe.get_dword_at_rva(thunk_rva)# imprt.hint_name_table_rva
                
            hint = imprt.hint
            
            self.functionList.SetStringItem(index, 0, hex_up(thunk_rva))
            self.functionList.SetStringItem(index, 1, hex_up(thunk_offset))
            
            if thunk_value != None:
                self.functionList.SetStringItem(index, 2, hex_up(thunk_value))
            else:
                self.functionList.SetStringItem(index, 2, "-")
                
            if hint != None:
                self.functionList.SetStringItem(index, 3, hex_up(hint, 4))
            else:
                self.functionList.SetStringItem(index, 3, "-")
                
            self.functionList.SetStringItem(index, 4, api_name)
            self.functionList.SetItemData(index,idx)
            idx +=1
            
    def loadDlls(self, pe):
        dlls = pedata.getAllDllInstances(pe)
        
        idx = 0
        for dll in dlls:
            dll_name = dll.dll
            
            index = self.dllList.InsertStringItem(sys.maxint, str(idx))
            
            dllStruct = pedata.getDllStructInstance(dll)
            
            oft = dllStruct.OriginalFirstThunk
            tds = dllStruct.TimeDateStamp
            fc = dllStruct.ForwarderChain
            name = dllStruct.Name
            ft = dllStruct.FirstThunk
            
            self.dllList.SetStringItem(index, 0, dll_name)
            self.dllList.SetStringItem(index, 1, hex_up(oft))
            self.dllList.SetStringItem(index, 2, hex_up(tds))
            self.dllList.SetStringItem(index, 3, hex_up(fc))
            self.dllList.SetStringItem(index, 4, hex_up(name))
            self.dllList.SetStringItem(index, 5, hex_up(ft))
            self.dllList.SetItemData(index, idx)
            idx += 1
            
    def getNumberOfDlls(self):
        return len(pedata.getAllDllInstances(self.__pe))
    
    def getNumberOfFunctions(self):
        j = 0
        for i in pedata.getAllDllInstances(self.__pe):
            j += len(i.imports)
        return j
    
    def OnImportsEdit(self, event):
        event.Skip()
        
    def OnImportsRefresh(self, event):
        event.Skip()

    def OnDllEdit(self, event):
        event.Skip()
        
    def OnDllAddImport(self, event):
        event.Skip()
        
    def OnDllKillIID(self, event):
        event.Skip()
        
    def OnDllKillOFT(self, event):
        event.Skip()
        
    def OnDllRefresh(self, event):
        event.Skip()