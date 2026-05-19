#!/usr/bin/env python3

import sys
import os
import struct
from enum import Enum, auto, IntFlag
import argparse
from pathlib import Path

###############################################################################
# Constants and Struct Formats
###############################################################################

COFF_HEADER_FORMAT = "<HHLLLHH"  # 20 bytes
COFF_HEADER_SIZE   = struct.calcsize(COFF_HEADER_FORMAT)

SECTION_HEADER_FORMAT = "<8sLLLLLLHHL"  # 40 bytes
SECTION_HEADER_SIZE   = struct.calcsize(SECTION_HEADER_FORMAT)

SYMBOL_FORMAT = "<8sLHHBB"  # 18 bytes
SYMBOL_SIZE   = struct.calcsize(SYMBOL_FORMAT)

RELOCATION_FORMAT = "<LLH"  # 10 bytes
RELOCATION_SIZE   = struct.calcsize(RELOCATION_FORMAT)

# Machine constants
MACHINE_X86   = 0x14C   # IMAGE_FILE_MACHINE_I386
MACHINE_AMD64 = 0x8664  # IMAGE_FILE_MACHINE_AMD64

# Define relocation types
class ImageRelocationType(Enum):
    IMAGE_REL_I386_ABSOLUTE      =  0x0000
    IMAGE_REL_I386_DIR16         =  0x0001
    IMAGE_REL_I386_REL16         =  0x0002
    IMAGE_REL_I386_DIR32         =  0x0006
    IMAGE_REL_I386_DIR32NB       =  0x0007
    IMAGE_REL_I386_SEG12         =  0x0009
    IMAGE_REL_I386_SECTION       =  0x000A
    IMAGE_REL_I386_SECREL        =  0x000B
    IMAGE_REL_I386_TOKEN         =  0x000C
    IMAGE_REL_I386_SECREL7       =  0x000D
    IMAGE_REL_I386_REL32         =  0x0014

    IMAGE_REL_AMD64_ABSOLUTE     =  0x0000
    IMAGE_REL_AMD64_ADDR64       =  0x0001
    IMAGE_REL_AMD64_ADDR32       =  0x0002
    IMAGE_REL_AMD64_ADDR32NB     =  0x0003
    IMAGE_REL_AMD64_REL32        =  0x0004
    IMAGE_REL_AMD64_REL32_1      =  0x0005
    IMAGE_REL_AMD64_REL32_2      =  0x0006
    IMAGE_REL_AMD64_REL32_3      =  0x0007
    IMAGE_REL_AMD64_REL32_4      =  0x0008
    IMAGE_REL_AMD64_REL32_5      =  0x0009
    IMAGE_REL_AMD64_SECTION      =  0x000A
    IMAGE_REL_AMD64_SECREL       =  0x000B
    IMAGE_REL_AMD64_SECREL7      =  0x000C
    IMAGE_REL_AMD64_TOKEN        =  0x000D
    IMAGE_REL_AMD64_SREL32       =  0x000E
    IMAGE_REL_AMD64_PAIR         =  0x000F
    IMAGE_REL_AMD64_SSPAN32      =  0x0010
    IMAGE_REL_AMD64_EHANDLER     =  0x0011
    IMAGE_REL_AMD64_IMPORT_BR    =  0x0012
    IMAGE_REL_AMD64_IMPORT_CALL  =  0x0013
    IMAGE_REL_AMD64_CFG_BR       =  0x0014
    IMAGE_REL_AMD64_CFG_BR_REX   =  0x0015
    IMAGE_REL_AMD64_CFG_CALL     =  0x0016
    IMAGE_REL_AMD64_INDIR_BR     =  0x0017
    IMAGE_REL_AMD64_INDIR_BR_REX =  0x0018
    IMAGE_REL_AMD64_INDIR_CALL   =  0x0019
    IMAGE_REL_AMD64_INDIR_BR_SWITCHTABLE_FIRST = 0x0020
    IMAGE_REL_AMD64_INDIR_BR_SWITCHTABLE_LAST  = 0x002F 

list_of_implant_functions_cs = [
    "BeaconDataParse",
    "BeaconDataPtr",
    "BeaconDataInt",
    "BeaconDataShort",
    "BeaconDataLength",
    "BeaconDataExtract",
    "BeaconFormatAlloc",
    "BeaconFormatReset",
    "BeaconFormatAppend",
    "BeaconFormatPrintf",
    "BeaconFormatToString",
    "BeaconFormatFree",
    "BeaconFormatInt",
    "BeaconOutput",
    "BeaconPrintf",
    "BeaconUseToken",
    "BeaconRevertToken",
    "BeaconIsAdmin",
    "BeaconGetSpawnTo",
    "BeaconInjectProcess",
    "BeaconInjectTemporaryProcess",
    "BeaconSpawnTemporaryProcess",
    "BeaconCleanupProcess",
    "toWideChar",
    "BeaconInformation",
    "BeaconAddValue",
    "BeaconGetValue",
    "BeaconRemoveValue",
    "BeaconDataStoreGetItem",
    "BeaconDataStoreProtectItem",
    "BeaconDataStoreUnprotectItem",
    "BeaconDataStoreMaxEntries",
    "BeaconGetCustomUserData",
    "BeaconGetSyscallInformation",
    "BeaconVirtualAlloc",
    "BeaconVirtualAllocEx",
    "BeaconVirtualProtect",
    "BeaconVirtualProtectEx",
    "BeaconVirtualFree",
    "BeaconGetThreadContext",
    "BeaconSetThreadContext",
    "BeaconResumeThread",
    "BeaconOpenProcess",
    "BeaconOpenThread",
    "BeaconCloseHandle",
    "BeaconUnmapViewOfFile",
    "BeaconVirtualQuery",
    "BeaconDuplicateHandle",
    "BeaconReadProcessMemory",
    "BeaconWriteProcessMemory",
    "BeaconDisableBeaconGate",
    "BeaconEnableBeaconGate",
    "GetProcAddress",
    "GetModuleHandleA",
    "GetModuleHandleW",
    "LoadLibraryA",
    "LoadLibraryW",
    "FreeLibrary"
]

list_of_implant_functions_oc2 = [
    "BeaconDataParse",
    "BeaconDataInt",
    "BeaconDataShort",
    "BeaconDataLength",
    "BeaconDataExtract",
    "BeaconFormatAlloc",
    "BeaconFormatFree",
    "BeaconFormatReset",
    "BeaconFormatAppend",
    "BeaconFormatPrintf",
    "BeaconFormatToString",
    "BeaconFormatInt",
    "BeaconPrintf",
    "BeaconOutput",
    "BeaconUseToken",
    "BeaconRevertToken",
    "BeaconIsAdmin",
    "BeaconThrow",
    "BeaconInjectProcess",
    "GetProcAddress",
    "GetModuleHandleA",
    "GetModuleHandleW",
    "LoadLibraryA",
    "LoadLibraryW",
    "FreeLibrary"
]

list_of_implant_functions_ci = [
    "BeaconDataParse",
    "BeaconDataPtr",
    "BeaconDataInt",
    "BeaconDataShort",
    "BeaconDataLength",
    "BeaconDataExtract",
    "BeaconFormatAlloc",
    "BeaconFormatReset",
    "BeaconFormatAppend",
    "BeaconFormatPrintf",
    "BeaconFormatToString",
    "BeaconFormatFree",
    "BeaconFormatInt",
    "BeaconOutput",
    "BeaconPrintf",
    "GetProcAddress",
    "GetModuleHandleA",
    "LoadLibraryA",
    "FreeLibrary"
]


###############################################################################
# Classes Representing COFF Structures
###############################################################################

class COFFFileHeader:
    """
    Represents the 20-byte COFF File Header.
    """
    __slots__ = (
        "machine", "number_of_sections", "time_date_stamp",
        "pointer_to_symbol_table", "number_of_symbols",
        "size_of_optional_header", "characteristics",
    )

    def __init__(self, machine, number_of_sections, time_date_stamp,
                 pointer_to_symbol_table, number_of_symbols,
                 size_of_optional_header, characteristics):
        self.machine = machine
        self.number_of_sections = number_of_sections
        self.time_date_stamp = time_date_stamp
        self.pointer_to_symbol_table = pointer_to_symbol_table
        self.number_of_symbols = number_of_symbols
        self.size_of_optional_header = size_of_optional_header
        self.characteristics = characteristics

    @classmethod
    def from_file(cls, f):
        data = f.read(COFF_HEADER_SIZE)
        if len(data) < COFF_HEADER_SIZE:
            raise ValueError("File too small to contain a valid COFF header.")

        (
            machine,
            number_of_sections,
            time_date_stamp,
            pointer_to_symbol_table,
            number_of_symbols,
            size_of_opt_header,
            characteristics
        ) = struct.unpack(COFF_HEADER_FORMAT, data)

        return cls(
            machine,
            number_of_sections,
            time_date_stamp,
            pointer_to_symbol_table,
            number_of_symbols,
            size_of_opt_header,
            characteristics
        )

class COFFSectionHeader:
    """
    Represents a 40-byte COFF Section Header.
    """
    __slots__ = (
        "name", "virtual_size", "virtual_address", "size_of_raw_data",
        "pointer_to_raw_data", "pointer_to_relocations", "pointer_to_line_numbers",
        "number_of_relocations", "number_of_line_numbers", "characteristics",
    )

    def __init__(self, name, virtual_size, virtual_address, size_of_raw_data,
                 pointer_to_raw_data, pointer_to_relocations, pointer_to_line_numbers,
                 number_of_relocations, number_of_line_numbers, characteristics):
        self.name = name
        self.virtual_size = virtual_size
        self.virtual_address = virtual_address
        self.size_of_raw_data = size_of_raw_data
        self.pointer_to_raw_data = pointer_to_raw_data
        self.pointer_to_relocations = pointer_to_relocations
        self.pointer_to_line_numbers = pointer_to_line_numbers
        self.number_of_relocations = number_of_relocations
        self.number_of_line_numbers = number_of_line_numbers
        self.characteristics = characteristics

    @classmethod
    def from_file(cls, f):
        data = f.read(SECTION_HEADER_SIZE)
        if len(data) < SECTION_HEADER_SIZE:
            raise ValueError("File ended while reading section header.")

        (
            name_bytes,
            virtual_size,
            virtual_address,
            size_of_raw_data,
            ptr_raw_data,
            ptr_relocs,
            ptr_linenums,
            num_relocs,
            num_linenums,
            characteristics
        ) = struct.unpack(SECTION_HEADER_FORMAT, data)

        # decode section name (null-terminated within 8 bytes)
        name = name_bytes.split(b'\x00', 1)[0].decode(errors='ignore')

        return cls(
            name,
            virtual_size,
            virtual_address,
            size_of_raw_data,
            ptr_raw_data,
            ptr_relocs,
            ptr_linenums,
            num_relocs,
            num_linenums,
            characteristics
        )

class COFFSymbol:
    """
    Represents an 18-byte COFF Symbol Table entry.
    """
    __slots__ = (
        "name_raw", "value", "section_number", "type_", "storage_class",
        "number_of_aux_symbols"
    )

    def __init__(self, name_raw, value, section_number, type_, storage_class, number_of_aux_symbols):
        self.name_raw = name_raw
        self.value = value
        self.section_number = section_number
        self.type_ = type_
        self.storage_class = storage_class
        self.number_of_aux_symbols = number_of_aux_symbols

    @classmethod
    def from_file(cls, f):
        data = f.read(SYMBOL_SIZE)
        if len(data) < SYMBOL_SIZE:
            raise ValueError("Unexpected end of file while reading symbol.")

        (name_bytes, value, section_number, type_, storage_class, num_aux) = \
            struct.unpack(SYMBOL_FORMAT, data)

        return cls(
            name_raw=name_bytes,
            value=value,
            section_number=section_number,
            type_=type_,
            storage_class=storage_class,
            number_of_aux_symbols=num_aux
        )

class COFFRelocation:
    """
    Represents a 10-byte COFF Relocation entry.
    """
    __slots__ = ("virtual_address", "symbol_table_index", "type_")

    def __init__(self, virtual_address, symbol_table_index, type_):
        self.virtual_address = virtual_address
        self.symbol_table_index = symbol_table_index
        self.type_ = type_

    @classmethod
    def from_file(cls, f):
        data = f.read(RELOCATION_SIZE)
        if len(data) < RELOCATION_SIZE:
            raise ValueError("Unexpected end of file while reading relocation.")

        virt_addr, sym_idx, typ = struct.unpack(RELOCATION_FORMAT, data)
        return cls(virt_addr, sym_idx, typ)

###############################################################################
# Main COFF Object Container
###############################################################################

class COFFObject:
    """
    Collects a parsed COFF object file:
      - file_header (COFFFileHeader)
      - section_headers (list[COFFSectionHeader])
      - symbols (list[COFFSymbol])
      - relocations (dict[int -> list[COFFRelocation]]) indexed by section index
      - raw string table
    Provides a .lint() method to do basic checks.
    """

    def __init__(self):
        self.file_header = None
        self.section_headers = []
        self.symbols = []
        self.relocations = {}  # section_index -> list of relocations
        self.string_table = b''

    @classmethod
    def from_file(cls, path):
        obj = cls()
        with open(path, "rb") as f:
            # 1) Parse COFF header
            obj.file_header = COFFFileHeader.from_file(f)

            # 2) Skip optional header if present
            sz_opt = obj.file_header.size_of_optional_header
            if sz_opt > 0:
                f.seek(sz_opt, os.SEEK_CUR)

            # 3) Parse section headers
            for _ in range(obj.file_header.number_of_sections):
                sec = COFFSectionHeader.from_file(f)
                obj.section_headers.append(sec)

            # 4) Parse symbols and string table
            obj._parse_symbols_and_strings(f)

        # 5) Read relocations from each section in a second pass
        with open(path, "rb") as f:
            for i, sec in enumerate(obj.section_headers):
                rels = obj._read_relocations_for_section(f, sec)
                obj.relocations[i] = rels

        return obj

    def _parse_symbols_and_strings(self, f):
        """
        Read the symbol table (18 bytes each, plus any auxiliary records),
        then read the string table if present.
        """
        hdr = self.file_header
        if hdr.pointer_to_symbol_table == 0 or hdr.number_of_symbols == 0:
            return  # no symbols

        # Seek to the start of the symbol table
        f.seek(hdr.pointer_to_symbol_table, os.SEEK_SET)
        symbol_count = hdr.number_of_symbols

        i = 0
        while i < symbol_count:
            sym = COFFSymbol.from_file(f)
            self.symbols.append(sym)

            # If the symbol has auxiliary entries, skip them
            if sym.number_of_aux_symbols > 0:
                skip_count = sym.number_of_aux_symbols * SYMBOL_SIZE
                f.seek(skip_count, os.SEEK_CUR)
                i += sym.number_of_aux_symbols
                self.symbols.extend([None] * sym.number_of_aux_symbols)

            i += 1

        # Next 4 bytes should be the string table size
        size_data = f.read(4)
        if len(size_data) == 4:
            string_table_size = struct.unpack("<L", size_data)[0]
            if string_table_size > 4:
                remaining = string_table_size - 4
                self.string_table = f.read(remaining)
            else:
                self.string_table = b''

    def _read_relocations_for_section(self, f, section):
        """
        Reads relocations for a given section.
        """
        relocs = []
        if section.pointer_to_relocations == 0 or section.number_of_relocations == 0:
            return relocs

        f.seek(section.pointer_to_relocations, os.SEEK_SET)
        for _ in range(section.number_of_relocations):
            rel = COFFRelocation.from_file(f)
            relocs.append(rel)
        return relocs

    def get_symbol_name(self, sym: COFFSymbol) -> str:
        """
        Extracts the symbol name from the raw bytes.
        If the first 4 bytes are zero, the last 4 are an offset into the string table.
        Otherwise, it is an inline name (null-terminated).
        """
        raw = sym.name_raw
        # check if first four bytes are zero
        if raw[:4] == b'\x00\x00\x00\x00':
            offset = struct.unpack("<L", raw[4:8])[0]
            # typical approach: offset - 4 from the start of self.string_table
            real_offset = offset - 4
            if real_offset < 0 or real_offset >= len(self.string_table):
                return "<invalid-offset>"
            # read until null
            sub = self.string_table[real_offset:]
            null_pos = sub.find(b'\x00')
            return sub[:null_pos].decode(errors='ignore') if null_pos != -1 else sub.decode(errors='ignore')
        else:
            # inline name
            null_pos = raw.find(b'\x00')
            return raw[:null_pos].decode(errors='ignore') if null_pos != -1 else raw.decode(errors='ignore')

    def is_64bit(self) -> bool:
        return self.file_header.machine == MACHINE_AMD64

    def lint(self):
        """Perform basic lint checks and print results."""
        hdr = self.file_header
        machine = hdr.machine

        # Print header info
        log_message(LogLevel.INFO, "=== COFF File Header ===")
        log_message(LogLevel.INFO, f" Machine:             0x{machine:04X}")
        log_message(LogLevel.INFO, f" NumberOfSections:    {hdr.number_of_sections}")
        log_message(LogLevel.INFO, f" TimeDateStamp:       0x{hdr.time_date_stamp:08X}")
        log_message(LogLevel.INFO, f" PointerToSymbolTable:0x{hdr.pointer_to_symbol_table:08X}")
        log_message(LogLevel.INFO, f" NumberOfSymbols:     {hdr.number_of_symbols}")
        log_message(LogLevel.INFO, f" SizeOfOptionalHeader:{hdr.size_of_optional_header}")
        log_message(LogLevel.INFO, f" Characteristics:     0x{hdr.characteristics:04X}")

        if machine == MACHINE_X86:
            log_message(LogLevel.INFO, " -> x86 (32-bit) COFF object.n")
        elif machine == MACHINE_AMD64:
            log_message(LogLevel.INFO, " -> AMD64 (x64) COFF object.\n")
        else:
            log_message(LogLevel.ERROR, " -> Unknown or non-standard machine type.\n")
            sys.exit(1)

        # Check sections
        log_message(LogLevel.INFO, "=== Sections ===")

        for i, sec in enumerate(self.section_headers):
            log_message(LogLevel.INFO, f" Section[{i}]: {sec.name}")
            log_message(LogLevel.INFO, f"   PointerToRelocations: 0x{sec.pointer_to_relocations:08X}")
            log_message(LogLevel.INFO, f"   NumberOfRelocations:  {sec.number_of_relocations}")
            log_message(LogLevel.INFO, f"   Characteristics:      0x{sec.characteristics:08X}")
            log_message(LogLevel.INFO, f"   VirtualSize:          0x{sec.virtual_size:08X}")
            log_message(LogLevel.INFO, f"   SizeOfRawData:        0x{sec.size_of_raw_data:08X}")

            if sec.name == ".bss" and (sec.size_of_raw_data > 0 or sec.virtual_size > 0) and loader_type not in (LoaderType.CS, LoaderType.OC2, LoaderType.CI):
                log_message(LogLevel.WARN, f"Section '{sec.name}' is present! Not all loaders support uninitialized data in a BOF.")
            elif sec.name == ".rdata" and sec.size_of_raw_data > 0 and loader_type not in (LoaderType.CS, LoaderType.OC2, LoaderType.CI):
                log_message(LogLevel.WARN, f"Section '{sec.name}' is present! Not all loaders support read-only/const data in a BOF.")
                
            #elif sec.name == ".pdata" and sec.size_of_raw_data > 0 and loader_type not in (LoaderType.CS, LoaderType.OC2):
            #    log_message(LogLevel.WARN, f"Section '{sec.name}' is present! This may indicate that your BOF is using exception handling, which is not supported.")

            log_message(LogLevel.INFO, "")

        # Symbols
        log_message(LogLevel.INFO, "=== Symbols ===")

        allowed_entry_names = {
            LoaderType.CS: { "go", "sleep_mask", "_go", "_sleep_mask" },
            LoaderType.OC2: { "go", "_go" },
            LoaderType.CI: {"go", "_go"},
        }

        allowed_entry_names[LoaderType.ANY] = allowed_entry_names[LoaderType.CS] | allowed_entry_names[LoaderType.OC2] | allowed_entry_names[LoaderType.CI]

        found_entry = False

        for i, sym in enumerate(self.symbols):
            if sym is None:
                continue # skip aux symbols
            sym_name = self.get_symbol_name(sym)

            log_message(LogLevel.INFO, f" [{i}] Name='{sym_name}' Value=0x{sym.value:08X} "
                  f"Section={sym.section_number} StorageClass={sym.storage_class}")
            
            if sym_name in allowed_entry_names[loader_type] and sym.section_number > 0:
                found_entry = True

            if "@" in sym_name:
                sym_name = sym_name.split("@", 1)[0] 

            if sym_name.startswith("__imp_"):
                sym_without_prefix = sym_name[6:]  # remove __imp_
                if not self.is_64bit():
                    if sym_without_prefix[0] == "_":
                        sym_without_prefix = sym_without_prefix[1:]

                if "$" in sym_without_prefix: # DFR
                    # split in exact two parts, not more
                    import_lib, import_func = sym_without_prefix.split("$", 1)
                    if "@" in import_func:
                        import_func = import_func.split("@", 1)[0]
                    import_func = import_func.strip("$")

                    log_message(LogLevel.INFO, f"Imported symbol '{sym_without_prefix}' from library '{import_lib}' and function '{import_func}'")
                else:
                    if loader_type == LoaderType.CS:
                        if sym_without_prefix not in list_of_implant_functions_cs:
                            log_message(LogLevel.ERROR, f"Imported symbol '{sym_without_prefix}' is not a recognized implant function.", LogDestination.CS)
                    elif loader_type == LoaderType.OC2:
                        if sym_without_prefix not in list_of_implant_functions_oc2:
                            log_message(LogLevel.ERROR, f"Imported symbol '{sym_without_prefix}' is not a recognized implant function.", LogDestination.OC2)
                    elif loader_type == LoaderType.CI:
                        if sym_without_prefix not in list_of_implant_functions_ci:
                            log_message(LogLevel.ERROR, f"Imported symbol '{sym_without_prefix}' is not a recognized implant function.", LogDestination.CI)
                    else:
                        if sym_without_prefix not in (list_of_implant_functions_cs + list_of_implant_functions_oc2 + list_of_implant_functions_ci):
                            log_message(LogLevel.ERROR, f"Imported symbol '{sym_without_prefix}' is not a recognized implant function.")
            else:
                if sym.section_number == 0:
                    unhandled = True

                    if unhandled and sym_name in ["___chkstk_ms", "__chkstk"]:
                        if loader_type != LoaderType.OC2:
                            log_message(LogLevel.ERROR, f"Symbol '{sym_name}' is a stack check function. You may have a stack variable that is too large.")
                        unhandled = False

                    if unhandled and sym_name in ["__stack_chk_fail", "__security_init_cookie"] or "security_check_cookie" in sym_name:
                        log_message(LogLevel.ERROR, f"Symbol '{sym_name}' is a stack check function. Disable stack protections.")
                        unhandled = False

                    if unhandled and sym_name in ["__C_specific_handler", "__cxa_begin_catch"] or "except_handler" in sym_name or "CxxFrameHandler" in sym_name:
                        log_message(LogLevel.WARN, f"Symbol '{sym_name}' is an exception handling function. This is not supported.")
                        unhandled = False

                    if unhandled and sym_name in ["memset", "memmove", "memcpy"]:
                        if loader_type == LoaderType.OC2: 
                            # OC2 shims these functions in the loader
                            unhandled = False

                    if unhandled:
                        log_message(LogLevel.ERROR, f"Symbol '{sym_name}' is an undefined symbol.")

        log_message(LogLevel.INFO, "")

        if not found_entry:
            entry_names = ', '.join(f"'{name}'" for name in allowed_entry_names[loader_type])
            log_message(LogLevel.ERROR, f"No {entry_names} entry point found in object file (required for BOF)")

        # Relocations
        log_message(LogLevel.INFO, "=== Relocations ===")
        for i, sec in enumerate(self.section_headers):
            rels = self.relocations.get(i, [])
            if rels:
                log_message(LogLevel.INFO, f" Section[{i}] '{sec.name}' has {len(rels)} relocation(s):")
                for r in rels:
                    # Symbol reference name
                    sym_name = "<invalid-symbol>"
                    if r.symbol_table_index < len(self.symbols):
                        sym_name = self.get_symbol_name(self.symbols[r.symbol_table_index])

                    try:
                        r_type = ImageRelocationType(r.type_)
                        r_type_str = r_type.name
                    except ValueError:
                        r_type_str = f"0x{r.type_:04X}"

                    # Map relocation type to a name
                    if self.is_64bit():
                        # Check for allowed relocation types
                        allowed_reloc_types = {
                            ImageRelocationType.IMAGE_REL_AMD64_ADDR64, 
                            ImageRelocationType.IMAGE_REL_AMD64_ADDR32NB, 
                            ImageRelocationType.IMAGE_REL_AMD64_REL32, 
                            ImageRelocationType.IMAGE_REL_AMD64_REL32_1,
                            ImageRelocationType.IMAGE_REL_AMD64_REL32_2,
                            ImageRelocationType.IMAGE_REL_AMD64_REL32_3,
                            ImageRelocationType.IMAGE_REL_AMD64_REL32_4,
                            ImageRelocationType.IMAGE_REL_AMD64_REL32_5
                        }
                        if r_type not in allowed_reloc_types:
                            log_message(LogLevel.WARN, f"Warning: Unexpected relocation type {r_type_str} at VA=0x{r.virtual_address:08X}")
                    else:
                        # Check for allowed relocation types
                        allowed_reloc_types = {
                            ImageRelocationType.IMAGE_REL_I386_DIR32, 
                            ImageRelocationType.IMAGE_REL_I386_REL32
                        }
                        if r_type not in allowed_reloc_types:
                            log_message(LogLevel.WARN, f"Warning: Unexpected relocation type {r_type_str} at VA=0x{r.virtual_address:08X}")


                    log_message(LogLevel.INFO, f"   VA=0x{r.virtual_address:08X}, "
                          f"SymIdx={r.symbol_table_index} ({sym_name}), "
                          f"Type={r_type_str}")
                log_message(LogLevel.INFO, "")

###############################################################################
# Command-line Entry Point
###############################################################################

class LogLevel(Enum):
    INFO = auto()
    WARN = auto()
    ERROR = auto()

class LogDestination(IntFlag):
    NONE = 0
    CS = auto()    # Cobalt Strike BOFs
    OC2 = auto()   # OC2 BOFs
    CI = auto()    # Core Impact BOFs
    ALL = CS | OC2 | CI  # All BOF types

class LogFormat(Enum):
    DEFAULT = "default" # Default format
    VS = "vs"           # Visual Studio

class LoaderType(Enum):
    ANY = "any"   # Any loader
    CS = "cs"     # Cobalt Strike
    OC2 = "oc2"   # OC2
    CI = "ci"     # Core Impact

loader_type = LoaderType.ANY
verbose_logging = False
has_errors = False
enable_colors = True
log_format = LogFormat.DEFAULT
input_file = ""

def log_message(level: LogLevel, message: str, dest: LogDestination = LogDestination.ALL):
    if not verbose_logging and level == LogLevel.INFO:
        return
    
    # Skip messages not meant for current loader
    if dest != LogDestination.ALL:
        if loader_type == LoaderType.CS and not (dest & LogDestination.CS):
            return
        if loader_type == LoaderType.OC2 and not (dest & LogDestination.OC2):
            return
        if loader_type == LoaderType.CI and not (dest & LogDestination.CI):
            return

    if level == LogLevel.ERROR:
        global has_errors
        has_errors = True

    format = {
        LogFormat.DEFAULT: log_format_default,
        LogFormat.VS: log_format_vs,
    }

    global log_format
    print(format[log_format](level, message, dest))

def log_format_default(level: LogLevel, message: str, dest: LogDestination):
    # ANSI color codes
    COLORS = {
        LogLevel.INFO: "",      # default
        LogLevel.WARN: "\033[93m",  # yellow
        LogLevel.ERROR: "\033[91m",  # red
    }

    global enable_colors
    RESET = "\033[0m" if enable_colors else ""
    COLOR = COLORS[level] if enable_colors else ""
    
    prefix = {
        LogLevel.INFO: "INFO",
        LogLevel.WARN: "WARN",
        LogLevel.ERROR: "ERROR"
    }

    destinations = format_destinations(dest)
    if dest == LogDestination.ALL:
        return f"{COLOR}[{prefix[level]}] {message}{RESET}"
    else:
        return f"{COLOR}[{prefix[level]}] {message}{RESET} [{destinations}]"

def log_format_vs(level: LogLevel, message: str, dest: LogDestination):
    global input_file
    bof_name = Path(input_file).name

    prefix = {
        LogLevel.INFO: "",
        LogLevel.WARN: "warning",
        LogLevel.ERROR: "error"
    }

    destinations = f" [{format_destinations(dest)}]" if dest != LogDestination.ALL else ""
    return f"{bof_name}: {prefix[level]} BOFLINT: {message}{destinations}"

def format_destinations(dest: LogDestination):
    # append the log destinations to a string, formatted like this [CS|OC2], properly checking it as an intflag, also properly expanding ALL to CS|OC2
    return "|".join([d.name for d in LogDestination if d & dest and d != LogDestination.ALL])

def is_valid_bof(filepath: str) -> bool:
    """Quick check if file is a valid BOF by checking machine type."""
    try:
        with open(filepath, 'rb') as f:
            machine_data = f.read(2)
            if len(machine_data) < 2:
                return False
            
            machine = struct.unpack("<H", machine_data)[0]
            return machine in (MACHINE_AMD64, MACHINE_X86)
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description='BOF Linter - Validates COFF object files')
    parser.add_argument('file', help='Path to COFF object file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show INFO messages')
    parser.add_argument('--loader', choices=['cs', 'oc2', 'ci', 'any'], default='any',
                       help='BOF loader type (cs=Cobalt Strike, oc2=OC2, ci=Core Impact, any=Any)')
    parser.add_argument('--nocolor', action='store_true', help='Disable color output')
    parser.add_argument('--logformat', choices=['default', 'vs'], default='default',
                       help='Output format (default=Normal output, vs=Visual Studio diagnostic)')
    
    args = parser.parse_args()
    global verbose_logging, loader_type, enable_colors, log_format, input_file
    verbose_logging = args.verbose
    loader_type = LoaderType(args.loader)
    enable_colors = not args.nocolor
    log_format = LogFormat(args.logformat)
    input_file = args.file

    if not os.path.isfile(args.file):
        log_message(LogLevel.ERROR, "File does not exist")
        sys.exit(1)

    if not is_valid_bof(args.file):
        log_message(LogLevel.ERROR, "Not a valid BOF COFF file (or unsupported machine type)")
        sys.exit(1)

    coff = COFFObject.from_file(args.file)
    coff.lint()

    if has_errors:
        sys.exit(1)

if __name__ == "__main__":
    main()