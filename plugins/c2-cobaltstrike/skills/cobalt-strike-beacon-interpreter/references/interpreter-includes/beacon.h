#include <wintypes.h>

typedef struct _DATA_P {
    char *original;
    char *buffer;
    int length;
    int size;
} datap;

BEACON$BeaconDataParse: cdecl void (ptr, cstr, i32);
BEACON$BeaconDataPtr: cdecl cstr (ptr, i32);
BEACON$BeaconDataInt: cdecl i32 (ptr);
BEACON$BeaconDataShort: cdecl i16 (ptr);
BEACON$BeaconDataLength: cdecl i32 (ptr);
BEACON$BeaconDataExtract: cdecl cstr (ptr, ptr);

typedef struct _FORMAT_P {
    char *original;
    char *buffer;
    int length;
    int size;
} formatp;

BEACON$BeaconFormatAlloc: cdecl void (ptr, i32);
BEACON$BeaconFormatReset: cdecl void (ptr);
BEACON$BeaconFormatAppend: cdecl void (ptr, cstr, i32);
BEACON$BeaconFormatPrintf: cdecl void (ptr, cstr, ...);
BEACON$BeaconFormatToString: cdecl cstr (ptr, ptr);
BEACON$BeaconFormatFree: cdecl void (ptr);
BEACON$BeaconFormatInt: cdecl void (ptr, i32);

#define CALLBACK_OUTPUT 0
#define CALLBACK_OUTPUT_OEM 0x1e
#define CALLBACK_OUTPUT_UTF8 0x20
#define CALLBACK_ERROR 0x0d
#define CALLBACK_CUSTOM 0x1000
#define CALLBACK_CUSTOM_LAST 0x13ff

BEACON$BeaconOutput: cdecl void (i32, cstr, i32);
BEACON$BeaconPrintf: cdecl void (i32, cstr, ...);
BEACON$BeaconDownload: cdecl i32 (cstr, cstr, u32);

BEACON$BeaconUseToken: cdecl i32 (ptr);
BEACON$BeaconRevertToken: cdecl void ();
BEACON$BeaconIsAdmin: cdecl i32 ();

BEACON$BeaconGetSpawnTo: cdecl void (i32, cstr, i32);
BEACON$BeaconInjectProcess: cdecl void (ptr, i32, ptr, i32, i32, ptr, i32);
BEACON$BeaconInjectTemporaryProcess: cdecl void (ptr, ptr, i32, i32, ptr, i32);
BEACON$BeaconSpawnTemporaryProcess: cdecl i32 (i32, i32, ptr, ptr);
BEACON$BeaconCleanupProcess: cdecl void (ptr);

BEACON$toWideChar: cdecl i32 (cstr, cstr, i32);

typedef struct _HEAP_RECORD {
	char * ptr;
	size_t size;
} HEAP_RECORD;
#define MASK_SIZE 13

typedef enum {
	PURPOSE_EMPTY,
	PURPOSE_GENERIC_BUFFER,
	PURPOSE_BEACON_MEMORY,
	PURPOSE_SLEEPMASK_MEMORY,
	PURPOSE_BOF_MEMORY,
	PURPOSE_UDC2_MEMORY,
	PURPOSE_USER_DEFINED_MEMORY = 1000
} ALLOCATED_MEMORY_PURPOSE;

typedef enum {
	LABEL_EMPTY,
	LABEL_BUFFER,
	LABEL_PEHEADER,
	LABEL_TEXT,
	LABEL_RDATA,
	LABEL_DATA,
	LABEL_PDATA,
	LABEL_RELOC,
	LABEL_USER_DEFINED = 1000
} ALLOCATED_MEMORY_LABEL;

typedef enum {
	METHOD_UNKNOWN,
	METHOD_VIRTUALALLOC,
	METHOD_HEAPALLOC,
	METHOD_MODULESTOMP,
	METHOD_NTMAPVIEW,
	METHOD_USER_DEFINED = 1000,
} ALLOCATED_MEMORY_ALLOCATION_METHOD;

typedef struct _HEAPALLOC_INFO {
	PVOID HeapHandle;
	BOOL  DestroyHeap;
} HEAPALLOC_INFO, *PHEAPALLOC_INFO;

typedef struct _MODULESTOMP_INFO {
	HMODULE ModuleHandle;
} MODULESTOMP_INFO, *PMODULESTOMP_INFO;

typedef union _ALLOCATED_MEMORY_ADDITIONAL_CLEANUP_INFORMATION {
	HEAPALLOC_INFO HeapAllocInfo;
	MODULESTOMP_INFO ModuleStompInfo;
	PVOID Custom;
} ALLOCATED_MEMORY_ADDITIONAL_CLEANUP_INFORMATION, *PALLOCATED_MEMORY_ADDITIONAL_CLEANUP_INFORMATION;

typedef struct _ALLOCATED_MEMORY_CLEANUP_INFORMATION {
	BOOL Cleanup;
	ALLOCATED_MEMORY_ALLOCATION_METHOD AllocationMethod;
	ALLOCATED_MEMORY_ADDITIONAL_CLEANUP_INFORMATION AdditionalCleanupInformation;
} ALLOCATED_MEMORY_CLEANUP_INFORMATION, *PALLOCATED_MEMORY_CLEANUP_INFORMATION;

typedef struct _ALLOCATED_MEMORY_SECTION {
	ALLOCATED_MEMORY_LABEL Label; // A label to simplify Sleepmask development
	PVOID  BaseAddress;           // Pointer to virtual address of section
	SIZE_T VirtualSize;           // Virtual size of the section
	DWORD  CurrentProtect;        // Current memory protection of the section
	DWORD  PreviousProtect;       // The previous memory protection of the section (prior to masking/unmasking)
	BOOL   MaskSection;           // A boolean to indicate whether the section should be masked
	DWORD  DripLoadPageSize;      // The page size used when committing memory during drip-loading
} ALLOCATED_MEMORY_SECTION, *PALLOCATED_MEMORY_SECTION;

typedef struct _ALLOCATED_MEMORY_REGION {
	ALLOCATED_MEMORY_PURPOSE Purpose;      // A label to indicate the purpose of the allocated memory
	PVOID  AllocationBase;                 // The base address of the allocated memory block
	SIZE_T RegionSize;                     // The size of the allocated memory block
	DWORD Type;                            // The type of memory allocated
	DWORD DripLoadAllocationGranularity;   // The allocation granularity used when reserving memory for drip-loading
	ALLOCATED_MEMORY_SECTION Sections[8];  // An array of section information structures
	ALLOCATED_MEMORY_CLEANUP_INFORMATION CleanupInformation; // Information required to cleanup the allocation
} ALLOCATED_MEMORY_REGION, *PALLOCATED_MEMORY_REGION;

typedef struct _ALLOCATED_MEMORY {
	ALLOCATED_MEMORY_REGION AllocatedMemoryRegions[6];
} ALLOCATED_MEMORY, *PALLOCATED_MEMORY;

typedef struct _BEACON_INFO {
	unsigned int version;
	char  * sleep_mask_ptr;
	DWORD   sleep_mask_text_size;
	DWORD   sleep_mask_total_size;

	char  * beacon_ptr;
	HEAP_RECORD * heap_records;
	char    mask[MASK_SIZE];

	ALLOCATED_MEMORY allocatedMemory;
} BEACON_INFO, *PBEACON_INFO;

BEACON$BeaconInformation: cdecl i32 (ptr);

BEACON$BeaconAddValue: cdecl i32 (cstr, ptr);
BEACON$BeaconGetValue: cdecl ptr (cstr);
BEACON$BeaconRemoveValue: cdecl i32 (cstr);

#define DATA_STORE_TYPE_EMPTY 0
#define DATA_STORE_TYPE_GENERAL_FILE 1

typedef struct _DATA_STORE_OBJECT {
	int type;
	unsigned long long hash;
	BOOL masked;
	char* buffer;
	size_t length;
} DATA_STORE_OBJECT, *PDATA_STORE_OBJECT;

BEACON$BeaconDataStoreGetItem: cdecl ptr (size_t);
BEACON$BeaconDataStoreProtectItem: cdecl void (size_t);
BEACON$BeaconDataStoreUnprotectItem: cdecl void (size_t);
BEACON$BeaconDataStoreMaxEntries: cdecl size_t ();

BEACON$BeaconGetCustomUserData: cdecl cstr ();

typedef struct _SYSCALL_API_ENTRY
{
	PVOID fnAddr;
	PVOID jmpAddr;
	DWORD sysnum;
} SYSCALL_API_ENTRY, *PSYSCALL_API_ENTRY;

typedef struct _SYSCALL_API
{
	SYSCALL_API_ENTRY ntAllocateVirtualMemory;
	SYSCALL_API_ENTRY ntProtectVirtualMemory;
	SYSCALL_API_ENTRY ntFreeVirtualMemory;
	SYSCALL_API_ENTRY ntGetContextThread;
	SYSCALL_API_ENTRY ntSetContextThread;
	SYSCALL_API_ENTRY ntResumeThread;
	SYSCALL_API_ENTRY ntCreateThreadEx;
	SYSCALL_API_ENTRY ntOpenProcess;
	SYSCALL_API_ENTRY ntOpenThread;
	SYSCALL_API_ENTRY ntClose;
	SYSCALL_API_ENTRY ntCreateSection;
	SYSCALL_API_ENTRY ntMapViewOfSection;
	SYSCALL_API_ENTRY ntUnmapViewOfSection;
	SYSCALL_API_ENTRY ntQueryVirtualMemory;
	SYSCALL_API_ENTRY ntDuplicateObject;
	SYSCALL_API_ENTRY ntReadVirtualMemory;
	SYSCALL_API_ENTRY ntWriteVirtualMemory;
	SYSCALL_API_ENTRY ntReadFile;
	SYSCALL_API_ENTRY ntWriteFile;
	SYSCALL_API_ENTRY ntCreateFile;
	SYSCALL_API_ENTRY ntQueueApcThread;
	SYSCALL_API_ENTRY ntCreateProcess;
	SYSCALL_API_ENTRY ntOpenProcessToken;
	SYSCALL_API_ENTRY ntTestAlert;
	SYSCALL_API_ENTRY ntSuspendProcess;
	SYSCALL_API_ENTRY ntResumeProcess;
	SYSCALL_API_ENTRY ntQuerySystemInformation;
	SYSCALL_API_ENTRY ntQueryDirectoryFile;
	SYSCALL_API_ENTRY ntSetInformationProcess;
	SYSCALL_API_ENTRY ntSetInformationThread;
	SYSCALL_API_ENTRY ntQueryInformationProcess;
	SYSCALL_API_ENTRY ntQueryInformationThread;
	SYSCALL_API_ENTRY ntOpenSection;
	SYSCALL_API_ENTRY ntAdjustPrivilegesToken;
	SYSCALL_API_ENTRY ntDeviceIoControlFile;
	SYSCALL_API_ENTRY ntWaitForMultipleObjects;
} SYSCALL_API, *PSYSCALL_API;

typedef struct _RTL_API
{
	PVOID rtlDosPathNameToNtPathNameUWithStatusAddr;
	PVOID rtlFreeHeapAddr;
	PVOID rtlGetProcessHeapAddr;
} RTL_API, *PRTL_API;

typedef struct _BEACON_SYSCALLS
{
	SYSCALL_API syscalls;
	RTL_API     rtls;
} BEACON_SYSCALLS, *PBEACON_SYSCALLS;

BEACON$BeaconGetSyscallInformation: i32 (ptr, size_t, i32);

BEACON$BeaconVirtualAlloc: cdecl ptr (ptr, size_t, u32, u32);
BEACON$BeaconVirtualAllocEx: cdecl ptr (ptr, ptr, size_t, u32, u32);
BEACON$BeaconVirtualProtect: cdecl i32 (ptr, size_t, u32, ptr);
BEACON$BeaconVirtualProtectEx: cdecl i32 (ptr, ptr, size_t, u32, ptr);
BEACON$BeaconVirtualFree: cdecl i32 (ptr, size_t, u32);
BEACON$BeaconGetThreadContext: cdecl i32 (ptr, ptr);
BEACON$BeaconSetThreadContext: cdecl i32 (ptr, ptr);
BEACON$BeaconResumeThread: cdecl u32 (ptr);
BEACON$BeaconOpenProcess: cdecl ptr (u32, i32, u32);
BEACON$BeaconOpenThread: cdecl ptr (u32, i32, u32);
BEACON$BeaconCloseHandle: cdecl i32 (ptr);
BEACON$BeaconUnmapViewOfFile: cdecl i32 (ptr);
BEACON$BeaconVirtualQuery: cdecl size_t (ptr, ptr, size_t);
BEACON$BeaconDuplicateHandle: cdecl i32 (ptr, ptr, ptr, ptr, u32, i32, u32);
BEACON$BeaconReadProcessMemory: cdecl i32 (ptr, ptr, ptr, size_t, ptr);
BEACON$BeaconWriteProcessMemory: cdecl i32 (ptr, ptr, ptr, size_t, ptr);

BEACON$BeaconDisableBeaconGate: cdecl void ();
BEACON$BeaconEnableBeaconGate: cdecl void ();
BEACON$BeaconDisableBeaconGateMasking: cdecl void ();
BEACON$BeaconEnableBeaconGateMasking: cdecl void ();

#define DLL_BEACON_USER_DATA 0x0d
#define BEACON_USER_DATA_CUSTOM_SIZE 32
typedef struct _USER_DATA
{
	unsigned int version;
	PSYSCALL_API syscalls;
	char         custom[BEACON_USER_DATA_CUSTOM_SIZE];
	PRTL_API     rtls;
	PALLOCATED_MEMORY allocatedMemory;
} USER_DATA, * PUSER_DATA;
