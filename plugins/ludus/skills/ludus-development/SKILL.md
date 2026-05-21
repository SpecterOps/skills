---
name: ludus-development
description: Provides information on how to develop Ludus configuration files
license: MIT
metadata:
  author: xpn
  version: "0.2.0"
  category: security
icon: ./assets/icon.png
---

# Ludus Configuration Skill

## When to Use

Use this skill when tasked to work on a project related to Ludus, including Ludus range configurations, Ludus roles, Ludus CLI usage, Ludus API interaction, or Ludus supporting files.

## When NOT to Use

Do not use this skill when the task you are given does not mention Ludus.

## Terminology

- **Ludus** - A system to build easy to use cyber environments ("ranges") for testing and development, built on Proxmox
- **Range** - A collection of VMs, networks, and firewall rules deployed by Ludus from a single YAML configuration file
- **Template** - A base VM image built from ISO that Ludus clones to create range VMs
- **VLAN** - Virtual LAN segments within a range; each VLAN becomes the third octet of the VM's IP (e.g., VLAN 10 = 10.X.10.Y)
- **Testing Mode** - A Ludus state that snapshots VMs and blocks internet access for safe tool/technique testing
- **Router VM** - A Debian-based VM automatically deployed per range that handles routing, DNS (AdGuard Home), and firewall rules
- **Deploy Tags** - Ansible tags that control which parts of the deployment process run (e.g., `vm-deploy`, `network`, `user-defined-roles`)
- **Role** - An Ansible role added to Ludus and applied to VMs during deployment for additional configuration

## Ludus Overview

Ludus is a system to build easy to use cyber environments, or "ranges" for testing and development.

Built on Proxmox, Ludus enables advanced automation while still allowing easy manual modifications or setup of virtual machines and networks.

Ludus is implemented as a server that runs Packer and Ansible to create templates and deploy complex cyber environments from a single configuration file. Ludus is accessed via the Ludus CLI (client) or the Proxmox web interface. Normal users should not need to access Ludus via SSH.

Users can always make manual changes or set up manual environments via Proxmox instead of/in addition to Ludus managed VMs/networks. Ludus is an automation overlay on top of Proxmox, not a 100% replacement for manual configuration - just most of the common setup tasks!

### Key Concepts

- Range configs are YAML files with a `ludus` array of VM definitions plus optional `network`, `router`, `defaults`, and `notify` sections
- VMs are assigned to VLANs (2-255) and given a unique `ip_last_octet` within the VLAN
- IP addresses follow the pattern: `10.<range_number>.<vlan>.<ip_last_octet>`
- The `{{ range_id }}` template string in configs resolves to the user's ID (e.g., "JD")
- Windows VMs require a `windows` key; Linux VMs require `linux: true`; macOS VMs require `macOS: true`
- Ansible roles are added via `ludus ansible role add` and referenced in the `roles` array per VM
- Network firewall rules use iptables on the router VM with `LUDUS_USER_RULES` and `LUDUS_DEFAULTS` chains

## References

For detailed information on specific areas of Ludus, consult the [Reference Index](./references/INDEX.md) which catalogs all available documentation.

Key references for common tasks:

* [Reference Index](./references/INDEX.md) - Master index of all documentation with descriptions and when to reference each document
* [Range Configuration](./references/configuration.md) - Full annotated range config YAML example with all fields
* [Range Config Schema](./references/range-config-schema.md) - JSON schema reference for all config properties, types, constraints, and enum values
* [API Reference](./references/api.md) - Complete REST API endpoint documentation
* [CLI Reference](./references/cli.md) - All Ludus CLI commands and flags
* [Networking](./references/networking.md) - Network architecture, VLANs, firewall rules, and packet capture
* [Templates](./references/templates.md) - Template management, creation, and performance tuning
* [Roles](./references/roles.md) - Using Ansible roles with Ludus and the community role catalog
* [Deploy Tags](./references/deploy-tags.md) - Controlling partial deployments with tags
* [Troubleshooting](./references/troubleshooting.md) - Solutions for common issues
