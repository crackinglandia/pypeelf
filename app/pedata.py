#!/usr/bin/env python
#
#   Description:
#       pefile wrapper
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

__revision__ = "$Id: pedata.py 211 2009-09-19 20:35:48Z reversing $"

import pefile

def getDosHeader(pe):
    return pe.DOS_HEADER

def getRelocDirectory(pe):
    return pe.DIRECTORY_ENTRY_BASERELOC

def getRelocDataStruct(reloc_entry):
    return reloc_entry.struct

def getRelocDataEntry(reloc_entry):
    return reloc_entry.entries
    
def getTlsStruct(pe):
    return pe.DIRECTORY_ENTRY_TLS.struct

def guess_section_from_rva(pe, rva):
    # TODO: improve search, we must implement some other kind
    # of search algorithm.
    if rva < pe.sections[0].VirtualAddress: # this means that the rva is in the HEADER
        return -1
    
    for i in range(pe.FILE_HEADER.NumberOfSections):
        if (pe.sections[i].VirtualAddress <= rva) and (rva  <= pe.sections[i].VirtualAddress + pe.sections[i].Misc_VirtualSize):
            break
    return i

def fromRvaToOffset(pe, rva):
    in_section = guess_section_from_rva(pe, rva)
    
    if in_section == -1:
        offset = rva
        return offset
        
    offset = (rva - pe.sections[in_section].VirtualAddress) + pe.sections[in_section].PointerToRawData
    return offset

def fromOffsetToRva(pe, offset, in_section):
    rva = (offset - pe.sections[in_section].PointerToRawData) + pe.sections[in_section].VirtualAddress
    return rva

def getPEHeaderData(pe):
    oh = pe.OPTIONAL_HEADER
    fh = pe.FILE_HEADER
    
    if pe.PE_TYPE == 0x10b: # x86
        peHeader = {"EntryPoint": oh.AddressOfEntryPoint, \
                    "ImageBase": oh.ImageBase, \
                    "BaseOfCode": oh.BaseOfCode, \
                    "BaseOfData": oh.BaseOfData, \
                    "SizeOfImage": oh.SizeOfImage, \
                    "SizeOfHeaders": oh.SizeOfHeaders, \
                    "SectionAlignment": oh.SectionAlignment, \
                    "FileAlignment": oh.FileAlignment, \
                    "Subsystem": oh.Subsystem, \
                    "MachineType": fh.Machine, \
                    "NumberOfSections": fh.NumberOfSections, \
                    "TimeDateStamp": fh.TimeDateStamp, \
                    "PointerToSymbolTable": fh.PointerToSymbolTable, \
                    "NumberOfSymbols": fh.NumberOfSymbols, \
                    "SizeOfOptionalHeader": fh.SizeOfOptionalHeader, \
                    "Characteristics": fh.Characteristics
                    }
        
    if pe.PE_TYPE == 0x20b: # IA64
        peHeader = {"EntryPoint": oh.AddressOfEntryPoint, \
            "ImageBase": oh.ImageBase, \
            "BaseOfCode": oh.BaseOfCode, \
            "SizeOfImage": oh.SizeOfImage, \
            "SizeOfHeaders": oh.SizeOfHeaders, \
            "SectionAlignment": oh.SectionAlignment, \
            "FileAlignment": oh.FileAlignment, \
            "Subsystem": oh.Subsystem, \
            "MachineType": fh.Machine, \
            "NumberOfSections": fh.NumberOfSections, \
            "TimeDateStamp": fh.TimeDateStamp, \
            "PointerToSymbolTable": fh.PointerToSymbolTable, \
            "NumberOfSymbols": fh.NumberOfSymbols, \
            "SizeOfOptionalHeader": fh.SizeOfOptionalHeader, \
            "Characteristics": fh.Characteristics
            }

    return peHeader

def getDirectoryEntryExport(pe):
    return pe.DIRECTORY_ENTRY_EXPORT

def getEntryExportStruct(pe):
    return pe.DIRECTORY_ENTRY_EXPORT.struct

def getEntryExportSymbols(pe):
    return pe.DIRECTORY_ENTRY_EXPORT.symbols

def getDebugDirectory(pe):
    return pe.DIRECTORY_ENTRY_DEBUG

def getDataDirectory(pe):
    return pe.OPTIONAL_HEADER.DATA_DIRECTORY

def getSectionData(pe):
    return pe.sections

def getAllDllNames(pe):
    return [x.dll for x in pe.DIRECTORY_ENTRY_IMPORT]

def getAllDllInstances(pe):
    return pe.DIRECTORY_ENTRY_IMPORT

def getDllInstance(pe, dllName):
    return [dll for dll in pe.DIRECTORY_ENTRY_IMPORT if dll.dll == dllName]

def getImports(dllInstance):
    return [apiInstance for apiInstance in dllInstance][0].imports

def getDllImportsInstances(dllInstance):
    return dllInstance.imports

def getDllStructInstance(dllInstance):
    return dllInstance.struct

def getDllStruct(dllInstance):
    return [structInstance for structInstance in dllInstance][0].struct
    
def getImportByName(apiName, dllInstance):
    apiInstances = getImports(dllInstance)
    return [api for api in apiInstances if apiInstances.name == apiName][0]

