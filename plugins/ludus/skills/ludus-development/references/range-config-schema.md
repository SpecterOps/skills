# Range Configuration Schema Reference

This document describes the JSON schema for Ludus range configuration files. The schema URL is `https://docs.ludus.cloud/schemas/range-config.json`. Range configs are written in YAML and validated against this schema.

The top-level object does not allow additional properties beyond those documented here.

## Top-Level Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `ludus` | array | **Yes** | Array of VM definitions |
| `network` | object | No | Network/firewall rules |
| `router` | object | No | Router VM settings |
| `defaults` | object | No | Default settings for domains and range behavior |
| `global_role_vars` | any | No | Variables passed to ALL user-defined roles on ALL VMs |
| `notify` | object | No | Notification settings for deployment completion/failure |

---

## VM Definition (`ludus` array items)

Each item in the `ludus` array defines a single VM. No additional properties are allowed.

**Constraint:** Each VM must have exactly one of `windows`, `linux`, or `macOS`. You cannot combine them (e.g., a VM cannot be both `windows: true` and `linux: true`).

### Required Properties

| Property | Type | Constraints | Description |
|---|---|---|---|
| `vm_name` | string | — | The name of the VM in Proxmox. Supports `{{ range_id }}` template string which resolves to the user's range ID (e.g. `JS`). |
| `hostname` | string | — | The hostname for the VM. Windows hostnames are limited to 15 characters due to NETBIOS. |
| `template` | string | — | The template that will be the base for this VM. Use `ludus templates list` to see available templates. |
| `vlan` | integer | min: 2, max: 255 | The VLAN for this VM. This number becomes the third octet of the VM's IP address. |
| `ip_last_octet` | integer | min: 1, max: 255 | The last octet for this VM's IP address. Must be unique within the VLAN. |
| `ram_gb` | integer | min: 1, max: 4096 | RAM in GB. In non-ballooning mode this is the fixed allocation. In ballooning mode (when `ram_min_gb` is also set) this is the maximum. |
| `cpus` | integer | min: 1, max: 512 | Number of CPU cores to allocate. Can exceed the host's physical CPU count. |

### Optional Properties

| Property | Type | Constraints | Description |
|---|---|---|---|
| `ram_min_gb` | integer | min: 1, max: 4096 | If defined, enables ballooning mode with this as the minimum RAM allocation. |
| `full_clone` | boolean | — | `true` for full clone, `false` for linked clone. Default: `false`. |
| `force_ip` | boolean | — | If `true`, the config-defined IP address is used when no IP is available via qemu-guest-agent. Only use for EDR appliances or anti-sandbox VMs without qemu-guest-agent. |
| `unmanaged` | boolean | — | Set `true` for VMs that cannot report an IP to Ansible via Proxmox (no qemu-guest-agent, e.g. EDR appliances). |
| `testing` | object | — | Controls behavior in testing mode. See [Testing Properties](#testing-properties). |
| `windows` | object | — | Windows-specific settings. See [Windows Properties](#windows-properties). |
| `linux` | boolean or object | — | Set `true` for Linux VMs, or provide an object with a `packages` array. See [Linux Properties](#linux-properties). |
| `macOS` | boolean | — | Set `true` for macOS VMs. |
| `domain` | object | — | Windows domain membership settings. See [Domain Properties](#domain-properties). |
| `roles` | array | — | User-defined Ansible roles. See [Roles and Role Variables](#roles-and-role-variables). |
| `role_vars` | any | — | Variables passed to all user-defined roles on this VM. Accepts any type: number, string, boolean, object, array, or null. |
| `ansible_groups` | array of strings | — | User-defined Ansible groups for this VM. Used in Ansible inventory and `range inventory` output. |
| `dns_rewrites` | array of strings | — | Domain names to assign this VM's IP in DNS for the whole range. Wildcards are allowed. |
| `primary_dns_server` | string | — | The primary DNS server to set for the VM. |
| `secondary_dns_server` | string | — | A secondary DNS server to set for the VM. |

---

### Windows Properties

The `windows` key is an object with the following optional properties. No additional properties are allowed.

**Dependent requirement:** If `autologon_user` is specified, `autologon_password` must also be specified.

| Property | Type | Constraints | Description |
|---|---|---|---|
| `sysprep` | boolean | — | Run sysprep before any other tasks on this VM. Default: `false`. |
| `install_additional_tools` | boolean | — | Install Firefox, Chrome, VSCode, Burp Suite, 7zip, Process Hacker, ILSpy, and other utilities. Default: `false`. |
| `chocolatey_ignore_checksums` | boolean | — | Ignore checksum errors when installing Chocolatey packages (for packages hosted by third parties that update before the choco package). Default: `false`. |
| `chocolatey_packages` | array of strings | — | Chocolatey package names to install on this VM. Default: none. |
| `office_version` | integer | enum: `2013`, `2016`, `2019`, `2021` | Microsoft Office version to install. Default: undefined (don't install Office). |
| `office_arch` | string | enum: `"64bit"`, `"32bit"` | Architecture for the Office install. Default: undefined (don't install Office). |
| `visual_studio_version` | integer | enum: `2017`, `2019`, `2022` | Visual Studio Community edition version. Note: 2022 cannot target < .NET 4.5. Default: undefined (don't install). |
| `autologon_user` | string | — | Username for autologon. Default: `localuser` unless domain-joined, then `defaults.ad_domain_user`. |
| `autologon_password` | string | — | Password for autologon. Default: `password` unless domain-joined, then `defaults.ad_domain_user_password`. |
| `gpos` | array of strings | enum items: `"disable_defender"`, `"anon_share_access"` | GPOs to enable for the domain. **Only applies to VMs with `domain.role: "primary-dc"`**. Default: none. |

---

### Domain Properties

The `domain` key defines Windows domain membership. Both properties are required when the `domain` key is present. Only applicable to Windows VMs.

| Property | Type | Constraints | Description |
|---|---|---|---|
| `fqdn` | string | format: hostname | **Required.** The FQDN of the domain (e.g. `ludus.domain`). |
| `role` | string | enum: `"primary-dc"`, `"alt-dc"`, `"member"` | **Required.** The role of this VM in the domain. |

Role meanings:
- `primary-dc` — Primary domain controller. Creates the domain. Only one per `fqdn`. Can have `gpos` set in `windows`.
- `alt-dc` — Alternate/additional domain controller.
- `member` — Domain member (joined to the domain but not a DC).

---

### Testing Properties

The `testing` key controls VM behavior during testing mode. If undefined, both values default to `true`.

| Property | Type | Required | Description |
|---|---|---|---|
| `snapshot` | boolean | Yes (when `testing` is defined) | Snapshot this VM when entering testing mode, and revert when exiting. Default: `true`. |
| `block_internet` | boolean | Yes (when `testing` is defined) | Cut this VM off from the internet during testing. Default: `true`. |

---

### Linux Properties

The `linux` key can be either:

1. **A boolean** — Set `true` for Linux VMs.
2. **An object** with the following property:

| Property | Type | Description |
|---|---|---|
| `packages` | array of strings | Packages to install using `ansible.builtin.package` (distribution-agnostic). |

---

## Network Configuration

The `network` key defines firewall rules for the range. It is optional; by default all traffic is allowed. No additional properties are allowed.

### Network Properties

| Property | Type | Constraints | Description |
|---|---|---|---|
| `inter_vlan_default` | string | enum: `"ACCEPT"`, `"REJECT"`, `"DROP"` | Default rule for traffic between VLANs. Default: `ACCEPT`. |
| `external_default` | string | enum: `"ACCEPT"`, `"REJECT"`, `"DROP"` | Default rule for traffic leaving the range to the internet. Default: `ACCEPT`. |
| `wireguard_vlan_default` | string | enum: `"ACCEPT"`, `"REJECT"`, `"DROP"` | Default rule for traffic from range to the WireGuard subnet. Default: `ACCEPT`. |
| `always_blocked_networks` | array of strings | Items must match pattern: `^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$` | CIDR networks that are always blocked regardless of other rules. |
| `rules` | array of objects | — | Specific firewall rules. See [Rule Properties](#rule-properties). |

None of the network properties are required — the entire object can be empty or only partially specified.

### Rule Properties

Each rule in the `rules` array is an object. No additional properties are allowed.

**All of the following properties are required** (except `ip_last_octet_src` and `ip_last_octet_dst` which are optional):

| Property | Type | Constraints | Description |
|---|---|---|---|
| `name` | string | **Required** | Rule name, added as a comment in iptables. |
| `vlan_src` | integer or string | **Required.** Integer: min 2, max 255. String enum: `"public"`, `"all"`, `"wireguard"` | Source VLAN for the traffic. |
| `vlan_dst` | integer or string | **Required.** Integer: min 2, max 255. String enum: `"public"`, `"all"`, `"wireguard"` | Destination VLAN for the traffic. |
| `ip_last_octet_src` | integer or string | Optional. Integer: min 1, max 255. String pattern: `^[0-9]{1,3}-[0-9]{1,3}$` | Single machine or range of machines (e.g. `10-20`) from `vlan_src` to apply the rule to. |
| `ip_last_octet_dst` | integer or string | Optional. Integer: min 1, max 255. String pattern: `^[0-9]{1,3}-[0-9]{1,3}$` | Single machine or range of machines from `vlan_dst` to apply the rule to. |
| `protocol` | string | **Required.** Enum: `"tcp"`, `"udp"`, `"udplite"`, `"icmp"`, `"ipv6-icmp"`, `"esp"`, `"ah"`, `"sctp"`, `"all"` | The protocol the rule acts on. |
| `ports` | integer or string | **Required.** Integer: min 0, max 65535. String pattern: `^([0-9]{1,5}|[0-9]{1,5}:[0-9]{1,5}|all)$` | A single port number, a range in `start:end` format, or `"all"`. |
| `action` | string | **Required.** Enum: `"ACCEPT"`, `"REJECT"`, `"DROP"` | Action to apply to matching packets. |

Special `vlan_src`/`vlan_dst` string values:
- `"public"` — Traffic from/to the public (external) network.
- `"all"` — Matches all VLANs.
- `"wireguard"` — Traffic from/to the WireGuard VPN subnet.

---

## Router Configuration

The `router` key configures the range's router VM. All properties are optional. No additional properties are allowed.

**Dependent requirement:** If `outbound_wireguard_config` is specified, `outbound_wireguard_vlans` must also be specified.

### Router Properties

| Property | Type | Constraints | Description |
|---|---|---|---|
| `vm_name` | string | — | The name of the router VM in Proxmox. Supports `{{ range_id }}` template string. |
| `hostname` | string | — | The hostname for the router VM. |
| `template` | string | — | The template to base the router VM on. |
| `ram_gb` | integer | min: 1, max: 4096 | RAM in GB (fixed or max in ballooning mode). |
| `ram_min_gb` | integer | min: 1, max: 4096 | Minimum RAM in GB (enables ballooning mode). |
| `cpus` | integer | min: 1, max: 512 | Number of CPU cores. |
| `roles` | array | — | Ansible roles to apply to the router. See [Roles and Role Variables](#roles-and-role-variables). |
| `role_vars` | any | — | Variables passed to all roles on the router. |
| `outbound_wireguard_config` | string | — | Contents of a WireGuard client configuration. The router will direct traffic out through this VPN for VLANs listed in `outbound_wireguard_vlans`. |
| `outbound_wireguard_vlans` | array of integers | — | VLANs whose traffic will be routed over the outbound WireGuard VPN. |
| `inbound_wireguard` | object | — | Inbound WireGuard server settings. See below. |
| `iptables_commands` | array of strings | — | Raw iptables commands run after firewall configuration. **Use with caution** — these can allow traffic that Ludus features would otherwise block. Example: `iptables -I LUDUS_DEFAULTS -i ens18 -s 192.0.2.103 -j ACCEPT` |

### Inbound WireGuard Properties

The `inbound_wireguard` object configures a WireGuard server on the router for inbound VPN access.

| Property | Type | Constraints | Description |
|---|---|---|---|
| `enabled` | boolean | **Required** | Enable or disable the WireGuard server on the router. Default: `false`. |
| `server_cidr` | string | Pattern: CIDR notation | The CIDR of the WireGuard server network. Default: `10.254.254.0/24`. |
| `port` | integer | enum: `51820` | The UDP port for the WireGuard server. Must be `51820` to work with port forwarding. Default: `51820`. |
| `allowed_vlans` | array of integers | Items: min 1, max 255 | VLANs that WireGuard clients are allowed to connect to. Default: all VLANs. |

---

## Defaults Configuration

The `defaults` key defines default settings for the range and Windows domains. When specified, **all properties are required**.

| Property | Type | Constraints | Description |
|---|---|---|---|
| `snapshot_with_RAM` | boolean | **Required** | When entering testing mode, capture RAM state to allow reverting to a running VM. |
| `stale_hours` | integer | **Required** | Hours until a pre-existing snapshot is deleted and retaken (for quick testing mode enter/exit cycles). |
| `ad_domain_functional_level` | string | **Required.** Enum: `"Win2003"`, `"Win2008"`, `"Win2008R2"`, `"Win2012"`, `"Win2012R2"`, `"WinThreshold"`, `"Win2025"` | Functional level of each Windows domain created by Ludus. |
| `ad_forest_functional_level` | string | **Required.** Enum: `"Win2003"`, `"Win2008"`, `"Win2008R2"`, `"Win2012"`, `"Win2012R2"`, `"WinThreshold"`, `"Win2025"` | Functional level of each Windows forest created by Ludus. |
| `ad_domain_admin` | string | **Required** | Domain admin username for every Windows domain. |
| `ad_domain_admin_password` | string | **Required** | Domain admin password for every Windows domain. |
| `ad_domain_user` | string | **Required** | Domain user username for every Windows domain. |
| `ad_domain_user_password` | string | **Required** | Domain user password for every Windows domain. |
| `ad_domain_safe_mode_password` | string | **Required** | Domain safe mode password for every Windows domain. |
| `timezone` | string | **Required** | Unix TZ format timezone string for all VMs in the range (e.g. `America/New_York`). |
| `enable_dynamic_wallpaper` | boolean | **Required** | Enable dynamic wallpaper for all Windows VMs in the range. Default: `true`. |

---

## Notify Configuration

The `notify` key configures notifications when a range deployment finishes or fails.

| Property | Type | Required | Description |
|---|---|---|---|
| `urls` | array of strings | **Yes** | Shoutrrr notification URLs. See [Shoutrrr services](https://containrrr.dev/shoutrrr/services/overview/) for supported services and URL formats. |

---

## Roles and Role Variables

### Roles Array

The `roles` property (available on VMs and the router) is an array where each item is one of:

1. **A string** — The name of an Ansible role installed on the Ludus host via `ludus ansible role add`.
   ```yaml
   roles:
     - my_role_name
   ```

2. **An object** with `name` and optional `depends_on`:
   ```yaml
   roles:
     - name: my_role_name
       depends_on:
         - vm_name: "{{ runique_id }}-dc01"
           role: some_other_role
   ```

   Object properties:

   | Property | Type | Required | Description |
   |---|---|---|---|
   | `name` | string | **Yes** | The role name. |
   | `depends_on` | array of objects | No | List of dependencies that must complete before this role runs. |

   Each `depends_on` item:

   | Property | Type | Required | Description |
   |---|---|---|---|
   | `vm_name` | string | **Yes** | The `vm_name` of the VM that must complete its role first. |
   | `role` | string | **Yes** | The role name that must complete on that VM first. |

### Role Variables (`role_vars` and `global_role_vars`)

Both `role_vars` (per-VM) and `global_role_vars` (top-level, applies to all VMs) accept any valid YAML value: number, string, boolean, object, array, or null. These variables are passed to ALL user-defined roles during Ansible execution.

Variables are specified as key-value pairs:
```yaml
role_vars:
  my_var: "value"
  my_number: 42
  my_list:
    - item1
    - item2
```

---

## IP Address Scheme

The full IP address of a VM is constructed as: `10.<range_second_octet>.<vlan>.<ip_last_octet>` where the second octet is assigned by Ludus based on the user's range ID. For example, a VM with `vlan: 10` and `ip_last_octet: 2` in a range with second octet `5` would have IP `10.5.10.2`.

---

## DNS Rewrites

The `dns_rewrites` property is an array of domain name strings. Each domain listed will resolve to the VM's IP address in DNS for the entire range. Wildcard entries are supported (e.g. `*.example.com`).

```yaml
dns_rewrites:
  - "myapp.example.com"
  - "*.internal.corp"
```
