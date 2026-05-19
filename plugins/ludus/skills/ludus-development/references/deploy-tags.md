# Deploy Tags

Ludus supports deploy tags to control which parts of the deployment process are run. This is useful after an initial deployment to skip steps that are not needed on subsequent deployments.

## Deploy Tags Meaning

| Tag | Meaning |
| --- | --- |
| additional-tools | Install firefox, chrome, VSCode, burp suite, 7zip, process hacker, ilspy and other useful utilities on Windows VMs |
| allow-share-access | Allow anonymous access to SMB shares on all Windows VMs. Consider using the `anon_share_access` gpo to allow anonymous access to SMB shares on all Windows VMs instead of this tag. |
| assign-ip | Configure the static IP and hostname for all VMs |
| custom-choco | Install user defined chocolatey packages |
| custom-groups | Sets custom ansible groups for VMs, which are reflected in the inventory returned by `ludus range inventory` |
| dcs | Configure primary and alternate domain controllers |
| debug | Runs a one-off task. Only useful when developing Ludus (edit the debug task and use this tag) |
| dns-rewrites | Setup all DNS mappings for VMs and any user defined DNS rewrite rules on the DNS server of the router |
| domain-join | Join Windows VMs to the domain |
| generate-rdp | Creates the RDP zip file for all Windows VMs. Should not be called directly. Use `ludus range rdp` |
| linux-packages | Install user-defined packages on Linux hosts |
| install-office | Install Microsoft Office on Windows VMs |
| install-visual-studio | Install Visual Studio on Windows VMs |
| network | Setup all VLANs and network rules on the router, including any firewall rules, inbound, and outbound WireGuard. Does **not** setup DNS rewrites (use `dns-rewrites` for that) |
| nexus | Deploy [Nexus cache](./nexus-cache.md) VM |
| share | Deploy Ludus Share VM - exposes `readonlyshare` and `readwriteshare`. Consider using the `anon_share_access` gpo to allow anonymous access to SMB shares on all Windows VMs |
| sysprep | Run Sysprep on Windows VMs with a sysprep key set to `true` |
| user-defined-roles | Apply all user defined roles to VMs |
| vm-deploy | Deploy all VMs defined in the range config and make sure they are powered on |
| windows | Configure all Windows VMs (automatic logon, firewall, RDP, SMB, Network Sharing) |

## Listing Deploy Tags

```shell
ludus range gettags
additional-tools, allow-share-access, assign-ip, custom-choco, custom-groups, dcs, debug, dns-rewrites,
domain-join, generate-rdp, linux-packages, install-office, install-visual-studio, network, nexus,
share, sysprep, user-defined-roles, vm-deploy, windows
```

## Using Deploy Tags

You can specify one or more deploy tags when deploying a range.

```shell
ludus range deploy -t user-defined-roles
ludus range deploy -t network,vm-deploy
```

## Common Use Cases

### Adding a single VM to a range, then configuring it

You must first deploy the VM before it can be used in a `--limit` argument.
The `network` tag is required in the event the VM is in a VLAN that was not previously configured.

```shell
ludus range deploy -t vm-deploy,network,dns-rewrites
ludus range deploy --limit <VM NAME>
```

### Setting up the Nexus cache

```shell
ludus range deploy -t nexus
```

### Setting up the Ludus Share

```shell
ludus range deploy -t share
```

### Allowing anonymous access to SMB shares

You must run this on a range after a deploy if you wish to use the Ludus Shares set up with `share` from Windows.

```shell
ludus range deploy -t allow-share-access
```
