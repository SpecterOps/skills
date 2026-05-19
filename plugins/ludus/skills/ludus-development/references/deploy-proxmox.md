# Proxmox Deployment

Reference for installing Ludus on an existing Proxmox 8/9 server, including changes Ludus makes, install steps, and datastore permissions.

**Warning:** Using an existing Proxmox installation may cause issues with existing customizations as it is impossible for Ludus to account for every Proxmox setup. If starting from scratch the bare metal Debian 12/13 install is recommended.

## Overview

Existing Proxmox 8/9 servers can install Ludus without a reboot.

Ludus will make the following changes - **do NOT do any actions below yourself before running the install script**:

- Extract files to `/opt/ludus`
- Install the following packages to the Proxmox host: ansible, packer, dnsmasq, sshpass, curl, jq, iptables-persistent, gpg-agent, dbus, dbus-user-session, and vim
- Install the following python packages to the host: proxmoxer, requests, netaddr, pywinrm, dnspython, and jmespath
- Create the proxmox groups `ludus_users` and `ludus_admins`
- Create the proxmox pools `SHARED` and `ADMIN`
- Create a wireguard server wg0 with IP range `198.51.100.0/24`
- Create an interface `vmbr1000` with IP range 192.0.2.0/24 that NATs traffic
- Create user ranges with IPs in the 10.0.0.0/16 network starting at 10.2.0.0/8 and incrementing the second octet for each user
- Create user interfaces starting at `vmbr1002` incrementing for each user
- Create the pam user `ludus` and pam users for all Ludus users added
- Create the `ludus-admin` and `ludus` systemd services that listen on 127.0.0.1:8081 and 0.0.0.0:8080

## Install

1. Run the install script. Be careful to choose your datastores correctly!

```shell
# All-in-one command
curl -s https://ludus.cloud/install | bash

# If you want to check out the install script
curl https://ludus.cloud/install > install.sh
cat install.sh
chmod +x install.sh
./install.sh
```

2. Follow the Quick start guide as normal starting at Create a User.

If you made a mistake, you can update the values in `/opt/ludus/config.yml` to reflect the install.
After updating the config, restart the ludus processes with `systemctl restart ludus-admin` and `systemctl restart ludus`.

## Datastore Permissions

If you changed the datastores you are using with Ludus, you will need to give permissions to the `ludus_users` and `ludus_admins` group. As root on your Proxmox host, run the following:

```shell
pveum acl modify /storage/<your new storage> -group ludus_users -role DatastoreUser
pveum acl modify /storage/<your new storage> -group ludus_admins -role PVEDatastoreAdmin
```

If you encounter networking issues like VMs not getting IP addresses or having internet access, see the network troubleshooting guide.
