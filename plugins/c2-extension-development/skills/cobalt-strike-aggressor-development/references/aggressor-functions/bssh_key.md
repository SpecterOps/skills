bssh_key

Ask Beacon to spawn an SSH session using the data from a key file. The key file needs to be in the PEM format. If the file is not in the PEM format then make a copy of the file and convert the copy with the following command:

/usr/bin/ssh-keygen -f [/path/to/copy] -e -m pem -p

#### Arguments

`$1` - id for the beacon. This may be an array or a single ID.

`$2` - IP address or hostname of the target

`$3` - port (e.g., 22)

`$4` - username

`$5` - key data (as a string)

`$6` - (optional) the PID to inject the SSH client into or $null

`$7` - (optional) the architecture of the target PID (x86|x64) or $null

#### Example

```
alias myssh {
   $pid = $2;
   $arch = $3;
   $handle = openf("/path/to/key.pem");
   $keydata = readb($handle, -1);
   closef($handle);

   if ($pid >= 0 && ($arch eq "x86" || $arch eq "x64")) {
      bssh_key($1, "172.16.20.128", 22, "root", $keydata, $pid, $arch);
   } else {
      bssh_key($1, "172.16.20.128", 22, "root", $keydata);
   }
};```
