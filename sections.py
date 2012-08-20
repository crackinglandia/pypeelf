#Boa:Frame:Sections
#
#   Description: 
#       Section Viewer
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

__revision__ = "$Id: sections.py 298 2010-02-26 20:43:24Z reversing $"


import wx
import sys
import os
import wx.grid

from app import ini, edit_section_hdr, lister
from app.pedata import getSectionData
from app.common import hex_up, toInt

from ConfigParser import ConfigParser

from wx.lib.anchors import LayoutAnchors

def create(parent):
    return Sections(parent)

[wxID_SECTIONS, wxID_SECTIONLIST, 
] = [wx.NewId() for _init_ctrls in range(2)]

[wxID_EDIT_SECTION_HEADER, wxID_HEX_EDIT_SECTION, wxID_LOAD_SECTION_FROM_DISK,
 wxID_SAVE_SECTION_TO_DISK, wxID_ADD_SECTION_HEADER, wxID_WIPE_SECTION_HEADER,
 wxID_TRUNCATE_AT_SECTION_START, wxID_TRUNCATE_AT_END_OF_SECTION,
 wxID_SPLIT, wxID_UNSPLIT, wxID_LIST_SECTION_HEADER_TABLE, wxID_REFRESH_LIST,  
] = [wx.NewId() for _init_coll_contextMenu_Items in range(12)]

class Sections(wx.Frame):
    def _init_coll_sectionList_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Section', width=80)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='Virtual Size', width=100)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Virtual Offset', width=115)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Raw Size', width=100)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT,
              heading='Raw Offset', width=100)
        parent.InsertColumn(col=5, format=wx.LIST_FORMAT_LEFT,
              heading='Characteristics', width=110)

    def _init_coll_contextMenu_Items(self, parent):
        parent.Append(help='', id=wxID_REFRESH_LIST, kind=wx.ITEM_NORMAL, text="Refresh list")
        
        parent.AppendSeparator()
        
        parent.Append(help='', id=wxID_EDIT_SECTION_HEADER,
              kind=wx.ITEM_NORMAL, text='Edit section header')
        parent.Append(help='', id=wxID_HEX_EDIT_SECTION,
              kind=wx.ITEM_NORMAL, text='Hex edit section')
        
        parent.AppendSeparator()
        
        parent.Append(help='', id=wxID_LOAD_SECTION_FROM_DISK,
              kind=wx.ITEM_NORMAL, text='Load section from disk ...')
        parent.Append(help='', id=wxID_SAVE_SECTION_TO_DISK,
              kind=wx.ITEM_NORMAL, text='Save section to disk ...')
        
        parent.AppendSeparator()
                
        parent.Append(help='', id=wxID_ADD_SECTION_HEADER,
              kind=wx.ITEM_NORMAL, text='Add section header')
        parent.Append(help='', id=wxID_WIPE_SECTION_HEADER,
              kind=wx.ITEM_NORMAL, text='Wipe section header')
        
        parent.AppendSeparator()
        
        parent.Append(help='', id=wxID_TRUNCATE_AT_SECTION_START,
              kind=wx.ITEM_NORMAL, text='Truncate at section start')
        parent.Append(help='', id=wxID_TRUNCATE_AT_END_OF_SECTION,
              kind=wx.ITEM_NORMAL, text='Truncate at end of section')

        parent.AppendSeparator()
        
        parent.Append(help='', id=wxID_SPLIT,
              kind=wx.ITEM_NORMAL, text='Split')
        parent.Append(help='', id=wxID_UNSPLIT,
              kind=wx.ITEM_NORMAL, text='Unsplit ...')
        
        parent.AppendSeparator()
        
        parent.Append(help='', id=wxID_LIST_SECTION_HEADER_TABLE,
              kind=wx.ITEM_NORMAL, text='List section header table ...')
        
        self.Bind(wx.EVT_MENU, self.refresh_list, id=wxID_REFRESH_LIST)
        
        self.Bind(wx.EVT_MENU, self.OnEditSectionHeader,
              id=wxID_EDIT_SECTION_HEADER)
        
        self.Bind(wx.EVT_MENU, self.OnHexEditSection,
              id=wxID_HEX_EDIT_SECTION)

        self.Bind(wx.EVT_MENU, self.OnLoadSectionFromDisk,
              id=wxID_LOAD_SECTION_FROM_DISK)
        
        self.Bind(wx.EVT_MENU, self.OnSaveSectionToDisk,
              id=wxID_SAVE_SECTION_TO_DISK)
        
        self.Bind(wx.EVT_MENU, self.OnAddSectionHeader,
              id=wxID_ADD_SECTION_HEADER)
        
        self.Bind(wx.EVT_MENU, self.OnWipeSectionHeader,
              id=wxID_WIPE_SECTION_HEADER)
        
        self.Bind(wx.EVT_MENU, self.OnTruncateAtSectionStart,
              id=wxID_TRUNCATE_AT_SECTION_START)
        
        self.Bind(wx.EVT_MENU, self.OnTruncateAtEndOfSection,
              id=wxID_TRUNCATE_AT_END_OF_SECTION)

        self.Bind(wx.EVT_MENU, self.OnSplit,
              id=wxID_SPLIT)
        
        self.Bind(wx.EVT_MENU, self.OnUnsplit,
              id=wxID_UNSPLIT)
        
        self.Bind(wx.EVT_MENU, self.OnListSectionHeaderTable,
              id=wxID_LIST_SECTION_HEADER_TABLE)
        
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_SECTIONS, name='sections',
              parent=prnt, pos=wx.Point(439, 269), size=wx.Size(548, 352),
              style=wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE,
              title='Sections Viewer')
        
        self.Centre()
        self._init_utils()
        
        self.SetClientSize(wx.Size(610, 160))
        self.SetMinSize(wx.Size(500, 150))
        
        self.sectionList = wx.ListCtrl(id=wxID_SECTIONLIST,
              name='dllList', parent=self, pos=wx.Point(0, 144),
              size=wx.Size(544, 152),
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
        
        self.sectionList.SetConstraints(LayoutAnchors(self.sectionList, True, True, True, True))
        
        self._init_coll_sectionList_Columns(self.sectionList)

        self.sectionList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSectionListItemSelected, id=wxID_SECTIONLIST)
        self.sectionList.Bind(wx.EVT_RIGHT_DOWN, self.OnSectionListRightDown)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self._init_sizers()
        
    def _custom_inits(self, parent):
        self.sectionListSizer.Add(self.sectionList, 2, wx.EXPAND)
        
    def _init_sizers(self):
        self.sectionListSizer = wx.BoxSizer(orient=wx.VERTICAL)
        
        self.SetSizer(self.sectionListSizer)
        
    def _init_utils(self):
        self.contextMenu = wx.Menu(title='Section Options')

        self._init_coll_contextMenu_Items(self.contextMenu)
        
    def __init__(self, parent):
        self.parent = parent
        
        self._init_ctrls(parent)
        self._custom_inits(parent)
        self.current_item = None
        self.hdr_data = dict()
        self.showSectionData()
        
    def OnClose(self, event):
        self.parent.Show()
        self.Destroy()
        
    def OnSectionListItemSelected(self, event):
        self.current_item = event.m_itemIndex
        
    def OnSectionListRightDown(self, event):
        x = event.GetX()
        y = event.GetY()
        item, flags = self.sectionList.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.sectionList.Select(item)

        self.PopupMenu(self.contextMenu, event.GetPosition())
    
    def refresh_list(self, event):
        self.sectionList.DeleteAllItems()
        self.showSectionData()
        
    def showSectionData(self):
        sec_data = getSectionData(self.parent.peInstance)
        
        number_of_sections = self.get_pe_instance().FILE_HEADER.NumberOfSections
        for i in range(number_of_sections):
            section_name    = sec_data[i].Name
            v_size          = hex_up(sec_data[i].Misc_VirtualSize)
            v_offset        = hex_up(sec_data[i].VirtualAddress)
            r_size          = hex_up(sec_data[i].SizeOfRawData)
            r_offset        = hex_up(sec_data[i].PointerToRawData)
            chars           = hex_up(sec_data[i].Characteristics)
            
            index = self.sectionList.InsertStringItem(sys.maxint, section_name)
            
            self.sectionList.SetStringItem(index, 0, section_name)
            self.sectionList.SetStringItem(index, 1, v_size)
            self.sectionList.SetStringItem(index, 2, v_offset)
            self.sectionList.SetStringItem(index, 3, r_size)
            self.sectionList.SetStringItem(index, 4, r_offset)
            self.sectionList.SetStringItem(index, 5, chars)

    def OnEditSectionHeader(self, event):
        if self.current_item != None:
            
            self.hdr_data["SectionName"] = self.sectionList.GetItem(self.current_item, 0).GetText()
            
            self.hdr_data["VirtualSize"] = toInt(self.sectionList.GetItem(self.current_item, 1).GetText())
            self.hdr_data["VirtualOffset"] = toInt(self.sectionList.GetItem(self.current_item, 2).GetText())
            self.hdr_data["RawSize"] = toInt(self.sectionList.GetItem(self.current_item, 3).GetText())
            self.hdr_data["RawOffset"] = toInt(self.sectionList.GetItem(self.current_item, 4).GetText())
            self.hdr_data["Characteristics"] = toInt(self.sectionList.GetItem(self.current_item, 5).GetText())
            
            secHdrDlg = edit_section_hdr.create(self)
            secHdrDlg.Show()
            self.Hide()
        else:
            wx.MessageBox("Error getting currentItem from list", "Error", wx.ICON_ERROR)
            
    def OnHexEditSection(self, event):
        event.Skip()

    def OnLoadSectionFromDisk(self, event):
        event.Skip()

    def OnSaveSectionToDisk(self, event):
        current_item = self.get_section_index()
        if current_item != None:
            section_name = self.sectionList.GetItem(self.current_item, 0).GetText()
            pe = self.get_pe_instance()
            if pe.sections[current_item].Name.strip("\x00") == section_name:
                data = pe.sections[current_item].data
                
                dialog = wx.FileDialog ( None, style = wx.SAVE | wx.OVERWRITE_PROMPT)
                if dialog.ShowModal() == wx.ID_OK:
                    try:
                        fd = open(dialog.GetPath() + ".bin", "wb")
                        fd.write(data)
                        
                        wx.MessageBox("Section successfully saved to the disk! :)", "PyPEELF", wx.ICON_INFORMATION)
                        
                    except IOError, e:
                        wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
                    finally:
                        if fd:
                            fd.close()
        else:
            wx.MessageBox("Error getting currentItem from list", "Error", wx.ICON_ERROR)
            
    def OnAddSectionHeader(self, event):
        event.Skip()
        
    def OnWipeSectionHeader(self, event):
        current_item = self.get_section_index()
        
        pe = self.get_pe_instance()
        sections = pe.sections
        sections.pop(current_item)
        
        pe.FILE_HEADER.NumberOfSections -= 1
        
        self.refresh_list(event)
        
    def OnTruncateAtSectionStart(self, event):
        event.Skip()

    def OnTruncateAtEndOfSection(self, event):
        event.Skip()

    def OnSplit(self, event):
        pe = self.get_pe_instance()
        f_split = ini.Ini()
        
        header_sec_data = pe.get_data(0, pe.sections[0].PointerToRawData)
        
        path = os.path.dirname(self.get_loaded_file())
        f = open(path + "\\0_header.bin", "wb")
        f.write(header_sec_data)
        f.close()
        
        f_split.add_section("SPLITINFO")
        f_split.add_key("EXTENSION", ".%s" % os.path.basename(self.get_loaded_file()).split(".")[1])
        f_split.add_key("HEADER", path + "\\0_header.bin")
        
        for i in range(pe.FILE_HEADER.NumberOfSections):
            section_data = pe.sections[i].data #pe.get_data(pe.get_rva_from_offset(pe.sections[i].PointerToRawData), pe.sections[i].SizeOfRawData)
            
            bin_name = path + "\\%d_%s.bin" % (i+1, pe.sections[i].Name.strip('\x00').strip("."))
            
            f_split.add_key("SECTION%d" % (i+1), bin_name)
            
            try:
                f = open(bin_name, "wb")
                f.write(section_data)
            except IOError, e:
                wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
            finally:
                if f:
                    f.close()
        
        try:
            f = open(path + "\\split_info.ini", "w")
            f.write(f_split.show())
            wx.MessageBox("Done!. Files were saved in: %s. split_info.ini contains more information." % path, "Split ...", wx.ICON_INFORMATION)
        except IOError, e:
            wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
        finally:
            if f:
                f.close()
        
    def OnUnsplit(self, event):
        filters = 'Ini Files (*.ini)|*.ini|All files (*.*)|*.*'

        dialog = wx.FileDialog ( None, message = 'Select file....', wildcard = filters, style = wx.OPEN | wx.MULTIPLE )

        if dialog.ShowModal() == wx.ID_OK:
            ini_path = dialog.GetPaths()[0]

            try:
                fd1 = open(ini_path, "r")
                
                parser = ConfigParser()
                parser.readfp(fd1)
                
                ext = parser.get("SPLITINFO", "EXTENSION")
                header = parser.get("SPLITINFO", "HEADER")
                
                try:
                    fd = open(header, "wb")
                    hdr = fd.read()
                except IOError, e:
                    wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
                finally:
                    if fd:
                        fd.close()
                        
                items = parser.items("SPLITINFO")
                
                items.sort()
                #print items
                data = ""
                data += hdr
                for i in range(len(items) - 2):
                    section, path = items[i+2][0], items[i+2][1]
                    #print section, path
                    try:
                        fd = open(path, "wb")
                        data += fd.read()
                        #print len(data)
                    except IOError, e:
                        pass
                    finally:
                        if fd:
                            fd.close()
                
                try:
                    fd2 = open(r"C:\unsplitted" + ext.lower(), "wb")
                    #print len(data)
                    fd2.write(data)
                    wx.MessageBox("All sections have been merged!.", "Unsplit", wx.ICON_INFORMATION)
                except IOError, e:
                    wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
                finally:
                    if fd2:
                        fd2.close()
                        
            except IOError, e:
                wx.MessageBox("%s" % e.strerror, "IOError", wx.ICON_ERROR)
            finally:
                if fd1:
                    fd1.close()
                    
    def OnListSectionHeaderTable(self, event):
        section_lister = lister.create(self)
        section_lister.Show()
        self.Hide()
        
    def get_section_hdr_data(self):
        return self.hdr_data
    
    def get_pe_instance(self):
        return self.parent.peInstance
    
    def get_loaded_file(self):
        return self.parent.get_loaded_file()

    def get_section_index(self):
        return self.current_item
        