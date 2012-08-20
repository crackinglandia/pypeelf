#
#   Description:
#       Running process
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

__revision__ = "$Id: process.py 284 2009-11-13 19:44:37Z mbordese $"

import os
import sys
import signal
import pefile

if sys.platform == 'win32':
    from winappdbg import Process as winappdbgProcess
else:
    import psi
    import pwd

class Process(object):
    """A system running process"""

    def __init__(self, pid):
        self.platform = None
        self.pid = pid

    def get_pid(self):
        return self.pid

    def get_filename(self):
        return ''

    def get_image_base(self):
        return 0

    def get_image_size(self):
        return 0

    def get_owner(self):
        return ''

    def get_modules(self):
        return []

    def kill(self):
        return ''

    def dump(self):
        return ''

class WinProcess(Process):
    def __init__(self, pid):
        self.pid = pid
        # Instance a Process object
        self.process = winappdbgProcess(pid)
        self.platform = sys.platform
        self._load_modules()

    def _load_modules(self):
        try:
            self.process.scan_modules()
        except:
            pass

    def get_filename(self):
        return self.process.get_filename()

    def get_image_base(self):
        return self.process.get_image_base()

    def get_image_size(self):
        """Given a pid, return the modules of the process"""
        main_module = self.process.get_main_module()
        module_size = main_module.get_size()
        return module_size

    def get_owner(self):
        return ''

    def get_modules(self):
        """Return the modules of the process"""
        self._load_modules()
        # Return the modules in the process (iterator)
        return self.process.iter_modules()

    def kill(self):
        try:
            self.process.kill()
            res = True
        except:
            res = False
        return True

    def dump(self, outfile=None):
        try:
            main_module = self.process.get_main_module()
            base = main_module.get_base()
            size = main_module.get_size()
            process_image = self.process.read(base, size)
        except:
            return False

        pe = pefile.PE(data=process_image, fast_load=True)

        # Fix sections
        for section in pe.sections:
            section.PointerToRawData = section.VirtualAddress
            section.SizeOfRawData = section.Misc_VirtualSize

        # Fix alignment
        optional_header = pe.OPTIONAL_HEADER
        optional_header.FileAlignment = 0x1000

        # Fix headers size
        optional_header.SizeOfHeaders = 0x1000

        if outfile:
            pe.write(filename=outfile)

        return True


class LinuxProcess(Process):
    def __init__(self, pid):
        self.pid = pid
        self.process = psi.process.Process(pid)
        self.platform = sys.platform

    def get_filename(self):
        return getattr(self.process, 'exe', '')

    def get_image_base(self):
        return 0

    def get_image_size(self):
        """Given a pid, return the modules of the process"""
        return self.process.vsz

    def get_owner(self):
        return pwd.getpwuid(self.process.ruid).pw_name

    def get_modules(self):
        """Return the modules of the process"""
        return []

    def kill(self):
        try:
            os.kill(self.pid, signal.SIGKILL)
            res = True
        except:
            res = False
        return True

    def dump(self):
        return 'dump!'
