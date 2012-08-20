#!/usr/bin/env python
#
#   Description:
#       Break and Enter module. This module allow to set an int3 in the EP
#       of the loaded program and if you have a JIT debugger on you will catch
#       the exception produced by the int3.
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

__revision__ = "$Id: bae.py 248 2009-09-30 00:27:32Z reversing $"

import wx
import os
import pefile
import ctypes
import win32con

from app import running_tasks

from ctypes import windll as dll

from winappdbg import win32

###
# TODO:
# () Show the original byte to restore
###

def BreakAtEP():
    debug = False
    isASLRPresent = False
    
    filters = 'Executable Files (*.exe)|*.exe|Dinamyc Libraries (*dll)|*.dll|All files (*.*)|*.*'
    
    dialog = wx.FileDialog ( None, message = 'Select file....', wildcard = filters, style = wx.OPEN | wx.MULTIPLE )
    
    if dialog.ShowModal() == wx.ID_OK:
        fp = str(dialog.GetPaths()[0])

        if debug:
            print "%s" % fp

        try:
            pe = pefile.PE(fp)
            if pe.OPTIONAL_HEADER.DllCharacteristics & 0x00FF == 0x40:
                # http://www.nynaeve.net/?p=100
                isASLRPresent = True
        except pefile.PEFormatError, e:
            raise str(e)

        b = ctypes.create_string_buffer(255)
        dll.kernel32.GetCurrentDirectoryA(255, b)
        CurrentDirectory = b.value

        if debug:
            print "CurDir: %s" % CurrentDirectory
        
        hProcess = win32.CreateProcess(fp,\
                                       win32con.NULL, \
                                       win32con.NULL, \
                                       win32con.NULL, \
                                       0, \
                                       win32con.CREATE_SUSPENDED, \
                                       win32con.NULL, \
                                       CurrentDirectory)

        _hProcess = hProcess.hProcess.value
        _hThread = hProcess.hThread.value
        
        if debug:
            print "hProcess: 0x%04x" % _hProcess
            print "hThread: 0x%04x" % _hProcess
        
        b = ctypes.create_string_buffer(255)

        if debug:
            print "EntryPoint: 0x%08x" % pe.OPTIONAL_HEADER.AddressOfEntryPoint
            print "ImageBase: 0x%08x" % pe.OPTIONAL_HEADER.ImageBase

        ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        if isASLRPresent:
            image_base, image_size = GetModuleBaseAddress(fp)
            if debug:
                print "ImageBase: 0x%08x" % image_base
                print "ImageSize: 0x%08x" % image_size
            ep += image_base
        else:
            ep += pe.OPTIONAL_HEADER.ImageBase
        
        try:
            success = win32.WriteProcessMemory(_hProcess, ep, "\xcc")
            if not success:
                raise "Could not write to the specified address"
        except ctypes.WinError:
            raise "Could not write to the specified address"
        
        success = win32.ResumeThread(_hThread)
        
        if success == -1:
            raise "Could't resume thread."
        
        win32.CloseHandle(_hProcess)
        win32.CloseHandle(_hThread)

def GetModuleBaseAddress(moduleName):
    (image_base, image_size) = 0, 0
    procs = running_tasks.get_processes_list()
    
    for p in procs:
        fn = p.get_filename()
        if fn:
            if fn == moduleName:
                try:
                    # There is a little bug when winappdbg looks for the module
                    # in a dict(). Even if the except is reached, the correct ImageBase
                    # is returned by the call to get_image_base().
                    image_base = p.get_image_base()
                    image_size = p.get_image_size()
                except KeyError, e:
                    print "Error in %s:%s" % (os.path.basename(fn), str(e))
                    continue
    return (image_base, image_size)
