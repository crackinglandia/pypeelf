#Boa:Frame:relocs
#
#   Description:
#       Relocs Viewer
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

__revision__ = "$Id: relocations.py 280 2009-10-27 00:51:57Z reversing $"

import wx
import sys
import pefile

from app import pedata
from app.common import hex_up, get_hex_bytes
from wx.lib.anchors import LayoutAnchors

#IMAGE_REL_BASED_ABSOLUTE        = 0
#IMAGE_REL_BASED_HIGH            = 1
#IMAGE_REL_BASED_LOW             = 2
#IMAGE_REL_BASED_HIGHLOW         = 3
#IMAGE_REL_BASED_HIGHADJ         = 4
#IMAGE_REL_BASED_MIPS_JMPADDR    = 5
#IMAGE_REL_BASED_SECTION         = 6
#IMAGE_REL_BASED_REL32           = 7

reloc_types = {0:"IMAGE_REL_BASED_ABSOLUTE", 1:"IMAGE_REL_BASED_HIGH", 2:"IMAGE_REL_BASED_LOW",3:"IMAGE_REL_BASED_HIGHLOW", 4:"IMAGE_REL_BASED_HIGHADJ", \
               5:"IMAGE_REL_BASED_MIPS_JMPADDR", 6:"IMAGE_REL_BASED_SECTION", 7:"IMAGE_REL_BASED_REL32"}

def create(parent):
    return relocs(parent)

[wxID_RELOCS, wxID_RELOC_BLOCKS_LIST, wxID_RELOC_BLOCKS_ITEMS, 
] = [wx.NewId() for _init_ctrls in range(3)]

class relocs(wx.Frame):
    def _init_relocblocks_colls(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Index', width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='Section', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='RVA', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Size of Block', width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT,
              heading='Items', width=-1)
    
    def _init_relocblocksitems_coll(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Index', width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='RVA', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Offset', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Type', width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT,
              heading='Far Address', width=-1)
        parent.InsertColumn(col=5, format=wx.LIST_FORMAT_LEFT,
              heading='Data Interpretation', width=-1)
        
    def _custom_inits(self, parent):
        self.relocViewer.Add(self.Blocks, 2, wx.EXPAND)
        self.relocViewer.Add(self.BlocksItems, 2, wx.EXPAND)
        
    def _init_sizers(self):
        self.relocViewer = wx.BoxSizer(orient=wx.VERTICAL)
        self.SetSizer(self.relocViewer)
    
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_RELOCS, name='relocs', parent=prnt,
              pos=wx.Point(439, 266), size=wx.Size(705, 463),
              style=wx.DEFAULT_FRAME_STYLE, title='Relocations')
        
        self.Centre()
        self.SetClientSize(wx.Size(689, 427))
        self.SetMinSize(wx.Size(500, 250))
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Blocks = wx.ListCtrl(id=wxID_RELOC_BLOCKS_LIST, name='Blocks',
              parent=self, pos=wx.Point(16, 16), size=wx.Size(656, 192),
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT) # wx.LC_SORT_ASCENDING isn't necessary in this case

        self.Blocks.SetConstraints(LayoutAnchors(self.Blocks, True, True, True, True))
        self._init_relocblocks_colls(self.Blocks)
        self.Blocks.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnBlockSelected, id=wxID_RELOC_BLOCKS_LIST)
        
        self.BlocksItems = wx.ListCtrl(id=wxID_RELOC_BLOCKS_ITEMS,
              name='BlocksItems', parent=self, pos=wx.Point(16, 240),
              size=wx.Size(656, 168), style=wx.LC_SINGLE_SEL | wx.LC_REPORT) # wx.LC_SORT_ASCENDING isn't necessary in this case

        self._init_relocblocksitems_coll(self.BlocksItems)
        
        self._init_sizers()
        
    def __init__(self, parent):
        self.__pe = parent.Parent.peInstance
        self.__parentDirectory = parent
        
        self._init_ctrls(parent)
        self._custom_inits(parent)
        
        self.loadRelocsInfo()
        
    def OnClose(self, event):
        self.__parentDirectory.Show()
        self.Destroy()
        
    def loadRelocsInfo(self):
        reloc_dir = pedata.getRelocDirectory(self.__pe)
        
        block_index = 1
        
        for entry in reloc_dir:
            
            index = self.Blocks.InsertStringItem(sys.maxint, str(block_index))
            
            entry_rva = entry.struct.VirtualAddress
            entry_size_of_block = entry.struct.SizeOfBlock
            entry_len = len(entry.entries)
            entry_section = self.__pe.sections[pedata.guess_section_from_rva(self.__pe, entry_rva)].Name
            
            self.Blocks.SetStringItem(index, 0, str(block_index))
            self.Blocks.SetStringItem(index, 1, entry_section)
            self.Blocks.SetStringItem(index, 2, hex_up(entry_rva))
            self.Blocks.SetStringItem(index, 3, hex_up(entry_size_of_block, 4))
            self.Blocks.SetStringItem(index, 4, "%sh / %sd" % (hex_up(len(entry.entries), 4), len(entry.entries)))
            
            block_index += 1
            
    def OnBlockSelected(self, event):
        self.BlocksItems.DeleteAllItems()
        item_id = self.Blocks.GetFirstSelected()
        item = self.Blocks.GetItem(item_id, 0)
        index = item.GetText()
        
        #wx.MessageBox("index: %d" % int(index), "index")
        
        reloc_dir = pedata.getRelocDirectory(self.__pe)
        
        items_index = 1
        entries = pedata.getRelocDataEntry(reloc_dir[int(index) - 1]) # -1 because index starts in 1
        
        for entry in entries:
            index = self.BlocksItems.InsertStringItem(sys.maxint, str(items_index))
            
            entry_rva = entry.rva
            entry_type = entry.type

            if entry_type >= 0:
                
                entry_far_address = self.__pe.get_dword_at_rva(entry_rva)
                entry_offset = self.__pe.get_offset_from_rva(entry_rva)
                entry_rva_data = entry_far_address - self.__pe.OPTIONAL_HEADER.ImageBase
                
                try:
                    entry_data = self.__pe.get_data(entry_rva_data, 10)
                    bytes = get_hex_bytes(entry_data)
                    if not bytes:
                        bytes = "-"
                except pefile.PEFormatError:
                    bytes = "-"
                
                self.BlocksItems.SetStringItem(index, 5, "%s" % bytes)
                
                if entry_type == 0: # ABSOLUTE
                    self.BlocksItems.SetStringItem(index, 0, str(items_index))
                    self.BlocksItems.SetStringItem(index, 1, "-")
                    self.BlocksItems.SetStringItem(index, 2, "-")
                    self.BlocksItems.SetStringItem(index, 3, "%s (%d)" % (reloc_types[entry_type], entry_type))
                    self.BlocksItems.SetStringItem(index, 4, "-")
                else:
                    self.BlocksItems.SetStringItem(index, 0, str(items_index))
                    self.BlocksItems.SetStringItem(index, 1, hex_up(entry_rva))
                    self.BlocksItems.SetStringItem(index, 2, hex_up(entry_offset))
                    self.BlocksItems.SetStringItem(index, 3, "%s (%d)" % (reloc_types[entry_type], entry_type))
                    self.BlocksItems.SetStringItem(index, 4, hex_up(entry_far_address))
                
                items_index += 1
            