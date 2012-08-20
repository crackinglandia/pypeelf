#!/usr/bin/env python
#
#   Description:
#       Signature database parser
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

__revision__ = "$Id: signaturesdb.py 131 2009-08-10 22:25:07Z mbordese $"

import os
import sys
import peutils
import wx

#sys.path.append(os.curdir)

def load_database():
    path = os.path.join(os.path.dirname(__file__), "UserDB.txt")
    return peutils.SignatureDatabase(path)

def match_pe(pe, signatures):
    return signatures.match(pe, ep_only = True)

def match_all(pe, signatures):
    return signatures.match_all(pe, ep_only = True)

def generate_signature(pe, signatures, name):
    signatures.generate_ep_signature(pe, name, len(name))

def getSignature(pe):
    db = load_database()
    return match_pe(pe, db)
