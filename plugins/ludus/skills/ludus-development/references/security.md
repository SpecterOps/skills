# Security

Security considerations for Ludus deployments.

The nature of Ludus, allowing users to add Ansible and Packer templates, presents security risks.
While efforts have been made to secure Ludus against malicious users, only trusted users should be granted access to Ludus.

## External Access

By default, Ludus listens on port 8080 on all interfaces. This allows users to deploy Ludus in a private network (like on a small form factor computer or laptop) and be able to access it immediately. However, if Ludus is deployed on a system with a public IP, access to port 8080 should be restricted. Ideally, a firewall should be used to disable all access to port 8080 except over WireGuard.

The following iptables command can be run on the Ludus host to restrict traffic to the Ludus server to only hosts that are connected via WireGuard.

```bash
sudo iptables -I INPUT -p tcp --dport 8080 ! -i wg0 -j DROP

# Persist the rule across reboots
sudo apt install iptables-persistent
sudo /sbin/iptables-save > /etc/iptables/rules.v4
```

You may also wish to limit access to the Proxmox web interface (tcp/8006) in the same way.

## Always Blocked Networks

If you wish to always prevent range networks from reaching a specific network, such as the LAN the Ludus host is deployed on, you can define a list of CIDRs that the range router will prevent access to in the `always_blocked_networks` key in your range config.

```
network: 
  always_blocked_networks:   # Define any networks that ranges should never be able to reach (i.e. the LAN where the Ludus host is located)
    - 192.168.1.0/24         # entries must be in CIDR format
```

## SSH Access

Users that have SSH access to the Ludus host can interact with any deployed VM if they tunnel traffic through the Ludus host, or initiate connections with utilities on the Ludus host.
For this reason, only trusted users should have SSH access to the Ludus host. The easiest way to prevent user access via SSH is to use [key-only authentication](https://www.server-world.info/en/note?os=Debian_12&p=ssh&f=4).

You may set the following iptables rules to limit access to the range routers from the ludus host to only system processes and the `ludus` user.

```
# For each user
iptables -A OUTPUT -d 10.{{ USER RANGE SECOND OCTET }}.0.0/16 ! -o {{ LUDUS EXTERNAL INTERFACE }} -m owner --uid-owner {{ UID }} -m comment --comment "Allow {{ USERNAME }} to reach their range" -j ACCEPT

# After all user rules have been added
iptables -A OUTPUT -d 10.0.0.0/8 ! -o {{ LUDUS EXTERNAL INTERFACE }} -m owner --uid-owner 0-999 -m comment --comment "Ludus: allow system processes to 10/8" -j ACCEPT
iptables -A OUTPUT -d 10.0.0.0/8 ! -o {{ LUDUS EXTERNAL INTERFACE }} -m owner --uid-owner {{ LUDUS USER UID }} -m comment --comment "Ludus: default allow ludus access to all user ranges" -j ACCEPT
iptables -A OUTPUT -d 10.0.0.0/8 ! -o {{ LUDUS EXTERNAL INTERFACE }} -m comment --comment "Ludus: default deny access to user ranges" -j DROP

iptables-save /etc/iptables/rules.v4
```

## Malicious Users

Giving users the ability to add arbitrary Ansible roles is effectively allowing for remote code execution, as a role could simply be a reverse shell executed on host `localhost` (the Ludus host).
The flexibility offered by arbitrary Ansible roles is worth the security trade off for nearly all use cases.

To prevent non-admin users from adding Ansible roles or collections, set the following option in the Ludus config file.

```yaml
# /opt/ludus/config.yml
prevent_user_ansible_add: true
```

The Ludus server process (port 8080), is heavily sandboxed (i.e. all files outside of /opt/ludus are read only), however there are likely still methods of privilege escalation.

User's router VMs are configured to allow traffic from the Ludus host, and the user's WireGuard IP. A user could write an Ansible module to execute as `localhost` and interact with other user's router VMs.

## CPU Flaws

In order to maximize CPU speed, Ludus disables all CPU mitigations for meltdown, spectre, retbleed, downfall, and others.
Ludus makes conscious tradeoffs between security and usability.
Ludus is designed for individual or team use, and not to be shared with untrusted users.

## Passwords

In order to allow admins to impersonate users (act on their behalf), user Proxmox passwords are stored in plain text and are readable by the `ludus` user. Malicious users could deploy custom Ansible roles to read other user's Proxmox credentials.

Simple passwords (often literally `password`) are used throughout Ludus virtual machines. Ludus VMs are meant for testing and not serious infrastructure deployment.
