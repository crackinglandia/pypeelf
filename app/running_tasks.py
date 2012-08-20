#
#   Description:
#       System running tasks
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

__revision__ = "$Id: running_tasks.py 233 2009-09-22 23:19:27Z mbordese $"

import os
import sys
from process import WinProcess, LinuxProcess

if sys.platform == 'win32':
    from winappdbg import System
    from app.process import WinProcess as Process

    # Request debugging privileges for the current process
    # This is needed to get some information from services
    # (based on winappdbg examples)
    System.request_debug_privileges()
else:
    import psi
    from app.process import LinuxProcess as Process


def get_process_from_pid(pid):
    return Process(pid)

def get_current_process_id():
    return os.getpid()

def get_processes_list():
    """Take a snapshot and return the list of processes"""

    if sys.platform == 'win32':
        # (based on winappdbg examples)
        # Create a system snaphot
        system = System()

        # The snapshot is initially empty, so populate it
        system.scan_processes()

        process_ids = list(system.iter_process_ids())
        # winappdbg does not include our pid, add it manually
        process_ids.append(get_current_process_id())
        process_ids.sort()

        # Return the processes in the system snapshot (iterator)
        return (WinProcess(pid) for pid in process_ids)
    else:
        pids = psi.process.ProcessTable()

        return (LinuxProcess(pid) for pid in pids)
