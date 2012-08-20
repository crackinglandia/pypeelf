#   Description:
#       Common functions
#   Authors:
#       +NCR/CRC! [ReVeRsEr] (nriva)
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

hex_up_1 = lambda s: "%0x".upper() % s
hex_up_8 = lambda s: "%08x".upper() % s
hex_up_4 = lambda s: "%04x".upper() % s
hex_up_16 = lambda s: "%016x".upper() % s


def hex_up(number, to_len=8):
    # return the hex string for number, filling with 0 up to to_len
    format = "%0" + str(to_len) + "X"
    ret = format % number
    return ret

def get_hex_bytes(data):
   #return map(lambda b: '%x' % ord(b), data)
   return ' '.join(map(lambda b: '%02X' % ord(b), data))

def toInt(s, base = 16):
    return int(s, base)
