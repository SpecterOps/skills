listeners_stageless

Return a list of listener names across all team servers this client is connected to. SMB and TCP listeners are filtered except for those hosted on the active team server. External C2 listeners are filtered as they are not actionable via staging or exporting as a Reflective DLL. 

#### Returns

An array of listener names.

#### Example

```
printAll(listeners_stageless());```

