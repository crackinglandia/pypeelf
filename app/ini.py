#!/usr/bin/env python

#Boa:Frame:Sections
#
#   Description: 
#       INI File Class Implementation
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

__revision__ = "$Id: ini.py 298 2010-02-26 20:43:24Z reversing $"

# http://code.activestate.com/recipes/464408/
class Ini(object):
    def __init__(self):
        self.ini = []

    def add_section(self, section):
        self.ini.append("[%s]" % section)

    def add_key(self, key, value):
        self.ini.append("%s=%s" % (key, value))

    def add_comment(self, comment):
        self.ini.append(";%s" % comment)

    def add_verb(self, verb):
        self.ini.append(verb)

    def show(self):
        return "\n".join(self.ini)