#!/usr/bin/env python

#Boa:App:PyPeElf
#
#   Description:
#       This module parse the config file for PyPEELF
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

__revision__ = "$Id: config_parser.py 225 2009-09-21 06:15:50Z reversing $"

import ConfigParser

class ConfigFileParser:
    
    def __init__(self):
        
        self.fname = ""
        self.config = ConfigParser.ConfigParser()
        
    def open_config_file(self, fname):
        self.fname = fname
        try:
            fd = open(self.fname, "r")
            self.config.readfp(fd)
        except IOError, e:
            raise e
        
    def get_task_list_section(self):
        self.open_config_file(self.fname)
        return self.config.get("tasklist", "pids")
    
    def set_task_list_section(self, value):
        if value:
            self.config.set("tasklist", "pids", value)
    
    def write_config(self):
        try:
            configfile = open(self.fname, "w")
            self.config.write(configfile)
        except IOError, e:
            raise e
