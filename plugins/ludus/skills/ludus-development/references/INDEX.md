# Ludus Documentation Reference Index

This index provides a categorized guide to all Ludus documentation references. Use this to locate the appropriate document for a given topic.

## Core Concepts

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Introduction](./introduction.md) | What Ludus is, system requirements, getting started overview | Understanding Ludus basics, checking hardware requirements |
| [Range Configuration](./configuration.md) | Full range config YAML format with all fields documented | Writing or modifying range configuration files |
| [Range Config Schema](./range-config-schema.md) | Detailed JSON schema reference for all config properties, types, and constraints | Validating config values, understanding field constraints and enums |
| [CLI Reference](./cli.md) | Complete Ludus CLI command reference | Looking up CLI commands, flags, and usage patterns |
| [API Reference](./api.md) | Full REST API endpoint documentation | Interacting with Ludus programmatically, understanding API capabilities |

## Quick Start Guides

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Install Ludus](./quick-start-install.md) | Server installation on Debian 12/13 or Proxmox 8/9 | First-time Ludus server setup |
| [Create a User](./quick-start-user-setup.md) | Creating users, setting API keys, getting Proxmox credentials | Initial user setup after install |
| [Build Templates](./quick-start-templates.md) | Building VM templates from ISOs | Setting up base VM templates |
| [Deploy a Range](./quick-start-deploy.md) | Deploying ranges, WireGuard setup, accessing VMs | Deploying and accessing a range for the first time |
| [Testing Mode](./quick-start-testing.md) | Entering/exiting testing mode, allowing domains and IPs | Using testing mode for safe tool/technique testing |
| [Local CLI Setup](./quick-start-local-cli.md) | Installing CLI on local machine, WireGuard, SSH tunnels | Setting up remote Ludus management |

## Infrastructure & Networking

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Networking](./networking.md) | Network architecture, VLANs, firewall rules, testing mode, packet capture | Understanding Ludus networking, writing firewall rules |
| [DNS](./dns.md) | AdGuard Home DNS, query logs, DNS rewrites, custom filtering | DNS configuration and troubleshooting |
| [Templates](./templates.md) | Template overview, builtin/custom templates, performance tuning | Creating or modifying VM templates |
| [Storage](./storage.md) | Storage types (Directory, LVM-thin, ZFS, Ceph), adding storage | Storage configuration and planning |

## Range Management

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Roles](./roles.md) | Using Ansible roles, role_vars, community role catalog | Adding automation roles to VMs |
| [Deploy Tags](./deploy-tags.md) | All deploy tags with meanings, common use cases | Partial deployments, redeploying specific components |
| [Snapshots](./snapshots.md) | Creating, reverting, and managing VM snapshots | Snapshot management outside of testing mode |
| [Sharing](./sharing.md) | Sharing ranges between users, workshops, multi-range setups | Collaborative range access |
| [File Share](./file-share.md) | SMB file share server setup and usage | Sharing files between ranges |
| [Nexus Cache](./nexus-cache.md) | Chocolatey/NuGet package caching | Speeding up deployments, avoiding rate limits |
| [Passwords](./passwords.md) | Default credentials for all VM types | Logging into VMs, changing domain passwords |

## Deployment Options

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Bare Metal](./deploy-bare-metal.md) | Recommended hardware, mini PC options, purchase links | Choosing and buying hardware for Ludus |
| [Proxmox](./deploy-proxmox.md) | Installing on existing Proxmox 8/9 servers | Adding Ludus to existing Proxmox infrastructure |
| [Azure](./deploy-azure.md) | Azure nested virtualization setup, ARM templates | Cloud deployment on Azure |
| [Google Cloud](./deploy-google-cloud.md) | GCP deployment via gcloud CLI and Terraform | Cloud deployment on GCP |
| [Hyper-V](./deploy-hyper-v.md) | Hyper-V VM setup for Ludus | Running Ludus in Hyper-V |
| [VMware Fusion](./deploy-vmware-fusion.md) | VMware Fusion setup (Intel Macs only) | Running Ludus in VMware Fusion |

## Environment Guides

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Basic AD Network](./env-basic-ad.md) | Default AD config: DC, Win11 workstation, Kali | Simple Active Directory lab setup |
| [GOAD](./env-goad.md) | Game of Active Directory deployment | Complex multi-domain AD lab |
| [GOAD NHA](./env-goad-nha.md) | GOAD NHA variant | NHA-specific GOAD configuration |
| [GOAD SCCM](./env-goad-sccm.md) | GOAD SCCM variant | SCCM-specific GOAD configuration |
| [SCCM Lab](./env-sccm.md) | Full SCCM/ConfigMgr environment | SCCM attack and defense lab |
| [ADCS Lab](./env-adcs.md) | Active Directory Certificate Services with ESC1-15 | Certificate services attack paths |
| [Elastic Security](./env-elastic.md) | Elastic Security server with endpoint agents | EDR/SIEM lab with Elastic |
| [Splunk Attack Range](./env-splunk.md) | Splunk Enterprise with attack simulation | Splunk-based detection lab |
| [Malware Lab](./env-malware-lab.md) | Malware analysis lab with xz backdoor (CVE-2024-3094) | Malware analysis and reverse engineering |
| [Pivot Lab](./env-pivot-lab.md) | Network pivoting lab with walkthroughs for multiple tools | Practicing network pivoting techniques |
| [Vulhub](./env-vulhub.md) | Vulhub vulnerable environments | Running Vulhub containers in Ludus |
| [Workshops](./env-workshops.md) | Conference workshop configs (SANS, BarbHack, leHACK, NetExec) | Reproducing workshop environments |

## Administration & Security

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Admin Notes](./admin-notes.md) | Promoting/demoting users, forcing testing mode off, resource calculation | Ludus server administration tasks |
| [Security](./security.md) | External access hardening, SSH access, malicious user mitigations | Securing a Ludus deployment |
| [Updating](./updating.md) | Updating server and client on all platforms | Keeping Ludus up to date |

## Enterprise Features

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Enterprise](./enterprise.md) | Feature comparison, KMS, anti-sandbox, outbound WireGuard, private roles | Enterprise-specific features and licensing |

## Development

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Developers](./developers.md) | Contributing guide, building from source, Ansible role development, CI/CD | Contributing to Ludus or developing custom roles |

## Troubleshooting

| Document | Description | When to Reference |
|----------|-------------|-------------------|
| [Troubleshooting](./troubleshooting.md) | All troubleshooting topics: Proxmox, templates, network, Ansible, WireGuard, Kali, Flare-VM, KasmVNC, client, API keys, packer cache, uninstall | Diagnosing and fixing issues |
