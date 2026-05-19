# Deploy a Range

Guide for deploying a Ludus range, checking status, setting up WireGuard, getting RDP files, and default credentials.

Ludus ranges (environments) are defined by a single yaml configuration file. By default, a simple range configuration is provided to each user.

To view your current configuration, run the following command

```shell-session
ludus range config get
```

For a detailed explanation of the configuration file, see the Ludus configuration documentation.

If you would like to make changes to this file, save it to disk, modify it, and set it with the following commands.

```shell-session
ludus range config get > ludus-range-config.yml
<vim|nano> config
ludus range config set -f ludus-range-config.yml
[INFO]  Your range config has been successfully updated.
```

Once you are satisfied with your range configuration, deploy it with `range deploy`.

```shell-session
ludus range deploy
[INFO]  range deploy started
```

Just like with templates, you can tail the ansible logs for range deployment with `range logs -f`

```shell-session
ludus range logs -f
PLAY [Pre run checks] **********************************************************

TASK [Acquire session ticket] **************************************************
changed: [localhost]

TASK [Check for valid dynamic inventory] ***************************************
ok: [localhost] => {
    "changed": false,
    "msg": "Dynamic inventory loaded!"
}
...
```

You can also check the status of your range at any time with `range status`

```shell-session
ludus range status
+---------+---------------+------------------+---------------+-------------------+-----------------+
| USER ID | RANGE NETWORK | LAST DEPLOYMENT  | NUMBER OF VMS | DEPLOYMENT STATUS | TESTING ENABLED |
+---------+---------------+------------------+---------------+-------------------+-----------------+
|   JD    |  10.2.0.0/16  | 2023-12-31 18:42 |       4       |      SUCCESS      |      FALSE      |
+---------+---------------+------------------+---------------+-------------------+-----------------+
+------------+-----------------------------------+-------+-------------+
| PROXMOX ID |              VM NAME              | POWER |     IP      |
+------------+-----------------------------------+-------+-------------+
|    107     | JD-router-debian11-x64            |  On   | 10.2.10.254 |
|    109     | JD-ad-dc-win2019-server-x64       |  On   | 10.2.10.11  |
|    113     | JD-ad-win11-22h2-enterprise-x64-1 |  On   | 10.2.10.21  |
|    114     | JD-kali                           |  On   | 10.2.99.1   |
+------------+-----------------------------------+-------+-------------+
```

When the range status shows `SUCCESS` your range is fully deployed!

**Tip:** Want to share this range with others or spin up a different range in addition to this one? Check out the range sharing documentation.

## WireGuard

The easiest way to interact with Ludus VMs is directly - via SSH, RDP, or KasmVNC.
This is possible thanks to a WireGuard VPN hosted on the Ludus server.
To get the WireGuard configuration file for your user, run the `user wireguard` command.
Admins can get WireGuard configurations for other users with the `user wireguard --user <UserID>` command.

```shell-session
ludus user wireguard | tee ludus.conf
[Interface]
PrivateKey = KBxrT+PFLClI+uJo9a6XLm/b23vbqL5KmNQ5Ac6uwGI=
Address = 198.51.100.2/32

[Peer]
PublicKey = 5nlDO6gtqVXI89xQNkd2c2L0US7RnPinbAlfiyWHHBM=
Endpoint = 203.0.113.54:51820
AllowedIPs = 10.2.0.0/16, 198.51.100.1/32
PersistentKeepalive = 25
```

**On your local machine**, import this WireGuard configuration (`ludus.conf`) into the [WireGuard GUI client](https://www.wireguard.com/install/) or on the command line with [wg-quick](https://manpages.ubuntu.com/manpages/jammy/man8/wg-quick.8.html) and connect.
`wg setconf` is not supported by this configuration.
Now you can directly interact with range VMs as if you were on the same network.

To get a zip file of RDP configuration files for the Windows machines, use the `range rdp` command.

```shell-session
ludus range rdp
[INFO]  File downloaded and saved as rdp.zip
```

These configuration files can be imported into any RDP client and used to connect to the Windows VMs using the credentials below.

All Linux machines have SSH running on port 22.

All Windows machines have RDP enabled on port 3389.

The Kali template is running [KasmVNC](https://github.com/kasmtech/KasmVNC) on `https://<kali IP>:8444/`.
The password for KasmVNC is `password` as it requires a 6 character password.

## Default Machine Credentials

- Kali
  - `kali:kali` (OS)
  - `kali:password` (KasmVNC - https port 8444)
- Windows
  - `localuser:password` (local Administrator)
  - `LUDUS\domainuser:password`
  - `LUDUS\domainadmin:password` (Domain Admin)
- Debian based boxes
  - `debian:debian`
- Others
  - `localuser:password`
