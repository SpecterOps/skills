# Built-in Beacon Commands

The following commands are built into Cobalt Strike, grouped as the team server's help groups them.

## Housekeeping

The following commands are built into Beacon and exist to configure Beacon or perform house-keeping actions.

- argue: Spoof arguments for matching processes
- beacon_config: Functions for managing Beacon configuration
- beacon_gate: Functions for managing Beacon gate
- blockdlls: Block non-Microsoft DLLs in child processes
- cancel: Cancel a download that's in-progress
- checkin: Call home and post data
- jobs: List long-running post-exploitation tasks
- mode: Sets the DNS Beacon mode [dns|dns6|dns-txt] (DNS Beacon only); `mode dns` uses DNS A, `mode dns-txt` DNS TXT, and `mode dns6` DNS AAAA as the data channel
- note: Assign a note to this Beacon
- powershell-import: Import a powershell script
- ppid: Set parent PID for spawned post-ex jobs
- sleep: Set Beacon sleep time
- spawnto: Set executable to spawn processes into
- syscall-method: Change or query the syscall method

## Native

These commands are built into Beacon and typically rely on Win32 APIs to meet their objectives:

- beacon-interpreter: Run a C script in this session's script VM
- beacon-interpreter-lint: Check a C script for any syntax errors
- cd: Change directory
- connect: Connect to a Beacon peer over TCP
- cp: Copy a file
- dllinject: Inject a Reflective DLL into a process
- download: Download a file
- drives: List drives on target
- execute: Execute a program on target (no output)
- execute-dll: Execute a user defined postex task
- exit: Terminate the Beacon session
- getprivs: Enable system privileges on current token
- getuid: Get User ID
- inject: Spawn a session in a specific process
- inline-execute: Run a Beacon Object File in this session
- inline-execute-pe: Run a complete PE file in this session (BOF-PE)
- jobkill: Kill a long-running post-exploitation task
- kill: Kill a process
- link: Connect to a Beacon peer over a named pipe
- ls: List files
- make_token: Create a token to pass credentials
- mkdir: Make a directory
- mv: Move a file
- powershell: Execute a command via powershell.exe
- ps: Show process list
- pwd: Print current directory
- rev2self: Revert to original token
- rm: Remove a file or folder
- rportfwd: Setup a reverse port forward
- rportfwd_local: Setup a reverse port forward via Cobalt Strike client
- run: Execute a program on target (returns output)
- runas: Execute a program as another user
- runu: Execute a program under another PID
- setenv: Set an environment variable
- shell: Execute a command via cmd.exe
- shinject: Inject shellcode into a process
- shspawn: Spawn process and inject shellcode into it
- socks: Start/Stop a SOCKS4a/SOCKS5 server to relay traffic
- spawn: Spawn a session
- spawnas: Spawn a session as another user
- spawnu: Spawn a session under another process
- spunnel: Spawn and tunnel an agent via rportfwd
- spunnel_local: Spawn and tunnel an agent via Cobalt Strike client rportfwd
- steal_token: Steal access token from a process
- token-store: Hot-swappable access tokens
- unlink: Disconnect from parent Beacon
- upload: Upload a file

## Postex DLL

These commands use a Postex DLL to achieve their objectives:

- browserpivot: Setup a browser pivot session
- chromedump: Recover credentials from Google Chrome
- covertvpn: Deploy Covert VPN client
- dcsync: Extract a password hash from a DC
- desktop: View and interact with target's desktop
- execute-assembly: Execute a local .NET program in-memory on target
- hashdump: Dump password hashes
- keylogger: Start a keystroke logger
- logonpasswords: Dump credentials and hashes with mimikatz
- mimikatz: Runs a mimikatz command
- net: Network and host enumeration tool
- portscan: Scan a network for open services
- powerpick: Execute a command via Unmanaged PowerShell
- printscreen: Take a single screenshot via PrintScr method
- psinject: Execute PowerShell command in specific process
- pth: Pass-the-hash using Mimikatz
- screenshot: Take a single screenshot
- screenwatch: Take periodic screenshots of desktop
- ssh: Use SSH to spawn an SSH session on a host
- ssh-key: Use SSH to spawn an SSH session on a host

## BOF

These commands execute as a Beacon Object File (BOF) and use the current Beacon thread:

- beacon_info: Prints Beacon's in-memory location
- clipboard: Attempt to get text clipboard contents
- dllload: Load DLL into a process with LoadLibrary()
- elevate: Spawn a session in an elevated context
- getsystem: Attempt to get SYSTEM
- jump: Spawn a session on a remote host
- kerberos_ticket_purge: Purge kerberos tickets from this session
- kerberos_ticket_use: Apply kerberos ticket to this session
- reg: Query the registry
- remote-exec: Run a command on a remote host
- runasadmin: Execute a program in an elevated context
- timestomp: Apply timestamps from one file to another
