# Basic Active Directory Network

Default Ludus configuration with a Domain Controller, Windows 11 workstation, and Kali VM. Users are created with this basic AD network as their default configuration.

The configuration, if deployed without modification, looks like this (for UserID: `JD` with RangeID: `2`):

This network contains a Domain Controller (`JD-DC01-2022`) for the domain `ludus.domain`, and Windows 11 workstation (`JD-WIN11-22H2-1` with Office 2019 64bit, Chrome, Firefox, Burpsuite, VSCode, 7zip, process hacker, ilspy and other useful utilities), and a Kali VM (`JD-Kali`) in a separate network.
The Windows hosts can only reach the Kali VM on tcp/80, tcp/443, and tcp/8080.
The Kali VM can reach the Windows VM on any protocol and any port.

When testing mode is enabled, both Windows hosts will be snapshotted and blocked from reaching the internet, while the Kali VM will not be snapshotted or blocked from reaching the internet.

The configuration for this range is below:

```yaml
ludus:
  - vm_name: "{{ range_id }}-ad-dc-win2022-server-x64"
    hostname: "{{ range_id }}-DC01-2022"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 11
    ram_gb: 8
    cpus: 4
    windows:
      sysprep: false
    domain:
      fqdn: ludus.domain
      role: primary-dc
  - vm_name: "{{ range_id }}-ad-win11-22h2-enterprise-x64-1"
    hostname: "{{ range_id }}-WIN11-22H2-1"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 21
    ram_gb: 8
    cpus: 4
    windows:
      install_additional_tools: true
      office_version: 2019
      office_arch: 64bit
    domain:
      fqdn: ludus.domain
      role: member
  - vm_name: "{{ range_id }}-kali"
    hostname: "{{ range_id }}-kali"
    template: kali-x64-desktop-template
    vlan: 99
    ip_last_octet: 1
    ram_gb: 8
    cpus: 4
    linux: true
    testing:
      snapshot: false
      block_internet: false

network:
  inter_vlan_default: REJECT
  rules:
    - name: Only allow windows to kali on 443
      vlan_src: 10
      vlan_dst: 99
      protocol: tcp
      ports: 443
      action: ACCEPT
    - name: Only allow windows to kali on 80
      vlan_src: 10
      vlan_dst: 99
      protocol: tcp
      ports: 80
      action: ACCEPT
    - name: Only allow windows to kali on 8080
      vlan_src: 10
      vlan_dst: 99
      protocol: tcp
      ports: 8080
      action: ACCEPT          
    - name: Allow kali to all windows
      vlan_src: 99
      vlan_dst: 10
      protocol: all
      ports: all
      action: ACCEPT
```
