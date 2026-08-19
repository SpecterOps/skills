# Controlling Post Exploitation

Larger Cobalt Strike post-exploitation features (e.g., screenshot, keylogger, hashdump, etc.) are implemented as Windows DLLs. To execute these features, Cobalt Strike spawns a temporary process, and injects the feature into it. The process-inject block controls the process injection step. The post-ex block controls the content and behaviors specific to Cobalt Strike’s post- exploitation features. With the 4.5 release these post-exploitation features now support explicit injection into an existing process when using the [pid] and [arch] arguments.

```
post-ex {
      # control the temporary process we spawn to
      set spawnto_x86 "%windir%\\syswow64\\rundll32.exe"; 
      set spawnto_x64 "%windir%\\sysnative\\rundll32.exe";

      # change the permissions and content of our post-ex DLLs 
      set obfuscate "true";

      # change our post-ex output named pipe names... 
      set pipename "evil_####, stuff\\not_##_ev#l";

      # pass key function pointers from Beacon to its child jobs 
      set smartinject "true";

      # disable AMSI in powerpick, execute-assembly, and psinject 
      set amsi_disable "true";

      # cleanup the post-ex UDRL memory when the post-ex DLL is loaded
      set cleanup "true";

      transform-x64 {
            # replace a string in the port scanner dll
            strrepex "PortScanner" "Scanner module is complete" "Scan is complete";

            # replace a string in all post exploitation dlls
            strrep "is alive." "is up.";
      }

      transform-x86 {
            # replace a string in the port scanner dll
            strrepex "PortScanner" "Scanner module is complete" "Scan is complete";

            # replace a string in all post exploitation dlls
            strrep "is alive." "is up.";
      }
}
```

The spawnto_x86 and spawnto_x64 options control the default temporary process Beacon will spawn for its post-exploitation features. Here are a few tips for these values:

- Always specify the full path to the program you want Beacon to spawn
- Environment variables (e.g., %windir%) are OK within these paths.
- Do not specify %windir%\system32 or c:\windows\system32 directly. Always use syswow64 (x86) and sysnative (x64). Beacon will adjust these values to system32 where it’s necessary.
- For an x86 spawnto value, you must specify an x86 program. For an x64 spawnto value, you must specify an x64 program.
- The paths you specify (minus the automatic syswow64/sysnative adjustment) must exist from both an x64 (native) and x86 (wow64) view of the file system.

The obfuscate option scrambles the content of the post-ex DLLs and settles the post-ex capability into memory in a more OPSEC-safe way. It’s very similar to the obfuscate and userwx options available for Beacon via the stage block. Some long-running post-ex DLLs will mask and unmask their string table, as needed, when this option is set.

Use pipename to change the named pipe names used, by post-ex DLLs, to send output back to Beacon. This option accepts a comma-separated list of pipenames. Cobalt Strike will select a random pipe name from this option when it sets up a post-exploitation job. Each # in the pipename is replaced with a valid hex character as well.

The smartinject option directs Beacon to embed key function pointers, like GetProcAddress and LoadLibrary, into its same-architecture post-ex DLLs. This allows post-ex DLLs to bootstrap themselves in a new process without shellcode-like behavior that is detected and mitigated by watching memory accesses to the PEB and kernel32.dll.

The thread_hint option allows multi-threaded post-ex DLLs to spawn threads with a spoofed start address. Specify the thread hint as "module!function+0x##" to specify the start address to spoof. The optional 0x## part is an offset added to the start address.

The amsi_disable option directs powerpick, execute-assembly, and psinject to patch the AmsiScanBuffer function before loading .NET or PowerShell code. This limits the Antimalware Scan Interface visibility into these capabilities. If the patch can not be applied a message will be returned to the beacon console window, however the command will still continue executing. For example running on a Windows OS prior to Windows 10, you will see the message ‘Could not find AmsiScanBuffer function’ along with the output.

The cleanup option cleans up the post-ex UDRL memory when the post-ex DLL is loaded. See Post-ex User Defined Reflective DLL Loader for more information on how this operates with a customized post-ex UDRL.

Set the keylogger option to configure Cobalt Strike's keystroke logger. The GetAsyncKeyState option (default) uses the GetAsyncKeyState API to observe keystrokes. The SetWindowsHookEx option uses SetWindowsHookEx to observe keystrokes.

The transform-x86 and transform-x64 blocks transform Beacon’s Post Exploitation DLLs. These blocks support two commands: strrep and strrepex.

The strrep command replaces a string within all Post Exploitation DLLs. The strrepex command replaces a string within the specific Post Exploitation DLLs, and it has the following syntax: strrepex <post-ex name> <original str> <new str>. Valid post-ex names are: BrowserPivot, ExecuteAssembly, Hashdump, Keylogger, Mimikatz, NetView, PortScanner, PowerPick, Screenshot, and SSHAgent.
