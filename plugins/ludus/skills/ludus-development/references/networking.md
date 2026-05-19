# Networking

Ludus networking overview covering the network architecture, VLANs, firewall rules, testing mode, and packet capture.

Ludus requires a static IP for access (a requirement inherited from Proxmox) which is set during install.

## Default Networks

Ludus uses [RFC 5735](https://www.rfc-editor.org/rfc/rfc5735#section-4) defined `TEST-NET` networks to hopefully avoid IP conflicts with the network Ludus is deployed into.

### WireGuard Network (wg0)

The WireGuard interface, `198.51.100.0/24` on `wg0`, is set up during Ludus install. The Ludus host is always `198.51.100.1`. Users will be assigned static IPs in this network starting at the `.2` and incrementing as users are added. The last octet of a user's WireGuard IP will match their range number.

The user's router VM only allows traffic in from the user's WireGuard IP. Additionally, the router VM always allows related or established traffic back out to the user's WireGuard IP, regardless of any user defined rules or testing status. This allows a user to RDP, SSH, VNC, or otherwise access VMs at all times.

### NAT'd Network (vmbr1000)

There is a single default network for VMs created during install: `192.0.2.0/24`, on interface `vmbr1000` (or other interface as specified in the ludus config with `ludus_nat_interface`). This network has DHCP and DNS thanks to a `dnsmasq` service running on the Ludus host.
This network's "router" is at `.254` and offers DHCP IPs in the range of `.50` to `.100`. This DHCP pool is used for template creation.

Ludus user routers are assigned a static IP in this network where their range number + 100 is the last octet. If a user has range number 2, their router has a "WAN" interface at `192.0.2.102`. This is what limits Ludus to 153 concurrent users, because each user will take one IP from this pool of 100-253. Ludus sets up a static route for the user's /16 through this "WAN" interface, allowing ansible and wireguard clients to access the range VMs.

#### Reserved IPs in the NAT'd Network

| IP | Description |
| --- | --- |
| 192.0.2.1 | KMS server |
| 192.0.2.2 | [Nexus cache server](./nexus-cache.md) |
| 192.0.2.3 | [File share server](./file-share.md) |

The remaining 49 IPs in the `.1 - .50` range are reserved for future use.

### CI/CD Network (ludusci)

If the Ludus admin has set up CI/CD, the CI/CD network is `203.0.113.0/24` on interface `ludusci`. This network is necessary because the CI/CD Ludus VMs will themselves set up a `vmbr1000` with a range of `192.0.2.0/24` which would conflict with the "public" IP of the CI/CD Ludus VM if it was in the host's `vmbr1000` (a DHCP'd `192.0.2.50-100` IP).

## User Networks

Ludus assigns a unique Linux bridge interface in Proxmox to each user which is capable of supporting 255 VLANs (1-255). The user's `vmbr` number is 1000 + their Ludus range number (e.g. a Ludus user with range number 2 would have `vmbr1002`).
This interface can be thought of conceptually as a virtual switch. If you wish to capture packets on this interface see [Packet Capture](#packet-capture).

All user networks are /16 with VLANs of /24 in the format `10.{{ ludus range number }}.{{ VLAN }}.{{ ip_last_octet }}`. Because all user networks are within 10.0.0.0/8, admins deploying Ludus into a network within 10.0.0.0/8 will need to avoid issuing users with a range number that overlaps the existing range. Ludus admins should set the `reserved_range_numbers` array in `/opt/ludus/config.yml` for any networks that would conflict. For example, if the Ludus server itself has an IP of 10.10.0.123, the tenth created user will cause routing issues if the user is also on the 10.10.0.0/16 network. The admin should set `reserved_range_numbers: [10]` to prevent this.

VMs are limited to a single network interface when deployed with Ludus.

Users simply define which VLAN each VM is a member of in their Ludus config file and the interface, DHCP/DNS, and routing is configured on the router automatically.

```yaml
ludus:
  - vm_name: "{{ range_id }}-ad-dc-win2019-server-x64"
    hostname: "{{ range_id }}-DC01-2019"
    template: win2019-server-x64-template
    vlan: 10
    ip_last_octet: 11
    ram_gb: 8
    cpus: 4
    domain:
      fqdn: ludus.network
      role: primary-dc
    windows:
      sysprep: true
```

## User defined firewall rules

For basic setups the defaults, allow internet and allow inter-vlan-routing, will be suitable for many users and no `network` key needs to be set in the user's config.

Users are able to define custom firewall rules that will always be enforced regardless of testing status. Testing rules will be inserted above user defined rules and take precedence over them.
Rules are defined in the `network.rules` object.
Two keys exists to set the default for traffic leaving the network: `external_default`, and traffic between VLANs: `inter_vlan_default`. By default both of these values are `ACCEPT`.

Rules can act on entire vlans by not defining `ip_last_octet_src` or `ip_last_octet_dst`, ranges of machines `ip_last_octet_src: 21-25`, or single machines `ip_last_octet_src: 21`.

`vlan_src` and `vlan_dst` can accept the special values:
 - `public` which allows traffic to the internet, but not other VLANs. This is useful for cases where the `external_default` is `REJECT`. In the rule this is converted to `! 10.ID.0.0/16`.
 - `all` which is all VLANs, and is converted to `10.ID.0.0/16` in the rule.
 - `wireguard` which is the wireguard users subnet. This is converted to `198.51.100.0/24` unless an `ip_last_octet_[src|dst]` is defined.

The `ports` key is optional, and if omitted `all` is assumed. A range of ports can be defined using the `start:end` syntax. These values should be quoted to avoid yaml interpreting them as hex values.

All user defined rules are added to the `LUDUS_USER_RULES` chain except rules that use `wireguard` as a vlan src or dst; those are applied to the `LUDUS_DEFAULTS` chain so they can override the default WireGuard client access rule or any access grant rules. Rules with `wireguard` as a vlan src or dst will take priority over testing mode rules, but since they only operate against hosts in the 198.51.100.0/24 range, this should not cause any issue.

**Note:** When these rules are deployed, first all the user defined rules are removed before being re-created in order to prevent rules removed from the config from remaining active. During this time the FORWARD chain is set to drop all traffic, so VMs may lose connectivity briefly during this time.

An example of different types of user defined firewall rules are listed below.

```yaml
network:
  external_default: ACCEPT
  inter_vlan_default: REJECT
  wireguard_vlan_default: ACCEPT
  always_blocked_networks:
    - 192.168.1.0/24
  rules:
    - name: Only allow TCP 443 from VLAN 10 to VLAN 20
      vlan_src: 10
      vlan_dst: 20
      protocol: tcp
      ports: 443
      action: ACCEPT
    - name: Allow VLAN 20 out to internet using any protocol (and any port) - only useful when external_default is set to REJECT
      vlan_src: 20
      vlan_dst: public
      protocol: all
      ports: all
      action: ACCEPT
    - name: Allow VLAN 30 to all VLANs using TCP on port 80
      vlan_src: 30
      vlan_dst: all
      protocol: tcp
      ports: 80
      action: ACCEPT
    - name: Only allow the .21 on VLAN 20 to hit port 445 of the .31 on VLAN 10 using TCP
      vlan_src: 20
      ip_last_octet_src: 21
      vlan_dst: 10
      ip_last_octet_dst: 31
      protocol: tcp
      ports: 445
      action: ACCEPT
    - name: Allow the .21 to .25 machines on VLAN 20 to access the .21 on VLAN 10 using TCP
      vlan_src: 20
      ip_last_octet_src: 21-25
      vlan_dst: 10
      ip_last_octet_dst: 21
      protocol: tcp
      ports: 445
      action: ACCEPT
    - name: Allow the .11 on VLAN 10 to access the .21 to .25 machines on VLAN 20 using TCP port 8080
      vlan_src: 10
      ip_last_octet_src: 11
      vlan_dst: 20
      ip_last_octet_dst: 21-25
      protocol: tcp
      ports: 8080
      action: ACCEPT
    - name: Allow TCP ports 8080 to 8088 from VLAN 10 to VLAN 20
      vlan_src: 10
      vlan_dst: 20
      protocol: tcp
      ports: "8080:8088"
      action: ACCEPT
    - name: Block all traffic from a specific WG client to a vlan
      vlan_src: wireguard
      ip_last_octet_src: 12
      vlan_dst: 20
      protocol: all
      ports: all
      action: REJECT
    - name: Block tcp traffic from a specific WG clients to a vlan
      vlan_src: wireguard
      ip_last_octet_src: 12-15
      vlan_dst: 30
      protocol: tcp
      ports: all
      action: REJECT
    - name: Block all traffic from a specific IP to any wireguard client
      vlan_src: 10
      ip_last_octet_src: 11
      vlan_dst: wireguard
      protocol: all
      ports: all
      action: REJECT
```

See more details about the range config schema in [Configuration](./configuration.md).

## Testing Mode

Each range has a Debian based router/firewall VM.
This VM controls how traffic is routed between VLANs/subnets in the range as well as traffic out of the range to other networks/the internet.
The router uses `iptables` to control traffic flow, using three custom chains in the filter table.
Note that the FORWARD chain, which controls traffic from outside the router with a destination that is not the route itself has a policy of `DROP` meaning that if no rule matches the traffic will not be forwarded.
This is a "deny by default" policy, and prevents accidental traffic from leaving the range in the event that IP addresses change or machines are added while testing mode is enabled.

The three custom iptables chains in the filter table are:

- **LUDUS_DEFAULTS** - Contains rules for WireGuard client access and access grants
- **LUDUS_USER_RULES** - Contains user-defined firewall rules
- **LUDUS_TESTING** - Contains testing mode rules (blocking internet, DNS)

Testing rules are inserted above user defined rules and take precedence.

## Packet Capture

By default, the bridge interfaces in Proxmox are MAC aware, which means they will "learn" which MACs are on which "ports" and only send traffic for a MAC to its "port." This means that VMs on the same VLAN only see traffic destined for their MAC (and broadcast) by default. If you wish to use some type of packet capture appliance like Zeek or Suricata, the `bridge-ageing` parameter needs to be set to `0` on the Proxmox host for the bridge interface of the range. This effectively turns the bridge interface into a hub, where all traffic on a VLAN is sent to all machines.

To complete this step, open up a shell to your proxmox host and enter the following commands:

`brctl setageing vmbr10XX 0` where `vmbr10XX` is the Linux bridge for your Ludus range (1000 + range number/range second octet)

You can confirm this settings with the `ip -d link show vmbr10XX` command which should show `ageing_time 0`.

To make this change persist reboots of the Ludus server, add `bridge-ageing 0` to the options for the interface in `/etc/network/interfaces`
