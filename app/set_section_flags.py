#Boa:Frame:section_flags
#
#   Description:
#       Set sections flags
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

__revision__ = "$Id: set_section_flags.py 297 2010-02-15 21:09:59Z reversing $"

# section's flags
IMAGE_NOPADDED = 3
IMAGE_SCN_CNT_CODE = 5
IMAGE_SCN_CNT_INITIALIZED_DATA = 6
IMAGE_SCN_CNT_UNINITIALIZED_DATA = 7
IMAGE_SCN_LNK_INFO = 9
IMAGE_SCN_LNK_REMOVE = 11
IMAGE_SCN_LNK_COMDAT = 12
IMAGE_SCN_MEM_FARDATA = 15
IMAGE_SCN_MEM_PURGEABLE = 17
IMAGE_SCN_MEM_LOCKED = 18
IMAGE_SCN_MEM_PRELOAD = 19
IMAGE_SCN_LNK_NRELOC_OVFL = 24
IMAGE_SCN_MEM_DISCARDABLE = 25
IMAGE_SCN_MEM_NOT_CACHED = 26
IMAGE_SCN_MEM_NOT_PAGED = 27
IMAGE_SCN_MEM_SHARED = 28
IMAGE_SCN_MEM_EXECUTE = 29
IMAGE_SCN_MEM_READ = 30
IMAGE_SCN_MEM_WRITE = 31

import wx

from app.common import hex_up

def create(parent):
    return section_flags(parent)

[wxID_SECTION_FLAGS, wxID_SECTION_FLAGSCANCEL, wxID_SECTION_FLAGSCB_COMDATA, 
 wxID_SECTION_FLAGSCB_CONTAINSCODE, wxID_SECTION_FLAGSCB_CONTAINSIDATA, 
 wxID_SECTION_FLAGSCB_CONTAINSUDATA, wxID_SECTION_FLAGSCB_DISCARDABLE, 
 wxID_SECTION_FLAGSCB_EXECUTABLE, wxID_SECTION_FLAGSCB_EXETENDED_RELOCS, 
 wxID_SECTION_FLAGSCB_NOCACHED, wxID_SECTION_FLAGSCB_NOIMAGE, 
 wxID_SECTION_FLAGSCB_NOPAGEABLE, wxID_SECTION_FLAGSCB_NOTPADDED, 
 wxID_SECTION_FLAGSCB_OTHERINFO, wxID_SECTION_FLAGSCB_READABLE, 
 wxID_SECTION_FLAGSCB_SHAREABLE, wxID_SECTION_FLAGSCB_WRITEABLE, 
 wxID_SECTION_FLAGSCURRENT_VAL, wxID_SECTION_FLAGSCURRENT_VALUE, 
 wxID_SECTION_FLAGSOK, wxID_SECTION_FLAGSSET_FLAGS, 
] = [wx.NewId() for _init_ctrls in range(21)]

class section_flags(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_SECTION_FLAGS, name='section_flags',
              parent=prnt, pos=wx.Point(813, 173), size=wx.Size(383, 338),
              style=wx.DEFAULT_FRAME_STYLE, title='[ Section Flags ]')
        self.SetClientSize(wx.Size(367, 302))

        self.set_flags = wx.StaticBox(id=wxID_SECTION_FLAGSSET_FLAGS,
              label='Set Flags', name='set_flags', parent=self, pos=wx.Point(8,
              0), size=wx.Size(232, 296), style=0)

        self.ok = wx.Button(id=wxID_SECTION_FLAGSOK, label='OK', name='ok',
              parent=self, pos=wx.Point(256, 8), size=wx.Size(96, 23), style=0)

        self.cancel = wx.Button(id=wxID_SECTION_FLAGSCANCEL, label='Cancel',
              name='cancel', parent=self, pos=wx.Point(256, 32),
              size=wx.Size(96, 23), style=0)

        self.current_value = wx.StaticBox(id=wxID_SECTION_FLAGSCURRENT_VALUE,
              label='Current Value', name='current_value', parent=self,
              pos=wx.Point(248, 248), size=wx.Size(114, 48), style=0)

        self.cb_shareable = wx.CheckBox(id=wxID_SECTION_FLAGSCB_SHAREABLE,
              label='Shareable in memory', name='cb_shareable', parent=self,
              pos=wx.Point(16, 24), size=wx.Size(120, 13), style=0)

        self.cb_executable = wx.CheckBox(id=wxID_SECTION_FLAGSCB_EXECUTABLE,
              label='Executable as code', name='cb_executable', parent=self,
              pos=wx.Point(16, 40), size=wx.Size(120, 13), style=0)

        self.cb_readable = wx.CheckBox(id=wxID_SECTION_FLAGSCB_READABLE,
              label='Readable', name='cb_readable', parent=self,
              pos=wx.Point(16, 56), size=wx.Size(70, 13), style=0)

        self.cb_writeable = wx.CheckBox(id=wxID_SECTION_FLAGSCB_WRITEABLE,
              label='Writeable', name='cb_writeable', parent=self,
              pos=wx.Point(16, 72), size=wx.Size(70, 13), style=0)

        self.cb_exetended_relocs = wx.CheckBox(id=wxID_SECTION_FLAGSCB_EXETENDED_RELOCS,
              label='Contains extended relocations', name='cb_exetended_relocs',
              parent=self, pos=wx.Point(16, 88), size=wx.Size(176, 13),
              style=0)

        self.cb_discardable = wx.CheckBox(id=wxID_SECTION_FLAGSCB_DISCARDABLE,
              label='Discardable as needed', name='cb_discardable', parent=self,
              pos=wx.Point(16, 104), size=wx.Size(136, 13), style=0)

        self.cb_nocached = wx.CheckBox(id=wxID_SECTION_FLAGSCB_NOCACHED,
              label="Can't be cached", name='cb_nocached', parent=self,
              pos=wx.Point(16, 120), size=wx.Size(104, 13), style=0)

        self.cb_nopageable = wx.CheckBox(id=wxID_SECTION_FLAGSCB_NOPAGEABLE,
              label='Not pageable', name='cb_nopageable', parent=self,
              pos=wx.Point(16, 136), size=wx.Size(96, 13), style=0)
        
        self.cb_comdata = wx.CheckBox(id=wxID_SECTION_FLAGSCB_COMDATA,
              label='Contains COMDAT data', name='cb_comdata', parent=self,
              pos=wx.Point(16, 152), size=wx.Size(144, 13), style=0)
        
        self.cb_otherinfo = wx.CheckBox(id=wxID_SECTION_FLAGSCB_OTHERINFO,
              label='Contains comments or other infos', name='cb_otherinfo',
              parent=self, pos=wx.Point(16, 168), size=wx.Size(192, 13),
              style=0)
        
        self.cb_noimage = wx.CheckBox(id=wxID_SECTION_FLAGSCB_NOIMAGE,
              label="Won't become part of the image", name='cb_noimage',
              parent=self, pos=wx.Point(16, 184), size=wx.Size(184, 13),
              style=0)
        
        self.cb_containscode = wx.CheckBox(id=wxID_SECTION_FLAGSCB_CONTAINSCODE,
              label='Contains executable code', name='cb_containscode',
              parent=self, pos=wx.Point(16, 200), size=wx.Size(160, 13),
              style=0)

        self.cb_containsidata = wx.CheckBox(id=wxID_SECTION_FLAGSCB_CONTAINSIDATA,
              label='Contains initialized data', name='cb_containsidata',
              parent=self, pos=wx.Point(16, 216), size=wx.Size(136, 13),
              style=0)

        self.cb_containsudata = wx.CheckBox(id=wxID_SECTION_FLAGSCB_CONTAINSUDATA,
              label='Contains unitializaed data', name='cb_containsudata',
              parent=self, pos=wx.Point(16, 232), size=wx.Size(152, 13),
              style=0)

        self.cb_notpadded = wx.CheckBox(id=wxID_SECTION_FLAGSCB_NOTPADDED,
              label="Shouldn't be padded to next boundary", name='cb_notpadded',
              parent=self, pos=wx.Point(16, 248), size=wx.Size(208, 13),
              style=0)

        self.current_val = wx.TextCtrl(id=wxID_SECTION_FLAGSCURRENT_VAL,
              name='current_val', parent=self, pos=wx.Point(256, 264),
              size=wx.Size(98, 21), style=0, value='')

        self.cb_shareable.SetValue(False)
        self.cb_executable.SetValue(False)
        self.cb_readable.SetValue(False)
        self.cb_writeable.SetValue(False)
        self.cb_exetended_relocs.SetValue(False)
        self.cb_discardable.SetValue(False)
        self.cb_nocached.SetValue(False)
        self.cb_nopageable.SetValue(False)
        self.cb_comdata.SetValue(False)
        self.cb_otherinfo.SetValue(False)
        self.cb_noimage.SetValue(False)
        self.cb_containscode.SetValue(False)
        self.cb_containsidata.SetValue(False)
        self.cb_containsudata.SetValue(False)
        self.cb_notpadded.SetValue(False)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.cancel.Bind(wx.EVT_BUTTON, self.OnClose, id=wxID_SECTION_FLAGSCANCEL)
        self.ok.Bind(wx.EVT_BUTTON, self.OnOkButton, id=wxID_SECTION_FLAGSOK)
        
        self.cb_containsudata.Bind(wx.EVT_CHECKBOX, self.OnContainsUData, id=wxID_SECTION_FLAGSCB_CONTAINSUDATA)
        self.cb_containsidata.Bind(wx.EVT_CHECKBOX, self.OnContainsIData, id=wxID_SECTION_FLAGSCB_CONTAINSIDATA)
        self.cb_shareable.Bind(wx.EVT_CHECKBOX, self.OnShareable, id=wxID_SECTION_FLAGSCB_SHAREABLE)
        self.cb_executable.Bind(wx.EVT_CHECKBOX, self.OnExecutable, id=wxID_SECTION_FLAGSCB_EXECUTABLE)
        self.cb_readable.Bind(wx.EVT_CHECKBOX, self.OnReadeable, id=wxID_SECTION_FLAGSCB_READABLE)
        self.cb_writeable.Bind(wx.EVT_CHECKBOX, self.OnWriteable, id=wxID_SECTION_FLAGSCB_WRITEABLE)
        self.cb_exetended_relocs.Bind(wx.EVT_CHECKBOX, self.OnExtendedRelocs, id=wxID_SECTION_FLAGSCB_EXETENDED_RELOCS)
        self.cb_discardable.Bind(wx.EVT_CHECKBOX, self.OnDiscardable, id=wxID_SECTION_FLAGSCB_DISCARDABLE)
        self.cb_nocached.Bind(wx.EVT_CHECKBOX, self.OnNoCached, id=wxID_SECTION_FLAGSCB_NOCACHED)
        self.cb_nopageable.Bind(wx.EVT_CHECKBOX, self.OnNoPageable, id=wxID_SECTION_FLAGSCB_NOPAGEABLE)
        self.cb_comdata.Bind(wx.EVT_CHECKBOX, self.OnComData, id=wxID_SECTION_FLAGSCB_COMDATA)
        self.cb_otherinfo.Bind(wx.EVT_CHECKBOX, self.OnOtherInfo, id=wxID_SECTION_FLAGSCB_OTHERINFO)
        self.cb_noimage.Bind(wx.EVT_CHECKBOX, self.OnNoImage, id=wxID_SECTION_FLAGSCB_NOIMAGE)
        self.cb_containscode.Bind(wx.EVT_CHECKBOX, self.OnContainsCode, id=wxID_SECTION_FLAGSCB_CONTAINSCODE)
        self.cb_notpadded.Bind(wx.EVT_CHECKBOX, self.OnNotPadded, id=wxID_SECTION_FLAGSCB_NOTPADDED)

    def __init__(self, parent):
        self._init_ctrls(parent)

        self.parent = parent
        self.flag_list = list()
        
        self.populate_checkboxes()
        
    def OnClose(self, event):
        self.parent.Show()
        self.Destroy()
    
    def populate_checkboxes(self):
        current_flags = self.parent.get_section_flags()
        current_value = 0
        
        if current_flags & 2**IMAGE_SCN_CNT_CODE != 0:
            self.cb_containscode.SetValue(True)
            current_value += 2**IMAGE_SCN_CNT_CODE
            
        if current_flags & 2**IMAGE_SCN_CNT_INITIALIZED_DATA != 0:
            self.cb_containsidata.SetValue(True)
            current_value += 2**IMAGE_SCN_CNT_INITIALIZED_DATA
            
        if current_flags & 2**IMAGE_SCN_CNT_UNINITIALIZED_DATA != 0:
            self.cb_containsudata.SetValue(True)
            current_value += 2**IMAGE_SCN_CNT_UNINITIALIZED_DATA
            
        if current_flags & 2**IMAGE_SCN_LNK_INFO != 0:
            self.cb_otherinfo.SetValue(True)
            current_value += 2**IMAGE_SCN_LNK_INFO
            
        if current_flags & 2**IMAGE_SCN_LNK_COMDAT != 0:
            self.cb_comdata.SetValue(True)
            current_value += 2**IMAGE_SCN_LNK_COMDAT
            
        if current_flags & 2**IMAGE_SCN_LNK_NRELOC_OVFL != 0:
            self.cb_exetended_relocs.SetValue(True)
            current_value += 2**IMAGE_SCN_LNK_NRELOC_OVFL
            
        if current_flags & 2**IMAGE_SCN_MEM_DISCARDABLE != 0:
            self.cb_discardable.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_DISCARDABLE
            
        if current_flags & 2**IMAGE_SCN_MEM_NOT_CACHED != 0:
            self.cb_nocached.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_NOT_CACHED
            
        if current_flags & 2**IMAGE_SCN_MEM_NOT_PAGED != 0:
            self.cb_nopageable.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_NOT_PAGED
            
        if current_flags & 2**IMAGE_SCN_MEM_SHARED != 0:
            self.cb_shareable.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_SHARED
            
        if current_flags & 2**IMAGE_SCN_MEM_EXECUTE != 0:
            self.cb_executable.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_EXECUTE
            
        if current_flags & 2**IMAGE_SCN_MEM_READ != 0:
            self.cb_readable.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_READ
            
        if current_flags & 2**IMAGE_SCN_MEM_WRITE != 0:
            self.cb_writeable.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_WRITE
        
        if current_flags & 2**IMAGE_SCN_MEM_FARDATA != 0:
            self.cb_noimage.SetValue(True)
            current_value += 2**IMAGE_SCN_MEM_FARDATA
        
        if current_flags & 2**IMAGE_NOPADDED != 0:
            self.cb_notpadded.SetValue(True)
            current_value += 2**IMAGE_NOPADDED
            
        self.current_val.SetValue(hex_up(current_value))
    
    def OnOkButton(self, event):
        self.parent.set_section_flags(int(self.current_val.GetValue()))
    
    def OnContainsUData(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_CNT_UNINITIALIZED_DATA
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_CNT_UNINITIALIZED_DATA
            
        self.current_val.SetValue(hex_up(cv))
    
    def OnContainsIData(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_CNT_INITIALIZED_DATA
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_CNT_INITIALIZED_DATA
            
        self.current_val.SetValue(hex_up(cv))

    def OnShareable(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_SHARED
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_SHARED
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnExecutable(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_EXECUTE
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_EXECUTE
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnReadeable(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_READ
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_READ
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnWriteable(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_WRITE
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_WRITE
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnExtendedRelocs(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_LNK_NRELOC_OVFL
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_LNK_NRELOC_OVFL
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnDiscardable(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_DISCARDABLE
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_DISCARDABLE
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnNoCached(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_NOT_CACHED
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_NOT_CACHED
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnNoPageable(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_NOT_PAGED
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_NOT_PAGED
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnComData(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_LNK_COMDAT
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_LNK_COMDAT
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnOtherInfo(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_LNK_INFO
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_LNK_INFO
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnNoImage(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_MEM_FARDATA
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_MEM_FARDATA
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnContainsCode(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_SCN_CNT_CODE
        
        if not event.IsChecked():
            cv -= 2**IMAGE_SCN_CNT_CODE
            
        self.current_val.SetValue(hex_up(cv))

    
    def OnNotPadded(self, event):
        cv = int(self.current_val.GetValue(), 16)
        
        if event.IsChecked():
            cv += 2**IMAGE_NOPADDED
        
        if not event.IsChecked():
            cv -= 2**IMAGE_NOPADDED
            
        self.current_val.SetValue(hex_up(cv))
        