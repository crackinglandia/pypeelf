#Boa:Frame:export_table_viewer
#
#   Description:
#       Export Table Viewer
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

__revision__ = "$Id: exports.py 289 2009-12-20 23:34:17Z reversing $"

import wx
import sys

from app import pedata, edit_exports
from app.common import hex_up, toInt

def create(parent):
    return export_table_viewer(parent)

[wxID_EXPORT_TABLE_VIEWER, wxID_EXPORT_TABLE_VIEWERADDRESS_OF_FUNCTIONS, 
 wxID_EXPORT_TABLE_VIEWERADDRESS_OF_NAMES, 
 wxID_EXPORT_TABLE_VIEWERADDRESS_OF_NAME_ORDINALS, 
 wxID_EXPORT_TABLE_VIEWERBASE, wxID_EXPORT_TABLE_VIEWERCHARACTERISTICS, 
 wxID_EXPORT_TABLE_VIEWEREXPORTS_LIST, 
 wxID_EXPORT_TABLE_VIEWEREXPORT_INFORMATION, 
 wxID_EXPORT_TABLE_VIEWERMAJOR_VERSION, wxID_EXPORT_TABLE_VIEWERMINOR_VERSION, 
 wxID_EXPORT_TABLE_VIEWERNAME, wxID_EXPORT_TABLE_VIEWERNAME_STRING, 
 wxID_EXPORT_TABLE_VIEWERNUMBER_OF_FUNCTIONS, 
 wxID_EXPORT_TABLE_VIEWERNUMBER_OF_NAMES, 
 wxID_EXPORT_TABLE_VIEWEROFFSET_TO_EXPORT_TABLE, wxID_EXPORT_TABLE_VIEWEROK, 
 wxID_EXPORT_TABLE_VIEWERSAVE, wxID_EXPORT_TABLE_VIEWERTIME_DATE_STAMP, 
 wxID_EXPORT_TABLE_VIEWER_ADDRESS_OF_FUNCTIONS, 
 wxID_EXPORT_TABLE_VIEWER_ADDRESS_OF_NAMES, 
 wxID_EXPORT_TABLE_VIEWER_ADDRESS_OF_NAME_ORDINALS, 
 wxID_EXPORT_TABLE_VIEWER_BASE, wxID_EXPORT_TABLE_VIEWER_CHARACTERISTICS, 
 wxID_EXPORT_TABLE_VIEWER_MAJOR_VERSION, 
 wxID_EXPORT_TABLE_VIEWER_MINOR_VERSION, wxID_EXPORT_TABLE_VIEWER_NAME, 
 wxID_EXPORT_TABLE_VIEWER_NAME_STRING, 
 wxID_EXPORT_TABLE_VIEWER_NUMBER_OF_FUNCTIONS, 
 wxID_EXPORT_TABLE_VIEWER_NUMBER_OF_NAMES, 
 wxID_EXPORT_TABLE_VIEWER_OFFSET_TO_EXPORT_TABLE, 
 wxID_EXPORT_TABLE_VIEWER_TIME_DATE_STAMP, 
] = [wx.NewId() for _init_ctrls in range(31)]

[wxID_EXPORTS_EDIT] = [wx.NewId() for _init_coll_ExportsContextMenu in range(1)]

class export_table_viewer(wx.Frame):
    def _init_coll_ExportsContextMenu(self, parent):
        parent.Append(help='', id=wxID_EXPORTS_EDIT,
              kind=wx.ITEM_NORMAL, text='Edit')
        
        self.Bind(wx.EVT_MENU, self.OnExportsEdit, id=wxID_EXPORTS_EDIT)

    def _init_coll_ExportsList_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Ordinal', width=90)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='RVA', width=200)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Offset', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Function Name', width=-1)

    def _init_utils(self):
        self.exportsContextMenu = wx.Menu(title='Exports Options')
        self._init_coll_ExportsContextMenu(self.exportsContextMenu)
        
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_EXPORT_TABLE_VIEWER,
              name='export_table_viewer', parent=prnt, pos=wx.Point(467, 239),
              size=wx.Size(622, 443),
              style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX,
              title='Export Table Viewer')
        
        self.Centre()
        
        self._init_utils()
        
        self.SetClientSize(wx.Size(606, 407))
        self.SetAutoLayout(False)
        self.SetThemeEnabled(True)
        self.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)

        self.export_information = wx.StaticBox(id=wxID_EXPORT_TABLE_VIEWEREXPORT_INFORMATION,
              label='Export Information', name='export_information',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(504, 200), style=0)

        self.ok = wx.Button(id=wxID_EXPORT_TABLE_VIEWEROK, label='OK',
              name='ok', parent=self, pos=wx.Point(520, 16), size=wx.Size(80,
              23), style=0)

        self.save = wx.Button(id=wxID_EXPORT_TABLE_VIEWERSAVE, label='Save',
              name='save', parent=self, pos=wx.Point(520, 40), size=wx.Size(80,
              23), style=0)

        self.exports_list = wx.ListCtrl(id=wxID_EXPORT_TABLE_VIEWEREXPORTS_LIST,
              name='exports_list', parent=self, pos=wx.Point(8, 216),
              size=wx.Size(592, 184), style=wx.LC_SINGLE_SEL | wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        
        self.offset_to_export_table = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWEROFFSET_TO_EXPORT_TABLE,
              label='Offset to Export Table', name='offset_to_export_table',
              parent=self, pos=wx.Point(24, 32), size=wx.Size(109, 13),
              style=0)

        self.characteristics = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERCHARACTERISTICS,
              label='Characteristics', name='characteristics', parent=self,
              pos=wx.Point(24, 56), size=wx.Size(72, 13), style=0)

        self.base = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERBASE, label='Base',
              name='base', parent=self, pos=wx.Point(24, 80), size=wx.Size(24,
              13), style=0)

        self.name = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERNAME, label='Name',
              name='name', parent=self, pos=wx.Point(24, 104), size=wx.Size(28,
              13), style=0)

        self.name_string = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERNAME_STRING,
              label='Name String', name='name_string', parent=self,
              pos=wx.Point(24, 128), size=wx.Size(59, 13), style=0)

        self._offset_to_export_table = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_OFFSET_TO_EXPORT_TABLE,
              name='_offset_to_export_table', parent=self, pos=wx.Point(144,
              24), size=wx.Size(100, 21), style=0, value='')

        self._characteristics = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_CHARACTERISTICS,
              name='_characteristics', parent=self, pos=wx.Point(144, 48),
              size=wx.Size(100, 21), style=0, value='')

        self._base = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_BASE, name='_base',
              parent=self, pos=wx.Point(144, 72), size=wx.Size(100, 21),
              style=0, value='')

        self._name = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_NAME, name='_name',
              parent=self, pos=wx.Point(144, 96), size=wx.Size(100, 21),
              style=0, value='')

        self._name_string = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_NAME_STRING,
              name='_name_string', parent=self, pos=wx.Point(96, 120),
              size=wx.Size(148, 21), style=0, value='')

        self.number_of_functions = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERNUMBER_OF_FUNCTIONS,
              label='Number Of Functions', name='number_of_functions',
              parent=self, pos=wx.Point(264, 32), size=wx.Size(102, 13),
              style=0)

        self.number_of_names = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERNUMBER_OF_NAMES,
              label='Number Of Names', name='number_of_names', parent=self,
              pos=wx.Point(264, 56), size=wx.Size(88, 13), style=0)

        self.address_of_functions = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERADDRESS_OF_FUNCTIONS,
              label='Address Of Functions', name='address_of_functions',
              parent=self, pos=wx.Point(264, 80), size=wx.Size(104, 13),
              style=0)

        self.address_of_names = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERADDRESS_OF_NAMES,
              label='Address Of Names', name='address_of_names', parent=self,
              pos=wx.Point(264, 104), size=wx.Size(90, 13), style=0)

        self.address_of_name_ordinals = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERADDRESS_OF_NAME_ORDINALS,
              label='Address Of Name Ordinals', name='address_of_name_ordinals',
              parent=self, pos=wx.Point(264, 128), size=wx.Size(127, 13),
              style=0)

        self._number_of_functions = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_NUMBER_OF_FUNCTIONS,
              name='_number_of_functions', parent=self, pos=wx.Point(400, 24),
              size=wx.Size(100, 21), style=0, value='')

        self._number_of_names = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_NUMBER_OF_NAMES,
              name='_number_of_names', parent=self, pos=wx.Point(400, 48),
              size=wx.Size(100, 21), style=0, value='')

        self._address_of_functions = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_ADDRESS_OF_FUNCTIONS,
              name='_address_of_functions', parent=self, pos=wx.Point(400, 72),
              size=wx.Size(100, 21), style=0, value='')

        self._address_of_names = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_ADDRESS_OF_NAMES,
              name='_address_of_names', parent=self, pos=wx.Point(400, 96),
              size=wx.Size(100, 21), style=0, value='')

        self._address_of_name_ordinals = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_ADDRESS_OF_NAME_ORDINALS,
              name='_address_of_name_ordinals', parent=self, pos=wx.Point(400,
              120), size=wx.Size(100, 21), style=0, value='')

        self.time_date_stamp = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERTIME_DATE_STAMP,
              label='TimeDateStamp', name='time_date_stamp', parent=self,
              pos=wx.Point(24, 152), size=wx.Size(76, 13), style=0)

        self._time_date_stamp = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_TIME_DATE_STAMP,
              name='_time_date_stamp', parent=self, pos=wx.Point(144, 144),
              size=wx.Size(100, 21), style=0, value='')

        self.minor_version = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERMINOR_VERSION,
              label='Minor Version', name='minor_version', parent=self,
              pos=wx.Point(264, 152), size=wx.Size(65, 13), style=0)

        self.major_version = wx.StaticText(id=wxID_EXPORT_TABLE_VIEWERMAJOR_VERSION,
              label='Major Version', name='major_version', parent=self,
              pos=wx.Point(264, 176), size=wx.Size(66, 13), style=0)

        self._minor_version = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_MINOR_VERSION,
              name='_minor_version', parent=self, pos=wx.Point(400, 144),
              size=wx.Size(100, 21), style=0, value='')

        self._major_version = wx.TextCtrl(id=wxID_EXPORT_TABLE_VIEWER_MAJOR_VERSION,
              name='_major_version', parent=self, pos=wx.Point(400, 168),
              size=wx.Size(100, 21), style=0, value='')

        self._init_coll_ExportsList_Columns(self.exports_list)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.exports_list.Bind(wx.EVT_RIGHT_DOWN, self.OnExportListRightDown)
        self.exports_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnExportListItemRightDown)
        self.exports_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnExportListItemSelected, id=wxID_EXPORT_TABLE_VIEWEREXPORTS_LIST)        
        self.save.Bind(wx.EVT_BUTTON, self.OnSaveButton, id=wxID_EXPORT_TABLE_VIEWERSAVE)
        
    def __init__(self, parent):
        self.__pe = parent.Parent.peInstance
        self.__fp = parent.Parent.get_loaded_file()
        self.__exp_data = dict()
        self.currentItem = None
        
        self.parentDirectory = parent
        export_data = pedata.getDirectoryEntryExport(self.__pe)
        
        self._init_ctrls(parent)
        
        self.loadExportData(export_data)
        self.loadExportSymbols(export_data)
        
    def OnClose(self, event):
        self.parentDirectory.Show()
        self.Destroy()
    
    def getFp(self):
        return self.__fp
    
    def getPeInstance(self):
        return self.__pe
    
    def getCurrentItemData(self):
        return self.__exp_data
    
    def OnExportsEdit(self, event):
        if self.currentItem != None:
            item_ordinal        = self.exports_list.GetItem(self.currentItem, 0)
            ordinal             = toInt(item_ordinal.GetText())
            item_rva            = self.exports_list.GetItem(self.currentItem, 1)
            rva                 = toInt(item_rva.GetText())
            item_offset         = self.exports_list.GetItem(self.currentItem, 2)
            offset              = toInt(item_offset.GetText())
            item_function_name  = self.exports_list.GetItem(self.currentItem, 3)
            function_name       = item_function_name.GetText()
            
            self.__exp_data["Ordinal"]  = ordinal - toInt(self._base.GetValue())
            self.__exp_data["RVA"]      = rva
            self.__exp_data["Offset"]   = offset
            self.__exp_data["Name"]     = function_name
            
            editItemDlg = edit_exports.create(self)
            editItemDlg.ShowModal()
        else:
            wx.MessageBox("Error getting currentItem from the list", "Error", wx.ICON_ERROR)
            
    def OnExportListItemRightDown(self, event):
        event.Skip()
        
    def OnExportListItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        
    def OnExportListRightDown(self, event):
        x = event.GetX()
        y = event.GetY()
        
        item, flags = self.exports_list.HitTest((x, y))
    
        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.exports_list.Select(item)

        position = self.exports_list.GetPosition() + event.GetPosition()
        self.PopupMenu(self.exportsContextMenu, position)
        
    def loadExportSymbols(self, export_data):
        e_symbols = export_data.symbols
        
        for symbol in e_symbols:
            ordinal = symbol.ordinal
            
            index = self.exports_list.InsertStringItem(sys.maxint, hex_up(ordinal, 4))
            
            symbol_rva = symbol.address
            offset = self.__pe.get_offset_from_rva(symbol_rva)
            symbol_name = symbol.name
            
            self.exports_list.SetStringItem(index, 0, hex_up(ordinal, 4))
            self.exports_list.SetStringItem(index, 1, hex_up(symbol_rva))
            self.exports_list.SetStringItem(index, 2, hex_up(offset))
            self.exports_list.SetStringItem(index, 3, symbol_name)
            
    def loadExportData(self, export_data):
        e_struct = export_data.struct
        
        end = self.__pe.get_data(e_struct.Name).find("\x00") + 1
        
        self._name_string.SetValue(self.__pe.get_data(e_struct.Name, end))
        self._offset_to_export_table.SetValue(hex_up(e_struct.get_file_offset()))
        self._characteristics.SetValue(hex_up(e_struct.Characteristics))
        self._base.SetValue(hex_up(e_struct.Base))
        self._name.SetValue(hex_up(e_struct.Name))
        self._address_of_functions.SetValue(hex_up(e_struct.AddressOfFunctions))
        self._address_of_names.SetValue(hex_up(e_struct.AddressOfNames))
        self._number_of_functions.SetValue(hex_up(e_struct.NumberOfFunctions))
        self._number_of_names.SetValue(hex_up(e_struct.NumberOfNames))
        self._address_of_name_ordinals.SetValue(hex_up(e_struct.AddressOfNameOrdinals))
        self._time_date_stamp.SetValue(hex_up(e_struct.TimeDateStamp))
        self._minor_version.SetValue(str(e_struct.MinorVersion))
        self._major_version.SetValue(str(e_struct.MajorVersion))
        
    def OnSaveButton(self, event):
        
        cs = pedata.getDirectoryEntryExport(self.__pe).struct
        
        new_dll_name = self._name_string.GetValue()
        
        end = self.__pe.get_data(cs.Name).find("\x00") + 1
        old_dll_name = self.__pe.get_data(cs.Name, end)
        
        if len(old_dll_name) == len(new_dll_name):    
            result = self.__pe.set_bytes_at_rva(cs.Name, new_dll_name)
            if not result:
                wx.MessageBox("Error saving the dll name", "Error", wx.ICON_ERROR)
        else:
            wx.MessageBox("The len of the dll name must be equal to the one in the file: %d" % len(old_dll_name), "Error in length", wx.ICON_ERROR)
            return False
        
        offset_to_et = toInt(self._offset_to_export_table.GetValue())
        
        self.__pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].VirtualAddress = offset_to_et
        
        cs.Characteristics       = toInt(self._characteristics.GetValue())
        cs.Base                  = toInt(self._base.GetValue())
        cs.Name                  = toInt(self._name.GetValue())
        cs.AddressOfFunctions    = toInt(self._address_of_functions.GetValue())
        cs.AddressOfNames        = toInt(self._address_of_names.GetValue())
        cs.NumberOfFunctions     = toInt(self._number_of_functions.GetValue())
        cs.NumberOfNames         = toInt(self._number_of_names.GetValue())
        cs.AddressOfNameOrdinals = toInt(self._address_of_name_ordinals.GetValue())
        cs.TimeDateStamp         = toInt(self._time_date_stamp.GetValue())
        cs.MinorVersion          = self._minor_version.GetValue()
        cs.MajorVersion          = self._major_version.GetValue()

        try:
            self.__pe.write(self.__fp)
        except IOError, e:
            raise str(e)
        