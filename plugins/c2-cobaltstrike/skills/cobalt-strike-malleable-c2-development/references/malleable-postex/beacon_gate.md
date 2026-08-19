# Beacon Gate

The beacon_gate block determines what WinAPIs Beacon will forward to the Sleepmask. By default, the Sleepmask will automatically mask Beacon for any API that is proxied (and subsequently) executed via BeaconGate. However, masking will be automatically disabled when you task Beacon to become interactive (< 3s) to avoid CPU spikes.

The default behavior can be customized via implementing a User Defined Sleepmask via the BEACON_SLEEP_MASK Aggressor hook. For an example of how to do this, see the Sleepmask-VS repo. This repository demonstrates simple examples of BeaconGate so operators can quickly develop a custom Sleepmask BOF for use with BeaconGate.

The table below shows the supported beacon_gate options and their corresponding WinAPIs:

| Option  | APIs                                                                                                                                                                                                                                                                                                                                                                  | Notes                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| None    | None                                                                                                                                                                                                                                                                                                                                                                  | The default option. No APIs are proxied via the Sleepmask.      |
| Comms   | InternetOpenA<br>InternetConnectA                                                                                                                                                                                                                                                                                                                                     | This is currently only supported by the HTTP(S) WinInet Beacon. |
| Core    | CloseHandle<br>CreateFileMappingA<br>CreateRemoteThread<br>CreateThread<br>DuplicateHandle<br>GetThreadContext<br>MapViewOfFile<br>OpenProcess<br>OpenThread<br>ReadProcessMemory<br>ResumeThread<br>SetThreadContext<br>UnMapViewOfFile<br>VirtualAlloc<br>VirtualAllocEx<br>VirtualFree<br>VirtualProtect<br>VirtualProtectEx<br>VirtualQuery<br>WriteProcessMemory | This is the core Beacon API set.                                |
| Cleanup | ExitThread                                                                                                                                                                                                                                                                                                                                                            | This is a special case, see the note below*.                    |
| All     | Comms, Core, and Cleanup APIs                                                                                                                                                                                                                                                                                                                                         |                                                                 |

> ExitThread is only proxied via BeaconGate when Exit Function is set to Thread and Beacon is not configured to use module stomping (i.e, `module_x*`). Enabling the Cleanup option out the box will result in the default Sleepmask cleaning up Beacon prior to calling ExitThread. If implementing a User Defined Sleepmask you can also perform additional clean up actions pre thread termination if desired.

It is also possible to proxy specific functions from the supported set with the following syntax:

```
stage {
        beacon_gate {
           VirtualAlloc;
           VirtualAllocEx;
           InternetConnectA;
        }
}
```

It is also important to point out that BeaconGate and Cobalt Strike's existing syscall_method option are mutually exclusive; if you enable BeaconGate for an API, it will take precedence over system calls. However, you can enable BeaconGate for a specific API and use Beacon's existing system call method for the rest. For example:

```
stage {
   set syscall_method "Indirect";
   beacon_gate {
      VirtualAlloc;  // Only VirtualAlloc is routed via BeaconGate
   }
}
```

As a note, some more intensive Beacon commands such as ps may spike CPU if you have the core set enabled. This is expected behaviour, as ps will call OpenProcess/CloseHandle multiple times while masking. If desired, you can disable BeaconGate at runtime via the beacon_gate disable command or alternatively disable masking for specific functions in your own Sleepmask BOF.

Lastly, there are occasions when it is not possible to forward WinAPI calls to BeaconGate. For example, some supported APIs (VirtualAlloc) may be needed to set up BOF memory in order to use BeaconGate in the first place. To get round this limitation you can specify User Defined memory for BOFs/Sleepmask in a UDRL via the ALLOCATED_MEMORY structure. The bud-loader in UDRL-VS contains examples of how to pass user defined memory to Beacon for use with BOFs and the Sleepmask.
