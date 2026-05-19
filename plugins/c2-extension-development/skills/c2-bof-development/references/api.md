# BOF C API

## BOF API Header File

The header file for `beacon.h` can be downloaded [here](https://hstechdocs.helpsystems.com/kbfiles/cobaltstrike/attachments/beacon.h)

## Data Parser API

The Data Parser API extracts arguments packed with Aggressor Script's &bof_pack function.

Extract a length-prefixed binary blob. The size argument may be NULL. If an address is provided, the size is populated with the number-of-bytes extracted.

```
char * BeaconDataExtract (datap * parser, int * size)
```

Extract a 4b integer.

```
int BeaconDataInt (datap * parser)
```

Get the amount of data left to parse.

```
int BeaconDataLength (datap * parser)
```

Prepare a data parser to extract arguments from the specified buffer.

```
void BeaconDataParse (datap * parser, char * buffer, int size)
```

Extract a binary blob with the specified size. Normally the size is prefixed before the blob in the buffer, so it is recommended to use the BeaconDataExtract API instead.

```
void BeaconDataPtr(datap * parser, int size)
```

Extract a 2b integer.

```
short BeaconDataShort (datap * parser)
```

## Output API

The Output API returns output to Cobalt Strike.

Format and present output to the Beacon operator.

```
void BeaconPrintf (int type, char * fmt, ...)
```

Send output to the Beacon operator.

```
void BeaconOutput (int type, char * data, int len)
```

Downloads an in-memory buffer via Beacon's native download functionality. Beacon will create its own copy of the provided buffer, allowing the Beacon Object File (BOF) to continue execution after calling the API and safely freeing the original memory. Go to View -> Downloads to view the file after it finishes downloading. The Sleepmask masks the buffer whilst Beacon is sleeping.

```
BOOL BeaconDownload (const char * filename, const char* buffer, unsigned int length);
```

Each of these functions accepts a type argument. This type determines how Cobalt Strike will process the output and what it will present the output as. The types are:

* CALLBACK_OUTPUT is generic output. Cobalt Strike will convert this output to UTF-16 (internally) using the target's default character set.
* CALLBACK_OUTPUT_OEM is generic output. Cobalt Strike will convert this output to UTF-16 (internally) using the target's OEM character set. You probably won't need this, unless you're dealing with output from cmd.exe.
* CALLBACK_ERROR is a generic error message.
* CALLBACK_OUTPUT_UTF8 is generic output. Cobalt Strike will convert this output to UTF-16 (internally) from UTF-8.

## Format API

The format API is used to build large or repeating output.

Allocate memory to format complex or large output.

```
void BeaconFormatAlloc (formatp * obj, int maxsz)
```

Append data to this format object.

```
void BeaconFormatAppend (formatp * obj, char * data, int len)
```

Free the format object.

```
void BeaconFormatFree (formatp * obj)
```

Append a 4b integer (big endian) to this object.

```
void BeaconFormatInt (formatp * obj, int val)
```

Append a formatted string to this object.

```
void BeaconFormatPrintf (formatp * obj, char * fmt, ...)
```

Resets the format object to its default state (prior to re-use).

```
void BeaconFormatReset (formatp * obj)
```

Extract formatted data into a single string. Populate the passed in size variable with the length of this string. These parameters are suitable for use with the BeaconOutput function.

```
char * BeaconFormatToString (formatp * obj, int * size)
```

## Internal APIs

The following functions manipulate the token used in the current Beacon context:

Apply the specified token as Beacon's current thread token. This will report the new token to the user too. Returns TRUE if successful. FALSE is not.

```
BOOL BeaconUseToken (HANDLE token)
```

Drop the current thread token. Use this over direct calls to RevertToSelf. This function cleans up other state information about the token.

```
void BeaconRevertToken ()
```

Returns TRUE if Beacon is in a high-integrity context.

```
BOOL BeaconIsAdmIn ()
```

The following functions provide some access to Beacon's process injection capability:

Populate the specified buffer with the x86 or x64 spawnto value configured for this Beacon session.

```
void BeaconGetSpawnTo (BOOL x86, char * buffer, int length)
```

This function spawns a temporary process accounting for ppid, spawnto, and blockdlls options. Grab the handle from PROCESS_INFORMATION to inject into or manipulate this process. Returns TRUE if successful.

```
BOOL BeaconSpawnTemporaryProcess (BOOL x86, BOOL ignoreToken, STARTUPINFO * sInfo, PROCESS_INFORMATION * pInfo)
```

This function will inject the specified payload into an existing process. Use payload_offset to specify the offset within the payload to begin execution. The arg value is for arguments. arg may be NULL.

```
void BeaconInjectProcess (HANDLE hProc, int pid, char * payload, int payload_len, int payload_offset, char * arg, int arg_len)
```

This function injects the specified payload into a temporary process that your BOF opted to launch. Use payload_offset to specify the offset within the payload to begin execution. The arg value is for arguments. arg may be NULL.

```
void BeaconInjectTemporaryProcess (PROCESS_INFORMATION * pInfo, char * payload, int payload_len, int payload_offset, char * arg, int arg_len)
```

This function cleans up some handles that are often forgotten about. Call this when you're done interacting with the handles for a process. You don't need to wait for the process to exit or finish.

```
void BeaconCleanupProcess (PROCESS_INFORMATION * pInfo)
```

The following functions are used to access stored items in Beacon Data Store:

Returns a pointer to the specific item. If there is no entry at that index, the function returns NULL.

```
PDATA_STORE_OBJECT BeaconDataStoreGetItem (size_t index)
```

This function obfuscates a specific item in Beacon Data Store.

```
void BeaconDataStoreProtectItem (size_t index)
```

This function un-obfuscates a specific item in Beacon Data Store.

```
void BeaconDataStoreUnprotectItem (size_t index)
```

Return the maximum size of Beacon Data Store.

```
size_t BeaconDataStoreMaxEntries ()
```

The following function is a utility function:

Convert the src string to a UTF16-LE wide-character string, using the target's default encoding. max is the size (in bytes!) of the destination buffer.

```
BOOL toWideChar (char * src, wchar_t * dst, int max)
```

This function returns information about beacon such as the beacon address, sections to mask, heap records to mask, the mask, sleep mask address and sleep mask size information.

```
void BeaconInformation (BEACON_INFO * info);
```

The following functions provide access to Beacon's key value store:

This function adds a memory address to an internal key value store to allow the ability to retrieve this value using the key in a subsequent BOF execution.

```
BOOL BeaconAddValue (const char * key, void * ptr);
```

This function retrieves the memory address that is associated with the key from the internal key value store. If the key is not found then NULL is returned.

```
void * BeaconGetValue (const char * key);
```

This function removes the key from the internal key value store. This will not do any memory clean up of the memory address and a finial execution of a BOF should do the necessary clean up in order to prevent memory leaks.

```
BOOL BeaconRemoveValue (const char * key);
```

The following function retrieves the custom data buffer from Beacon User Data.

```
char* BeaconGetCustomUserData ()
```

When a User Defined Reflective Loader provides Beacon User Data (BUD) during the loading process, then this function will return a pointer to the custom buffer array associated with the BUD. The size of this buffer array is fixed at 32 bytes, as defined in the USER_DATA structure. A valid memory pointer is always returned. If no BUD is provided by the User Defined Reflective Loader, then the pointer is to the default buffer array with all 32 values set to zero.

## System Call API

This function returns the BEACON_SYSCALLS data structure containing the resolved function addresses and system call numbers. This information is either resolved by beacon or is provided through a UDRL using the USER_DATA structure. This information can be useful for implementing your own system calls implementation within a BOF.

```
BOOL BeaconGetSyscallInformation(PBEACON_SYSCALLS info, BOOL resolveIfNotInitialized);
```

The following functions are provided to perform the specific Windows API using the current system call method (None, Direct, or Indirect) for the beacon process. Note, If the BeaconGate is currently configured and enabled for the specific Windows API then it will be proxied through the BeaconGate instead. The list of supported beacon system call APIs for a BOF is a subset of the internally supported system call APIs for beacon. The reason the full list is not supported is because those functions require additional setup and/or only support beacon’s specific use case and are not available for typical use. For those functions that are not supported you will have to implement your own system call if needed.

NOTE: Refer to the Microsoft Windows Documentation for more information on each of these APIs.

```
LPVOID BeaconVirtualAlloc(LPVOID lpAddress, SIZE_T dwSize, DWORD flAllocationType, DWORD flProtect);
```

```
LPVOID BeaconVirtualAllocEx(HANDLE processHandle, LPVOID lpAddress, SIZE_T dwSize, DWORD flAllocationType, DWORD flProtect);
```

```
BOOL BeaconVirtualProtect(LPVOID lpAddress, SIZE_T dwSize, DWORD flNewProtect, PDWORD lpflOldProtect);
```

```
BOOL BeaconVirtualProtectEx(HANDLE processHandle, LPVOID lpAddress, SIZE_T dwSize, DWORD flNewProtect, PDWORD lpflOldProtect);
```

```
BOOL BeaconVirtualFree(LPVOID lpAddress, SIZE_T dwSize, DWORD dwFreeType);
```

```
BOOL BeaconGetThreadContext(HANDLE threadHandle, PCONTEXT threadContext);
```

```
BOOL BeaconSetThreadContext(HANDLE threadHandle, PCONTEXT threadContext);
```

```
DWORD BeaconResumeThread(HANDLE threadHandle);
```

```
HANDLE BeaconOpenProcess(DWORD desiredAccess, BOOL inheritHandle, DWORD processId);
```

```
HANDLE BeaconOpenThread(DWORD desiredAccess, BOOL inheritHandle, DWORD threadId);
```

```
BOOL BeaconCloseHandle(HANDLE object);
```

```
BOOL BeaconUnmapViewOfFile(LPCVOID baseAddress);
```

```
SIZE_T BeaconVirtualQuery(LPCVOID address, PMEMORY_BASIC_INFORMATION buffer, SIZE_T length);
```

```
BOOL BeaconDuplicateHandle(HANDLE hSourceProcessHandle, HANDLE hSourceHandle, HANDLE hTargetProcessHandle, LPHANDLE lpTargetHandle, DWORD dwDesiredAccess, BOOL bInheritHandle, DWORD dwOptions);
```

```
BOOL BeaconReadProcessMemory(HANDLE hProcess, LPCVOID lpBaseAddress, LPVOID lpBuffer, SIZE_T nSize, SIZE_T *lpNumberOfBytesRead);
```

```
BOOL BeaconWriteProcessMemory(HANDLE hProcess, LPVOID lpBaseAddress, LPCVOID lpBuffer, SIZE_T nSize, SIZE_T *lpNumberOfBytesWritten);
```

## Beacon Gate API

The following functions provide access to enable or disable the beacon BeaconGate functionality within a BOF.

This function will disable the BeaconGate functionality, and the Windows APIs configured to use the BeaconGate will no longer be proxied.

```
VOID BeaconDisableBeaconGate();
```

This function will enable the BeaconGate functionality, and the Windows APIs configured to use the BeaconGate will now be proxied.

```
VOID BeaconEnableBeaconGate();
```

This function will disable the BeaconGate masking functionality, and the Windows APIs configured to use the BeaconGate will not mask Beacon.

```
VOID BeaconDisableBeaconGateMasking();
```

This function will enable the BeaconGate masking functionality, and the Windows APIs configured to use BeaconGate will mask Beacon.

```
VOID BeaconEnableBeaconGateMasking();
```
