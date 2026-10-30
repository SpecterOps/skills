# Built-in Implant Commands

The following commands are built into Outflank C2.

- burn: Switch to the next communication channel.
- cat: Reads a file and writes it to the terminal output.
- cd: Changes the current working directory.
- config: Interact with the configuration of the implant.
- cp: Copies a file.
- delay: Delays the execution with a one-off timeout in miliseconds.
- dnsname: Returns the DNS name of the machine.
- download: Download a file from the machine.
- drives: Lists all available drives/mounts on the current machine.
- env: Lists all the environment variables.
- exec_bof: Execute a Beacon Object File.
- exec_command: Execute a command using the regular Command Shell or PowerShell interpreter on Windows or the default shell on macOS/Linux.
- exit: Exits the implant thread or full process.
- fullcheckin: Re-retrieve all information about the implant.
- getprivs: Enable as many system privileges as possible on your current thread or process token.
- help: Display available commands
- ip: Returns all IPv4 and IPv6 addresses.
- kill: Kill a process with the given process ID.
- link: Link an SMB, tcp, or file based implant.
- load_library: Manually load the specified module into the address space of the current process.
- ls: List files
- mkdir: Creates a directory.
- mv: Moves a file.
- note: Stores a note with the implant.
- portforward: Manage TCP/UDP port-forward tunnels for the current implant.
- ps: List running processes
- pwd: Returns the current working directory
- rm: Deletes a file.
- rmdir: Deletes a directory.
- rportforward: Manage reverse port-forward tunnels for the current implant.
- sleep: Change beaconing interval and jitter factor.
- socks: Manage SOCKS5 tunnels for the current implant.
- upload: Uploads an artifact to the machine.
- whoami: Return the current user.
