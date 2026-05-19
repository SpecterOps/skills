# Updating Ludus

How to update the Ludus server and client on Linux, macOS, and Windows.

**Tip:** Ludus binaries are built in CI, but you can always build them from source yourself.

## Updating a Ludus server

Simply run the install script again. It will detect an existing installation and update the server.

```shell
ssh user@ludus

# All-in-one command
curl -s https://ludus.cloud/install | bash

# If you want to check out the install script
curl https://ludus.cloud/install > install.sh
cat install.sh
chmod +x install.sh
./install.sh

====================================
 _      _   _  ____   _   _  ____
| |    | | | ||  _ \ | | | |/ ___\
| |    | | | || | | || | | |\___ \
| |___ | |_| || |_| || |_| | ___) |
|____/  \___/ |____/  \___/  \___/

====================================
[+] Client install prefix set to /usr/local/bin
[+] Created temp dir at /tmp/ludus-client.AvRubQ
[+] Architecture detected as x86_64
[+] OS detected as Linux
[+] Downloaded ludus-client_linux-amd64-v1.5.0 into /tmp/ludus-client.AvRubQ
[+] Downloaded ludus checksums file into /tmp/ludus-client.AvRubQ
[+] Checksum of /tmp/ludus-client.AvRubQ/ludus-client_linux-amd64-v1.5.0 verified
[+] Install prefix already exists. No need to create it.
[+] Asking for sudo password to install file: /tmp/ludus-client.AvRubQ/ludus to directory: /usr/local/bin/
[sudo] password for debian:
[+] Installed ludus-client_linux-amd64-v1.5.0 to /usr/local/bin/ as 'ludus'
[+] Ludus client installation complete
[+] Shell completions already installed
[+] Ludus server already installed in /opt/ludus
[?] Would you like to update the Ludus server on this host?
[?] (y/n): y
[+] Updating Ludus server
[+] Downloaded ludus-server-v1.5.0 into /tmp/ludus-client.AvRubQ
[+] Checksum of /tmp/ludus-client.AvRubQ/ludus-server-v1.5.0 verified
Backed up /opt/ludus/ansible to /opt/ludus/previous-versions/1724356681992145034/ansible
Backed up /opt/ludus/packer to /opt/ludus/previous-versions/1724356681992145034/packer
Backed up /opt/ludus/ci to /opt/ludus/previous-versions/1724356681992145034/ci
Extracting ludus to /opt/ludus...
Ludus files extracted successfully
Ludus updated to v1.5.0+2d39950
```

**Note:** If you are updating from < 1.3.0 see [UPDATING.md](https://gitlab.com/badsectorlabs/ludus/-/blob/main/UPDATING.md?ref_type=heads)

**Warning:** The Ludus server binary will refuse to update if any `ansible` or `packer` processes are active on the machine to prevent possible interruption to active range or template activity.

## Updating the Ludus client

### Linux

Run the update command:

```shell
ludus update client
```

OR

The same installer script used to install the server/client will update the client on a Linux machine.

```shell
# All-in-one command
curl -s https://ludus.cloud/install | bash

# If you want to check out the install script
curl https://ludus.cloud/install > install.sh
cat install.sh
chmod +x install.sh
./install.sh
```

### macOS

Run the update command:

```shell
ludus update client
```

OR

The same installer script used to install the server/client will update the client on a macOS machine.

```shell
# All-in-one command
curl -s https://ludus.cloud/install | zsh

# If you want to check out the install script
curl https://ludus.cloud/install > install.sh
cat install.sh
chmod +x install.sh
./install.sh
```

### Windows

Run the update command:

```
PS C:\> ludus update client
```

OR

```
PS C:\> irm https://ludus.cloud/install-client.ps1 | iex
```

## Updating a Ludus server manually

Updating a Ludus server manually is easy:

1. Download the server [release binary](https://gitlab.com/badsectorlabs/ludus/-/releases) (or build from source) of the version you wish to update to.
2. Copy the Ludus server binary to the Ludus server host
3. Run the Ludus server binary as root with the `--update` flag.

```
local:~$ scp ludus-server user@ludus:
local:~$ ssh user@ludus
user@ludus:~$ chmod +x ludus-server
user@ludus:~$ sudo ./ludus-server --update
Backed up /opt/ludus/ansible to /opt/ludus/previous-versions/1707349133263620491/ansible
Backed up /opt/ludus/packer to /opt/ludus/previous-versions/1707349133263620491/packer
Backed up /opt/ludus/ci to /opt/ludus/previous-versions/1707349133263620491/ci
Extracting ludus to /opt/ludus...
Ludus files extracted successfully
Ludus updated to v1.0.2+6a96b3ef
```
