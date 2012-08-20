#!/usr/bin/env python
#
#   Description:
#       COM Directory raw parser.
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

__revision__ = "$Id: comparser.py 206 2009-09-17 00:18:26Z reversing $"

import struct

class COMHeader:
    def __init__(self, pe):
        if pe == None:
            raise Exception, "Error: PE instance was not specified."
        
        self.pe = pe
        self.com_descriptor = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[14]
        self.com_rva = self.com_descriptor.VirtualAddress
        self.com_size = self.com_descriptor.Size
    
    def get_com_cb(self):
        return self.unpack_as_dword(self.get_data(self.com_rva, 4))[0]
    
    def get_major_runtime_version(self):
        return self.unpack_as_word(self.get_data(self.com_rva+4, 2))[0]
    
    def get_minor_runtime_version(self):
        return self.unpack_as_word(self.get_data(self.com_rva+6, 2))[0]

    def get_com_flags(self):
        return self.unpack_as_word(self.get_data(self.com_rva+16, 2))[0]
    
    def get_entry_point_token(self):
        return self.unpack_as_dword(self.get_data(self.com_rva+20, 4))[0]
    
    def get_metadata(self):
        rva = self.unpack_as_dword(self.get_data(self.com_rva+8, 4))[0]
        size = self.unpack_as_dword(self.get_data(self.com_rva+12, 4))[0]
        return (rva, size)
    
    def get_resources(self):
        rva = self.unpack_as_dword(self.get_data(self.com_rva+24, 4))[0]
        size = self.unpack_as_dword(self.get_data(self.com_rva+28, 4))[0]
        return (rva, size)

    def get_strong_name_signature(self):
        rva = self.unpack_as_dword(self.get_data(self.com_rva+32, 4))[0]
        size = self.unpack_as_dword(self.get_data(self.com_rva+36, 4))[0]
        return (rva, size)
    
    def get_code_manager_table(self):
        rva = self.unpack_as_dword(self.get_data(self.com_rva+40, 4))[0]
        size = self.unpack_as_dword(self.get_data(self.com_rva+44, 4))[0]
        return (rva, size)
    
    def get_vtable_fixups(self):
        rva = self.unpack_as_dword(self.get_data(self.com_rva+48, 4))[0]
        size = self.unpack_as_dword(self.get_data(self.com_rva+52, 4))[0]
        return (rva, size)
    
    def get_export_address_table_jumps(self):
        rva = self.unpack_as_dword(self.get_data(self.com_rva+56, 4))[0]
        size = self.unpack_as_dword(self.get_data(self.com_rva+60, 4))[0]
        return (rva, size)
    
    def get_managed_native_headers(self):
        rva = self.unpack_as_dword(self.get_data(self.com_rva+64, 4))[0]
        size = self.unpack_as_dword(self.get_data(self.com_rva+68, 4))[0]
        return (rva, size)

    def get_data(self, rva, size = None):
        if not size:
            return self.pe.get_data(rva)
        return self.pe.get_data(rva, size)
    
    def custom_pack(self, fmt, data):
        return struct.pack(fmt, data)
    
    def custom_unpack(self, fmt, data):
        return struct.unpack(fmt, data)
    
    def unpack_as_dword(self, Str):
        return struct.unpack("<L", Str)
    
    def unpack_as_word(self, Str):
        return struct.unpack("<H", Str)
    
    def unpack_as_byte(self, Str):
        return struct.unpack("B", Str)
    
    def pack_as_dword(self, Str):
        return struct.pack("<L", Str)
    
    def pack_as_word(self, Str):
        return struct.pack("<H", Str)
    
    def pack_as_byte(self, Str):
        return struct.pack("B", Str)
    
class MetaDataHeader(COMHeader):
    def __init__(self, pe):
        COMHeader.__init__(self, pe)
    
        self.metadata = self.get_metadata()
        self.metadata_rva = self.metadata[0]
        self.metadata_size = self.metadata[1]
        
    def get_signature(self):
        return self.unpack_as_dword(self.get_data(self.metadata_rva, 4))[0]
    
    def get_minor_version(self):
        return self.unpack_as_word(self.get_data(self.metadata_rva+4, 2))[0]
    
    def get_major_version(self):    
        return self.unpack_as_word(self.get_data(self.metadata_rva+6, 2))[0]
    
    def get_reserved(self):
        return self.unpack_as_dword(self.get_data(self.metadata_rva+8, 4))[0]
    
    def get_version_length(self):
        return self.unpack_as_dword(self.get_data(self.metadata_rva+12, 4))[0]
    
    def get_version_string(self):
        return self.get_data(self.metadata_rva+16, self.get_version_length())
    
    def get_metadata_flags(self):
        return self.unpack_as_word(self.get_data(self.metadata_rva+16+self.get_version_length(), 2))[0]
    
    def get_number_of_streams(self):
        return self.unpack_as_word(self.get_data(self.metadata_rva+18+self.get_version_length(), 2))[0]
    

class MetadataStreams(MetaDataHeader):
    def __init__(self, pe):
        MetaDataHeader.__init__(self, pe)
        
        # every key in the dict is a touple with (RVA, SIZE) values.
        self.md_sections = dict()
        
    def get_headers(self):
        count = self.get_number_of_streams()
        # magic! this is where the MetadataHeader ends, the last field is NumberOfStreams
        # next to it is the MetadataSectionHeaders, so we parse all the data after
        # this field.
        start_offset = self.metadata_rva + 18 + self.get_version_length() + 2
        for i in range(count):
            offset, size = struct.unpack("<LL", self.get_data(start_offset, 8))
            
            start_offset += 8
            
            string_len = self.get_data(start_offset).find("\x00") + 1
            padding = (string_len % 4) and (4 - (string_len % 4)) or 0
            fmt = "%ds%dx" % (string_len, padding)
            total_len = string_len + padding
            string_read = struct.unpack(fmt, self.get_data(start_offset, total_len))[0]
            start_offset += total_len
            
            #print string_read
            self.md_sections[string_read] = (offset, size)
    
    
    
    
"""
## XXX: we must implement the header as a struct
## http://msdn.microsoft.com/en-us/magazine/bb985996.aspx
## of we can add this functionality to pefile :P
#
#    type IMAGE_COR20_HEADER = RECORD
#    
#        cb: DWORD;
#        MajorRuntimeVersion: word;
#        MinorRuntimeVersion: word;
#        
#        // Symbol table and startup information
#        MetaData: IMAGE_DATA_DIRECTORY;
#        Flags: dword;
#        EntryPointToken: dword;
#    
#        // Binding information
#        Resources: IMAGE_DATA_DIRECTORY;
#        StrongNameSignature: IMAGE_DATA_DIRECTORY;
#        
#        // Regular fixup and binding information
#        CodeManagerTable: IMAGE_DATA_DIRECTORY;
#        VTableFixups: IMAGE_DATA_DIRECTORY;
#        ExportAddressTableJumps: IMAGE_DATA_DIRECTORY;
#        ManagedNativeHeader: IMAGE_DATA_DIRECTORY;
#    end;
#    
#    IMAGE_DATA_DIRECTORY:
#    
#    type IMAGE_DATA_DIRECTORY = RECORD
#        VirtualAddress: longword;
#        isize: longword;
#     end;
##
"""

"""
The MetaData Section

This section begins with a header that I called MetaData Header (yes, I'm full of imagination indeed). Let's take a look at this header (since it's a dynamic header, it makes no sense declaring a structure, I'll just list the members):

Signature It's a simple dword-signature (similary to the ones you find in the Dos Header and the Optional Header). Anyway the value of this signature has to be 0x424A5342.

MajorVersion and MinorVersion Two word elements that are totally ignored by the loader. The value is 0x0001 for both.

Reserved A dword which value is always 0.
Length The length of the UTF string that follows (it's the version string, something like: "v1.1.4322"). The length has to be rounded up to a multiple of 4.

Version The string we just talked about.

Flags Reserved, this word is always 0.

Streams A word telling us the number of streams present in the MetaData.
"""