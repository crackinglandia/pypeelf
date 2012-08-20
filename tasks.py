#Boa:Frame:task_viewer
#
#   Description:
#       System running tasks UI
#   Author:
#       Matias Bordese (mbordese)
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

__revision__ = "$Id: tasks.py 286 2009-11-13 20:01:52Z mbordese $"

import sys
import os.path
import wx
import wx.lib.mixins.listctrl as listmix

from wx.lib.anchors import LayoutAnchors

from app import config_parser
from app.common import hex_up
from app import running_tasks, images

def create(parent):
    return task_viewer(parent)

[wxID_TASK_VIEWER, wxID_TASK_VIEWERMODULELIST, wxID_TASK_VIEWERPROCESSLIST,
 wxID_TASK_VIEWERTASKSTATUS,
] = [wx.NewId() for _init_ctrls in range(4)]

[wxID_TASK_VIEWERCONTEXTMENUITEMS3, wxID_TASK_VIEWERCONTEXTMENUITEMS2, wxID_TASK_VIEWERCONTEXTMENUITEMS1, wxID_TASK_VIEWERMENU1ITEMS0,
] = [wx.NewId() for _init_coll_contextMenu_Items in range(4)]

class task_viewer(wx.Frame, listmix.ColumnSorterMixin):
    def _init_coll_contextMenu_Items(self, parent):
        parent.Append(help='', id=wxID_TASK_VIEWERMENU1ITEMS0,
              kind=wx.ITEM_NORMAL, text='dump')
        parent.Append(help='', id=wxID_TASK_VIEWERCONTEXTMENUITEMS1,
              kind=wx.ITEM_NORMAL, text='kill')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_TASK_VIEWERCONTEXTMENUITEMS2,
              kind=wx.ITEM_NORMAL, text='refresh')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_TASK_VIEWERCONTEXTMENUITEMS3,
              kind=wx.ITEM_NORMAL, text='exit')
        self.Bind(wx.EVT_MENU, self.OnContextMenuDump,
              id=wxID_TASK_VIEWERMENU1ITEMS0)
        self.Bind(wx.EVT_MENU, self.OnContextMenuKill,
              id=wxID_TASK_VIEWERCONTEXTMENUITEMS1)
        self.Bind(wx.EVT_MENU, self.OnContextMenuRefresh,
              id=wxID_TASK_VIEWERCONTEXTMENUITEMS2)
        self.Bind(wx.EVT_MENU, self.OnClose,
              id=wxID_TASK_VIEWERCONTEXTMENUITEMS3)

    def _init_coll_taskStatus_Fields(self, parent):
        parent.SetFieldsCount(6)

        parent.SetStatusText(number=0, text='Number of Processes')
        parent.SetStatusText(number=1, text='0')
        parent.SetStatusText(number=2, text='Number of Modules')
        parent.SetStatusText(number=3, text='0')
        parent.SetStatusText(number=4, text='Search')
        parent.SetStatusText(number=5, text='')

        parent.SetStatusWidths([150, 40, 150, 40, 75, 150])

    def _init_coll_moduleList_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Module Name', width=225)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='Module Entry Point', width=110)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Image base', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Size of image', width=-1)

    def _init_coll_processList_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading='Process Name', width=150)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='Process Id', width=75)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading='Image base', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading='Size of image', width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT, heading='Owner',
              width=-1)

    def _init_utils(self):
        self.contextMenu = wx.Menu(title='Process options')

        self._init_coll_contextMenu_Items(self.contextMenu)

    def _init_sizers(self):
        self.taskListSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.SetSizer(self.taskListSizer)

    def _init_column_sorting(self):
        self.itemDataMap = {}
        self.il = wx.ImageList(16, 16)
        self.sm_up = self.il.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.il.Add(images.getSmallDnArrowBitmap())
        self.processList.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_TASK_VIEWER, name='task_viewer',
              parent=prnt, pos=wx.Point(439, 269), size=wx.Size(548, 352),
              style=wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE,
              title='Tasks Viewer')

        self.Centre()
        self._init_utils()
        self.SetClientSize(wx.Size(540, 318))
        self.SetMinSize(wx.Size(500, 250))

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        self.moduleList = wx.ListCtrl(id=wxID_TASK_VIEWERMODULELIST,
              name='moduleList', parent=self.splitter,
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.moduleList.SetConstraints(LayoutAnchors(self.moduleList, True,
              True, True, True))

        #self.moduleList.SetBackgroundColour("black")
        #self.moduleList.SetTextColour("white")

        self._init_coll_moduleList_Columns(self.moduleList)

        self.taskStatus = wx.StatusBar(id=wxID_TASK_VIEWERTASKSTATUS,
              name='taskStatus', parent=self, style=0)
        self._init_coll_taskStatus_Fields(self.taskStatus)
        self.SetStatusBar(self.taskStatus)

        self.processList = wx.ListCtrl(id=wxID_TASK_VIEWERPROCESSLIST,
              name='processList', parent=self.splitter,
              style=wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.LC_REPORT)

        self._init_coll_processList_Columns(self.processList)

        self.processList.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnProcessListListItemSelected,
              id=wxID_TASK_VIEWERPROCESSLIST)
        self.processList.Bind(wx.EVT_RIGHT_DOWN, self.OnProcessListRightDown)

        self.splitter.SetMinimumPaneSize(100)
        self.splitter.SplitHorizontally(self.processList, self.moduleList)

        self._init_sizers()

    def _custom_inits(self, parent):
        self.taskListSizer.Add(self.splitter, 1, wx.EXPAND)

        acceltable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wxID_TASK_VIEWERCONTEXTMENUITEMS3),
                                          (wx.ACCEL_NORMAL, wx.WXK_F5, wxID_TASK_VIEWERCONTEXTMENUITEMS2)])
        self.SetAcceleratorTable(acceltable)


    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self._init_column_sorting()
        self._custom_inits(parent)

        self.search = ""
        self.processList.Bind(wx.EVT_CHAR, self.OnChar)

        config_file = os.path.join(os.path.dirname(__file__), "config/config.cfg")
        config = config_parser.ConfigFileParser()
        config.open_config_file(config_file)
        self.type_pid_ch = config.get_task_list_section()

        listmix.ColumnSorterMixin.__init__(self, 5)
        self.loadProcesses()
        #self.SortListItems(0, True)
        self.processList.SetFocus()
        self.MakeModal(True)

    def OnChar(self, evt):
        keycode = evt.GetKeyCode()

        if keycode == wx.WXK_ESCAPE:
            self.OnClose(evt)

        if keycode == 8:
            # Backspace removes last letter
            self.search = self.search[:-1]
        elif keycode < 256:
            self.search += chr(keycode)
        elif keycode == 127:
            # Delete erases phrase
            self.search = ''
        else:
            # Do the default action for nonascii keycodes
            evt.Skip()
            return 0

        idx = self.processList.FindItem(-1, self.search, partial=True)
        if idx != -1:
            self.taskStatus.SetStatusText(self.search, 5)
            self.processList.Select(idx)
            self.processList.EnsureVisible(idx)
        elif self.search != '':
            self.taskStatus.SetStatusText('%s not found!' % self.search, 5)
            self.search = ''

    def GetListCtrl(self):
        return self.processList

    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

    def loadProcesses(self):
        self.processList.DeleteAllItems()
        self.moduleList.DeleteAllItems()
        procs = running_tasks.get_processes_list()

        i = 0
        for p in procs:
            i += 1
            # the pid act as a key
            pid = p.get_pid()

            if p.get_filename():
                try:
                    name = os.path.basename(p.get_filename())
                    image_base = hex_up(p.get_image_base())
                    size_image = hex_up(p.get_image_size())
                except KeyError, e:
                    wx.MessageBox("Error in: %s, %s" % (name, str(e)), "Error", wx.ICON_ERROR)
            else:
                name = '[System]'
                image_base = hex_up(0)
                size_image = hex_up(0)
            owner = p.get_owner()

            # create the listctrl item
            index = self.processList.InsertStringItem(sys.maxint, name)
            if self.type_pid_ch == "decimal":
                self.processList.SetStringItem(index, 1, "%d" % pid)
                #index = self.processList.InsertStringItem(sys.maxint, "%d" % pid)
            else:
                self.processList.SetStringItem(index, 1, hex_up(pid))
                #index = self.processList.InsertStringItem(sys.maxint, hex_up_8(pid))

            #self.processList.SetStringItem(index, 1, name)
            self.processList.SetStringItem(index, 2, image_base)
            self.processList.SetStringItem(index, 3, size_image)
            self.processList.SetStringItem(index, 4, owner)
            self.processList.SetItemData(index, i)
            self.itemDataMap[i] = (name, pid, image_base, size_image, owner)
        self.SortListItems(0, True)
        self.taskStatus.SetStatusText(str(i), 1)

    def OnClose(self, event):
        self.MakeModal(False)
        self.parent.Restore()
        self.Destroy()

    def OnProcessListListItemSelected(self, event):
        item_id = self.processList.GetFirstSelected()
        item = self.processList.GetItem(item_id, 1)
        base = self.type_pid_ch == "decimal" and 10 or 16
        pid = int(item.GetText(), base)

        self.moduleList.DeleteAllItems()
        i = 0
        try:
            process = running_tasks.get_process_from_pid(pid)
            modules = process.get_modules()

            for m in modules:
                i += 1
                # the entry point act as a key
                ep = m.get_entry_point()
                m_id = ep and hex_up(ep) or '-'
                name = m.get_filename()
                image_base = hex_up(m.get_base())
                size_image = hex_up(m.get_size())
                # create the listctrl item
                index = self.moduleList.InsertStringItem(sys.maxint, name)
                self.moduleList.SetStringItem(index, 1, m_id)
                self.moduleList.SetStringItem(index, 2, image_base)
                self.moduleList.SetStringItem(index, 3, size_image)
                self.moduleList.SetItemData(index, i)
        except:
            # couldn't load modules
            wx.MessageBox('Could not load modules for %s' % pid, 'Error')

        self.taskStatus.SetStatusText(str(i), 3)

    def _get_selected_process(self):
        base = self.type_pid_ch == "decimal" and 10 or 16
        item_id = self.processList.GetFirstSelected()
        item = self.processList.GetItem(item_id, 1)
        pid = int(item.GetText(), base)
        process = running_tasks.get_process_from_pid(pid)

        return process


    def OnContextMenuDump(self, event):
        process = self._get_selected_process()
        save_dlg = wx.FileDialog(self, message="Save dump as ...", defaultDir=os.getcwd(),
                                 defaultFile="", wildcard="All files (*.*)|*.*", style=wx.SAVE)

        if save_dlg.ShowModal() == wx.ID_OK:
            outfile = save_dlg.GetPath()
            success = process.dump(outfile)

            msg = success and 'Dump file successfully saved' or 'Could not read process memory'
            dlg = wx.MessageDialog(self, msg, 'Information', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        save_dlg.Destroy()


    def OnProcessListRightDown(self, event):
        x = event.GetX()
        y = event.GetY()
        item, flags = self.processList.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.processList.Select(item)

        self.PopupMenu(self.contextMenu, event.GetPosition())

    def OnContextMenuKill(self, event):
        rsp = wx.MessageBox("Are you sure yo want to kill this process?", "Kill Process", wx.YES_NO)
        if rsp == wx.YES:
            # Refactoring needed: getDataFrom(list, index, column)
            process = self._get_selected_process()
            success = process.kill()

            msg = success and 'Process killed' or 'Could not kill the process'
            dlg = wx.MessageDialog(self, msg, 'Information', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

            self.loadProcesses()

    def OnContextMenuRefresh(self, event):
        self.loadProcesses()
