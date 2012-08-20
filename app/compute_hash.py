#
#   Description: 
#       This module compute the hashes of the file or string passed as input
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

__revision__ = "$Id: compute_hash.py 37 2009-07-11 05:47:41Z reversing $"

import wx
import zlib
import array
import hashlib

def computeMd5Hash(object):
    # http://thejaswihr.blogspot.com/2008/06/python-md5-checksum-of-file.html
    m = hashlib.md5()
    return compute_hash(object, m)

def computeCRC32Hash(fd, fz):
        # http://mail.python.org/pipermail/python-list/2002-January/120831.html

        v = array.array("B")
        try:
            v.fromfile(fd, fz)
            i = zlib.crc32(v.tostring())
        except:
            wx.MessageBox("Error: Not able to read or generate CRC", "Error")
            return
        return i

def computeSha1Hash(object):
    m = hashlib.sha1()
    return compute_hash(object, m)

def computeSha256Hash(object):
    m = hashlib.sha256()
    return compute_hash(object, m)

def computeSha384Hash(object):
    m = hashlib.sha384()
    return compute_hash(object, m)

def computeSha512Hash(object):
    m = hashlib.sha512()
    return compute_hash(object, m)

def compute_hash(object, m):
    if type(object) is file:
        content = object.readlines()
        
        for eachLine in content:
            m.update(eachLine)
            
        return m.hexdigest()
    
    if type(object) is str:
        m.update(object)
        return m.hexdigest()
    
    return False
