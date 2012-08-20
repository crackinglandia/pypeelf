#Boa:Frame:com
#
#   Description:
#       COM Viewer/Editor
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

__revision__ = "$Id: com.py 279 2009-10-25 23:53:06Z reversing $"

import wx

from app import comparser

from app.comparser import COMHeader
from app.common import hex_up

def create(parent):
    return com(parent)

[wxID_COM, wxID_COMCOM_TREE, 
] = [wx.NewId() for _init_ctrls in range(2)]

class com(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_COM, name='com', parent=prnt,
              pos=wx.Point(476, 289), size=wx.Size(629, 436),
              style=wx.DEFAULT_FRAME_STYLE, title='COM')
        
        self.SetClientSize(wx.Size(613, 400))

        self.Centre()
        
        self.com_tree = wx.TreeCtrl(id=wxID_COMCOM_TREE, name='com_tree',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(600, 384),
              style=wx.TR_HAS_BUTTONS)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __init__(self, parent):
        self._pe = parent.Parent.peInstance
        self._parentDirectory = parent
        
        self._init_ctrls(parent)

        self.populateComTree()
        
    def OnClose(self, event):
        self._parentDirectory.Show()
        self.Destroy()
    
    def populateComTree(self):
        ## http://www.ntcore.com/Files/dotnetformat.htm
        
        root = self.com_tree.AddRoot("COM Directory Data")
        self.set_py_data(root)
    
        comHdr = COMHeader(self._pe)
        
        CLRHeaderItem = self.com_tree.AppendItem(root, "CLR Header")
        self.set_py_data(CLRHeaderItem)
        
        cb = self.com_tree.AppendItem(CLRHeaderItem, "cb: %s" % hex_up(comHdr.get_com_cb()))
        self.set_py_data(cb)
        
        minor_version = comHdr.get_minor_runtime_version()
        major_version = comHdr.get_major_runtime_version()
        
        versionItem = self.com_tree.AppendItem(CLRHeaderItem, "Version: %d.%d" % (major_version, minor_version))
        self.set_py_data(versionItem)
        
        MjVersionRuntimeItem = self.com_tree.AppendItem(versionItem, "MajorRuntimeVersion: %s" % hex_up(major_version, 4))
        self.set_py_data(MjVersionRuntimeItem)
        
        MinorVersionRuntimeItem = self.com_tree.AppendItem(versionItem, "MinorRuntimeVersion: %s" % hex_up(minor_version, 4))
        self.set_py_data(MinorVersionRuntimeItem)
        
        FlagsItem = self.com_tree.AppendItem(CLRHeaderItem, "Flags: %s" % hex_up(comHdr.get_com_flags()))
        self.set_py_data(FlagsItem)
        
        EntryPointTokenItem = self.com_tree.AppendItem(CLRHeaderItem, "EntryPointToken: %s" % hex_up(comHdr.get_entry_point_token()))
        self.set_py_data(EntryPointTokenItem)
        
        MetaDataItem = self.com_tree.AppendItem(CLRHeaderItem, "MetaData DataDirectory")
        self.set_py_data(MetaDataItem)
        
        #### metadata struct ####
        metaDataStruct = comHdr.get_metadata()
        
        MetaDataRvaItem = self.com_tree.AppendItem(MetaDataItem, "VirtualAddress: %s" % hex_up(metaDataStruct[0]))
        self.set_py_data(MetaDataRvaItem)
        
        MetaDataSizeItem = self.com_tree.AppendItem(MetaDataItem, "VirtualSize: %s" % hex_up(metaDataStruct[1]))
        self.set_py_data(MetaDataSizeItem)
        
        #### resources struct ####
        ResourceDirStruct = comHdr.get_resources()
        
        ResourceDataItem = self.com_tree.AppendItem(CLRHeaderItem, "Resources DataDirectory")
        self.set_py_data(ResourceDataItem )
        
        ResourceRva = self.com_tree.AppendItem(ResourceDataItem, "VirtualAddress: %s" % hex_up(ResourceDirStruct[0]))
        self.set_py_data(ResourceRva)
        
        ResourceSize = self.com_tree.AppendItem(ResourceDataItem, "VirtualSize: %s" % hex_up(ResourceDirStruct[1]))
        self.set_py_data(ResourceSize)
        
        #### strongnames struct ####
        StrongNameStruct = comHdr.get_strong_name_signature()
        
        StrongNamesItem = self.com_tree.AppendItem(CLRHeaderItem, "StrongNameSignature DataDirectory")
        self.set_py_data(StrongNamesItem )
        
        SNRvaItem = self.com_tree.AppendItem(StrongNamesItem, "VirtualAddress: %s" % hex_up(StrongNameStruct[0]))
        self.set_py_data(SNRvaItem)
        
        SNSizeItem = self.com_tree.AppendItem(StrongNamesItem, "VirtualSize: %s" % hex_up(StrongNameStruct[1]))
        self.set_py_data(SNSizeItem)
        
        #### code manager table struct ####
        
        cmts = comHdr.get_code_manager_table()
        
        cmtItem = self.com_tree.AppendItem(CLRHeaderItem, "CodeManagerTable DataDirectory")
        self.set_py_data(cmtItem)
        
        cmtrvaItem = self.com_tree.AppendItem(cmtItem, "VirtualAddress: %s" % hex_up(cmts[0]))
        self.set_py_data(cmtrvaItem)
        
        cmtsizeItem = self.com_tree.AppendItem(cmtItem, "VirtualSize: %s" % hex_up(cmts[1]))
        self.set_py_data(cmtsizeItem)
        
        #### vtable fixups struct ####
        vtfs = comHdr.get_vtable_fixups()
        
        vtfItem = self.com_tree.AppendItem(CLRHeaderItem, "VtableFixups DataDirectory")
        self.set_py_data(vtfItem)
        
        vtfrvaItem = self.com_tree.AppendItem(vtfItem, "VirtualAddress: %s" % hex_up(vtfs[0]))
        self.set_py_data(vtfrvaItem)
        
        vtfsizeItem = self.com_tree.AppendItem(vtfItem, "VirtualSize: %s" % hex_up(vtfs[1]))
        self.set_py_data(vtfsizeItem)
        
        #### export address table jmps struct ####
        eatjs = comHdr.get_vtable_fixups()
        
        eatjItem = self.com_tree.AppendItem(CLRHeaderItem, "ExportAddressTableJumps DataDirectory")
        self.set_py_data(eatjItem)
        
        eatjrvaItem = self.com_tree.AppendItem(eatjItem, "VirtualAddress: %s" % hex_up(eatjs[0]))
        self.set_py_data(eatjrvaItem)
        
        eatjsizeItem = self.com_tree.AppendItem(eatjItem, "VirtualSize: %s" % hex_up(eatjs[1]))
        self.set_py_data(eatjsizeItem)
        
        #### managed native header struct ####
        mnhs = comHdr.get_vtable_fixups()
        
        mnhItem = self.com_tree.AppendItem(CLRHeaderItem, "ManagedNativeHeader DataDirectory")
        self.set_py_data(mnhItem)
        
        mnhrvaItem = self.com_tree.AppendItem(mnhItem, "VirtualAddress: %s" % hex_up(mnhs[0]))
        self.set_py_data(mnhrvaItem)
        
        mnhsizeItem = self.com_tree.AppendItem(mnhItem, "VirtualSize: %s" % hex_up(mnhs[1]))
        self.set_py_data(mnhsizeItem)
        
        ####################################
        ### METADATA HEADER
        ####################################
        metadataHdrItem = self.com_tree.AppendItem(CLRHeaderItem, "MetaData Header")
        self.set_py_data(metadataHdrItem)
        
        mdHdr = comparser.MetaDataHeader(self._pe)
        
        md_sig = self.com_tree.AppendItem(metadataHdrItem, "Signature: %s" % hex_up(mdHdr.get_signature()))
        self.set_py_data(md_sig)
        
        md_mj_version = self.com_tree.AppendItem(metadataHdrItem, "Major Version: %s" % hex_up(mdHdr.get_major_version(), 4))
        self.set_py_data(md_mj_version)
        
        md_mn_version = self.com_tree.AppendItem(metadataHdrItem, "Minor Version: %s" % hex_up(mdHdr.get_minor_version(), 4))
        self.set_py_data(md_mn_version)
        
        md_reserved = self.com_tree.AppendItem(metadataHdrItem, "Reserved: %s" % hex_up(mdHdr.get_reserved()))
        self.set_py_data(md_reserved)
        
        md_version_len = self.com_tree.AppendItem(metadataHdrItem, "Version Length: %s" % hex_up(mdHdr.get_version_length()))
        self.set_py_data(md_version_len)
        
        md_version_str = self.com_tree.AppendItem(metadataHdrItem, "Version String: %s" % mdHdr.get_version_string())
        self.set_py_data(md_version_str)
        
        md_flags = self.com_tree.AppendItem(metadataHdrItem, "Flags: %s" % hex_up(mdHdr.get_metadata_flags(), 4))
        self.set_py_data(md_flags)
        
        md_number_of_streams = self.com_tree.AppendItem(metadataHdrItem, "Number of Streams: %s" % hex_up(mdHdr.get_number_of_streams(), 4))
        self.set_py_data(md_number_of_streams)
        
        # METADATA STREAM HEADERS
        streams = comparser.MetadataStreams(self._pe)
        
        streams.get_headers()
        
        self.com_tree.Expand(root)
    
    def set_py_data(self, item, obj = None):
        self.com_tree.SetPyData(item, obj)
        