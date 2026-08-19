# Post-ex User Defined Reflective DLL Loader

Cobalt Strike 4.9 added support for using customer reflective loaders for the post-ex payloads. The Post-ex User Defined Reflective Loader example is part of the udrl-vs kit in the Arsenal Kit. Got to Help -> Arsenal and download the Arsenal Kit. Your licence key is required.

A Post-ex User Defined Reflective Loader can only be applied to the following post-ex DLLs:

| Beacon Command   | Aggressor Script Function     | DLL Name       |
| ---------------- | ----------------------------- | -------------- |
| browserpivot     | bbrowserpivot                 | browserpivot   |
| hashdump         | bhashdump                     | hashdump       |
| execute-assembly | bexecute_assembly             | invokeassembly |
| keylogger        | bkeylogger                    | keylogger      |
| chromedump       | N/A                           | mimikatz       |
| logonpasswords   | blogonpasswords               | mimikatz       |
| mimikatz         | bmimikatz and bmimikatz_small | mimikatz       |
| pth              | bpassthehash                  | mimikatz       |
| net              | bnet                          | netview        |
| portscan         | bportscan                     | portscan       |
| powerpick        | bpowerpick                    | powershell     |
| psinject         | bpsinject                     | powershell     |
| printscreen      | bprintscreen                  | screenshot     |
| screenshot       | bscreenshot                   | screenshot     |
| screenwatch      | bscreenwatch                  | screenshot     |
| ssh-key          | bssh_key                      | shagent        |
| ssh              | bssh                          | sshagent       |

## Implementation

The following Aggressor script hook is provided to allow implementation of Post-ex User Defined Reflective Loaders:

| Function             | Description                                                                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| POSTEX_RDLL_GENERATE | Hook used to implement Reflective Loader replacement for post-ex DLLs. Arguments provided include Beacon ID, GetModuleHandleA address, and GetProcAddress address. |

## Using Post-ex User Defined Reflective DLL Loaders

### Create/Compile your Reflective Loaders

The Post-ex User Defined Reflective Loader example is part of the udrl-vs kit in the Arsenal Kit. Got to Help -> Arsenal and download the Arsenal Kit. Your license key is required. Please note that User Defined Reflective Loaders for Beacon payloads and post-ex payloads are very similar but have some subtle differences.

The loader entry function is called with the WinAPI calling convention, and it takes a single LPVOID argument. Therefore, the entry function must be declared as follows:

```
void WINAPI ReflectiveLoader(LPVOID loaderArgument)
```

Post-exploitation payloads assume that the DLL's entry point is called with the following order and arguments:

```
DllMain(<Loaded DLL Base Address>, DLL_PROCESS_ATTACH, <Pointer to RDATA_SECTION strucutre>);
DllMain(<Loader Base Address>, 4, <Loader Argument from the entry function>);
```

The RDATA_SECTION point argument is as some long-running post-exploitation payloads obfuscate their .rdata section during the waiting period. It is the loader's responsibility to provide the following structure to the DLL. However, if the NULL value is passed then the DLL does not perform runtime obfuscation.

```
typedef struct {
   char* start; // The start address of the .rdata section
   DWORD length; // The length (Size of Raw Data) of the .rdata section
   DWORD offset; // The obfuscation start offset
} RDATA_SECTION, *PRDATA_SECTION;
```

The obfuscation start offset ensures that the Import Address Table (IAT) will not be obfuscated. Typically, this value should be set to the size of the IMAGE_DIRECTORY_ENTRY_IAT Data Directory entry as follows:

```
rdata->offset = ntHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IAT].Size;
```