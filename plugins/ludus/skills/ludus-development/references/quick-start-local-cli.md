# Use the CLI Locally

Guide for setting up the Ludus CLI on your local machine, including WireGuard setup, installing on Linux/macOS/Windows, setting the API key, and creating users via SSH tunnel.

## WireGuard

The easiest way to interact with Ludus is over WireGuard which allows the ludus CLI to talk to the API server
and allows you to access VMs directly - via SSH, RDP, KasmVNC, etc.
To get the WireGuard configuration file for your user, run the `user wireguard` command.
Admins can get WireGuard configurations for other users with the `user wireguard --user <UserID>` command.

Once connected, the ludus client's default url (`https://198.51.100.1:8080`)
will work for all future commands.

```shell-session
ludus user wireguard | tee ludus.conf
[Interface]
PrivateKey = KBxrT+PFLClI+uJo9a6XLm/b23vbqL5KmNQ5Ac6uwGI=
Address = 198.51.100.2/32

[Peer]
PublicKey = 5nlDO6gtqVXI89xQNkd2c2L0US7RnPinbAlfiyWHHBM=
Endpoint = 10.2.99.240:51820
AllowedIPs = 10.2.0.0/16, 198.51.100.1/32
PersistentKeepalive = 25
```

**On your local machine**, import this WireGuard configuration (`ludus.conf`) into the [WireGuard GUI client](https://www.wireguard.com/install/) or on the command line with [wg-quick](https://manpages.ubuntu.com/manpages/jammy/man8/wg-quick.8.html) and connect. `wg setconf` is not supported by this configuration. Now you can directly interact with range VMs as if you were on the same network.

## Setting up the Ludus client locally

### Linux

The same installer script used to install the server will install the client on a Linux machine.

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

The same installer script used to install the server will install the client on a macOS machine.

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

**Note:** This documentation assumes the use of the Windows Terminal and Powershell (not cmd.exe and batch).

```shell-session
irm https://ludus.cloud/install-client.ps1 | iex

ludus
Ludus client v1.5.4

Ludus is a CLI application to control a Ludus server
This application can manage users as well as ranges.
...
```

If you don't want to use the powershell script you can copy the correct Ludus client binary (get it from the [releases page](https://gitlab.com/badsectorlabs/ludus/-/releases)) to your Windows device and place it in your PATH.

## Set the API Key

Using the key from the previous step, run `ludus apikey` and provide the user API key.

### Linux

```shell-session
ludus apikey
[INFO]  Enter your Ludus API Key for https://198.51.100.1:8080:
JD._7Gx2T5kTUSD%uTWZ*lFi=Os6MpFR^OrG+yT94Xt
[INFO]  Ludus API key set successfully
```

**Tip:** On headless Linux systems or Linux systems without a keyring, set the LUDUS_API_KEY environment variable instead:
`export LUDUS_API_KEY='JD._7Gx2T5kTUSD%uTWZ*lFi=Os6MpFR^OrG+yT94Xt'`

### macOS

```shell-session
ludus apikey
[INFO]  Enter your Ludus API Key for https://198.51.100.1:8080:
JD._7Gx2T5kTUSD%uTWZ*lFi=Os6MpFR^OrG+yT94Xt
[INFO]  Ludus API key set successfully
```

**Tip:** On headless macOS systems or macOS systems without a keyring, set the LUDUS_API_KEY environment variable instead:
`export LUDUS_API_KEY='JD._7Gx2T5kTUSD%uTWZ*lFi=Os6MpFR^OrG+yT94Xt'`

### Windows

```shell-session
ludus apikey
[INFO]  Enter your Ludus API Key for https://198.51.100.1:8080:
JD._7Gx2T5kTUSD%uTWZ*lFi=Os6MpFR^OrG+yT94Xt
[INFO]  Ludus API key set successfully
```

With the API key set, all user commands are available!

You can manage your range, enter/exit testing mode, and more from your local machine.

`ludus -h` will show you all the options.

## Using the Ludus client to create a Ludus user locally

To perform user related actions, which modify the Ludus host as root, we must connect to the
admin service which only listens on localhost of the Ludus server. To do this we will create an SSH tunnel.

```
ssh -L 8081:127.0.0.1:8081 user@<Ludus IP>
```

Open a second terminal.

Now create a ludus user! This user will be an admin as we specify `--admin`.
Initials are commonly used for the userID.

**Warning:** If the user name you specify (converted to lowercase and spaces replaced with `-`) exists
on the system already, it's PAM password will be changed by Ludus! This user's groups will be modified (i.e. removed from sudoers) as well. You should use a username that is not present on the system when installing Ludus.

Prepend the LUDUS_API_KEY variable to the command to authenticate properly.

### Linux

**Tip:** Adding a space at the beginning of this command will prevent it from being written to the
shell's history file in most common shells.

```shell-session
ludus user add --name "Jane Smith" --userid JS --admin --url https://127.0.0.1:8081
+--------+------------------+-------+---------------------------------------------+
| USERID | PROXMOX USERNAME | ADMIN |                   API KEY                   |
+--------+------------------+-------+---------------------------------------------+
| JS     | jane-smith       | true  | JS._8Bx2T5kTXMR*uTWZ%lFi^Os6MpFR=OrH+yT96Dq |
+--------+------------------+-------+---------------------------------------------+
```

### macOS

**Tip:** Adding a space at the beginning of this command will prevent it from being written to the
shell's history file in most common shells.

```shell-session
ludus user add --name "Jane Smith" --userid JS --admin --url https://127.0.0.1:8081
+--------+------------------+-------+---------------------------------------------+
| USERID | PROXMOX USERNAME | ADMIN |                   API KEY                   |
+--------+------------------+-------+---------------------------------------------+
| JS     | jane-smith       | true  | JS._8Bx2T5kTXMR*uTWZ%lFi^Os6MpFR=OrH+yT96Dq |
+--------+------------------+-------+---------------------------------------------+
```

### Windows

```shell-session
ludus user add --name "Jane Smith" --userid JS --admin --url https://127.0.0.1:8081
+--------+------------------+-------+---------------------------------------------+
| USERID | PROXMOX USERNAME | ADMIN |                   API KEY                   |
+--------+------------------+-------+---------------------------------------------+
| JS     | jane-smith       | true  | JS._8Bx2T5kTXMR*uTWZ%lFi^Os6MpFR=OrH+yT96Dq |
+--------+------------------+-------+---------------------------------------------+
```

**Note:** This command construct is only required for user add and delete actions. Normal user actions don't require the SSH tunnel or url parameter.
