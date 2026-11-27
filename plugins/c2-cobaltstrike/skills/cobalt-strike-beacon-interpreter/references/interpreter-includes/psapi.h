#ifndef BUILTINS_PSAPI_H
#define BUILTINS_PSAPI_H

#include <winnt.h>

/* Module enumeration filters */
#define LIST_MODULES_DEFAULT 0x0
#define LIST_MODULES_32BIT   0x01
#define LIST_MODULES_64BIT   0x02
#define LIST_MODULES_ALL     (LIST_MODULES_32BIT | LIST_MODULES_64BIT)

typedef struct _MODULEINFO {
    LPVOID lpBaseOfDll;
    DWORD SizeOfImage;
    LPVOID EntryPoint;
} MODULEINFO, *LPMODULEINFO;

typedef struct _PSAPI_WS_WATCH_INFORMATION {
    LPVOID FaultingPc;
    LPVOID FaultingVa;
} PSAPI_WS_WATCH_INFORMATION, *PPSAPI_WS_WATCH_INFORMATION;

typedef struct _PSAPI_WS_WATCH_INFORMATION_EX {
    PSAPI_WS_WATCH_INFORMATION BasicInfo;
    ULONG_PTR FaultingThreadId;
    ULONG_PTR Flags;
} PSAPI_WS_WATCH_INFORMATION_EX, *PPSAPI_WS_WATCH_INFORMATION_EX;

/*
 * SDK uses anonymous unions/bitfields for these blocks.
 * Keep compatible layout by exposing the raw flags field.
 */
typedef struct _PSAPI_WORKING_SET_BLOCK {
    ULONG_PTR Flags;
} PSAPI_WORKING_SET_BLOCK, *PPSAPI_WORKING_SET_BLOCK;

typedef struct _PSAPI_WORKING_SET_INFORMATION {
    ULONG_PTR NumberOfEntries;
    PSAPI_WORKING_SET_BLOCK WorkingSetInfo[1];
} PSAPI_WORKING_SET_INFORMATION, *PPSAPI_WORKING_SET_INFORMATION;

typedef struct _PSAPI_WORKING_SET_EX_BLOCK {
    ULONG_PTR Flags;
} PSAPI_WORKING_SET_EX_BLOCK, *PPSAPI_WORKING_SET_EX_BLOCK;

typedef struct _PSAPI_WORKING_SET_EX_INFORMATION {
    PVOID VirtualAddress;
    PSAPI_WORKING_SET_EX_BLOCK VirtualAttributes;
} PSAPI_WORKING_SET_EX_INFORMATION, *PPSAPI_WORKING_SET_EX_INFORMATION;

typedef struct _PROCESS_MEMORY_COUNTERS {
    DWORD cb;
    DWORD PageFaultCount;
    SIZE_T PeakWorkingSetSize;
    SIZE_T WorkingSetSize;
    SIZE_T QuotaPeakPagedPoolUsage;
    SIZE_T QuotaPagedPoolUsage;
    SIZE_T QuotaPeakNonPagedPoolUsage;
    SIZE_T QuotaNonPagedPoolUsage;
    SIZE_T PagefileUsage;
    SIZE_T PeakPagefileUsage;
} PROCESS_MEMORY_COUNTERS, *PPROCESS_MEMORY_COUNTERS;

typedef struct _PROCESS_MEMORY_COUNTERS_EX {
    DWORD cb;
    DWORD PageFaultCount;
    SIZE_T PeakWorkingSetSize;
    SIZE_T WorkingSetSize;
    SIZE_T QuotaPeakPagedPoolUsage;
    SIZE_T QuotaPagedPoolUsage;
    SIZE_T QuotaPeakNonPagedPoolUsage;
    SIZE_T QuotaNonPagedPoolUsage;
    SIZE_T PagefileUsage;
    SIZE_T PeakPagefileUsage;
    SIZE_T PrivateUsage;
} PROCESS_MEMORY_COUNTERS_EX, *PPROCESS_MEMORY_COUNTERS_EX;

typedef struct _PERFORMANCE_INFORMATION {
    DWORD cb;
    SIZE_T CommitTotal;
    SIZE_T CommitLimit;
    SIZE_T CommitPeak;
    SIZE_T PhysicalTotal;
    SIZE_T PhysicalAvailable;
    SIZE_T SystemCache;
    SIZE_T KernelTotal;
    SIZE_T KernelPaged;
    SIZE_T KernelNonpaged;
    SIZE_T PageSize;
    DWORD HandleCount;
    DWORD ProcessCount;
    DWORD ThreadCount;
} PERFORMANCE_INFORMATION, *PPERFORMANCE_INFORMATION;
typedef PERFORMANCE_INFORMATION PERFORMACE_INFORMATION;
typedef PPERFORMANCE_INFORMATION PPERFORMACE_INFORMATION;

typedef struct _ENUM_PAGE_FILE_INFORMATION {
    DWORD cb;
    DWORD Reserved;
    SIZE_T TotalSize;
    SIZE_T TotalInUse;
    SIZE_T PeakUsage;
} ENUM_PAGE_FILE_INFORMATION, *PENUM_PAGE_FILE_INFORMATION;

PSAPI$EnumProcesses: u32 (ptr, u32, ptr);
PSAPI$EnumProcessModules: u32 (ptr, ptr, u32, ptr);
PSAPI$GetModuleBaseNameA: u32 (ptr, ptr, ptr, u32);
PSAPI$GetModuleBaseNameW: u32 (ptr, ptr, ptr, u32);
PSAPI$GetModuleFileNameExA: u32 (ptr, ptr, ptr, u32);
PSAPI$GetModuleFileNameExW: u32 (ptr, ptr, ptr, u32);
PSAPI$GetModuleInformation: u32 (ptr, ptr, ptr, u32);
PSAPI$EmptyWorkingSet: u32 (ptr);
PSAPI$QueryWorkingSet: u32 (ptr, ptr, u32);
PSAPI$QueryWorkingSetEx: u32 (ptr, ptr, u32);
PSAPI$InitializeProcessForWsWatch: u32 (ptr);
PSAPI$GetWsChanges: u32 (ptr, ptr, u32);
PSAPI$GetMappedFileNameW: u32 (ptr, ptr, ptr, u32);
PSAPI$GetMappedFileNameA: u32 (ptr, ptr, ptr, u32);
PSAPI$EnumDeviceDrivers: u32 (ptr, u32, ptr);
PSAPI$GetDeviceDriverBaseNameA: u32 (ptr, ptr, u32);
PSAPI$GetDeviceDriverBaseNameW: u32 (ptr, ptr, u32);
PSAPI$GetDeviceDriverFileNameA: u32 (ptr, ptr, u32);
PSAPI$GetDeviceDriverFileNameW: u32 (ptr, ptr, u32);
PSAPI$GetProcessMemoryInfo: u32 (ptr, ptr, u32);
PSAPI$GetPerformanceInfo: u32 (ptr, u32);
PSAPI$EnumPageFilesW: u32 (ptr, ptr);
PSAPI$EnumPageFilesA: u32 (ptr, ptr);
PSAPI$GetProcessImageFileNameA: u32 (ptr, ptr, u32);
PSAPI$GetProcessImageFileNameW: u32 (ptr, ptr, u32);
PSAPI$GetWsChangesEx: u32 (ptr, ptr, u32);
PSAPI$EnumProcessModulesEx: u32 (ptr, ptr, u32, ptr, u32);

#endif
