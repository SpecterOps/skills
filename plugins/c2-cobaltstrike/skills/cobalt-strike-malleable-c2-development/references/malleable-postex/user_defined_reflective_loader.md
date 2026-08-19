# 

Cobalt Strike supports using customized reflective loaders for beacon payloads. The User Defined Reflective Loader (UDRL-VS) Kit is the source code for the UDRL example. Go to Help -> Arsenal and download the Arsenal Kit which includes the UDRL-VS Kit. Your license key is required.

> The reflective loader's executable code is the extracted .text section from a user provided compiled executable file.

## Implementation

The following Aggressor script hooks are provided to allow implementation of User Defined Reflective Loaders:

| Function                   | Description                                                                                                                                                           |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BEACON_RDLL_GENERATE       | Hook used to implement basic Reflective Loader replacement.                                                                                                           |
| BEACON_RDLL_GENERATE_LOCAL | Hook used to implement advanced Reflective Loader replacement. Additional arguments provided include Beacon ID, GetModuleHandleA address, and GetProcAddress address. |

The following Aggressor script functions are provided to modify the beacon payload using information from the Malleable C2 profile:

| Function              | Description                                                                               |
| --------------------- | ----------------------------------------------------------------------------------------- |
| setup_strings         | Apply the strings defined in the Malleable C2 profile to the beacon payload.              |
| setup_transformations | Apply the transformation rules defined in the Malleable C2 profile to the beacon payload. |

The following Aggressor script function is provided to obtain information about the beacon payload to assist with custom modifications to the payload:

| Function | Description                                                                                                                                           |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| pedump   | Loads a map of information about the beacon payload. This map information is similar to the output of the "peclone" command with the "dump" argument. |

The following Aggressor script functions are provided to perform custom modifications to the beacon payload:

> Depending on the custom modifications made (obfuscation, mask, etc...), the reflective loader may have to reverse those modifications when loading.

| Function                        | Description                                                                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| pe_insert_rich_header           | Insert rich header data into Beacon DLL Content. If there is existing rich header information, it will be replaced.                       |
| pe_mask                         | Mask data in the Beacon DLL Content based on position and length.                                                                         |
| pe_mask_section                 | Mask data in the Beacon DLL Content based on position and length.                                                                         |
| pe_mask_string                  | Mask a string in the Beacon DLL Content based on position.                                                                                |
| pe_patch_code                   | Patch code in the Beacon DLL Content based on find/replace in '.text' section.                                                            |
| pe_remove_rich_header           | Remove the rich header from Beacon DLL Content.                                                                                           |
| pe_set_compile_time_with_long   | Set the compile time in the Beacon DLL Content.                                                                                           |
| pe_set_compile_time_with_string | Set the compile time in the Beacon DLL Content.                                                                                           |
| pe_set_export_name              | Set the export name in the Beacon DLL Content.                                                                                            |
| pe_set_long                     | Places a long value at a specified location.                                                                                              |
| pe_set_short                    | Places a short value at a specified location.                                                                                             |
| pe_set_string                   | Places a string value at a specified location.                                                                                            |
| pe_set_stringz                  | Places a string value at a specified location and adds a zero terminator.                                                                 |
| pe_set_value_at                 | Sets a long value based on the location resolved by a name from the PE Map (see pedump).                                                  |
| pe_stomp                        | Set a string to null characters. Start at a specified location and sets all characters to null until a null string terminator is reached. |
| pe_update_checksum              | Update the checksum in the Beacon DLL Content.                                                                                            |

## Using User Defined Reflective DLL Loaders

### Create/Compile your Reflective Loaders

The User Defined Reflective Loader (UDRL-VS) Kit is the source code for the UDRL example. Go to Help -> Arsenal and download the Artifact Kit which includes the UDRL-VS kit (your license key is required).

The following is the Cobalt Strike process for prepping beacons:

- Beacons are patched with required settings as payload data.
    - The following are patched into Beacons for UDRL:
        - Listener Settings
        - Some Malleable C2 Settings.
    - The following is NOT patched into Beacons for UDRL:
        - PE Modifications
- BEACON_RDLL_GENERATE or BEACON_RDLL_GENERATE_LOCAL hook is called to support user modifications.
    - There are additional functions available to help inspect and make modifications to the Beacons based on the Reflective Loaders capabilities. For example:
        - Provide obfuscation
        - Patch in addresses for your own smart injection support
- Beacons are patched into artifacts.
    - Go to Help -> Arsenal from a licensed Cobalt Strike to download the Artifact Kit.
    - See the "stagesize" references in these artifact kit files provided by Cobalt Strike:
        - See "stagesize" references in artifact build script.
        - See "stagesize" references in ‘script.example’

### Beacon User Data

Beacon User Data (BUD) is a C-structure that allows Reflective Loaders to pass additional data to Beacons. You can download the beacon.h file. In addition, the udrl-vs kit in the Arsenal Kit includes an example BUD loader.

### Passing Beacon User Data

The BUD is passed as a pointer to the Beacon by calling Beacon's DllMain function with a custom reasoning known as DLL_BEACON_USER_DATA (0x0d). The BUD must be given to Beacon before the standard DLL_PROCESS_ATTACH reason is invoked.

Beacon copies necessary values from the BUD during the DLL_USER_DATA call, and therefore it is not required to keep the BUD structure in memory after the call.

### Version Number

The first value contained within the BUD structure is the version number. This version number is essential in ensuring backward compatibility between different versions of Beacons and Reflective Loaders since it allows newer Beacons to handle and utilize the older BUD structure without crashing.

The version number uses the following format: 0xMMmmPP, where:

- MM = Cobalt Strike’s major version number
- mm = Cobalt Strike’s minor version number
- PP = Cobalt Strike’s patch version number

For example, 0x040900 translates to version CS 4.9.

### System Calls

Beacon User Data allows a Reflective Loader to resolve and pass system call information to Beacon, which overtakes Beacon's default system call resolver. See System Calls to learn more.

Beacon User Data has an SYSCALL_API_ENTRY structure for each supported System Call, and the SYSCALL_API structure holds these entries. The entry contains the following values

- jmpAddr: The address of the correct System Call instruction depending on system architecture:
    - x64: the syscall instruction
    - WOW64 (32-bit on x64): FastSysCall in WOW64
    - Native x86: KiFastSystemCall
- sysnum: The System Call number
- fnAddr: The address of the corresponding Nt* function

The jmpAddr and sysnum values are required for indirect System Calls, and fnAddr is required for direct System Calls. If the value is zero, Beacon falls back to the corresponding WinAPI call.

The user-defined System Call information is skipped if the syscalls fields in the USER_DATA structure points to NULL.

### Custom Data

Beacon User Data allows a Reflective Loader to pass a small (32 bytes) data buffer to Beacon. Beacon Object Files (BOFs) can retrieve a pointer to this data with the BeaconGetCustomUserData function.
