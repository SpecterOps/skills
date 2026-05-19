# Ludus Enterprise Reference

## Overview and Feature Comparison

While Ludus is free and open source, Ludus Enterprise is a paid service that provides additional features and support.

| Feature | Community | Enterprise |
| --- | :---: | :---:|
| Easy one command install | ✅  | ✅ |
| Automated template builds | ✅ | ✅ |
| Chocolatey package manager support | ✅ | ✅ |
| Ansible role management | ✅ | ✅ |
| Command line client | ✅ | ✅ |
| Fully documented API | ✅ | ✅ |
| Up to 255 VLANs per range | ✅ | ✅ |
| Support | Community | Professional |
| Roles on the router | ❌ | ✅ |
| Inbound WireGuard Server per range | ❌ | ✅ |
| CTFd integration | ❌ | ✅ |
| Private Role Catalog | ❌ | ✅ |
| Outbound WireGuard | ❌ | ✅ |
| Windows Licensing | ❌ | ✅ |
| Anti-Sandbox | ❌ | Add-on |
| Arbitrary credential support | ❌ | In development |
| Web Interface | ❌ | In development |

Ludus Enterprise directly supports the development of the free and open source core Ludus product that helps thousands of cybersecurity professionals around the world every day.

To enquire about Ludus Enterprise, please contact ludus-support@badsectorlabs.com.

## License Key

The Ludus Enterprise license key is a unique string that is used to activate the Ludus Enterprise features.

Your license key will look like this:

```
46C1CA-B11C52-80E9E7-19E436-FDDG1B-V3
```

### How to get a license key

To enquire about Ludus Enterprise licensing for your organization, please contact ludus-support@badsectorlabs.com.

### How to use the license key

Once you have a license key, you can activate Ludus Enterprise by setting the `license_key` key in the Ludus config file (or during install).

```yaml
license_key: 46C1CA-B11C52-80E9E7-19E436-FDDG1B-V3
```

Once the license key is set, Ludus will check the license key on startup and if it is valid, it will activate the Ludus Enterprise features and any add-ons you are entitled to.

You can manually restart the Ludus services to have the license key check run again.

```shell-session
systemctl restart ludus
systemctl restart ludus-admin
```

## Windows KMS Licensing

**Note:** Ludus users are responsible for ensuring they have valid licenses for all Windows machines licensed via the KMS.

### Overview

Ludus provides commands to manage a Key Management Service (KMS) server for activating Windows virtual machines within your ranges. This functionality is available in Ludus enterprise.

The KMS server runs on the Ludus host at a static IP address (`192.0.2.1`) and is used to activate volume-licensed Windows VMs.

### Commands

#### `ludus kms install`

**Description:** Installs a Key Management Service (KMS) server on the Ludus host.
The server will be configured to listen on `192.0.2.1`.

**Usage:**
```bash
ludus kms install
```

**Arguments:** None

#### `ludus kms license`

**Description:** Licenses one or more Windows VMs using the installed KMS server.

**Usage:**
```bash
ludus kms license --vmids <vmids> [--product-key <key>]
```

**Arguments:**

*   `--vmids, -n <vmids>` (Required): A comma-separated list of VM IDs to license (e.g., `104`, `104,105`).
*   `--product-key, -p <key>` (Optional): The specific volume license product key to use for activation. If not provided, Ludus attempts to determine the appropriate key based on the Windows version of the VM.
*   `--user <userID>` (Optional, Admin only): Impersonate a specific user to license VMs in their range.

### Usage Examples

**1. Install the KMS server:**

```bash
ludus kms install
# Wait for the installation to complete.
```

**2. License a single Windows VM:**

**Note:** Windows servers that have been promoted to Domain Controllers cannot be licensed. License the VM before configuring Active Directory.

```bash
# Assuming VM ID 110 is a Windows VM
ludus kms license --vmids 110
```

**3. License multiple Windows VMs:**

```bash
# Assuming VM IDs 110 and 112 are Windows VMs
ludus kms license --vmids 110,112
```

**4. License VMs with a specific product key:**

Keys can be found at [learn.microsoft.com](https://learn.microsoft.com/en-us/windows-server/get-started/kms-client-activation-keys)

```bash
ludus kms license --vmids 110,112 --product-key TVRH6-WHNXV-R9WG3-9XRFY-MY832
```

**5. License VMs for another user (as admin):**

```bash
ludus kms license --vmids 205 --user JD
```

## Anti-Sandbox

**Note:** Available as an add-on to Ludus Enterprise.

Ludus Enterprise can optionally include a plugin that enables the use of the Anti-Sandbox measures.

### What is a VM sandbox?

A VM sandbox is a virtual machine that is used for malware research or other purposes. It often includes software and other tools that are used to perform malware analysis, such as a debugger, memory analyzer, or disassembler.

However, some malware or other software may specifically look for artifacts of a virtual machine that are not normally present on "real" hosts. This allows the malware to change its behavior, and potentially mislead the analyst or otherwise not perform the same actions as it would on a "real" host.

### What is the Ludus Anti-Sandbox plugin?

The Ludus Anti-Sandbox plugin uses custom compiled QEMU and OVMF packages that have sandbox artifacts (i.e. QEMU strings, etc) removed to create a VM that appears to be a "real" host. Additionally, the Ludus Anti-Sandbox plugin modifies specified VMs in the following ways:

* Drop and configure realistic user files:
  * Adds random numbers of PDF, DOC, PPTX, and XLSX files to Desktop and Downloads folders
  * Sets random creation/modification dates on files spanning the last 5 years
  * Opens random files to create usage artifacts and recent files history

* Modifies system timestamps and registration:
  * Sets a random Windows installation date between 2021-2024
  * Can configure custom registered organization and owner information

* Removes virtualization artifacts:
  * Uninstalls VirtIO Serial Driver
  * Removes QEMU Guest Agent and related services
  * Deletes RedHat registry keys
  * Removes virtualization-related folders (C:\ludus, C:\Tools, C:\QEMU-ga)

* Configures a more realistic desktop environment:
  * Restores default Windows wallpaper
  * Removes Ludus-specific background configurations

* Modifies processor information:
  * Can configure custom processor name
  * Can configure custom processor vendor identifier
  * Can configure custom processor speed
  * Can configure custom processor identifier

### How to use

**Note:** Ludus Anti-Sandbox is not supported on macOS or Linux VMs at this time. Contact us if you need this feature for those platforms.

The Ludus Anti-Sandbox plugin works best with Windows VMs that have the bare minimum required to function in a hypervisor. One such template is included in the plugin: `win11-22h2-x64-enterprise-antisandbox`.

To use the Ludus Anti-Sandbox plugin, first build the `win11-22h2-x64-enterprise-antisandbox` template with the Ludus Enterprise plugin:

```shell-session
ludus templates build -n win11-22h2-x64-enterprise-antisandbox-template
[INFO]  Template building started
```

You can now use the `win11-22h2-x64-enterprise-antisandbox` template in ranges.
You should also set `force_ip: true` in the range config to ensure the VMs maintain their IP addresses for ansible after the QEMU guest agent is removed.

```yaml
ludus:
    ...
    template: win11-22h2-x64-enterprise-antisandbox
    ...
    force_ip: true
    ...
```

To take full advantage of the Anti-Sandbox feature, you must install the custom QEMU and OVMF packages:

```shell-session
ludus --url https://127.0.0.1:8081 antisandbox install-custom
[INFO]  Anti-Sandbox QEMU and OVMF installed - will take effect on VM's next power cycle
```

**Note:** The custom QEMU and OVMF packages apply to the entire Ludus host.

Once your range config is updated to use the `win11-22h2-x64-enterprise-antisandbox` template, deploy the range:

```shell-session
ludus range deploy
[INFO]  Range deploy started
```

When the range is fully deployed, make any modifications to the VMs you want before enabling Anti-Sandbox (take a snapshot as well).
When you are ready to enable Anti-Sandbox, note the VMID for the VM and run the following command. Multiple VMs can be specified with a comma separated list.

```shell-session
ludus snapshot create -n 179 -d "Clean snapshot before enabling anti-sandbox" pre-antisandbox
ludus --url https://127.0.0.1:8081 antisandbox enable -n 179
[INFO]  Enabling Anti-Sandbox settings for VM(s), this can take some time. Please wait.
[INFO]  Successfully enabled anti-sandbox for VM(s): 179
```

You can also specify `--drop-files` to populate the autologon user's desktop and download folders with random files (PPTX, DOC, XLSX, and PDF). The `--org` and `--owner` flags can be used to specify the organization and owner of the Machine set in the registry.

If there are any errors during the enable process, you can check the logs with `ludus range logs` or `ludus range errors`.

**Note:** If you experience a Blue Screen of Death (BSOD) after enabling Anti-Sandbox, you can try the following:

```
echo 1 > /sys/module/kvm/parameters/ignore_msrs
```

If that allows the VM to boot, make it permanent by adding the following to `/etc/modprobe.d/kvm.conf`:

```
options kvm ignore_msrs=1
options kvm report_ignored_msrs=0
```

### Example Anti-Sandbox Configuration

```yaml
ludus:
  - vm_name: "{{ range_id }}-ad-dc-win2022-server-x64"
    hostname: "NYC-DC01-ACQ34"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 11
    force_ip: true
    ram_gb: 8
    cpus: 4
    windows:
      sysprep: false
    domain:
      fqdn: company.com
      role: primary-dc
  - vm_name: "{{ range_id }}-ad-win11-22h2-enterprise-x64-1"
    hostname: "Q2VZX232CY"
    template: win11-22h2-x64-enterprise-antisandbox-template
    vlan: 10
    ip_last_octet: 21
    force_ip: true
    ram_gb: 8
    cpus: 4
    windows:
      install_additional_tools: false
      chocolatey_ignore_checksums: true # Chrome is always out of date
      chocolatey_packages:
        - googlechrome
        - firefox
        - adobereader
        - zoom
        - microsoft-teams-new-bootstrapper
        - webex
        - slack
        - bitwarden
        - 7zip
      office_version: 2021
      office_arch: 64bit
      autologon_user: DA-john.doe
      autologon_password: password
    domain:
      fqdn: company.com
      role: member
  - vm_name: "{{ range_id }}-ad-win11-22h2-enterprise-x64-2"
    hostname: "BAVZ2532VD"
    template: win11-22h2-x64-enterprise-antisandbox-template
    vlan: 10
    ip_last_octet: 22
    force_ip: true
    ram_gb: 8
    cpus: 4
    windows:
      install_additional_tools: false
      chocolatey_ignore_checksums: true # Chrome is always out of date
      chocolatey_packages:
        - googlechrome
        - firefox
        - adobereader
        - zoom
        - microsoft-teams-new-bootstrapper
        - webex
        - slack
        - bitwarden
        - 7zip
      office_version: 2021
      office_arch: 64bit
      autologon_user: john.doe
      autologon_password: password
    domain:
      fqdn: company.com
      role: member

defaults:
  snapshot_with_RAM: true
  stale_hours: 0
  ad_domain_functional_level: Win2012R2
  ad_forest_functional_level: Win2012R2
  ad_domain_admin: DA-john.doe
  ad_domain_admin_password: password
  ad_domain_user: john.doe
  ad_domain_user_password: password
  ad_domain_safe_mode_password: password
  timezone: America/New_York
  enable_dynamic_wallpaper: false
```

## Private Role Catalog

**Note:** Available in Ludus Enterprise.

Ludus Enterprise can optionally include a plugin that enables the use of a private role catalog.

These roles are written by Bad Sector Labs and include the following:

* Apache Guacamole server with automated VM connection creation
* Microsoft Defender for Endpoint (formerly ATP)
* Google Chronicle exporter
* Microsoft Active Directory group management
* Microsoft Active Directory user management
* Microsoft Active Directory unconstrained delegation management
* Mythic C2 Server with multiple agents and transports
* SMB Share creation and mounting
* Microsoft Sysmon
* Velociraptor Server and Client

## Outbound WireGuard

**Note:** Available in Ludus Enterprise.

### Setup

This feature routes range traffic out over a WireGuard tunnel specified in the range configuration.
This can be useful for OPSEC, OSINT, or malware research.

**While enabled, Ludus users can still interact directly VMs via RDP, SSH, etc via their Ludus WireGuard tunnel, and Ludus can still reach the VMs to configure them.**

To enable this feature, specify the `router` item in your configuration and populate the `outbound_wireguard_config` and `outbound_wireguard_vlans` keys.

The `AllowedIPs` value in your WireGuard configuration should always be `0.0.0.0/0`.
Ludus does not support "split tunnel" WireGuard configurations for outbound Wireguard at this time. Please contact us if this feature is required in your environment.

```yaml
# range-config.yml
...
router:
  outbound_wireguard_config: |-
    [Interface]
    PrivateKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
    Address = 10.0.38.224/32
    DNS = 91.231.153.2, 192.211.0.2

    [Peer]
    PublicKey = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=
    AllowedIPs = 0.0.0.0/0
    Endpoint = my.wireguard.provider.net:51820
  outbound_wireguard_vlans: # Specify which VLANs should be routed over the WireGuard tunnel
    - 10
...
```

**Warning:** IPv6 addresses in the `Address` or `AllowedIPs` fields are not supported.

### How does it work?

In order to route traffic over the WireGuard tunnel, the Linux (Debian) router marks packets from the `outbound_wireguard_vlans` (except those destined for `192.0.2.254` which is the Ludus host, or `198.51.100.0/24` which are client WireGuard addresses) using iptables. It then uses an `ip` rule to use a special `outbound_wg` routing table for these packets.

In the following example, the `ens19` interface is the interface for VLAN 10 in `outbound_wireguard_vlans`.

This is accomplished with 2 iptables rules in the `MANGLE` table's `PREROUTING` chain, and the modification of the `NAT` table's `POSTROUTING` rule for the user specified vlan's interfaces.

```plaintext
# Normal MANGLE table PREROUTING
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
```

```plaintext
# Normal NAT table POSTROUTING
Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
  146  8279 MASQUERADE  all  --  *      ens18   10.2.10.0/24        !198.51.100.0/24
    1    76 MASQUERADE  all  --  *      ens18   10.2.99.0/24        !198.51.100.0/24
```

After the outbound WireGuard tunnel is enabled:

```plaintext
# Outbound WireGuard enabled for VLAN 10 MANGLE table PREROUTING
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 RETURN     all  --  *      *       10.2.10.0/24         192.0.2.254
   11   646 MARK       all  --  *      *       10.2.10.0/24        !198.51.100.0/24      MARK set 0x1
```

```plaintext
# Outbound WireGuard enabled for VLAN 10 NAT table POSTROUTING
Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
  146  8279 MASQUERADE  all  --  *      outbound_wg   10.2.10.0/24        !198.51.100.0/24
    1    76 MASQUERADE  all  --  *      ens18   10.2.99.0/24        !198.51.100.0/24
```
