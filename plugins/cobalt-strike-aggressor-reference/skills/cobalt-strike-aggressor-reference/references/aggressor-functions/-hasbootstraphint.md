-hasbootstraphint

This function checks the stage.smartinject malleable c2 profile setting for the active team server. If the setting is set to false, the function will return false. If the setting is set to true, then the payload will be checked for the x86 or x64 bootstrap hints and will return true if the hint is found. Use this function to determine if it is safe to use an artifact that passes GetProcAddress/GetModuleHandlA pointers to this payload.

#### Arguments

`$1` - byte array with a payload or shellcode.

See also&payload_bootstrap_hint

