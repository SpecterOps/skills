#ifndef BUILTINS_WINNT_H
#define BUILTINS_WINNT_H

#include <wintypes.h>
#include <limits.h>

#define ANYSIZE_ARRAY 1

typedef long NTSTATUS;
typedef ULONG LCID;

#define NT_SUCCESS(status) ((NTSTATUS)(status) >= 0)
#define NtCurrentProcess() ((HANDLE)(LONG_PTR)-1)
#define IMAGE_DOS_SIGNATURE 0x5A4D
#define IMAGE_NT_SIGNATURE 0x00004550

typedef struct _IMAGE_DOS_HEADER {
    WORD e_magic;
    WORD e_cblp;
    WORD e_cp;
    WORD e_crlc;
    WORD e_cparhdr;
    WORD e_minalloc;
    WORD e_maxalloc;
    WORD e_ss;
    WORD e_sp;
    WORD e_csum;
    WORD e_ip;
    WORD e_cs;
    WORD e_lfarlc;
    WORD e_ovno;
    WORD e_res[4];
    WORD e_oemid;
    WORD e_oeminfo;
    WORD e_res2[10];
    LONG e_lfanew;
} IMAGE_DOS_HEADER,*PIMAGE_DOS_HEADER;

typedef struct _IMAGE_FILE_HEADER {
    WORD Machine;
    WORD NumberOfSections;
    DWORD TimeDateStamp;
    DWORD PointerToSymbolTable;
    DWORD NumberOfSymbols;
    WORD SizeOfOptionalHeader;
    WORD Characteristics;
} IMAGE_FILE_HEADER,*PIMAGE_FILE_HEADER;

#define IMAGE_SIZEOF_FILE_HEADER 20

#define IMAGE_FILE_RELOCS_STRIPPED 0x0001
#define IMAGE_FILE_EXECUTABLE_IMAGE 0x0002
#define IMAGE_FILE_LINE_NUMS_STRIPPED 0x0004
#define IMAGE_FILE_LOCAL_SYMS_STRIPPED 0x0008
#define IMAGE_FILE_AGGRESIVE_WS_TRIM 0x0010
#define IMAGE_FILE_LARGE_ADDRESS_AWARE 0x0020
#define IMAGE_FILE_BYTES_REVERSED_LO 0x0080
#define IMAGE_FILE_32BIT_MACHINE 0x0100
#define IMAGE_FILE_DEBUG_STRIPPED 0x0200
#define IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP 0x0400
#define IMAGE_FILE_NET_RUN_FROM_SWAP 0x0800
#define IMAGE_FILE_SYSTEM 0x1000
#define IMAGE_FILE_DLL 0x2000
#define IMAGE_FILE_UP_SYSTEM_ONLY 0x4000
#define IMAGE_FILE_BYTES_REVERSED_HI 0x8000

#define IMAGE_FILE_MACHINE_UNKNOWN 0
#define IMAGE_FILE_MACHINE_I386 0x014c
#define IMAGE_FILE_MACHINE_R3000 0x0162
#define IMAGE_FILE_MACHINE_R4000 0x0166
#define IMAGE_FILE_MACHINE_R10000 0x0168
#define IMAGE_FILE_MACHINE_WCEMIPSV2 0x0169
#define IMAGE_FILE_MACHINE_ALPHA 0x0184
#define IMAGE_FILE_MACHINE_SH3 0x01a2
#define IMAGE_FILE_MACHINE_SH3DSP 0x01a3
#define IMAGE_FILE_MACHINE_SH3E 0x01a4
#define IMAGE_FILE_MACHINE_SH4 0x01a6
#define IMAGE_FILE_MACHINE_SH5 0x01a8
#define IMAGE_FILE_MACHINE_ARM 0x01c0
#define IMAGE_FILE_MACHINE_ARMV7 0x01c4
#define IMAGE_FILE_MACHINE_ARMNT 0x01c4
#define IMAGE_FILE_MACHINE_ARM64 0xaa64
#define IMAGE_FILE_MACHINE_THUMB 0x01c2
#define IMAGE_FILE_MACHINE_AM33 0x01d3
#define IMAGE_FILE_MACHINE_POWERPC 0x01F0
#define IMAGE_FILE_MACHINE_POWERPCFP 0x01f1
#define IMAGE_FILE_MACHINE_IA64 0x0200
#define IMAGE_FILE_MACHINE_MIPS16 0x0266
#define IMAGE_FILE_MACHINE_ALPHA64 0x0284
#define IMAGE_FILE_MACHINE_MIPSFPU 0x0366
#define IMAGE_FILE_MACHINE_MIPSFPU16 0x0466
#define IMAGE_FILE_MACHINE_AXP64 IMAGE_FILE_MACHINE_ALPHA64
#define IMAGE_FILE_MACHINE_TRICORE 0x0520
#define IMAGE_FILE_MACHINE_CEF 0x0CEF
#define IMAGE_FILE_MACHINE_EBC 0x0EBC
#define IMAGE_FILE_MACHINE_AMD64 0x8664
#define IMAGE_FILE_MACHINE_M32R 0x9041
#define IMAGE_FILE_MACHINE_CEE 0xc0ee

typedef struct _IMAGE_DATA_DIRECTORY {
    DWORD VirtualAddress;
    DWORD Size;
} IMAGE_DATA_DIRECTORY,*PIMAGE_DATA_DIRECTORY;

#define IMAGE_NUMBEROF_DIRECTORY_ENTRIES 16

typedef struct _IMAGE_OPTIONAL_HEADER {
    WORD Magic;
    BYTE MajorLinkerVersion;
    BYTE MinorLinkerVersion;
    DWORD SizeOfCode;
    DWORD SizeOfInitializedData;
    DWORD SizeOfUninitializedData;
    DWORD AddressOfEntryPoint;
    DWORD BaseOfCode;
    DWORD BaseOfData;
    DWORD ImageBase;
    DWORD SectionAlignment;
    DWORD FileAlignment;
    WORD MajorOperatingSystemVersion;
    WORD MinorOperatingSystemVersion;
    WORD MajorImageVersion;
    WORD MinorImageVersion;
    WORD MajorSubsystemVersion;
    WORD MinorSubsystemVersion;
    DWORD Win32VersionValue;
    DWORD SizeOfImage;
    DWORD SizeOfHeaders;
    DWORD CheckSum;
    WORD Subsystem;
    WORD DllCharacteristics;
    DWORD SizeOfStackReserve;
    DWORD SizeOfStackCommit;
    DWORD SizeOfHeapReserve;
    DWORD SizeOfHeapCommit;
    DWORD LoaderFlags;
    DWORD NumberOfRvaAndSizes;
    IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES];
} IMAGE_OPTIONAL_HEADER32,*PIMAGE_OPTIONAL_HEADER32;

typedef struct _IMAGE_OPTIONAL_HEADER64 {
    WORD Magic;
    BYTE MajorLinkerVersion;
    BYTE MinorLinkerVersion;
    DWORD SizeOfCode;
    DWORD SizeOfInitializedData;
    DWORD SizeOfUninitializedData;
    DWORD AddressOfEntryPoint;
    DWORD BaseOfCode;
    ULONGLONG ImageBase;
    DWORD SectionAlignment;
    DWORD FileAlignment;
    WORD MajorOperatingSystemVersion;
    WORD MinorOperatingSystemVersion;
    WORD MajorImageVersion;
    WORD MinorImageVersion;
    WORD MajorSubsystemVersion;
    WORD MinorSubsystemVersion;
    DWORD Win32VersionValue;
    DWORD SizeOfImage;
    DWORD SizeOfHeaders;
    DWORD CheckSum;
    WORD Subsystem;
    WORD DllCharacteristics;
    ULONGLONG SizeOfStackReserve;
    ULONGLONG SizeOfStackCommit;
    ULONGLONG SizeOfHeapReserve;
    ULONGLONG SizeOfHeapCommit;
    DWORD LoaderFlags;
    DWORD NumberOfRvaAndSizes;
    IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES];
} IMAGE_OPTIONAL_HEADER64,*PIMAGE_OPTIONAL_HEADER64;

#define IMAGE_SIZEOF_NT_OPTIONAL32_HEADER 224
#define IMAGE_SIZEOF_NT_OPTIONAL64_HEADER 240

#define IMAGE_NT_OPTIONAL_HDR32_MAGIC 0x10b
#define IMAGE_NT_OPTIONAL_HDR64_MAGIC 0x20b

#ifndef _WIN32 
typedef IMAGE_OPTIONAL_HEADER64 IMAGE_OPTIONAL_HEADER;
typedef PIMAGE_OPTIONAL_HEADER64 PIMAGE_OPTIONAL_HEADER;
#define IMAGE_SIZEOF_NT_OPTIONAL_HEADER IMAGE_SIZEOF_NT_OPTIONAL64_HEADER
#define IMAGE_NT_OPTIONAL_HDR_MAGIC IMAGE_NT_OPTIONAL_HDR64_MAGIC
#else 
typedef IMAGE_OPTIONAL_HEADER32 IMAGE_OPTIONAL_HEADER;
typedef PIMAGE_OPTIONAL_HEADER32 PIMAGE_OPTIONAL_HEADER;
#define IMAGE_SIZEOF_NT_OPTIONAL_HEADER IMAGE_SIZEOF_NT_OPTIONAL32_HEADER
#define IMAGE_NT_OPTIONAL_HDR_MAGIC IMAGE_NT_OPTIONAL_HDR32_MAGIC
#endif

typedef struct _IMAGE_NT_HEADERS64 {
    DWORD Signature;
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER64 OptionalHeader;
} IMAGE_NT_HEADERS64,*PIMAGE_NT_HEADERS64;

typedef struct _IMAGE_NT_HEADERS {
    DWORD Signature;
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER32 OptionalHeader;
} IMAGE_NT_HEADERS32,*PIMAGE_NT_HEADERS32;

#ifndef _WIN32
typedef IMAGE_NT_HEADERS64 IMAGE_NT_HEADERS;
typedef PIMAGE_NT_HEADERS64 PIMAGE_NT_HEADERS;
#else
typedef IMAGE_NT_HEADERS32 IMAGE_NT_HEADERS;
typedef PIMAGE_NT_HEADERS32 PIMAGE_NT_HEADERS;
#endif

#define IMAGE_SUBSYSTEM_UNKNOWN 0
#define IMAGE_SUBSYSTEM_NATIVE 1
#define IMAGE_SUBSYSTEM_WINDOWS_GUI 2
#define IMAGE_SUBSYSTEM_WINDOWS_CUI 3
#define IMAGE_SUBSYSTEM_OS2_CUI 5
#define IMAGE_SUBSYSTEM_POSIX_CUI 7
#define IMAGE_SUBSYSTEM_NATIVE_WINDOWS 8
#define IMAGE_SUBSYSTEM_WINDOWS_CE_GUI 9
#define IMAGE_SUBSYSTEM_EFI_APPLICATION 10
#define IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER 11
#define IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER 12
#define IMAGE_SUBSYSTEM_EFI_ROM 13
#define IMAGE_SUBSYSTEM_XBOX 14
#define IMAGE_SUBSYSTEM_WINDOWS_BOOT_APPLICATION 16

#define IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA 0x0020
#define IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE 0x0040
#define IMAGE_DLLCHARACTERISTICS_FORCE_INTEGRITY 0x0080
#define IMAGE_DLLCHARACTERISTICS_NX_COMPAT 0x0100
#define IMAGE_DLLCHARACTERISTICS_NO_ISOLATION 0x0200
#define IMAGE_DLLCHARACTERISTICS_NO_SEH 0x0400
#define IMAGE_DLLCHARACTERISTICS_NO_BIND 0x0800
#define IMAGE_DLLCHARACTERISTICS_APPCONTAINER 0x1000
#define IMAGE_DLLCHARACTERISTICS_WDM_DRIVER 0x2000
#define IMAGE_DLLCHARACTERISTICS_GUARD_CF 0x4000
#define IMAGE_DLLCHARACTERISTICS_TERMINAL_SERVER_AWARE 0x8000

#define IMAGE_DIRECTORY_ENTRY_EXPORT 0
#define IMAGE_DIRECTORY_ENTRY_IMPORT 1
#define IMAGE_DIRECTORY_ENTRY_RESOURCE 2
#define IMAGE_DIRECTORY_ENTRY_EXCEPTION 3
#define IMAGE_DIRECTORY_ENTRY_SECURITY 4
#define IMAGE_DIRECTORY_ENTRY_BASERELOC 5
#define IMAGE_DIRECTORY_ENTRY_DEBUG 6
#define IMAGE_DIRECTORY_ENTRY_ARCHITECTURE 7
#define IMAGE_DIRECTORY_ENTRY_GLOBALPTR 8
#define IMAGE_DIRECTORY_ENTRY_TLS 9
#define IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG 10
#define IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT 11
#define IMAGE_DIRECTORY_ENTRY_IAT 12
#define IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT 13
#define IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR 14

#define IMAGE_SIZEOF_SHORT_NAME 8

typedef struct _IMAGE_SECTION_HEADER {
    BYTE Name[IMAGE_SIZEOF_SHORT_NAME];
    union {
        DWORD PhysicalAddress;
        DWORD VirtualSize;
    } Misc;
    DWORD VirtualAddress;
    DWORD SizeOfRawData;
    DWORD PointerToRawData;
    DWORD PointerToRelocations;
    DWORD PointerToLinenumbers;
    WORD NumberOfRelocations;
    WORD NumberOfLinenumbers;
    DWORD Characteristics;
} IMAGE_SECTION_HEADER,*PIMAGE_SECTION_HEADER;

#define IMAGE_SIZEOF_SECTION_HEADER 40

#define IMAGE_SCN_TYPE_NO_PAD 0x00000008

#define IMAGE_SCN_CNT_CODE 0x00000020
#define IMAGE_SCN_CNT_INITIALIZED_DATA 0x00000040
#define IMAGE_SCN_CNT_UNINITIALIZED_DATA 0x00000080
#define IMAGE_SCN_LNK_OTHER 0x00000100
#define IMAGE_SCN_LNK_INFO 0x00000200
#define IMAGE_SCN_LNK_REMOVE 0x00000800
#define IMAGE_SCN_LNK_COMDAT 0x00001000
#define IMAGE_SCN_NO_DEFER_SPEC_EXC 0x00004000
#define IMAGE_SCN_GPREL 0x00008000
#define IMAGE_SCN_MEM_FARDATA 0x00008000
#define IMAGE_SCN_MEM_PURGEABLE 0x00020000
#define IMAGE_SCN_MEM_16BIT 0x00020000
#define IMAGE_SCN_MEM_LOCKED 0x00040000
#define IMAGE_SCN_MEM_PRELOAD 0x00080000

#define IMAGE_SCN_ALIGN_1BYTES 0x00100000
#define IMAGE_SCN_ALIGN_2BYTES 0x00200000
#define IMAGE_SCN_ALIGN_4BYTES 0x00300000
#define IMAGE_SCN_ALIGN_8BYTES 0x00400000
#define IMAGE_SCN_ALIGN_16BYTES 0x00500000
#define IMAGE_SCN_ALIGN_32BYTES 0x00600000
#define IMAGE_SCN_ALIGN_64BYTES 0x00700000
#define IMAGE_SCN_ALIGN_128BYTES 0x00800000
#define IMAGE_SCN_ALIGN_256BYTES 0x00900000
#define IMAGE_SCN_ALIGN_512BYTES 0x00A00000
#define IMAGE_SCN_ALIGN_1024BYTES 0x00B00000
#define IMAGE_SCN_ALIGN_2048BYTES 0x00C00000
#define IMAGE_SCN_ALIGN_4096BYTES 0x00D00000
#define IMAGE_SCN_ALIGN_8192BYTES 0x00E00000

#define IMAGE_SCN_ALIGN_MASK 0x00F00000

#define IMAGE_SCN_LNK_NRELOC_OVFL 0x01000000
#define IMAGE_SCN_MEM_DISCARDABLE 0x02000000
#define IMAGE_SCN_MEM_NOT_CACHED 0x04000000
#define IMAGE_SCN_MEM_NOT_PAGED 0x08000000
#define IMAGE_SCN_MEM_SHARED 0x10000000
#define IMAGE_SCN_MEM_EXECUTE 0x20000000
#define IMAGE_SCN_MEM_READ 0x40000000
#define IMAGE_SCN_MEM_WRITE 0x80000000

#define IMAGE_SCN_SCALE_INDEX 0x00000001

typedef struct _IMAGE_RELOCATION {
    union {
        DWORD VirtualAddress;
        DWORD RelocCount;
    };
    DWORD SymbolTableIndex;
    WORD Type;
} IMAGE_RELOCATION;
typedef IMAGE_RELOCATION *PIMAGE_RELOCATION;

#define IMAGE_SIZEOF_RELOCATION 10
typedef struct _IMAGE_BASE_RELOCATION {
    DWORD VirtualAddress;
    DWORD SizeOfBlock;
} IMAGE_BASE_RELOCATION;
typedef IMAGE_BASE_RELOCATION *PIMAGE_BASE_RELOCATION;

#define IMAGE_SIZEOF_BASE_RELOCATION 8

#define IMAGE_REL_BASED_ABSOLUTE 0
#define IMAGE_REL_BASED_HIGH 1
#define IMAGE_REL_BASED_LOW 2
#define IMAGE_REL_BASED_HIGHLOW 3
#define IMAGE_REL_BASED_HIGHADJ 4
#define IMAGE_REL_BASED_MIPS_JMPADDR 5
#define IMAGE_REL_BASED_ARM_MOV32 5
#define IMAGE_REL_BASED_THUMB_MOV32 7
#define IMAGE_REL_BASED_MIPS_JMPADDR16 9
#define IMAGE_REL_BASED_IA64_IMM64 9
#define IMAGE_REL_BASED_DIR64 10

typedef struct _IMAGE_EXPORT_DIRECTORY {
    DWORD Characteristics;
    DWORD TimeDateStamp;
    WORD MajorVersion;
    WORD MinorVersion;
    DWORD Name;
    DWORD Base;
    DWORD NumberOfFunctions;
    DWORD NumberOfNames;
    DWORD AddressOfFunctions;
    DWORD AddressOfNames;
    DWORD AddressOfNameOrdinals;
} IMAGE_EXPORT_DIRECTORY,*PIMAGE_EXPORT_DIRECTORY;

typedef struct _IMAGE_IMPORT_BY_NAME {
    WORD Hint;
    CHAR Name[1];
} IMAGE_IMPORT_BY_NAME,*PIMAGE_IMPORT_BY_NAME;

typedef struct _IMAGE_THUNK_DATA64 {
    union {
        ULONGLONG ForwarderString;
        ULONGLONG Function;
        ULONGLONG Ordinal;
        ULONGLONG AddressOfData;
    } u1;
} IMAGE_THUNK_DATA64;
typedef IMAGE_THUNK_DATA64 *PIMAGE_THUNK_DATA64;

typedef struct _IMAGE_THUNK_DATA32 {
    union {
        DWORD ForwarderString;
        DWORD Function;
        DWORD Ordinal;
        DWORD AddressOfData;
    } u1;
} IMAGE_THUNK_DATA32;
typedef IMAGE_THUNK_DATA32 *PIMAGE_THUNK_DATA32;

#define IMAGE_ORDINAL_FLAG64 0x8000000000000000ull
#define IMAGE_ORDINAL_FLAG32 0x80000000
#define IMAGE_ORDINAL64(Ordinal) (Ordinal & 0xffffull)
#define IMAGE_ORDINAL32(Ordinal) (Ordinal & 0xffff)
#define IMAGE_SNAP_BY_ORDINAL64(Ordinal) ((Ordinal & IMAGE_ORDINAL_FLAG64)!=0)
#define IMAGE_SNAP_BY_ORDINAL32(Ordinal) ((Ordinal & IMAGE_ORDINAL_FLAG32)!=0)

typedef struct _IMAGE_TLS_DIRECTORY64 {
    ULONGLONG StartAddressOfRawData;
    ULONGLONG EndAddressOfRawData;
    ULONGLONG AddressOfIndex;
    ULONGLONG AddressOfCallBacks;
    DWORD SizeOfZeroFill;
    DWORD Characteristics;
} IMAGE_TLS_DIRECTORY64;
typedef IMAGE_TLS_DIRECTORY64 *PIMAGE_TLS_DIRECTORY64;

typedef struct _IMAGE_TLS_DIRECTORY32 {
    DWORD StartAddressOfRawData;
    DWORD EndAddressOfRawData;
    DWORD AddressOfIndex;
    DWORD AddressOfCallBacks;
    DWORD SizeOfZeroFill;
    DWORD Characteristics;
} IMAGE_TLS_DIRECTORY32;
typedef IMAGE_TLS_DIRECTORY32 *PIMAGE_TLS_DIRECTORY32;

#ifndef _WIN32
#define IMAGE_ORDINAL_FLAG IMAGE_ORDINAL_FLAG64
#define IMAGE_ORDINAL(Ordinal) IMAGE_ORDINAL64(Ordinal)
typedef IMAGE_THUNK_DATA64 IMAGE_THUNK_DATA;
typedef PIMAGE_THUNK_DATA64 PIMAGE_THUNK_DATA;
#define IMAGE_SNAP_BY_ORDINAL(Ordinal) IMAGE_SNAP_BY_ORDINAL64(Ordinal)
typedef IMAGE_TLS_DIRECTORY64 IMAGE_TLS_DIRECTORY;
typedef PIMAGE_TLS_DIRECTORY64 PIMAGE_TLS_DIRECTORY;
#else
#define IMAGE_ORDINAL_FLAG IMAGE_ORDINAL_FLAG32
#define IMAGE_ORDINAL(Ordinal) IMAGE_ORDINAL32(Ordinal)
typedef IMAGE_THUNK_DATA32 IMAGE_THUNK_DATA;
typedef PIMAGE_THUNK_DATA32 PIMAGE_THUNK_DATA;
#define IMAGE_SNAP_BY_ORDINAL(Ordinal) IMAGE_SNAP_BY_ORDINAL32(Ordinal)
typedef IMAGE_TLS_DIRECTORY32 IMAGE_TLS_DIRECTORY;
typedef PIMAGE_TLS_DIRECTORY32 PIMAGE_TLS_DIRECTORY;
#endif

typedef struct _IMAGE_IMPORT_DESCRIPTOR {
    union {
        DWORD Characteristics;
        DWORD OriginalFirstThunk;
    };
    DWORD TimeDateStamp;

    DWORD ForwarderChain;
    DWORD Name;
    DWORD FirstThunk;
} IMAGE_IMPORT_DESCRIPTOR;
typedef IMAGE_IMPORT_DESCRIPTOR *PIMAGE_IMPORT_DESCRIPTOR;

#ifndef _LIST_ENTRY_DEFINED
#define _LIST_ENTRY_DEFINED

  typedef struct _LIST_ENTRY {
    struct _LIST_ENTRY *Flink;
    struct _LIST_ENTRY *Blink;
  } LIST_ENTRY,*PLIST_ENTRY;

  typedef struct _SINGLE_LIST_ENTRY {
    struct _SINGLE_LIST_ENTRY *Next;
  } SINGLE_LIST_ENTRY,*PSINGLE_LIST_ENTRY;

  typedef struct LIST_ENTRY32 {
    DWORD Flink;
    DWORD Blink;
  } LIST_ENTRY32;
  typedef LIST_ENTRY32 *PLIST_ENTRY32;

  typedef struct LIST_ENTRY64 {
    ULONGLONG Flink;
    ULONGLONG Blink;
  } LIST_ENTRY64;
  typedef LIST_ENTRY64 *PLIST_ENTRY64;

#endif

typedef struct _OSVERSIONINFOA {
    DWORD dwOSVersionInfoSize;
    DWORD dwMajorVersion;
    DWORD dwMinorVersion;
    DWORD dwBuildNumber;
    DWORD dwPlatformId;
    CHAR szCSDVersion[128];
} OSVERSIONINFOA,*POSVERSIONINFOA,*LPOSVERSIONINFOA;

typedef struct _OSVERSIONINFOW {
    DWORD dwOSVersionInfoSize;
    DWORD dwMajorVersion;
    DWORD dwMinorVersion;
    DWORD dwBuildNumber;
    DWORD dwPlatformId;
    WCHAR szCSDVersion[128];
} OSVERSIONINFOW,*POSVERSIONINFOW,*LPOSVERSIONINFOW,RTL_OSVERSIONINFOW,*PRTL_OSVERSIONINFOW;

#ifdef UNICODE
typedef OSVERSIONINFOW OSVERSIONINFO;
typedef POSVERSIONINFOW POSVERSIONINFO;
typedef LPOSVERSIONINFOW LPOSVERSIONINFO;
#else
typedef OSVERSIONINFOA OSVERSIONINFO;
typedef POSVERSIONINFOA POSVERSIONINFO;
typedef LPOSVERSIONINFOA LPOSVERSIONINFO;
#endif

typedef struct _OSVERSIONINFOEXA {
    DWORD dwOSVersionInfoSize;
    DWORD dwMajorVersion;
    DWORD dwMinorVersion;
    DWORD dwBuildNumber;
    DWORD dwPlatformId;
    CHAR szCSDVersion[128];
    WORD wServicePackMajor;
    WORD wServicePackMinor;
    WORD wSuiteMask;
    BYTE wProductType;
    BYTE wReserved;
} OSVERSIONINFOEXA,*POSVERSIONINFOEXA,*LPOSVERSIONINFOEXA;

typedef struct _OSVERSIONINFOEXW {
    DWORD dwOSVersionInfoSize;
    DWORD dwMajorVersion;
    DWORD dwMinorVersion;
    DWORD dwBuildNumber;
    DWORD dwPlatformId;
    WCHAR szCSDVersion[128];
    WORD wServicePackMajor;
    WORD wServicePackMinor;
    WORD wSuiteMask;
    BYTE wProductType;
    BYTE wReserved;
} OSVERSIONINFOEXW,*POSVERSIONINFOEXW,*LPOSVERSIONINFOEXW,RTL_OSVERSIONINFOEXW,*PRTL_OSVERSIONINFOEXW;

#ifdef UNICODE
typedef OSVERSIONINFOEXW OSVERSIONINFOEX;
typedef POSVERSIONINFOEXW POSVERSIONINFOEX;
typedef LPOSVERSIONINFOEXW LPOSVERSIONINFOEX;
#else
typedef OSVERSIONINFOEXA OSVERSIONINFOEX;
typedef POSVERSIONINFOEXA POSVERSIONINFOEX;
typedef LPOSVERSIONINFOEXA LPOSVERSIONINFOEX;
#endif

typedef struct _STARTUPINFOA {
    DWORD cb;
    LPSTR lpReserved;
    LPSTR lpDesktop;
    LPSTR lpTitle;
    DWORD dwX;
    DWORD dwY;
    DWORD dwXSize;
    DWORD dwYSize;
    DWORD dwXCountChars;
    DWORD dwYCountChars;
    DWORD dwFillAttribute;
    DWORD dwFlags;
    WORD wShowWindow;
    WORD cbReserved2;
    LPBYTE lpReserved2;
    HANDLE hStdInput;
    HANDLE hStdOutput;
    HANDLE hStdError;
} STARTUPINFOA, *LPSTARTUPINFOA;

typedef struct _STARTUPINFOW {
    DWORD cb;
    LPWSTR lpReserved;
    LPWSTR lpDesktop;
    LPWSTR lpTitle;
    DWORD dwX;
    DWORD dwY;
    DWORD dwXSize;
    DWORD dwYSize;
    DWORD dwXCountChars;
    DWORD dwYCountChars;
    DWORD dwFillAttribute;
    DWORD dwFlags;
    WORD wShowWindow;
    WORD cbReserved2;
    LPBYTE lpReserved2;
    HANDLE hStdInput;
    HANDLE hStdOutput;
    HANDLE hStdError;
} STARTUPINFOW, *LPSTARTUPINFOW;

#ifdef UNICODE
typedef STARTUPINFOW STARTUPINFO;
#else
typedef STARTUPINFOA STARTUPINFO;
#endif

typedef struct _STARTUPINFOEXA {
    STARTUPINFOA StartupInfo;
    PVOID lpAttributeList;
} STARTUPINFOEXA,*LPSTARTUPINFOEXA;

typedef struct _STARTUPINFOEXW {
    STARTUPINFOW StartupInfo;
    PVOID lpAttributeList;
} STARTUPINFOEXW,*LPSTARTUPINFOEXW;

#ifdef UNICODE
typedef STARTUPINFOEXW STARTUPINFOEX;
#else
typedef STARTUPINFOEXA STARTUPINFOEX;
#endif

typedef struct _PROCESS_INFORMATION {
    HANDLE hProcess;
    HANDLE hThread;
    DWORD dwProcessId;
    DWORD dwThreadId;
} PROCESS_INFORMATION, *PPROCESS_INFORMATION, *LPPROCESS_INFORMATION;

typedef struct _SYSTEM_INFO {
    union {
        DWORD dwOemId;
        struct {
            WORD wProcessorArchitecture;
            WORD wReserved;
	};
    };
    DWORD dwPageSize;
    LPVOID lpMinimumApplicationAddress;
    LPVOID lpMaximumApplicationAddress;
    DWORD_PTR dwActiveProcessorMask;
    DWORD dwNumberOfProcessors;
    DWORD dwProcessorType;
    DWORD dwAllocationGranularity;
    WORD wProcessorLevel;
    WORD wProcessorRevision;
} SYSTEM_INFO, *LPSYSTEM_INFO;

typedef struct _MEMORYSTATUSEX {
    DWORD dwLength;
    DWORD dwMemoryLoad;
    DWORDLONG ullTotalPhys;
    DWORDLONG ullAvailPhys;
    DWORDLONG ullTotalPageFile;
    DWORDLONG ullAvailPageFile;
    DWORDLONG ullTotalVirtual;
    DWORDLONG ullAvailVirtual;
    DWORDLONG ullAvailExtendedVirtual;
} MEMORYSTATUSEX,*LPMEMORYSTATUSEX;

typedef struct _RTL_CRITICAL_SECTION {
    PVOID DebugInfo;
    LONG LockCount;
    LONG RecursionCount;
    HANDLE OwningThread;
    HANDLE LockSemaphore;
    ULONG_PTR SpinCount;
} RTL_CRITICAL_SECTION,*PRTL_CRITICAL_SECTION;
typedef RTL_CRITICAL_SECTION CRITICAL_SECTION;
typedef PRTL_CRITICAL_SECTION PCRITICAL_SECTION;
typedef PRTL_CRITICAL_SECTION LPCRITICAL_SECTION;

typedef enum _PROCESSINFOCLASS {
    ProcessBasicInformation,
    ProcessQuotaLimits,
    ProcessIoCounters,
    ProcessVmCounters,
    ProcessTimes,
    ProcessBasePriority,
    ProcessRaisePriority,
    ProcessDebugPort,
    ProcessExceptionPort,
    ProcessAccessToken,
    ProcessLdtInformation,
    ProcessLdtSize,
    ProcessDefaultHardErrorMode,
    ProcessIoPortHandlers,
    ProcessPooledUsageAndLimits,
    ProcessWorkingSetWatch,
    ProcessUserModeIOPL,
    ProcessEnableAlignmentFaultFixup,
    ProcessPriorityClass,
    ProcessWx86Information,
    ProcessHandleCount,
    ProcessAffinityMask,
    ProcessPriorityBoost,
    ProcessDeviceMap,
    ProcessSessionInformation,
    ProcessForegroundInformation,
    ProcessWow64Information,
    ProcessImageFileName,
    ProcessLUIDDeviceMapsEnabled,
    ProcessBreakOnTermination,
    ProcessDebugObjectHandle,
    ProcessDebugFlags,
    ProcessHandleTracing,
    ProcessIoPriority,
    ProcessExecuteFlags,
    ProcessTlsInformation,
    ProcessCookie,
    ProcessImageInformation,
    ProcessCycleTime,
    ProcessPagePriority,
    ProcessInstrumentationCallback,
    ProcessThreadStackAllocation,
    ProcessWorkingSetWatchEx,
    ProcessImageFileNameWin32,
    ProcessImageFileMapping,
    ProcessAffinityUpdateMode,
    ProcessMemoryAllocationMode,
    ProcessGroupInformation,
    ProcessTokenVirtualizationEnabled,
    ProcessConsoleHostProcess,
    ProcessWindowInformation,
    MaxProcessInfoClass
} PROCESSINFOCLASS;

typedef enum _THREADINFOCLASS {
    ThreadBasicInformation,
    ThreadTimes,
    ThreadPriority,
    ThreadBasePriority,
    ThreadAffinityMask,
    ThreadImpersonationToken,
    ThreadDescriptorTableEntry,
    ThreadEnableAlignmentFaultFixup,
    ThreadEventPair,
    ThreadQuerySetWin32StartAddress,
    ThreadZeroTlsCell,
    ThreadPerformanceCount,
    ThreadAmILastThread,
    ThreadIdealProcessor,
    ThreadPriorityBoost,
    ThreadSetTlsArrayAddress,
    ThreadIsIoPending,
    ThreadHideFromDebugger
} THREADINFOCLASS;

typedef enum _FILE_INFORMATION_CLASS {
    FileDirectoryInformation = 1,
    FileFullDirectoryInformation,
    FileBothDirectoryInformation,
    FileBasicInformation,
    FileStandardInformation,
    FileInternalInformation,
    FileEaInformation,
    FileAccessInformation,
    FileNameInformation,
    FileRenameInformation,
    FileLinkInformation,
    FileNamesInformation,
    FileDispositionInformation,
    FilePositionInformation,
    FileFullEaInformation,
    FileModeInformation,
    FileAlignmentInformation,
    FileAllInformation,
    FileAllocationInformation,
    FileEndOfFileInformation,
    FileAlternateNameInformation,
    FileStreamInformation,
    FilePipeInformation,
    FilePipeLocalInformation,
    FilePipeRemoteInformation,
    FileMailslotQueryInformation,
    FileMailslotSetInformation,
    FileCompressionInformation,
    FileObjectIdInformation,
    FileCompletionInformation,
    FileMoveClusterInformation,
    FileQuotaInformation,
    FileReparsePointInformation,
    FileNetworkOpenInformation,
    FileAttributeTagInformation,
    FileTrackingInformation,
    FileIdBothDirectoryInformation,
    FileIdFullDirectoryInformation,
    FileValidDataLengthInformation,
    FileShortNameInformation = 40,
    FileSfioReserveInformation = 44,
    FileSfioVolumeInformation = 45,
    FileHardLinkInformation = 46,
    FileNormalizedNameInformation = 48,
    FileIdGlobalTxDirectoryInformation = 50,
    FileStandardLinkInformation = 54,
    FileMaximumInformation
} FILE_INFORMATION_CLASS, *PFILE_INFORMATION_CLASS;

typedef enum _SYSTEM_INFORMATION_CLASS {
    SystemBasicInformation = 0,
    SystemProcessorInformation = 1,
    SystemPerformanceInformation = 2,
    SystemTimeOfDayInformation = 3,
    SystemProcessInformation = 5,
    SystemProcessorPerformanceInformation = 8,
    SystemHandleInformation = 16,
    SystemPagefileInformation = 18,
    SystemInterruptInformation = 23,
    SystemExceptionInformation = 33,
    SystemRegistryQuotaInformation = 37,
    SystemLookasideInformation = 45
} SYSTEM_INFORMATION_CLASS;

typedef enum _OBJECT_INFORMATION_CLASS {
    ObjectBasicInformation,
    ObjectNameInformation,
    ObjectTypeInformation,
    ObjectAllInformation,
    ObjectDataInformation
} OBJECT_INFORMATION_CLASS, *POBJECT_INFORMATION_CLASS;

typedef enum _SECTION_INHERIT {
  ViewShare = 1,
  ViewUnmap = 2
} SECTION_INHERIT;

typedef enum _WAIT_TYPE
{
    WaitAll,
    WaitAny,
    WaitNotification,
    WaitDequeue,
    WaitDpc,
} WAIT_TYPE;

#define SIZE_OF_80387_REGISTERS 80
#define MAXIMUM_SUPPORTED_EXTENSION 512

#define THREAD_TERMINATE (0x0001)
#define THREAD_SUSPEND_RESUME (0x0002)
#define THREAD_GET_CONTEXT (0x0008)
#define THREAD_SET_CONTEXT (0x0010)
#define THREAD_SET_INFORMATION (0x0020)
#define THREAD_QUERY_INFORMATION (0x0040)
#define THREAD_SET_THREAD_TOKEN (0x0080)
#define THREAD_IMPERSONATE (0x0100)
#define THREAD_DIRECT_IMPERSONATION (0x0200)
#define THREAD_SET_LIMITED_INFORMATION (0x0400)
#define THREAD_QUERY_LIMITED_INFORMATION (0x0800)

#define WT_EXECUTEDEFAULT 0x00000000
#define WT_EXECUTEINIOTHREAD 0x00000001
#define WT_EXECUTEINUITHREAD 0x00000002
#define WT_EXECUTEINWAITTHREAD 0x00000004
#define WT_EXECUTEONLYONCE 0x00000008
#define WT_EXECUTEINTIMERTHREAD 0x00000020
#define WT_EXECUTELONGFUNCTION 0x00000010
#define WT_EXECUTEINPERSISTENTIOTHREAD 0x00000040
#define WT_EXECUTEINPERSISTENTTHREAD 0x00000080
#define WT_TRANSFER_IMPERSONATION 0x00000100

#define WT_SET_MAX_THREADPOOL_THREADS(Flags, Limit) ((Flags) |= (Limit) << 16)

#define WT_EXECUTEDELETEWAIT 0x00000008
#define WT_EXECUTEINLONGTHREAD 0x00000010

typedef struct _FLOATING_SAVE_AREA {
    DWORD ControlWord;
    DWORD StatusWord;
    DWORD TagWord;
    DWORD ErrorOffset;
    DWORD ErrorSelector;
    DWORD DataOffset;
    DWORD DataSelector;
    BYTE RegisterArea[SIZE_OF_80387_REGISTERS];
    DWORD Cr0NpxState;
} FLOATING_SAVE_AREA;

typedef FLOATING_SAVE_AREA *PFLOATING_SAVE_AREA;

typedef struct _CONTEXT {
    DWORD ContextFlags;
    DWORD Dr0;     
    DWORD Dr1;
    DWORD Dr2;
    DWORD Dr3;
    DWORD Dr6;
    DWORD Dr7;
    FLOATING_SAVE_AREA FloatSave;
    DWORD SegGs;
    DWORD SegFs;
    DWORD SegEs;
    DWORD SegDs;

    DWORD Edi;
    DWORD Esi;
    DWORD Ebx;
    DWORD Edx;
    DWORD Ecx;
    DWORD Eax;
    DWORD Ebp;
    DWORD Eip;
    DWORD SegCs;
    DWORD EFlags;
    DWORD Esp;
    DWORD SegSs;
    BYTE ExtendedRegisters[MAXIMUM_SUPPORTED_EXTENSION];
} CONTEXT;

typedef CONTEXT *PCONTEXT;

typedef struct _M128A {
    ULONGLONG Low;
    LONGLONG High;
} M128A,*PM128A;

typedef struct _XMM_SAVE_AREA32 {
    WORD ControlWord;
    WORD StatusWord;
    BYTE TagWord;
    BYTE Reserved1;
    WORD ErrorOpcode;
    DWORD ErrorOffset;
    WORD ErrorSelector;
    WORD Reserved2;
    DWORD DataOffset;
    WORD DataSelector;
    WORD Reserved3;
    DWORD MxCsr;
    DWORD MxCsr_Mask;
    M128A FloatRegisters[8];
    M128A XmmRegisters[16];
    BYTE Reserved4[96];
} XMM_SAVE_AREA32,*PXMM_SAVE_AREA32;

typedef struct _CONTEXT64 {
    DWORD64 P1Home;
    DWORD64 P2Home;
    DWORD64 P3Home;
    DWORD64 P4Home;
    DWORD64 P5Home;
    DWORD64 P6Home;
    DWORD ContextFlags;
    DWORD MxCsr;
    WORD SegCs;
    WORD SegDs;
    WORD SegEs;
    WORD SegFs;
    WORD SegGs;
    WORD SegSs;
    DWORD EFlags;
    DWORD64 Dr0;
    DWORD64 Dr1;
    DWORD64 Dr2;
    DWORD64 Dr3;
    DWORD64 Dr6;
    DWORD64 Dr7;
    DWORD64 Rax;
    DWORD64 Rcx;
    DWORD64 Rdx;
    DWORD64 Rbx;
    DWORD64 Rsp;
    DWORD64 Rbp;
    DWORD64 Rsi;
    DWORD64 Rdi;
    DWORD64 R8;
    DWORD64 R9;
    DWORD64 R10;
    DWORD64 R11;
    DWORD64 R12;
    DWORD64 R13;
    DWORD64 R14;
    DWORD64 R15;
    DWORD64 Rip;
    union {
      XMM_SAVE_AREA32 FltSave;
      XMM_SAVE_AREA32 FloatSave;
      struct {
        M128A Header[2];
        M128A Legacy[8];
        M128A Xmm0;
        M128A Xmm1;
        M128A Xmm2;
        M128A Xmm3;
        M128A Xmm4;
        M128A Xmm5;
        M128A Xmm6;
        M128A Xmm7;
        M128A Xmm8;
        M128A Xmm9;
        M128A Xmm10;
        M128A Xmm11;
        M128A Xmm12;
        M128A Xmm13;
        M128A Xmm14;
        M128A Xmm15;
      };
    };
    M128A VectorRegister[26];
    DWORD64 VectorControl;
    DWORD64 DebugControl;
    DWORD64 LastBranchToRip;
    DWORD64 LastBranchFromRip;
    DWORD64 LastExceptionToRip;
    DWORD64 LastExceptionFromRip;
} CONTEXT64,*PCONTEXT64;

typedef struct _CLIENT_ID
{
    HANDLE UniqueProcess;
    HANDLE UniqueThread;
} CLIENT_ID, *PCLIENT_ID;

typedef LONG KPRIORITY;

typedef struct _STRING {
    USHORT Length;
    USHORT MaximumLength;
    PCHAR Buffer;
} STRING;

#ifndef __STRING_DEFINED
#define __STRING_DEFINED
typedef STRING *PSTRING;
typedef STRING ANSI_STRING;
typedef PSTRING PANSI_STRING;
typedef PSTRING PCANSI_STRING;
#endif

#ifndef __UNICODE_STRING_DEFINED
#define __UNICODE_STRING_DEFINED
typedef struct _UNICODE_STRING
{
    USHORT Length;
    USHORT MaximumLength;
    PWCH Buffer;
} UNICODE_STRING, *PUNICODE_STRING;
#endif

typedef struct _PEB_LDR_DATA {
    BYTE Reserved1[8];
    PVOID Reserved2[3];
    LIST_ENTRY InMemoryOrderModuleList;
} PEB_LDR_DATA,*PPEB_LDR_DATA;
 
  typedef struct _LDR_DATA_TABLE_ENTRY {
    PVOID Reserved1[2];
    LIST_ENTRY InMemoryOrderLinks;
    PVOID Reserved2[2];
    PVOID DllBase;
    PVOID Reserved3[2];
    UNICODE_STRING FullDllName;
    BYTE Reserved4[8];
    PVOID Reserved5[3];
    union {
      ULONG CheckSum;
      PVOID Reserved6;
    };
    ULONG TimeDateStamp;
} LDR_DATA_TABLE_ENTRY,*PLDR_DATA_TABLE_ENTRY;

typedef struct _RTL_USER_PROCESS_PARAMETERS {
    BYTE Reserved1[16];
    PVOID Reserved2[10];
    UNICODE_STRING ImagePathName;
    UNICODE_STRING CommandLine;
} RTL_USER_PROCESS_PARAMETERS,*PRTL_USER_PROCESS_PARAMETERS;
  
typedef struct _PEB {
    BYTE Reserved1[2];
    BYTE BeingDebugged;
    BYTE Reserved2[1];
    PVOID Reserved3[2];
    PPEB_LDR_DATA Ldr;
    PRTL_USER_PROCESS_PARAMETERS ProcessParameters;
    PVOID Reserved4[3];
    PVOID AtlThunkSListPtr;
    PVOID Reserved5;
    ULONG Reserved6;
    PVOID Reserved7;
    ULONG Reserved8;
    ULONG AtlThunkSListPtr32;
    PVOID Reserved9[45];
    BYTE Reserved10[96];
    PVOID PostProcessInitRoutine;
    BYTE Reserved11[128];
    PVOID Reserved12[1];
    ULONG SessionId;
} PEB,*PPEB;

typedef struct _TEB {
    PVOID Reserved1[12];
    PPEB ProcessEnvironmentBlock;
    PVOID Reserved2[399];
    BYTE Reserved3[1952];
    PVOID TlsSlots[64];
    BYTE Reserved4[8];
    PVOID Reserved5[26];
    PVOID ReservedForOle;
    PVOID Reserved6[4];
    PVOID TlsExpansionSlots;
} TEB;

typedef TEB *PTEB;

typedef struct _EXCEPTION_REGISTRATION_RECORD {
    union {
        struct _EXCEPTION_REGISTRATION_RECORD *Next;
        struct _EXCEPTION_REGISTRATION_RECORD *prev;
    };
    union {
        PVOID Handler;
        PVOID handler;
    };
} EXCEPTION_REGISTRATION_RECORD;

typedef EXCEPTION_REGISTRATION_RECORD *PEXCEPTION_REGISTRATION_RECORD;

typedef EXCEPTION_REGISTRATION_RECORD EXCEPTION_REGISTRATION;
typedef PEXCEPTION_REGISTRATION_RECORD PEXCEPTION_REGISTRATION;

#ifndef _NT_TIB_DEFINED
#define _NT_TIB_DEFINED
typedef struct _NT_TIB {
    EXCEPTION_REGISTRATION_RECORD *ExceptionList;
    PVOID StackBase;
    PVOID StackLimit;
    PVOID SubSystemTib;
    union {
        PVOID FiberData;
        DWORD Version;
    };
    PVOID ArbitraryUserPointer;
    struct _NT_TIB *Self;
} NT_TIB;
typedef NT_TIB *PNT_TIB;
#endif /* _NT_TIB_DEFINED */

typedef struct _NT_TIB32 {
    DWORD ExceptionList;
    DWORD StackBase;
    DWORD StackLimit;
    DWORD SubSystemTib;
    union {
        DWORD FiberData;
        DWORD Version;
    };
    DWORD ArbitraryUserPointer;
    DWORD Self;
} NT_TIB32,*PNT_TIB32;

typedef struct _NT_TIB64 {
    DWORD64 ExceptionList;
    DWORD64 StackBase;
    DWORD64 StackLimit;
    DWORD64 SubSystemTib;
    union {
        DWORD64 FiberData;
        DWORD Version;
    };
    DWORD64 ArbitraryUserPointer;
    DWORD64 Self;
} NT_TIB64,*PNT_TIB64;

typedef ULONG_PTR KAFFINITY;

typedef struct _PROCESS_BASIC_INFORMATION {
    NTSTATUS ExitStatus;
    PPEB PebBaseAddress;
    KAFFINITY AffinityMask;
    KPRIORITY BasePriority;
    ULONG_PTR UniqueProcessId;
    ULONG_PTR InheritedFromUniqueProcessId;
} PROCESS_BASIC_INFORMATION, *PPROCESS_BASIC_INFORMATION;

typedef struct _THREAD_BASIC_INFORMATION {
    NTSTATUS ExitStatus;
    PTEB TebBaseAddress;
    CLIENT_ID ClientId;
    KAFFINITY AffinityMask;
    KPRIORITY Priority;
    KPRIORITY BasePriority;
} THREAD_BASIC_INFORMATION, *PTHREAD_BASIC_INFORMATION;

typedef struct _SYSTEM_THREAD_INFORMATION {
    LARGE_INTEGER KernelTime;
    LARGE_INTEGER UserTime;
    LARGE_INTEGER CreateTime;
    ULONG WaitTime;
    PVOID StartAddress;
    CLIENT_ID ClientId;
    KPRIORITY Priority;
    LONG BasePriority;
    ULONG ContextSwitches;
    ULONG ThreadState;
    ULONG WaitReason;
 } SYSTEM_THREAD_INFORMATION, *PSYSTEM_THREAD_INFORMATION;

typedef struct _SYSTEM_PROCESS_INFORMATION {
    ULONG NextEntryOffset;
    ULONG NumberOfThreads;
    LARGE_INTEGER WorkingSetPrivateSize;
    ULONG HardFaultCount;
    ULONG NumberOfThreadsHighWatermark;
    ULONGLONG CycleTime;
    LARGE_INTEGER CreateTime;
    LARGE_INTEGER UserTime;
    LARGE_INTEGER KernelTime;
    UNICODE_STRING ImageName;
    KPRIORITY BasePriority;
    HANDLE UniqueProcessId;
    HANDLE InheritedFromUniqueProcessId;
    ULONG HandleCount;
    ULONG SessionId;
    ULONG_PTR UniqueProcessKey;
    SIZE_T PeakVirtualSize;
    SIZE_T VirtualSize;
    ULONG PageFaultCount;
    SIZE_T PeakWorkingSetSize;
    SIZE_T WorkingSetSize;
    SIZE_T QuotaPeakPagedPoolUsage;
    SIZE_T QuotaPagedPoolUsage;
    SIZE_T QuotaPeakNonPagedPoolUsage;
    SIZE_T QuotaNonPagedPoolUsage;
    SIZE_T PagefileUsage;
    SIZE_T PeakPagefileUsage;
    SIZE_T PrivatePageCount;
    LARGE_INTEGER ReadOperationCount;
    LARGE_INTEGER WriteOperationCount;
    LARGE_INTEGER OtherOperationCount;
    LARGE_INTEGER ReadTransferCount;
    LARGE_INTEGER WriteTransferCount;
    LARGE_INTEGER OtherTransferCount;
    SYSTEM_THREAD_INFORMATION Threads[1];
} SYSTEM_PROCESS_INFORMATION, *PSYSTEM_PROCESS_INFORMATION;

typedef struct _OBJECT_ATTRIBUTES {
    ULONG Length;
    HANDLE RootDirectory;
    PUNICODE_STRING ObjectName;
    ULONG Attributes;
    PVOID SecurityDescriptor;
    PVOID SecurityQualityOfService;
} OBJECT_ATTRIBUTES, *POBJECT_ATTRIBUTES;

void InitializeObjectAttributes(POBJECT_ATTRIBUTES p, PUNICODE_STRING n, ULONG a, HANDLE r, PVOID s) {
	p->Length = sizeof(OBJECT_ATTRIBUTES);
	p->RootDirectory = r;
	p->Attributes = a;
	p->ObjectName = n;
	p->SecurityDescriptor = s;
	p->SecurityQualityOfService = NULL;
}

/* Values for the Attributes member */
#define OBJ_INHERIT 0x00000002L
#define OBJ_PERMANENT 0x00000010L
#define OBJ_EXCLUSIVE 0x00000020L
#define OBJ_CASE_INSENSITIVE 0x00000040L
#define OBJ_OPENIF 0x00000080L
#define OBJ_OPENLINK 0x00000100L
#define OBJ_KERNEL_HANDLE 0x00000200L
#define OBJ_FORCE_ACCESS_CHECK 0x00000400L
#define OBJ_IGNORE_IMPERSONATED_DEVICEMAP 0x00000800L
#define OBJ_DONT_REPARSE 0x00001000L
#define OBJ_VALID_ATTRIBUTES 0x00001FF2L

typedef enum _MEMORY_INFORMATION_CLASS
{
    MemoryBasicInformation,                     // q: MEMORY_BASIC_INFORMATION
    MemoryWorkingSetInformation,                // q: MEMORY_WORKING_SET_INFORMATION
    MemoryMappedFilenameInformation,            // q: UNICODE_STRING
    MemoryRegionInformation,                    // q: MEMORY_REGION_INFORMATION/MEMORY_REGION_INFORMATION_EX
    MemoryWorkingSetExInformation,              // q: MEMORY_WORKING_SET_EX_INFORMATION // since VISTA
    MemorySharedCommitInformation,              // q: MEMORY_SHARED_COMMIT_INFORMATION // since WIN8
    MemoryImageInformation,                     // q: MEMORY_IMAGE_INFORMATION
    MemoryRegionInformationEx,                  // q: MEMORY_REGION_INFORMATION/MEMORY_REGION_INFORMATION_EX
    MemoryPrivilegedBasicInformation,           // q: MEMORY_BASIC_INFORMATION
    MemoryEnclaveImageInformation,              // q: MEMORY_ENCLAVE_IMAGE_INFORMATION // since REDSTONE3
    MemoryBasicInformationCapped,               // q: 10
    MemoryPhysicalContiguityInformation,        // q: MEMORY_PHYSICAL_CONTIGUITY_INFORMATION // since 20H1
    MemoryBadInformation,                       // q: MEMORY_BAD_INFORMATION // since WIN11
    MemoryBadInformationAllProcesses,           // qs: not implemented // since 22H1
    MemoryImageExtensionInformation,            // q: MEMORY_IMAGE_EXTENSION_INFORMATION // since 24H2
    MaxMemoryInfoClass
} MEMORY_INFORMATION_CLASS;

#ifndef _WIN32
typedef struct _MEMORY_BASIC_INFORMATION {
    PVOID BaseAddress;
    PVOID AllocationBase;
    DWORD AllocationProtect;
    WORD   PartitionId;
    SIZE_T RegionSize;
    DWORD State;
    DWORD Protect;
    DWORD Type;
} MEMORY_BASIC_INFORMATION, *PMEMORY_BASIC_INFORMATION;
#else
typedef struct _MEMORY_BASIC_INFORMATION {
    PVOID BaseAddress;
    PVOID AllocationBase;
    DWORD AllocationProtect;
    SIZE_T RegionSize;
    DWORD State;
    DWORD Protect;
    DWORD Type;
} MEMORY_BASIC_INFORMATION, *PMEMORY_BASIC_INFORMATION;
#endif

typedef struct _MEMORY_BASIC_INFORMATION32 {
    DWORD BaseAddress;
    DWORD AllocationBase;
    DWORD AllocationProtect;
    DWORD RegionSize;
    DWORD State;
    DWORD Protect;
    DWORD Type;
} MEMORY_BASIC_INFORMATION32, *PMEMORY_BASIC_INFORMATION32;

typedef struct _MEMORY_BASIC_INFORMATION64 {
    ULONGLONG BaseAddress;
    ULONGLONG AllocationBase;
    DWORD     AllocationProtect;
    DWORD     __alignment1;
    ULONGLONG RegionSize;
    DWORD     State;
    DWORD     Protect;
    DWORD     Type;
    DWORD     __alignment2;
} MEMORY_BASIC_INFORMATION64, *PMEMORY_BASIC_INFORMATION64;

typedef USHORT SECURITY_DESCRIPTOR_CONTROL,*PSECURITY_DESCRIPTOR_CONTROL;

/* minimal dependency types for lmaccess-derived definitions */
typedef PVOID PSID;
typedef DWORD NET_API_STATUS;
typedef DWORD_PTR *PDWORD_PTR;
typedef unsigned char BOOLEAN;

typedef struct _ACL {
    BYTE AclRevision;
    BYTE Sbz1;
    WORD AclSize;
    WORD AceCount;
    WORD Sbz2;
} ACL;
typedef ACL *PACL;

typedef struct _ACE_HEADER {
    BYTE AceType;
    BYTE AceFlags;
    WORD AceSize;
} ACE_HEADER;
typedef ACE_HEADER *PACE_HEADER;

typedef struct _SECURITY_DESCRIPTOR_RELATIVE {
  UCHAR Revision;
  UCHAR Sbz1;
  SECURITY_DESCRIPTOR_CONTROL Control;
  ULONG Owner;
  ULONG Group;
  ULONG Sacl;
  ULONG Dacl;
} SECURITY_DESCRIPTOR_RELATIVE, *PISECURITY_DESCRIPTOR_RELATIVE;

typedef struct _SECURITY_DESCRIPTOR {
  UCHAR Revision;
  UCHAR Sbz1;
  SECURITY_DESCRIPTOR_CONTROL Control;
  PSID Owner;
  PSID Group;
  PACL Sacl;
  PACL Dacl;
} SECURITY_DESCRIPTOR, *PISECURITY_DESCRIPTOR;

typedef enum _SID_NAME_USE {
    SidTypeUser = 1,
    SidTypeGroup,
    SidTypeDomain,
    SidTypeAlias,
    SidTypeWellKnownGroup,
    SidTypeDeletedAccount,
    SidTypeInvalid,
    SidTypeUnknown,
    SidTypeComputer,
    SidTypeLabel,
    SidTypeLogonSession
} SID_NAME_USE,*PSID_NAME_USE;

typedef struct _SID_AND_ATTRIBUTES {
    PSID Sid;
    DWORD Attributes;
} SID_AND_ATTRIBUTES,*PSID_AND_ATTRIBUTES;

typedef enum _SECURITY_LOGON_TYPE {
    UndefinedLogonType = 0,
    Interactive = 2,
    Network,
    Batch,
    Service,
    Proxy,
    Unlock,
    NetworkCleartext,
    NewCredentials,
    /* bvmc preprocessor doesn't support expression-style #if conditions.
     * Keep modern SDK values unconditionally with explicit numbering.
     */
    RemoteInteractive = 10,
    CachedInteractive = 11,
    CachedRemoteInteractive = 12,
    CachedUnlock = 13
} SECURITY_LOGON_TYPE, *PSECURITY_LOGON_TYPE;

typedef enum _TOKEN_TYPE {
    TokenPrimary = 1,TokenImpersonation
} TOKEN_TYPE;
typedef TOKEN_TYPE *PTOKEN_TYPE;

typedef enum _TOKEN_ELEVATION_TYPE {
    TokenElevationTypeDefault   = 1,
    TokenElevationTypeFull,
    TokenElevationTypeLimited
} TOKEN_ELEVATION_TYPE, *PTOKEN_ELEVATION_TYPE;

typedef enum _TOKEN_INFORMATION_CLASS {
    TokenUser = 1,
    TokenGroups,
    TokenPrivileges,
    TokenOwner,
    TokenPrimaryGroup,
    TokenDefaultDacl,
    TokenSource,
    TokenType,
    TokenImpersonationLevel,
    TokenStatistics,
    TokenRestrictedSids,
    TokenSessionId,
    TokenGroupsAndPrivileges,
    TokenSessionReference,
    TokenSandBoxInert,
    TokenAuditPolicy,
    TokenOrigin,
    TokenElevationType,
    TokenLinkedToken,
    TokenElevation,
    TokenHasRestrictions,
    TokenAccessInformation,
    TokenVirtualizationAllowed,
    TokenVirtualizationEnabled,
    TokenIntegrityLevel,
    TokenUIAccess,
    TokenMandatoryPolicy,
    TokenLogonSid,
    TokenIsAppContainer,
    TokenCapabilities,
    TokenAppContainerSid,
    TokenAppContainerNumber,
    TokenUserClaimAttributes,
    TokenDeviceClaimAttributes,
    TokenRestrictedUserClaimAttributes,
    TokenRestrictedDeviceClaimAttributes,
    TokenDeviceGroups,
    TokenRestrictedDeviceGroups,
    TokenSecurityAttributes,
    TokenIsRestricted,
    MaxTokenInfoClass
} TOKEN_INFORMATION_CLASS,*PTOKEN_INFORMATION_CLASS;

typedef struct _TOKEN_USER {
    SID_AND_ATTRIBUTES User;
} TOKEN_USER,*PTOKEN_USER;

typedef enum _SECURITY_IMPERSONATION_LEVEL {
    SecurityAnonymous,SecurityIdentification,SecurityImpersonation,SecurityDelegation
} SECURITY_IMPERSONATION_LEVEL,*PSECURITY_IMPERSONATION_LEVEL;

/* lmcons.h constants used by lmaccess structures/macros */
#ifndef ENCRYPTED_PWLEN
#define ENCRYPTED_PWLEN 16
#endif
#ifndef PWLEN
#define PWLEN 256
#endif
#ifndef PARMNUM_BASE_INFOLEVEL
#define PARMNUM_BASE_INFOLEVEL 1000
#endif

#ifndef BUILTINS_GUID_DEFINED
#define BUILTINS_GUID_DEFINED
typedef struct _GUID {
    DWORD Data1;
    WORD Data2;
    WORD Data3;
    BYTE Data4[8];
} GUID, *PGUID, *LPGUID;
#endif

#ifndef BUILTINS_LUID_DEFINED
#define BUILTINS_LUID_DEFINED
typedef struct _LUID {
    DWORD LowPart;
    LONG HighPart;
} LUID, *PLUID;
#endif

typedef struct _LUID_AND_ATTRIBUTES {
    LUID Luid;
    DWORD Attributes;
} LUID_AND_ATTRIBUTES,*PLUID_AND_ATTRIBUTES;

typedef struct _TOKEN_PRIVILEGES {
    DWORD PrivilegeCount;
    LUID_AND_ATTRIBUTES Privileges[ANYSIZE_ARRAY];
} TOKEN_PRIVILEGES,*PTOKEN_PRIVILEGES;

/* Data Structures - Tokens */
typedef struct _TOKEN_STATISTICS {
    LUID TokenId;
    LUID AuthenticationId;
    LARGE_INTEGER ExpirationTime;
    TOKEN_TYPE TokenType;
    SECURITY_IMPERSONATION_LEVEL ImpersonationLevel;
    DWORD DynamicCharged;
    DWORD DynamicAvailable;
    DWORD GroupCount;
    DWORD PrivilegeCount;
    LUID ModifiedId;
} TOKEN_STATISTICS,*PTOKEN_STATISTICS;

/* Data Structures - User */
typedef struct _USER_INFO_0 {
    LPWSTR usri0_name;
} USER_INFO_0, *PUSER_INFO_0, *LPUSER_INFO_0;

typedef struct _USER_INFO_1 {
    LPWSTR usri1_name;
    LPWSTR usri1_password;
    DWORD usri1_password_age;
    DWORD usri1_priv;
    LPWSTR usri1_home_dir;
    LPWSTR usri1_comment;
    DWORD usri1_flags;
    LPWSTR usri1_script_path;
} USER_INFO_1, *PUSER_INFO_1, *LPUSER_INFO_1;

typedef struct _USER_INFO_2 {
    LPWSTR usri2_name;
    LPWSTR usri2_password;
    DWORD usri2_password_age;
    DWORD usri2_priv;
    LPWSTR usri2_home_dir;
    LPWSTR usri2_comment;
    DWORD usri2_flags;
    LPWSTR usri2_script_path;
    DWORD usri2_auth_flags;
    LPWSTR usri2_full_name;
    LPWSTR usri2_usr_comment;
    LPWSTR usri2_parms;
    LPWSTR usri2_workstations;
    DWORD usri2_last_logon;
    DWORD usri2_last_logoff;
    DWORD usri2_acct_expires;
    DWORD usri2_max_storage;
    DWORD usri2_units_per_week;
    PBYTE usri2_logon_hours;
    DWORD usri2_bad_pw_count;
    DWORD usri2_num_logons;
    LPWSTR usri2_logon_server;
    DWORD usri2_country_code;
    DWORD usri2_code_page;
} USER_INFO_2, *PUSER_INFO_2, *LPUSER_INFO_2;

typedef struct _USER_INFO_3 {
    LPWSTR usri3_name;
    LPWSTR usri3_password;
    DWORD usri3_password_age;
    DWORD usri3_priv;
    LPWSTR usri3_home_dir;
    LPWSTR usri3_comment;
    DWORD usri3_flags;
    LPWSTR usri3_script_path;
    DWORD usri3_auth_flags;
    LPWSTR usri3_full_name;
    LPWSTR usri3_usr_comment;
    LPWSTR usri3_parms;
    LPWSTR usri3_workstations;
    DWORD usri3_last_logon;
    DWORD usri3_last_logoff;
    DWORD usri3_acct_expires;
    DWORD usri3_max_storage;
    DWORD usri3_units_per_week;
    PBYTE usri3_logon_hours;
    DWORD usri3_bad_pw_count;
    DWORD usri3_num_logons;
    LPWSTR usri3_logon_server;
    DWORD usri3_country_code;
    DWORD usri3_code_page;
    DWORD usri3_user_id;
    DWORD usri3_primary_group_id;
    LPWSTR usri3_profile;
    LPWSTR usri3_home_dir_drive;
    DWORD usri3_password_expired;
} USER_INFO_3, *PUSER_INFO_3, *LPUSER_INFO_3;

typedef struct _USER_INFO_4 {
    LPWSTR usri4_name;
    LPWSTR usri4_password;
    DWORD usri4_password_age;
    DWORD usri4_priv;
    LPWSTR usri4_home_dir;
    LPWSTR usri4_comment;
    DWORD usri4_flags;
    LPWSTR usri4_script_path;
    DWORD usri4_auth_flags;
    LPWSTR usri4_full_name;
    LPWSTR usri4_usr_comment;
    LPWSTR usri4_parms;
    LPWSTR usri4_workstations;
    DWORD usri4_last_logon;
    DWORD usri4_last_logoff;
    DWORD usri4_acct_expires;
    DWORD usri4_max_storage;
    DWORD usri4_units_per_week;
    PBYTE usri4_logon_hours;
    DWORD usri4_bad_pw_count;
    DWORD usri4_num_logons;
    LPWSTR usri4_logon_server;
    DWORD usri4_country_code;
    DWORD usri4_code_page;
    PSID usri4_user_sid;
    DWORD usri4_primary_group_id;
    LPWSTR usri4_profile;
    LPWSTR usri4_home_dir_drive;
    DWORD usri4_password_expired;
} USER_INFO_4, *PUSER_INFO_4, *LPUSER_INFO_4;

typedef struct _USER_INFO_10 {
    LPWSTR usri10_name;
    LPWSTR usri10_comment;
    LPWSTR usri10_usr_comment;
    LPWSTR usri10_full_name;
} USER_INFO_10, *PUSER_INFO_10, *LPUSER_INFO_10;

typedef struct _USER_INFO_11 {
    LPWSTR usri11_name;
    LPWSTR usri11_comment;
    LPWSTR usri11_usr_comment;
    LPWSTR usri11_full_name;
    DWORD usri11_priv;
    DWORD usri11_auth_flags;
    DWORD usri11_password_age;
    LPWSTR usri11_home_dir;
    LPWSTR usri11_parms;
    DWORD usri11_last_logon;
    DWORD usri11_last_logoff;
    DWORD usri11_bad_pw_count;
    DWORD usri11_num_logons;
    LPWSTR usri11_logon_server;
    DWORD usri11_country_code;
    LPWSTR usri11_workstations;
    DWORD usri11_max_storage;
    DWORD usri11_units_per_week;
    PBYTE usri11_logon_hours;
    DWORD usri11_code_page;
} USER_INFO_11, *PUSER_INFO_11, *LPUSER_INFO_11;

typedef struct _USER_INFO_20 {
    LPWSTR usri20_name;
    LPWSTR usri20_full_name;
    LPWSTR usri20_comment;
    DWORD usri20_flags;
    DWORD usri20_user_id;
} USER_INFO_20, *PUSER_INFO_20, *LPUSER_INFO_20;

typedef struct _USER_INFO_21 {
    BYTE usri21_password[ENCRYPTED_PWLEN];
} USER_INFO_21, *PUSER_INFO_21, *LPUSER_INFO_21;

typedef struct _USER_INFO_22 {
    LPWSTR usri22_name;
    BYTE usri22_password[ENCRYPTED_PWLEN];
    DWORD usri22_password_age;
    DWORD usri22_priv;
    LPWSTR usri22_home_dir;
    LPWSTR usri22_comment;
    DWORD usri22_flags;
    LPWSTR usri22_script_path;
    DWORD usri22_auth_flags;
    LPWSTR usri22_full_name;
    LPWSTR usri22_usr_comment;
    LPWSTR usri22_parms;
    LPWSTR usri22_workstations;
    DWORD usri22_last_logon;
    DWORD usri22_last_logoff;
    DWORD usri22_acct_expires;
    DWORD usri22_max_storage;
    DWORD usri22_units_per_week;
    PBYTE usri22_logon_hours;
    DWORD usri22_bad_pw_count;
    DWORD usri22_num_logons;
    LPWSTR usri22_logon_server;
    DWORD usri22_country_code;
    DWORD usri22_code_page;
} USER_INFO_22, *PUSER_INFO_22, *LPUSER_INFO_22;

typedef struct _USER_INFO_23 {
    LPWSTR usri23_name;
    LPWSTR usri23_full_name;
    LPWSTR usri23_comment;
    DWORD usri23_flags;
    PSID usri23_user_sid;
} USER_INFO_23, *PUSER_INFO_23, *LPUSER_INFO_23;

typedef struct _USER_INFO_24 {
    BOOL usri24_internet_identity;
    DWORD usri24_flags;
    LPWSTR usri24_internet_provider_name;
    LPWSTR usri24_internet_principal_name;
    PSID usri24_user_sid;
} USER_INFO_24, *PUSER_INFO_24, *LPUSER_INFO_24;

typedef struct _USER_INFO_1003 { LPWSTR usri1003_password; } USER_INFO_1003, *PUSER_INFO_1003, *LPUSER_INFO_1003;
typedef struct _USER_INFO_1005 { DWORD usri1005_priv; } USER_INFO_1005, *PUSER_INFO_1005, *LPUSER_INFO_1005;
typedef struct _USER_INFO_1006 { LPWSTR usri1006_home_dir; } USER_INFO_1006, *PUSER_INFO_1006, *LPUSER_INFO_1006;
typedef struct _USER_INFO_1007 { LPWSTR usri1007_comment; } USER_INFO_1007, *PUSER_INFO_1007, *LPUSER_INFO_1007;
typedef struct _USER_INFO_1008 { DWORD usri1008_flags; } USER_INFO_1008, *PUSER_INFO_1008, *LPUSER_INFO_1008;
typedef struct _USER_INFO_1009 { LPWSTR usri1009_script_path; } USER_INFO_1009, *PUSER_INFO_1009, *LPUSER_INFO_1009;
typedef struct _USER_INFO_1010 { DWORD usri1010_auth_flags; } USER_INFO_1010, *PUSER_INFO_1010, *LPUSER_INFO_1010;
typedef struct _USER_INFO_1011 { LPWSTR usri1011_full_name; } USER_INFO_1011, *PUSER_INFO_1011, *LPUSER_INFO_1011;
typedef struct _USER_INFO_1012 { LPWSTR usri1012_usr_comment; } USER_INFO_1012, *PUSER_INFO_1012, *LPUSER_INFO_1012;
typedef struct _USER_INFO_1013 { LPWSTR usri1013_parms; } USER_INFO_1013, *PUSER_INFO_1013, *LPUSER_INFO_1013;
typedef struct _USER_INFO_1014 { LPWSTR usri1014_workstations; } USER_INFO_1014, *PUSER_INFO_1014, *LPUSER_INFO_1014;
typedef struct _USER_INFO_1017 { DWORD usri1017_acct_expires; } USER_INFO_1017, *PUSER_INFO_1017, *LPUSER_INFO_1017;
typedef struct _USER_INFO_1018 { DWORD usri1018_max_storage; } USER_INFO_1018, *PUSER_INFO_1018, *LPUSER_INFO_1018;
typedef struct _USER_INFO_1020 { DWORD usri1020_units_per_week; LPBYTE usri1020_logon_hours; } USER_INFO_1020, *PUSER_INFO_1020, *LPUSER_INFO_1020;
typedef struct _USER_INFO_1023 { LPWSTR usri1023_logon_server; } USER_INFO_1023, *PUSER_INFO_1023, *LPUSER_INFO_1023;
typedef struct _USER_INFO_1024 { DWORD usri1024_country_code; } USER_INFO_1024, *PUSER_INFO_1024, *LPUSER_INFO_1024;
typedef struct _USER_INFO_1025 { DWORD usri1025_code_page; } USER_INFO_1025, *PUSER_INFO_1025, *LPUSER_INFO_1025;
typedef struct _USER_INFO_1051 { DWORD usri1051_primary_group_id; } USER_INFO_1051, *PUSER_INFO_1051, *LPUSER_INFO_1051;
typedef struct _USER_INFO_1052 { LPWSTR usri1052_profile; } USER_INFO_1052, *PUSER_INFO_1052, *LPUSER_INFO_1052;
typedef struct _USER_INFO_1053 { LPWSTR usri1053_home_dir_drive; } USER_INFO_1053, *PUSER_INFO_1053, *LPUSER_INFO_1053;

/* Data Structures - User Modals */
typedef struct _USER_MODALS_INFO_0 {
    DWORD usrmod0_min_passwd_len;
    DWORD usrmod0_max_passwd_age;
    DWORD usrmod0_min_passwd_age;
    DWORD usrmod0_force_logoff;
    DWORD usrmod0_password_hist_len;
} USER_MODALS_INFO_0, *PUSER_MODALS_INFO_0, *LPUSER_MODALS_INFO_0;

typedef struct _USER_MODALS_INFO_1 {
    DWORD usrmod1_role;
    LPWSTR usrmod1_primary;
} USER_MODALS_INFO_1, *PUSER_MODALS_INFO_1, *LPUSER_MODALS_INFO_1;

typedef struct _USER_MODALS_INFO_2 {
    LPWSTR usrmod2_domain_name;
    PSID usrmod2_domain_id;
} USER_MODALS_INFO_2, *PUSER_MODALS_INFO_2, *LPUSER_MODALS_INFO_2;

typedef struct _USER_MODALS_INFO_3 {
    DWORD usrmod3_lockout_duration;
    DWORD usrmod3_lockout_observation_window;
    DWORD usrmod3_lockout_threshold;
} USER_MODALS_INFO_3, *PUSER_MODALS_INFO_3, *LPUSER_MODALS_INFO_3;

typedef struct _USER_MODALS_INFO_1001 { DWORD usrmod1001_min_passwd_len; } USER_MODALS_INFO_1001, *PUSER_MODALS_INFO_1001, *LPUSER_MODALS_INFO_1001;
typedef struct _USER_MODALS_INFO_1002 { DWORD usrmod1002_max_passwd_age; } USER_MODALS_INFO_1002, *PUSER_MODALS_INFO_1002, *LPUSER_MODALS_INFO_1002;
typedef struct _USER_MODALS_INFO_1003 { DWORD usrmod1003_min_passwd_age; } USER_MODALS_INFO_1003, *PUSER_MODALS_INFO_1003, *LPUSER_MODALS_INFO_1003;
typedef struct _USER_MODALS_INFO_1004 { DWORD usrmod1004_force_logoff; } USER_MODALS_INFO_1004, *PUSER_MODALS_INFO_1004, *LPUSER_MODALS_INFO_1004;
typedef struct _USER_MODALS_INFO_1005 { DWORD usrmod1005_password_hist_len; } USER_MODALS_INFO_1005, *PUSER_MODALS_INFO_1005, *LPUSER_MODALS_INFO_1005;
typedef struct _USER_MODALS_INFO_1006 { DWORD usrmod1006_role; } USER_MODALS_INFO_1006, *PUSER_MODALS_INFO_1006, *LPUSER_MODALS_INFO_1006;
typedef struct _USER_MODALS_INFO_1007 { LPWSTR usrmod1007_primary; } USER_MODALS_INFO_1007, *PUSER_MODALS_INFO_1007, *LPUSER_MODALS_INFO_1007;

/* Standard rights */
#define DELETE 0x00010000
#define READ_CONTROL 0x00020000
#define WRITE_DAC 0x00040000
#define WRITE_OWNER 0x00080000
#define SYNCHRONIZE 0x00100000

#define STANDARD_RIGHTS_REQUIRED 0x000F0000

#define STANDARD_RIGHTS_READ READ_CONTROL
#define STANDARD_RIGHTS_WRITE READ_CONTROL
#define STANDARD_RIGHTS_EXECUTE READ_CONTROL

#define STANDARD_RIGHTS_ALL 0x001F0000

#define SPECIFIC_RIGHTS_ALL 0x0000FFFF

#define ACCESS_SYSTEM_SECURITY 0x01000000
#define MAXIMUM_ALLOWED 0x02000000

#define GENERIC_READ 0x80000000
#define GENERIC_WRITE 0x40000000
#define GENERIC_EXECUTE 0x20000000
#define GENERIC_ALL 0x10000000

/* Memory constants */
#define PAGE_NOACCESS 0x01
#define PAGE_READONLY 0x02
#define PAGE_READWRITE 0x04
#define PAGE_WRITECOPY 0x08
#define PAGE_EXECUTE 0x10
#define PAGE_EXECUTE_READ 0x20
#define PAGE_EXECUTE_READWRITE 0x40
#define PAGE_EXECUTE_WRITECOPY 0x80
#define PAGE_GUARD 0x100
#define PAGE_NOCACHE 0x200
#define PAGE_WRITECOMBINE 0x400
#define PAGE_GRAPHICS_NOACCESS 0x0800
#define PAGE_GRAPHICS_READONLY 0x1000
#define PAGE_GRAPHICS_READWRITE 0x2000
#define PAGE_GRAPHICS_EXECUTE 0x4000
#define PAGE_GRAPHICS_EXECUTE_READ 0x8000
#define PAGE_GRAPHICS_EXECUTE_READWRITE 0x10000
#define PAGE_GRAPHICS_COHERENT 0x20000
#define PAGE_ENCLAVE_THREAD_CONTROL 0x80000000
#define PAGE_REVERT_TO_FILE_MAP 0x80000000
#define PAGE_TARGETS_NO_UPDATE 0x40000000
#define PAGE_TARGETS_INVALID 0x40000000
#define PAGE_ENCLAVE_UNVALIDATED 0x20000000
#define PAGE_ENCLAVE_DECOMMIT 0x10000000

#define SEC_PARTITION_OWNER_HANDLE 0x40000
#define SEC_64K_PAGES 0x80000
#define SEC_FILE 0x800000
#define SEC_IMAGE 0x1000000
#define SEC_PROTECTED_IMAGE 0x2000000
#define SEC_RESERVE 0x4000000
#define SEC_COMMIT 0x8000000
#define SEC_NOCACHE 0x10000000
#define SEC_WRITECOMBINE 0x40000000
#define SEC_LARGE_PAGES 0x80000000
#define SEC_IMAGE_NO_EXECUTE (SEC_IMAGE | SEC_NOCACHE)
#define MEM_IMAGE SEC_IMAGE

#define MEM_COMMIT 0x1000
#define MEM_RESERVE 0x2000
#define MEM_DECOMMIT 0x4000
#define MEM_RELEASE 0x8000
#define MEM_FREE 0x10000
#define MEM_PRIVATE 0x20000
#define MEM_MAPPED 0x40000
#define MEM_RESET 0x80000
#define MEM_TOP_DOWN 0x100000
#define MEM_WRITE_WATCH 0x200000
#define MEM_PHYSICAL 0x400000
#define MEM_ROTATE 0x800000
#define MEM_DIFFERENT_IMAGE_BASE_OK 0x800000
#define MEM_RESET_UNDO 0x1000000
#define MEM_LARGE_PAGES 0x20000000
#define MEM_4MB_PAGES 0x80000000
#define MEM_64K_PAGES (MEM_LARGE_PAGES | MEM_PHYSICAL)

#define GMEM_FIXED 0x0
#define GMEM_MOVEABLE 0x2
#define GMEM_NOCOMPACT 0x10
#define GMEM_NODISCARD 0x20
#define GMEM_ZEROINIT 0x40
#define GMEM_MODIFY 0x80
#define GMEM_DISCARDABLE 0x100
#define GMEM_NOT_BANKED 0x1000
#define GMEM_SHARE 0x2000
#define GMEM_DDESHARE 0x2000
#define GMEM_NOTIFY 0x4000
#define GMEM_LOWER GMEM_NOT_BANKED
#define GMEM_VALID_FLAGS 0x7f72
#define GMEM_INVALID_HANDLE 0x8000

#define GHND (GMEM_MOVEABLE | GMEM_ZEROINIT)
#define GPTR (GMEM_FIXED | GMEM_ZEROINIT)

#define GMEM_DISCARDED 0x4000
#define GMEM_LOCKCOUNT 0x00ff

/* Section constants */
#define SECTION_QUERY 0x0001
#define SECTION_MAP_WRITE 0x0002
#define SECTION_MAP_READ 0x0004
#define SECTION_MAP_EXECUTE 0x0008
#define SECTION_EXTEND_SIZE 0x0010
#define SECTION_MAP_EXECUTE_EXPLICIT 0x0020

#define SECTION_ALL_ACCESS (STANDARD_RIGHTS_REQUIRED|SECTION_QUERY| SECTION_MAP_WRITE | SECTION_MAP_READ | SECTION_MAP_EXECUTE | SECTION_EXTEND_SIZE)

#define SESSION_QUERY_ACCESS 0x1
#define SESSION_MODIFY_ACCESS 0x2

#define SESSION_ALL_ACCESS (STANDARD_RIGHTS_REQUIRED | SESSION_QUERY_ACCESS | SESSION_MODIFY_ACCESS)

/* Process constants */
#define PROCESS_TERMINATE (0x0001)
#define PROCESS_CREATE_THREAD (0x0002)
#define PROCESS_SET_SESSIONID (0x0004)
#define PROCESS_VM_OPERATION (0x0008)
#define PROCESS_VM_READ (0x0010)
#define PROCESS_VM_WRITE (0x0020)
#define PROCESS_DUP_HANDLE (0x0040)
#define PROCESS_CREATE_PROCESS (0x0080)
#define PROCESS_SET_QUOTA (0x0100)
#define PROCESS_SET_INFORMATION (0x0200)
#define PROCESS_QUERY_INFORMATION (0x0400)
#define PROCESS_SUSPEND_RESUME (0x0800)
#define PROCESS_QUERY_LIMITED_INFORMATION (0x1000)

/* Token constants */
#define TOKEN_ASSIGN_PRIMARY 0x0001
#define TOKEN_DUPLICATE 0x0002
#define TOKEN_IMPERSONATE 0x0004
#define TOKEN_QUERY 0x0008
#define TOKEN_QUERY_SOURCE 0x0010
#define TOKEN_ADJUST_PRIVILEGES 0x0020
#define TOKEN_ADJUST_GROUPS 0x0040
#define TOKEN_ADJUST_DEFAULT 0x0080
#define TOKEN_ADJUST_SESSIONID 0x0100

#define TOKEN_ALL_ACCESS_P (STANDARD_RIGHTS_REQUIRED | TOKEN_ASSIGN_PRIMARY | TOKEN_DUPLICATE | TOKEN_IMPERSONATE | TOKEN_QUERY | TOKEN_QUERY_SOURCE | TOKEN_ADJUST_PRIVILEGES | TOKEN_ADJUST_GROUPS | TOKEN_ADJUST_DEFAULT)
#define TOKEN_ALL_ACCESS (TOKEN_ALL_ACCESS_P | TOKEN_ADJUST_SESSIONID)
#define TOKEN_READ (STANDARD_RIGHTS_READ | TOKEN_QUERY)

#define TOKEN_WRITE (STANDARD_RIGHTS_WRITE | TOKEN_ADJUST_PRIVILEGES | TOKEN_ADJUST_GROUPS | TOKEN_ADJUST_DEFAULT)

#define TOKEN_EXECUTE (STANDARD_RIGHTS_EXECUTE)

/* User flags and constants */
#define UF_SCRIPT 0x0001
#define UF_ACCOUNTDISABLE 0x0002
#define UF_HOMEDIR_REQUIRED 0x0008
#define UF_LOCKOUT 0x0010
#define UF_PASSWD_NOTREQD 0x0020
#define UF_PASSWD_CANT_CHANGE 0x0040
#define UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED 0x0080
#define UF_TEMP_DUPLICATE_ACCOUNT 0x0100
#define UF_NORMAL_ACCOUNT 0x0200
#define UF_INTERDOMAIN_TRUST_ACCOUNT 0x0800
#define UF_WORKSTATION_TRUST_ACCOUNT 0x1000
#define UF_SERVER_TRUST_ACCOUNT 0x2000
#define UF_MACHINE_ACCOUNT_MASK (UF_INTERDOMAIN_TRUST_ACCOUNT | UF_WORKSTATION_TRUST_ACCOUNT | UF_SERVER_TRUST_ACCOUNT)
#define UF_ACCOUNT_TYPE_MASK (UF_TEMP_DUPLICATE_ACCOUNT | UF_NORMAL_ACCOUNT | UF_INTERDOMAIN_TRUST_ACCOUNT | UF_WORKSTATION_TRUST_ACCOUNT | UF_SERVER_TRUST_ACCOUNT)
#define UF_DONT_EXPIRE_PASSWD 0x10000
#define UF_MNS_LOGON_ACCOUNT 0x20000
#define UF_SMARTCARD_REQUIRED 0x40000
#define UF_TRUSTED_FOR_DELEGATION 0x80000
#define UF_NOT_DELEGATED 0x100000
#define UF_USE_DES_KEY_ONLY 0x200000
#define UF_DONT_REQUIRE_PREAUTH 0x400000
#define UF_PASSWORD_EXPIRED 0x800000
#define UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION 0x1000000
#define UF_NO_AUTH_DATA_REQUIRED 0x2000000
#define UF_PARTIAL_SECRETS_ACCOUNT 0x4000000
#define UF_USE_AES_KEYS 0x8000000
#define UF_SETTABLE_BITS (UF_SCRIPT | UF_ACCOUNTDISABLE | UF_LOCKOUT | UF_HOMEDIR_REQUIRED | UF_PASSWD_NOTREQD | UF_PASSWD_CANT_CHANGE | UF_ACCOUNT_TYPE_MASK | UF_DONT_EXPIRE_PASSWD | UF_MNS_LOGON_ACCOUNT | UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED | UF_SMARTCARD_REQUIRED | UF_TRUSTED_FOR_DELEGATION | UF_NOT_DELEGATED | UF_USE_DES_KEY_ONLY | UF_DONT_REQUIRE_PREAUTH | UF_PASSWORD_EXPIRED | UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION | UF_NO_AUTH_DATA_REQUIRED | UF_USE_AES_KEYS | UF_PARTIAL_SECRETS_ACCOUNT)

#define FILTER_TEMP_DUPLICATE_ACCOUNT 0x0001
#define FILTER_NORMAL_ACCOUNT 0x0002
#define FILTER_INTERDOMAIN_TRUST_ACCOUNT 0x0008
#define FILTER_WORKSTATION_TRUST_ACCOUNT 0x0010
#define FILTER_SERVER_TRUST_ACCOUNT 0x0020

#define LG_INCLUDE_INDIRECT 0x0001

#define AF_OP_PRINT 0x1
#define AF_OP_COMM 0x2
#define AF_OP_SERVER 0x4
#define AF_OP_ACCOUNTS 0x8
#define AF_SETTABLE_BITS (AF_OP_PRINT | AF_OP_COMM | AF_OP_SERVER | AF_OP_ACCOUNTS)

#define UAS_ROLE_STANDALONE 0
#define UAS_ROLE_MEMBER 1
#define UAS_ROLE_BACKUP 2
#define UAS_ROLE_PRIMARY 3

#define USER_NAME_PARMNUM 1
#define USER_PASSWORD_PARMNUM 3
#define USER_PASSWORD_AGE_PARMNUM 4
#define USER_PRIV_PARMNUM 5
#define USER_HOME_DIR_PARMNUM 6
#define USER_COMMENT_PARMNUM 7
#define USER_FLAGS_PARMNUM 8
#define USER_SCRIPT_PATH_PARMNUM 9
#define USER_AUTH_FLAGS_PARMNUM 10
#define USER_FULL_NAME_PARMNUM 11
#define USER_USR_COMMENT_PARMNUM 12
#define USER_PARMS_PARMNUM 13
#define USER_WORKSTATIONS_PARMNUM 14
#define USER_LAST_LOGON_PARMNUM 15
#define USER_LAST_LOGOFF_PARMNUM 16
#define USER_ACCT_EXPIRES_PARMNUM 17
#define USER_MAX_STORAGE_PARMNUM 18
#define USER_UNITS_PER_WEEK_PARMNUM 19
#define USER_LOGON_HOURS_PARMNUM 20
#define USER_PAD_PW_COUNT_PARMNUM 21
#define USER_NUM_LOGONS_PARMNUM 22
#define USER_LOGON_SERVER_PARMNUM 23
#define USER_COUNTRY_CODE_PARMNUM 24
#define USER_CODE_PAGE_PARMNUM 25
#define USER_PRIMARY_GROUP_PARMNUM 51
#define USER_PROFILE 52
#define USER_PROFILE_PARMNUM 52
#define USER_HOME_DIR_DRIVE_PARMNUM 53

#define USER_NAME_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_NAME_PARMNUM)
#define USER_PASSWORD_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_PASSWORD_PARMNUM)
#define USER_PASSWORD_AGE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_PASSWORD_AGE_PARMNUM)
#define USER_PRIV_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_PRIV_PARMNUM)
#define USER_HOME_DIR_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_HOME_DIR_PARMNUM)
#define USER_COMMENT_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_COMMENT_PARMNUM)
#define USER_FLAGS_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_FLAGS_PARMNUM)
#define USER_SCRIPT_PATH_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_SCRIPT_PATH_PARMNUM)
#define USER_AUTH_FLAGS_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_AUTH_FLAGS_PARMNUM)
#define USER_FULL_NAME_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_FULL_NAME_PARMNUM)
#define USER_USR_COMMENT_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_USR_COMMENT_PARMNUM)
#define USER_PARMS_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_PARMS_PARMNUM)
#define USER_WORKSTATIONS_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_WORKSTATIONS_PARMNUM)
#define USER_LAST_LOGON_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_LAST_LOGON_PARMNUM)
#define USER_LAST_LOGOFF_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_LAST_LOGOFF_PARMNUM)
#define USER_ACCT_EXPIRES_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_ACCT_EXPIRES_PARMNUM)
#define USER_MAX_STORAGE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_MAX_STORAGE_PARMNUM)
#define USER_UNITS_PER_WEEK_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_UNITS_PER_WEEK_PARMNUM)
#define USER_LOGON_HOURS_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_LOGON_HOURS_PARMNUM)
#define USER_PAD_PW_COUNT_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_PAD_PW_COUNT_PARMNUM)
#define USER_NUM_LOGONS_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_NUM_LOGONS_PARMNUM)
#define USER_LOGON_SERVER_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_LOGON_SERVER_PARMNUM)
#define USER_COUNTRY_CODE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_COUNTRY_CODE_PARMNUM)
#define USER_CODE_PAGE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_CODE_PAGE_PARMNUM)
#define USER_PRIMARY_GROUP_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_PRIMARY_GROUP_PARMNUM)
#define USER_HOME_DIR_DRIVE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + USER_HOME_DIR_DRIVE_PARMNUM)

#define NULL_USERSETINFO_PASSWD "              "
#define TIMEQ_FOREVER ((unsigned long)-1L)
#define USER_MAXSTORAGE_UNLIMITED ((unsigned long)-1L)
#define USER_NO_LOGOFF ((unsigned long)-1L)
#define UNITS_PER_DAY 24
#define UNITS_PER_WEEK (UNITS_PER_DAY * 7)

#define USER_PRIV_MASK 0x3
#define USER_PRIV_GUEST 0
#define USER_PRIV_USER 1
#define USER_PRIV_ADMIN 2

#define MAX_PASSWD_LEN PWLEN
#define DEF_MIN_PWLEN 6
#define DEF_PWUNIQUENESS 5
#define DEF_MAX_PWHIST 8
#define DEF_MAX_PWAGE TIMEQ_FOREVER
#define DEF_MIN_PWAGE ((unsigned long)0L)
#define DEF_FORCE_LOGOFF ((unsigned long)0xffffffff)
#define DEF_MAX_BADPW 0
#define ONE_DAY ((unsigned long)1*24*3600)

#define VALIDATED_LOGON 0
#define PASSWORD_EXPIRED 2
#define NON_VALIDATED_LOGON 3
#define VALID_LOGOFF 1

#define MODALS_MIN_PASSWD_LEN_PARMNUM 1
#define MODALS_MAX_PASSWD_AGE_PARMNUM 2
#define MODALS_MIN_PASSWD_AGE_PARMNUM 3
#define MODALS_FORCE_LOGOFF_PARMNUM 4
#define MODALS_PASSWD_HIST_LEN_PARMNUM 5
#define MODALS_ROLE_PARMNUM 6
#define MODALS_PRIMARY_PARMNUM 7
#define MODALS_DOMAIN_NAME_PARMNUM 8
#define MODALS_DOMAIN_ID_PARMNUM 9
#define MODALS_LOCKOUT_DURATION_PARMNUM 10
#define MODALS_LOCKOUT_OBSERVATION_WINDOW_PARMNUM 11
#define MODALS_LOCKOUT_THRESHOLD_PARMNUM 12

#define MODALS_MIN_PASSWD_LEN_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_MIN_PASSWD_LEN_PARMNUM)
#define MODALS_MAX_PASSWD_AGE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_MAX_PASSWD_AGE_PARMNUM)
#define MODALS_MIN_PASSWD_AGE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_MIN_PASSWD_AGE_PARMNUM)
#define MODALS_FORCE_LOGOFF_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_FORCE_LOGOFF_PARMNUM)
#define MODALS_PASSWD_HIST_LEN_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_PASSWD_HIST_LEN_PARMNUM)
#define MODALS_ROLE_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_ROLE_PARMNUM)
#define MODALS_PRIMARY_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_PRIMARY_PARMNUM)
#define MODALS_DOMAIN_NAME_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_DOMAIN_NAME_PARMNUM)
#define MODALS_DOMAIN_ID_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + MODALS_DOMAIN_ID_PARMNUM)

/* Data Structures - Group */
typedef struct _GROUP_INFO_0 { LPWSTR grpi0_name; } GROUP_INFO_0, *PGROUP_INFO_0, *LPGROUP_INFO_0;
typedef struct _GROUP_INFO_1 { LPWSTR grpi1_name; LPWSTR grpi1_comment; } GROUP_INFO_1, *PGROUP_INFO_1, *LPGROUP_INFO_1;
typedef struct _GROUP_INFO_2 { LPWSTR grpi2_name; LPWSTR grpi2_comment; DWORD grpi2_group_id; DWORD grpi2_attributes; } GROUP_INFO_2, *PGROUP_INFO_2;
typedef struct _GROUP_INFO_3 { LPWSTR grpi3_name; LPWSTR grpi3_comment; PSID grpi3_group_sid; DWORD grpi3_attributes; } GROUP_INFO_3, *PGROUP_INFO_3;
typedef struct _GROUP_INFO_1002 { LPWSTR grpi1002_comment; } GROUP_INFO_1002, *PGROUP_INFO_1002, *LPGROUP_INFO_1002;
typedef struct _GROUP_INFO_1005 { DWORD grpi1005_attributes; } GROUP_INFO_1005, *PGROUP_INFO_1005, *LPGROUP_INFO_1005;

typedef struct _GROUP_USERS_INFO_0 { LPWSTR grui0_name; } GROUP_USERS_INFO_0, *PGROUP_USERS_INFO_0, *LPGROUP_USERS_INFO_0;
typedef struct _GROUP_USERS_INFO_1 { LPWSTR grui1_name; DWORD grui1_attributes; } GROUP_USERS_INFO_1, *PGROUP_USERS_INFO_1, *LPGROUP_USERS_INFO_1;

#define GROUPIDMASK 0x8000
#define GROUP_ALL_PARMNUM 0
#define GROUP_NAME_PARMNUM 1
#define GROUP_COMMENT_PARMNUM 2
#define GROUP_ATTRIBUTES_PARMNUM 3
#define GROUP_ALL_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + GROUP_ALL_PARMNUM)
#define GROUP_NAME_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + GROUP_NAME_PARMNUM)
#define GROUP_COMMENT_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + GROUP_COMMENT_PARMNUM)
#define GROUP_ATTRIBUTES_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + GROUP_ATTRIBUTES_PARMNUM)

/* Data Structures - LocalGroup */
typedef struct _LOCALGROUP_INFO_0 { LPWSTR lgrpi0_name; } LOCALGROUP_INFO_0, *PLOCALGROUP_INFO_0, *LPLOCALGROUP_INFO_0;
typedef struct _LOCALGROUP_INFO_1 { LPWSTR lgrpi1_name; LPWSTR lgrpi1_comment; } LOCALGROUP_INFO_1, *PLOCALGROUP_INFO_1, *LPLOCALGROUP_INFO_1;
typedef struct _LOCALGROUP_INFO_1002 { LPWSTR lgrpi1002_comment; } LOCALGROUP_INFO_1002, *PLOCALGROUP_INFO_1002, *LPLOCALGROUP_INFO_1002;

typedef struct _LOCALGROUP_MEMBERS_INFO_0 {
    PSID lgrmi0_sid;
} LOCALGROUP_MEMBERS_INFO_0, *PLOCALGROUP_MEMBERS_INFO_0, *LPLOCALGROUP_MEMBERS_INFO_0;

typedef struct _LOCALGROUP_MEMBERS_INFO_1 {
    PSID lgrmi1_sid;
    SID_NAME_USE lgrmi1_sidusage;
    LPWSTR lgrmi1_name;
} LOCALGROUP_MEMBERS_INFO_1, *PLOCALGROUP_MEMBERS_INFO_1, *LPLOCALGROUP_MEMBERS_INFO_1;

typedef struct _LOCALGROUP_MEMBERS_INFO_2 {
    PSID lgrmi2_sid;
    SID_NAME_USE lgrmi2_sidusage;
    LPWSTR lgrmi2_domainandname;
} LOCALGROUP_MEMBERS_INFO_2, *PLOCALGROUP_MEMBERS_INFO_2, *LPLOCALGROUP_MEMBERS_INFO_2;

typedef struct _LOCALGROUP_MEMBERS_INFO_3 {
    LPWSTR lgrmi3_domainandname;
} LOCALGROUP_MEMBERS_INFO_3, *PLOCALGROUP_MEMBERS_INFO_3, *LPLOCALGROUP_MEMBERS_INFO_3;

typedef struct _LOCALGROUP_USERS_INFO_0 {
    LPWSTR lgrui0_name;
} LOCALGROUP_USERS_INFO_0, *PLOCALGROUP_USERS_INFO_0, *LPLOCALGROUP_USERS_INFO_0;

#define LOCALGROUP_NAME_PARMNUM 1
#define LOCALGROUP_COMMENT_PARMNUM 2

/* Display information */
typedef struct _NET_DISPLAY_USER {
    LPWSTR usri1_name;
    LPWSTR usri1_comment;
    DWORD usri1_flags;
    LPWSTR usri1_full_name;
    DWORD usri1_user_id;
    DWORD usri1_next_index;
} NET_DISPLAY_USER, *PNET_DISPLAY_USER;

typedef struct _NET_DISPLAY_MACHINE {
    LPWSTR usri2_name;
    LPWSTR usri2_comment;
    DWORD usri2_flags;
    DWORD usri2_user_id;
    DWORD usri2_next_index;
} NET_DISPLAY_MACHINE, *PNET_DISPLAY_MACHINE;

typedef struct _NET_DISPLAY_GROUP {
    LPWSTR grpi3_name;
    LPWSTR grpi3_comment;
    DWORD grpi3_group_id;
    DWORD grpi3_attributes;
    DWORD grpi3_next_index;
} NET_DISPLAY_GROUP, *PNET_DISPLAY_GROUP;

/* Data Structures - Access */
typedef struct _ACCESS_INFO_0 { LPWSTR acc0_resource_name; } ACCESS_INFO_0, *PACCESS_INFO_0, *LPACCESS_INFO_0;
typedef struct _ACCESS_INFO_1 { LPWSTR acc1_resource_name; DWORD acc1_attr; DWORD acc1_count; } ACCESS_INFO_1, *PACCESS_INFO_1, *LPACCESS_INFO_1;
typedef struct _ACCESS_INFO_1002 { DWORD acc1002_attr; } ACCESS_INFO_1002, *PACCESS_INFO_1002, *LPACCESS_INFO_1002;
typedef struct _ACCESS_LIST { LPWSTR acl_ugname; DWORD acl_access; } ACCESS_LIST, *PACCESS_LIST, *LPACCESS_LIST;

#define MAXPERMENTRIES 64
#define ACCESS_NONE 0
#define ACCESS_READ 0x01
#define ACCESS_WRITE 0x02
#define ACCESS_CREATE 0x04
#define ACCESS_EXEC 0x08
#define ACCESS_DELETE 0x10
#define ACCESS_ATRIB 0x20
#define ACCESS_PERM 0x40
#define ACCESS_ALL (ACCESS_READ | ACCESS_WRITE | ACCESS_CREATE | ACCESS_EXEC | ACCESS_DELETE | ACCESS_ATRIB | ACCESS_PERM)
#define ACCESS_GROUP 0x8000
#define ACCESS_AUDIT 0x1
#define ACCESS_SUCCESS_OPEN 0x10
#define ACCESS_SUCCESS_WRITE 0x20
#define ACCESS_SUCCESS_DELETE 0x40
#define ACCESS_SUCCESS_ACL 0x80
#define ACCESS_SUCCESS_MASK 0xF0
#define ACCESS_FAIL_OPEN 0x100
#define ACCESS_FAIL_WRITE 0x200
#define ACCESS_FAIL_DELETE 0x400
#define ACCESS_FAIL_ACL 0x800
#define ACCESS_FAIL_MASK 0xF00
#define ACCESS_FAIL_SHIFT 4
#define ACCESS_RESOURCE_NAME_PARMNUM 1
#define ACCESS_ATTR_PARMNUM 2
#define ACCESS_COUNT_PARMNUM 3
#define ACCESS_ACCESS_LIST_PARMNUM 4
#define ACCESS_RESOURCE_NAME_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + ACCESS_RESOURCE_NAME_PARMNUM)
#define ACCESS_ATTR_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + ACCESS_ATTR_PARMNUM)
#define ACCESS_COUNT_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + ACCESS_COUNT_PARMNUM)
#define ACCESS_ACCESS_LIST_INFOLEVEL (PARMNUM_BASE_INFOLEVEL + ACCESS_ACCESS_LIST_PARMNUM)
#define ACCESS_LETTERS "RWCXDAP         "

/* Password Checking API structures */
typedef enum _NET_VALIDATE_PASSWORD_TYPE {
    NetValidateAuthentication = 1,
    NetValidatePasswordChange,
    NetValidatePasswordReset
} NET_VALIDATE_PASSWORD_TYPE, *PNET_VALIDATE_PASSWORD_TYPE;

typedef struct _NET_VALIDATE_PASSWORD_HASH {
    ULONG Length;
    LPBYTE Hash;
} NET_VALIDATE_PASSWORD_HASH, *PNET_VALIDATE_PASSWORD_HASH;

#define NET_VALIDATE_PASSWORD_LAST_SET 0x00000001
#define NET_VALIDATE_BAD_PASSWORD_TIME 0x00000002
#define NET_VALIDATE_LOCKOUT_TIME 0x00000004
#define NET_VALIDATE_BAD_PASSWORD_COUNT 0x00000008
#define NET_VALIDATE_PASSWORD_HISTORY_LENGTH 0x00000010
#define NET_VALIDATE_PASSWORD_HISTORY 0x00000020

typedef struct _NET_VALIDATE_PERSISTED_FIELDS {
    ULONG PresentFields;
    FILETIME PasswordLastSet;
    FILETIME BadPasswordTime;
    FILETIME LockoutTime;
    ULONG BadPasswordCount;
    ULONG PasswordHistoryLength;
    PNET_VALIDATE_PASSWORD_HASH PasswordHistory;
} NET_VALIDATE_PERSISTED_FIELDS, *PNET_VALIDATE_PERSISTED_FIELDS;

typedef struct _NET_VALIDATE_OUTPUT_ARG {
    NET_VALIDATE_PERSISTED_FIELDS ChangedPersistedFields;
    NET_API_STATUS ValidationStatus;
} NET_VALIDATE_OUTPUT_ARG, *PNET_VALIDATE_OUTPUT_ARG;

typedef struct _NET_VALIDATE_AUTHENTICATION_INPUT_ARG {
    NET_VALIDATE_PERSISTED_FIELDS InputPersistedFields;
    BOOLEAN PasswordMatched;
} NET_VALIDATE_AUTHENTICATION_INPUT_ARG, *PNET_VALIDATE_AUTHENTICATION_INPUT_ARG;

typedef struct _NET_VALIDATE_PASSWORD_CHANGE_INPUT_ARG {
    NET_VALIDATE_PERSISTED_FIELDS InputPersistedFields;
    LPWSTR ClearPassword;
    LPWSTR UserAccountName;
    NET_VALIDATE_PASSWORD_HASH HashedPassword;
    BOOLEAN PasswordMatch;
} NET_VALIDATE_PASSWORD_CHANGE_INPUT_ARG, *PNET_VALIDATE_PASSWORD_CHANGE_INPUT_ARG;

typedef struct _NET_VALIDATE_PASSWORD_RESET_INPUT_ARG {
    NET_VALIDATE_PERSISTED_FIELDS InputPersistedFields;
    LPWSTR ClearPassword;
    LPWSTR UserAccountName;
    NET_VALIDATE_PASSWORD_HASH HashedPassword;
    BOOLEAN PasswordMustChangeAtNextLogon;
    BOOLEAN ClearLockout;
} NET_VALIDATE_PASSWORD_RESET_INPUT_ARG, *PNET_VALIDATE_PASSWORD_RESET_INPUT_ARG;

/* Netlogon controls and query structures */
#define NETLOGON_CONTROL_QUERY 1
#define NETLOGON_CONTROL_REPLICATE 2
#define NETLOGON_CONTROL_SYNCHRONIZE 3
#define NETLOGON_CONTROL_PDC_REPLICATE 4
#define NETLOGON_CONTROL_REDISCOVER 5
#define NETLOGON_CONTROL_TC_QUERY 6
#define NETLOGON_CONTROL_TRANSPORT_NOTIFY 7
#define NETLOGON_CONTROL_FIND_USER 8
#define NETLOGON_CONTROL_CHANGE_PASSWORD 9
#define NETLOGON_CONTROL_TC_VERIFY 10
#define NETLOGON_CONTROL_FORCE_DNS_REG 11
#define NETLOGON_CONTROL_QUERY_DNS_REG 12
#define NETLOGON_CONTROL_QUERY_ENC_TYPES 13

#define NETLOGON_CONTROL_UNLOAD_NETLOGON_DLL 0xFFFB
#define NETLOGON_CONTROL_BACKUP_CHANGE_LOG 0xFFFC
#define NETLOGON_CONTROL_TRUNCATE_LOG 0xFFFD
#define NETLOGON_CONTROL_SET_DBFLAG 0xFFFE
#define NETLOGON_CONTROL_BREAKPOINT 0xFFFF

typedef struct _NETLOGON_INFO_1 {
    DWORD netlog1_flags;
    NET_API_STATUS netlog1_pdc_connection_status;
} NETLOGON_INFO_1, *PNETLOGON_INFO_1;

typedef struct _NETLOGON_INFO_2 {
    DWORD netlog2_flags;
    NET_API_STATUS netlog2_pdc_connection_status;
    LPWSTR netlog2_trusted_dc_name;
    NET_API_STATUS netlog2_tc_connection_status;
} NETLOGON_INFO_2, *PNETLOGON_INFO_2;

typedef struct _NETLOGON_INFO_3 {
    DWORD netlog3_flags;
    DWORD netlog3_logon_attempts;
    DWORD netlog3_reserved1;
    DWORD netlog3_reserved2;
    DWORD netlog3_reserved3;
    DWORD netlog3_reserved4;
    DWORD netlog3_reserved5;
} NETLOGON_INFO_3, *PNETLOGON_INFO_3;

typedef struct _NETLOGON_INFO_4 {
    LPWSTR netlog4_trusted_dc_name;
    LPWSTR netlog4_trusted_domain_name;
} NETLOGON_INFO_4, *PNETLOGON_INFO_4;

#define NETLOGON_REPLICATION_NEEDED 0x01
#define NETLOGON_REPLICATION_IN_PROGRESS 0x02
#define NETLOGON_FULL_SYNC_REPLICATION 0x04
#define NETLOGON_REDO_NEEDED 0x08
#define NETLOGON_HAS_IP 0x10
#define NETLOGON_HAS_TIMESERV 0x20
#define NETLOGON_DNS_UPDATE_FAILURE 0x40
#define NETLOGON_VERIFY_STATUS_RETURNED 0x80

#define SERVICE_ACCOUNT_FLAG_LINK_TO_HOST_ONLY 0x00000001L
#define SERVICE_ACCOUNT_FLAG_ADD_AGAINST_RODC 0x00000002L
#define SERVICE_ACCOUNT_FLAG_UNLINK_FROM_HOST_ONLY 0x00000001L
#define SERVICE_ACCOUNT_FLAG_REMOVE_OFFLINE 0x00000002L

/* Data Structures - Service */
typedef enum _MSA_INFO_LEVEL {
    MsaInfoLevel0 = 0,
    MsaInfoLevelMax
} MSA_INFO_LEVEL, *PMSA_INFO_LEVEL;

typedef enum _MSA_INFO_STATE {
    MsaInfoNotExist = 1,
    MsaInfoNotService,
    MsaInfoCannotInstall,
    MsaInfoCanInstall,
    MsaInfoInstalled
} MSA_INFO_STATE, *PMSA_INFO_STATE;

typedef struct _MSA_INFO_0 {
    MSA_INFO_STATE State;
} MSA_INFO_0, *PMSA_INFO_0, *LPMSA_INFO_0;

/* LMERR error codes (ported from Windows SDK lmerr.h) */
/* LMERR error codes (ported from Windows SDK lmerr.h) */
/* BEGIN LMERR_PORT */
#define NERR_Success            0
#define NERR_BASE       2100
#define NERR_NetNotStarted      (NERR_BASE+2)
#define NERR_UnknownServer      (NERR_BASE+3)
#define NERR_ShareMem           (NERR_BASE+4)
#define NERR_NoNetworkResource  (NERR_BASE+5)
#define NERR_RemoteOnly         (NERR_BASE+6)
#define NERR_DevNotRedirected   (NERR_BASE+7)
#define NERR_ServerNotStarted   (NERR_BASE+14)
#define NERR_ItemNotFound       (NERR_BASE+15)
#define NERR_UnknownDevDir      (NERR_BASE+16)
#define NERR_RedirectedPath     (NERR_BASE+17)
#define NERR_DuplicateShare     (NERR_BASE+18)
#define NERR_NoRoom             (NERR_BASE+19)
#define NERR_TooManyItems       (NERR_BASE+21)
#define NERR_InvalidMaxUsers    (NERR_BASE+22)
#define NERR_BufTooSmall        (NERR_BASE+23)
#define NERR_RemoteErr          (NERR_BASE+27)
#define NERR_LanmanIniError     (NERR_BASE+31)
#define NERR_NetworkError       (NERR_BASE+36)
#define NERR_WkstaInconsistentState (NERR_BASE+37)
#define NERR_WkstaNotStarted    (NERR_BASE+38)
#define NERR_BrowserNotStarted  (NERR_BASE+39)
#define NERR_InternalError      (NERR_BASE+40)
#define NERR_BadTransactConfig  (NERR_BASE+41)
#define NERR_InvalidAPI         (NERR_BASE+42)
#define NERR_BadEventName       (NERR_BASE+43)
#define NERR_DupNameReboot      (NERR_BASE+44)
#define NERR_CfgCompNotFound    (NERR_BASE+46)
#define NERR_CfgParamNotFound   (NERR_BASE+47)
#define NERR_LineTooLong        (NERR_BASE+49)
#define NERR_QNotFound          (NERR_BASE+50)
#define NERR_JobNotFound        (NERR_BASE+51)
#define NERR_DestNotFound       (NERR_BASE+52)
#define NERR_DestExists         (NERR_BASE+53)
#define NERR_QExists            (NERR_BASE+54)
#define NERR_QNoRoom            (NERR_BASE+55)
#define NERR_JobNoRoom          (NERR_BASE+56)
#define NERR_DestNoRoom         (NERR_BASE+57)
#define NERR_DestIdle           (NERR_BASE+58)
#define NERR_DestInvalidOp      (NERR_BASE+59)
#define NERR_ProcNoRespond      (NERR_BASE+60)
#define NERR_SpoolerNotLoaded   (NERR_BASE+61)
#define NERR_DestInvalidState   (NERR_BASE+62)
#define NERR_QInvalidState      (NERR_BASE+63)
#define NERR_JobInvalidState    (NERR_BASE+64)
#define NERR_SpoolNoMemory      (NERR_BASE+65)
#define NERR_DriverNotFound     (NERR_BASE+66)
#define NERR_DataTypeInvalid    (NERR_BASE+67)
#define NERR_ProcNotFound       (NERR_BASE+68)
#define NERR_ServiceTableLocked (NERR_BASE+80)
#define NERR_ServiceTableFull   (NERR_BASE+81)
#define NERR_ServiceInstalled   (NERR_BASE+82)
#define NERR_ServiceEntryLocked (NERR_BASE+83)
#define NERR_ServiceNotInstalled (NERR_BASE+84)
#define NERR_BadServiceName     (NERR_BASE+85)
#define NERR_ServiceCtlTimeout  (NERR_BASE+86)
#define NERR_ServiceCtlBusy     (NERR_BASE+87)
#define NERR_BadServiceProgName (NERR_BASE+88)
#define NERR_ServiceNotCtrl     (NERR_BASE+89)
#define NERR_ServiceKillProc    (NERR_BASE+90)
#define NERR_ServiceCtlNotValid (NERR_BASE+91)
#define NERR_NotInDispatchTbl   (NERR_BASE+92)
#define NERR_BadControlRecv     (NERR_BASE+93)
#define NERR_ServiceNotStarting (NERR_BASE+94)
#define NERR_AlreadyLoggedOn    (NERR_BASE+100)
#define NERR_NotLoggedOn        (NERR_BASE+101)
#define NERR_BadUsername        (NERR_BASE+102)
#define NERR_BadPassword        (NERR_BASE+103)
#define NERR_UnableToAddName_W  (NERR_BASE+104)
#define NERR_UnableToAddName_F  (NERR_BASE+105)
#define NERR_UnableToDelName_W  (NERR_BASE+106)
#define NERR_UnableToDelName_F  (NERR_BASE+107)
#define NERR_LogonsPaused       (NERR_BASE+109)
#define NERR_LogonServerConflict (NERR_BASE+110)
#define NERR_LogonNoUserPath    (NERR_BASE+111)
#define NERR_LogonScriptError   (NERR_BASE+112)
#define NERR_StandaloneLogon    (NERR_BASE+114)
#define NERR_LogonServerNotFound (NERR_BASE+115)
#define NERR_LogonDomainExists  (NERR_BASE+116)
#define NERR_NonValidatedLogon  (NERR_BASE+117)
#define NERR_ACFNotFound        (NERR_BASE+119)
#define NERR_GroupNotFound      (NERR_BASE+120)
#define NERR_UserNotFound       (NERR_BASE+121)
#define NERR_ResourceNotFound   (NERR_BASE+122)
#define NERR_GroupExists        (NERR_BASE+123)
#define NERR_UserExists         (NERR_BASE+124)
#define NERR_ResourceExists     (NERR_BASE+125)
#define NERR_NotPrimary         (NERR_BASE+126)
#define NERR_ACFNotLoaded       (NERR_BASE+127)
#define NERR_ACFNoRoom          (NERR_BASE+128)
#define NERR_ACFFileIOFail      (NERR_BASE+129)
#define NERR_ACFTooManyLists    (NERR_BASE+130)
#define NERR_UserLogon          (NERR_BASE+131)
#define NERR_ACFNoParent        (NERR_BASE+132)
#define NERR_CanNotGrowSegment  (NERR_BASE+133)
#define NERR_SpeGroupOp         (NERR_BASE+134)
#define NERR_NotInCache         (NERR_BASE+135)
#define NERR_UserInGroup        (NERR_BASE+136)
#define NERR_UserNotInGroup     (NERR_BASE+137)
#define NERR_AccountUndefined   (NERR_BASE+138)
#define NERR_AccountExpired     (NERR_BASE+139)
#define NERR_InvalidWorkstation (NERR_BASE+140)
#define NERR_InvalidLogonHours  (NERR_BASE+141)
#define NERR_PasswordExpired    (NERR_BASE+142)
#define NERR_PasswordCantChange (NERR_BASE+143)
#define NERR_PasswordHistConflict (NERR_BASE+144)
#define NERR_PasswordTooShort   (NERR_BASE+145)
#define NERR_PasswordTooRecent  (NERR_BASE+146)
#define NERR_InvalidDatabase    (NERR_BASE+147)
#define NERR_DatabaseUpToDate   (NERR_BASE+148)
#define NERR_SyncRequired       (NERR_BASE+149)
#define NERR_UseNotFound        (NERR_BASE+150)
#define NERR_BadAsgType         (NERR_BASE+151)
#define NERR_DeviceIsShared     (NERR_BASE+152)
#define NERR_SameAsComputerName (NERR_BASE+153)
#define NERR_NoComputerName     (NERR_BASE+170)
#define NERR_MsgAlreadyStarted  (NERR_BASE+171)
#define NERR_MsgInitFailed      (NERR_BASE+172)
#define NERR_NameNotFound       (NERR_BASE+173)
#define NERR_AlreadyForwarded   (NERR_BASE+174)
#define NERR_AddForwarded       (NERR_BASE+175)
#define NERR_AlreadyExists      (NERR_BASE+176)
#define NERR_TooManyNames       (NERR_BASE+177)
#define NERR_DelComputerName    (NERR_BASE+178)
#define NERR_LocalForward       (NERR_BASE+179)
#define NERR_GrpMsgProcessor    (NERR_BASE+180)
#define NERR_PausedRemote       (NERR_BASE+181)
#define NERR_BadReceive         (NERR_BASE+182)
#define NERR_NameInUse          (NERR_BASE+183)
#define NERR_MsgNotStarted      (NERR_BASE+184)
#define NERR_NotLocalName       (NERR_BASE+185)
#define NERR_NoForwardName      (NERR_BASE+186)
#define NERR_RemoteFull         (NERR_BASE+187)
#define NERR_NameNotForwarded   (NERR_BASE+188)
#define NERR_TruncatedBroadcast (NERR_BASE+189)
#define NERR_InvalidDevice      (NERR_BASE+194)
#define NERR_WriteFault         (NERR_BASE+195)
#define NERR_DuplicateName      (NERR_BASE+197)
#define NERR_DeleteLater        (NERR_BASE+198)
#define NERR_IncompleteDel      (NERR_BASE+199)
#define NERR_MultipleNets       (NERR_BASE+200)
#define NERR_NetNameNotFound    (NERR_BASE+210)
#define NERR_DeviceNotShared    (NERR_BASE+211)
#define NERR_ClientNameNotFound (NERR_BASE+212)
#define NERR_FileIdNotFound     (NERR_BASE+214)
#define NERR_ExecFailure        (NERR_BASE+215)
#define NERR_TmpFile            (NERR_BASE+216)
#define NERR_TooMuchData        (NERR_BASE+217)
#define NERR_DeviceShareConflict (NERR_BASE+218)
#define NERR_BrowserTableIncomplete (NERR_BASE+219)
#define NERR_NotLocalDomain     (NERR_BASE+220)
#define NERR_IsDfsShare         (NERR_BASE+221)
#define NERR_DevInvalidOpCode   (NERR_BASE+231)
#define NERR_DevNotFound        (NERR_BASE+232)
#define NERR_DevNotOpen         (NERR_BASE+233)
#define NERR_BadQueueDevString  (NERR_BASE+234)
#define NERR_BadQueuePriority   (NERR_BASE+235)
#define NERR_NoCommDevs         (NERR_BASE+237)
#define NERR_QueueNotFound      (NERR_BASE+238)
#define NERR_BadDevString       (NERR_BASE+240)
#define NERR_BadDev             (NERR_BASE+241)
#define NERR_InUseBySpooler     (NERR_BASE+242)
#define NERR_CommDevInUse       (NERR_BASE+243)
#define NERR_InvalidComputer   (NERR_BASE+251)
#define NERR_MaxLenExceeded    (NERR_BASE+254)
#define NERR_BadComponent      (NERR_BASE+256)
#define NERR_CantType          (NERR_BASE+257)
#define NERR_TooManyEntries    (NERR_BASE+262)
#define NERR_ProfileFileTooBig  (NERR_BASE+270)
#define NERR_ProfileOffset      (NERR_BASE+271)
#define NERR_ProfileCleanup     (NERR_BASE+272)
#define NERR_ProfileUnknownCmd  (NERR_BASE+273)
#define NERR_ProfileLoadErr     (NERR_BASE+274)
#define NERR_ProfileSaveErr     (NERR_BASE+275)
#define NERR_LogOverflow           (NERR_BASE+277)
#define NERR_LogFileChanged        (NERR_BASE+278)
#define NERR_LogFileCorrupt        (NERR_BASE+279)
#define NERR_SourceIsDir   (NERR_BASE+280)
#define NERR_BadSource     (NERR_BASE+281)
#define NERR_BadDest       (NERR_BASE+282)
#define NERR_DifferentServers   (NERR_BASE+283)
#define NERR_RunSrvPaused       (NERR_BASE+285)
#define NERR_ErrCommRunSrv      (NERR_BASE+289)
#define NERR_ErrorExecingGhost  (NERR_BASE+291)
#define NERR_ShareNotFound      (NERR_BASE+292)
#define NERR_InvalidLana        (NERR_BASE+300)
#define NERR_OpenFiles          (NERR_BASE+301)
#define NERR_ActiveConns        (NERR_BASE+302)
#define NERR_BadPasswordCore    (NERR_BASE+303)
#define NERR_DevInUse           (NERR_BASE+304)
#define NERR_LocalDrive         (NERR_BASE+305)
#define NERR_AlertExists        (NERR_BASE+330)
#define NERR_TooManyAlerts      (NERR_BASE+331)
#define NERR_NoSuchAlert        (NERR_BASE+332)
#define NERR_BadRecipient       (NERR_BASE+333)
#define NERR_AcctLimitExceeded  (NERR_BASE+334)
#define NERR_InvalidLogSeek     (NERR_BASE+340)
#define NERR_BadUasConfig       (NERR_BASE+350)
#define NERR_InvalidUASOp       (NERR_BASE+351)
#define NERR_LastAdmin          (NERR_BASE+352)
#define NERR_DCNotFound         (NERR_BASE+353)
#define NERR_LogonTrackingError (NERR_BASE+354)
#define NERR_NetlogonNotStarted (NERR_BASE+355)
#define NERR_CanNotGrowUASFile  (NERR_BASE+356)
#define NERR_TimeDiffAtDC       (NERR_BASE+357)
#define NERR_PasswordMismatch   (NERR_BASE+358)
#define NERR_NoSuchServer       (NERR_BASE+360)
#define NERR_NoSuchSession      (NERR_BASE+361)
#define NERR_NoSuchConnection   (NERR_BASE+362)
#define NERR_TooManyServers     (NERR_BASE+363)
#define NERR_TooManySessions    (NERR_BASE+364)
#define NERR_TooManyConnections (NERR_BASE+365)
#define NERR_TooManyFiles       (NERR_BASE+366)
#define NERR_NoAlternateServers (NERR_BASE+367)
#define NERR_TryDownLevel       (NERR_BASE+370)
#define NERR_UPSDriverNotStarted    (NERR_BASE+380)
#define NERR_UPSInvalidConfig       (NERR_BASE+381)
#define NERR_UPSInvalidCommPort     (NERR_BASE+382)
#define NERR_UPSSignalAsserted      (NERR_BASE+383)
#define NERR_UPSShutdownFailed      (NERR_BASE+384)
#define NERR_BadDosRetCode      (NERR_BASE+400)
#define NERR_ProgNeedsExtraMem  (NERR_BASE+401)
#define NERR_BadDosFunction     (NERR_BASE+402)
#define NERR_RemoteBootFailed   (NERR_BASE+403)
#define NERR_BadFileCheckSum    (NERR_BASE+404)
#define NERR_NoRplBootSystem    (NERR_BASE+405)
#define NERR_RplLoadrNetBiosErr (NERR_BASE+406)
#define NERR_RplLoadrDiskErr    (NERR_BASE+407)
#define NERR_ImageParamErr      (NERR_BASE+408)
#define NERR_TooManyImageParams (NERR_BASE+409)
#define NERR_NonDosFloppyUsed   (NERR_BASE+410)
#define NERR_RplBootRestart     (NERR_BASE+411)
#define NERR_RplSrvrCallFailed  (NERR_BASE+412)
#define NERR_CantConnectRplSrvr (NERR_BASE+413)
#define NERR_CantOpenImageFile  (NERR_BASE+414)
#define NERR_CallingRplSrvr     (NERR_BASE+415)
#define NERR_StartingRplBoot    (NERR_BASE+416)
#define NERR_RplBootServiceTerm (NERR_BASE+417)
#define NERR_RplBootStartFailed (NERR_BASE+418)
#define NERR_RPL_CONNECTED      (NERR_BASE+419)
#define NERR_BrowserConfiguredToNotRun     (NERR_BASE+450)
#define NERR_RplNoAdaptersStarted          (NERR_BASE+510)
#define NERR_RplBadRegistry                (NERR_BASE+511)
#define NERR_RplBadDatabase                (NERR_BASE+512)
#define NERR_RplRplfilesShare              (NERR_BASE+513)
#define NERR_RplNotRplServer               (NERR_BASE+514)
#define NERR_RplCannotEnum                 (NERR_BASE+515)
#define NERR_RplWkstaInfoCorrupted         (NERR_BASE+516)
#define NERR_RplWkstaNotFound              (NERR_BASE+517)
#define NERR_RplWkstaNameUnavailable       (NERR_BASE+518)
#define NERR_RplProfileInfoCorrupted       (NERR_BASE+519)
#define NERR_RplProfileNotFound            (NERR_BASE+520)
#define NERR_RplProfileNameUnavailable     (NERR_BASE+521)
#define NERR_RplProfileNotEmpty            (NERR_BASE+522)
#define NERR_RplConfigInfoCorrupted        (NERR_BASE+523)
#define NERR_RplConfigNotFound             (NERR_BASE+524)
#define NERR_RplAdapterInfoCorrupted       (NERR_BASE+525)
#define NERR_RplInternal                   (NERR_BASE+526)
#define NERR_RplVendorInfoCorrupted        (NERR_BASE+527)
#define NERR_RplBootInfoCorrupted          (NERR_BASE+528)
#define NERR_RplWkstaNeedsUserAcct         (NERR_BASE+529)
#define NERR_RplNeedsRPLUSERAcct           (NERR_BASE+530)
#define NERR_RplBootNotFound               (NERR_BASE+531)
#define NERR_RplIncompatibleProfile        (NERR_BASE+532)
#define NERR_RplAdapterNameUnavailable     (NERR_BASE+533)
#define NERR_RplConfigNotEmpty             (NERR_BASE+534)
#define NERR_RplBootInUse                  (NERR_BASE+535)
#define NERR_RplBackupDatabase             (NERR_BASE+536)
#define NERR_RplAdapterNotFound            (NERR_BASE+537)
#define NERR_RplVendorNotFound             (NERR_BASE+538)
#define NERR_RplVendorNameUnavailable      (NERR_BASE+539)
#define NERR_RplBootNameUnavailable        (NERR_BASE+540)
#define NERR_RplConfigNameUnavailable      (NERR_BASE+541)
#define NERR_DfsInternalCorruption         (NERR_BASE+560)
#define NERR_DfsVolumeDataCorrupt          (NERR_BASE+561)
#define NERR_DfsNoSuchVolume               (NERR_BASE+562)
#define NERR_DfsVolumeAlreadyExists        (NERR_BASE+563)
#define NERR_DfsAlreadyShared              (NERR_BASE+564)
#define NERR_DfsNoSuchShare                (NERR_BASE+565)
#define NERR_DfsNotALeafVolume             (NERR_BASE+566)
#define NERR_DfsLeafVolume                 (NERR_BASE+567)
#define NERR_DfsVolumeHasMultipleServers   (NERR_BASE+568)
#define NERR_DfsCantCreateJunctionPoint    (NERR_BASE+569)
#define NERR_DfsServerNotDfsAware          (NERR_BASE+570)
#define NERR_DfsBadRenamePath              (NERR_BASE+571)
#define NERR_DfsVolumeIsOffline            (NERR_BASE+572)
#define NERR_DfsNoSuchServer               (NERR_BASE+573)
#define NERR_DfsCyclicalName               (NERR_BASE+574)
#define NERR_DfsNotSupportedInServerDfs    (NERR_BASE+575)
#define NERR_DfsDuplicateService           (NERR_BASE+576)
#define NERR_DfsCantRemoveLastServerShare  (NERR_BASE+577)
#define NERR_DfsVolumeIsInterDfs           (NERR_BASE+578)
#define NERR_DfsInconsistent               (NERR_BASE+579)
#define NERR_DfsServerUpgraded             (NERR_BASE+580)
#define NERR_DfsDataIsIdentical            (NERR_BASE+581)
#define NERR_DfsCantRemoveDfsRoot          (NERR_BASE+582)
#define NERR_DfsChildOrParentInDfs         (NERR_BASE+583)
#define NERR_DfsInternalError              (NERR_BASE+590)
#define NERR_SetupAlreadyJoined            (NERR_BASE+591)
#define NERR_SetupNotJoined                (NERR_BASE+592)
#define NERR_SetupDomainController         (NERR_BASE+593)
#define NERR_DefaultJoinRequired           (NERR_BASE+594)
#define NERR_InvalidWorkgroupName          (NERR_BASE+595)
#define NERR_NameUsesIncompatibleCodePage  (NERR_BASE+596)
#define NERR_ComputerAccountNotFound       (NERR_BASE+597)
#define NERR_PersonalSku                   (NERR_BASE+598)
#define NERR_SetupCheckDNSConfig           (NERR_BASE+599)
#define NERR_AlreadyCloudDomainJoined      (NERR_BASE+600)
#define NERR_PasswordMustChange            (NERR_BASE + 601)
#define NERR_AccountLockedOut              (NERR_BASE + 602)
#define NERR_PasswordTooLong               (NERR_BASE + 603)
#define NERR_PasswordNotComplexEnough      (NERR_BASE + 604)
#define NERR_PasswordFilterError           (NERR_BASE + 605)
#define NERR_NoOfflineJoinInfo             (NERR_BASE + 609)
#define NERR_BadOfflineJoinInfo            (NERR_BASE + 610)
#define NERR_CantCreateJoinInfo            (NERR_BASE + 611)
#define NERR_BadDomainJoinInfo             (NERR_BASE + 612)
#define NERR_JoinPerformedMustRestart      (NERR_BASE + 613)
#define NERR_NoJoinPending                 (NERR_BASE + 614)
#define NERR_ValuesNotSet                  (NERR_BASE + 615)
#define NERR_CantVerifyHostname            (NERR_BASE + 616)
#define NERR_CantLoadOfflineHive           (NERR_BASE + 617)
#define NERR_ConnectionInsecure            (NERR_BASE + 618)
#define NERR_ProvisioningBlobUnsupported   (NERR_BASE + 619)
#define NERR_DS8DCRequired                 (NERR_BASE + 620)
#define NERR_LDAPCapableDCRequired         (NERR_BASE + 621)
#define NERR_DS8DCNotFound                 (NERR_BASE + 622)
#define NERR_TargetVersionUnsupported      (NERR_BASE + 623)
#define NERR_InvalidMachineNameForJoin     (NERR_BASE + 624)
#define NERR_DS9DCNotFound                 (NERR_BASE + 625)
#define NERR_PlainTextSecretsRequired      (NERR_BASE + 626)
#define NERR_CannotUnjoinAadDomain         (NERR_BASE + 627)
#define MAX_NERR                (NERR_BASE+899)
/* END LMERR_PORT */

#endif


