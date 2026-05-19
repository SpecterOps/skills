# Ludus Introduction

Ludus is a system to build easy-to-use cyber environments, or "ranges," for testing and development.

> "90 percent of security research is getting test environments setup properly" - @hotnops

Built on [Proxmox](https://www.proxmox.com/en/), Ludus enables advanced automation while still allowing easy manual modifications or setup of virtual machines and networks.

Ludus is implemented as a server that runs [Packer](https://www.packer.io/) and [Ansible](https://www.ansible.com/) to create templates and deploy complex cyber environments from a single configuration file. Ludus is accessed via the [Ludus CLI](./cli.md) (client) or the Proxmox web interface. Normal users should not need to access Ludus via SSH.

As a user, you can *always* make manual changes or set up manual environments via Proxmox instead of/in addition to Ludus managed VMs/networks.
Ludus is an automation overlay on top of Proxmox, not a 100% replacement for manual configuration - just most of the common setup tasks!

## Getting Started

Ludus is *only* compatible with virtualization capable Debian 12/13 or Proxmox 8/9. No other environments or hosting solutions will be supported.

### Requirements

- x86_64 (aka amd64 aka 64-bit "Intel") CPU with a [Passmark](https://www.cpubenchmark.net/cpu_list.php) score > 6,000
- A host capable of virtualization running Debian 12/13 or Proxmox 8/9 (e.g. "bare metal", Azure Dv3 and Ev3, AWS *.metal, supported Google Cloud VMs)
- at least 32GB RAM per user/range that will be deployed
- at least 200GB storage for initial templates and at least 50GB per user/range that will be deployed (large, fast NVMe drives recommended)
- no more than 150 users per Ludus host
- Internet connected (not via WiFi)
- Root shell access
- If you want to access Ludus across the internet
    - 1 public IP address
    - the ability to allow in arbitrary ports (i.e. port forwarding or control of the cloud firewall)

Machines with lower specs than listed above may work, but are not tested/supported.

### User Quick Start

If you are a Ludus user and your Ludus server has already been installed, getting started is easy!

1. Get your API key and WireGuard config from your Ludus admin.
2. Download or compile the Ludus client
3. Import and connect the WireGuard VPN
4. Run `ludus apikey` and give it your API key
5. Use the **[Ludus CLI](./cli.md)** to manage your range!
