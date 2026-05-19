# Range Configuration

The Ludus range configuration file is a YAML document that describes the virtual machines and optionally the network rules, router settings, and defaults a user would like to deploy.

**Tip:** You can add the following to the top of your range config to get schema validation in your editor, if your editor supports it:

```
# yaml-language-server: $schema=https://docs.ludus.cloud/schemas/range-config.json
```

The full JSON schema is available at: https://docs.ludus.cloud/schemas/range-config.json

## Range Config Example

```yaml
# yaml-language-server: $schema=https://docs.ludus.cloud/schemas/range-config.json

ludus:
  - vm_name: "{{ range_id }}-ad-dc-win2019-server-x64" # The name of the VM in Proxmox. You can use the `{{ range_id }}` template string which resolves to your range ID (i.e. JS)
    hostname: "{{ range_id }}-DC01-2019"   # The hostname for the VM. Note: Windows host names are limited to 15 characters due to NETBIOS
    template: win2019-server-x64-template  # The template that will be the base for this VM (`ludus templates list` to get a list of them)
    vlan: 10            # The VLAN for this VM. This number will be the third octet of the VM's IP and must be 2<=vlan<=255
    ip_last_octet: 11   # The last octet for this VM's IP address. Must be unique in the VLAN.
    force_ip: true      # If set to true, the config defined IP address will be used for the VM when no IP is available via qemu-guest-agent (only use for EDR appliances or anti-sandbox VMs that do not have qemu-guest-agent installed)
    ram_gb: 8           # The amount of RAM for this VM
    cpus: 4             # The number of cpu cores to allocate to this VM (can provision more CPUs than the host physically has)
    windows:            # This key must be set for windows VMs - all subkeys are optional
      sysprep: false    # Set to true to run sysprep before any other tasks on this VM. Default: false
      gpos:
        - disable_defender   # Create and link a GPO this disables Windows Defender for every domain joined Windows machine
        - anon_share_access # Create and link a GPO that enables anonymous SMB share access for every domain joined Windows machine (for use with `ludus range deploy -t share`)
    domain:               # Define this key to put this machine in a domain
      fqdn: ludus.network # The FQDN of the domain
      role: primary-dc    # The role of the VM in the domain (primary-dc|alt-dc|member)
    linux: false          # Set this to true for linux VMs - leave undefined or false for Windows/macOS VMs
    macOS : false         # Set this to true for macOS VMs - leave undefined or false for Windows/Linux VMs
    testing:                # This key controls the behavior of the VM in testing mode. If undefined, both values are set to true
      snapshot: true        # Snapshot this VM going into testing, and revert it coming out of testing. Default: true
      block_internet: true  # Cut this VM off from the internet during testing. Default true
    roles:                  # This key is an array of user-defined roles that will be installed on this VM. Roles must exist on the Ludus server and can be installed with `ludus ansible role add`
      - geerlingguy.docker  # Arbitrary role name, as it appears in `ludus ansible roles list`
      - name: badsectorlabs.ludus_elastic_agent # You can also specify a role with a an array of dependencies that have to run first
        depends_on:
          - vm_name: "{{ range_id }}-elastic"  # In this case, we have to set up the elastic container (server) before the agent
            role: badsectorlabs.ludus_elastic_container
    role_vars:              # This key contains `key: value` pairs of variables that are passed to ALL user-defined roles.
      docker_edition: ce    # Arbitrary variables for user-defined roles. Do *not* use hyphens to prefix these variables, the role_vars key *must* be a dictionary!
      docker_users:         # You can use lists or dicts here
        - localuser
    ansible_groups:         # Define the groups this VM will be a part of when `ludus range inventory` is run. These groups can be set after VM deployment with `ludus range deploy -t custom-groups`
      - customgroup1        # An arbitrary group name
      - customgroup2
    dns_rewrites:           # Any values in this array will be added to DNS for the range and return an A record for this VM's IP
      - example.com         # rewrites responses for this domain name only
      - '*.example.com'     # rewrites responses for all example.com subdomains but *not* example.com
    unmanaged: false        # Set this to true for VMs that cannot report an IP to ansible via proxmox (no qemu-guest-agent, i.e. EDR appliances). You will have to manually configure this VM to have the IP defined in the config. Default: false
    primary_dns_server: 1.1.1.1   # Set a primary DNS server to be set for this VM. Defaults to 10.range_number1.vlan.254 (the router) when not set
    secondary_dns_server: 8.8.8.8 # Set a secondary DNS server for this VM
  - vm_name: "{{ range_id }}-ad-win11-22h2-enterprise-x64-1"
    hostname: "{{ range_id }}-WIN11-22H2-1"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 21
    ram_gb: 8
    cpus: 4
    windows:
      sysprep: false
      chocolatey_ignore_checksums: false # Set to true to ignore any checksum errors when installing chocolatey packages (for packages that are 3rd party hosted and update before the choco package hash updates). Default: false
      chocolatey_packages:
        - vscodium                # An array of chocolatey package names you'd like installed on this VM. Default: none
      office_version: 2019        # The Microsoft office version you would like installed on this VM (2013|2016|2019|2021). Default: undefined (don't install office)
      office_arch: 64bit          # The architecture for the Microsoft office install (64bit|32bit)
      visual_studio_version: 2019 # The version of Microsoft Visual Studio to install (community edition). Note: 2022 cannot target < .NET 4.5. Default: undefined (don't install visual studio)
      autologon_user: myuser      # The username to use for autologon. Default: localuser unless domain joined, then default.ad_domain_user
      autologon_password: mypass  # The password to use for autologon. Default: password unless domain joined, then default.ad_domain_user_password
    domain:
      fqdn: ludus.network
      role: member
  - vm_name: "{{ range_id }}-elastic"
    hostname: "{{ range_id }}-elastic"
    template: debian-12-x64-server-template
    vlan: 20
    ip_last_octet: 2
    ram_gb: 8
    cpus: 4
    linux: true
    roles:
      - badsectorlabs.ludus_elastic_container # This role will run before the elastic agent role on the windows VM     
  - vm_name: "{{ range_id }}-kali"
    hostname: "{{ range_id }}-kali"
    template: kali-x64-desktop-template
    vlan: 99
    ip_last_octet: 1
    ram_gb: 8
    cpus: 4
    linux:
      packages: # You can define packages to install on Linux hosts
        - curl
        - python3
    testing:
      snapshot: false
      block_internet: false

# This key contains `key: value` pairs of variables that are passed to ALL user-defined roles on all VMs in the range
global_role_vars:
  docker_edition: ce

# This key defines the settings for the router VM in your range. It is optional, and by default Ludus will deploy a router VM with the default settings.
router:
  vm_name: "{{ range_id }}-router-debian11-x64"
  hostname: "{{ range_id }}-router"
  template: debian-11-x64-server-template
  ram_gb: 2
  ram_min_gb: 1
  cpus: 2
  roles: # Enterprise only
    - ludus_guacamole_server # You can add roles to the router VM just like any other VM
  role_vars: # Enterprise only
    somevar: value
  outbound_wireguard_config: |- # Enterprise only; Note: this config must have AllowedIPs set to 0.0.0.0/0, split tunnels are not supported (yet)
    [Interface]
    PrivateKey = XXXX
    ...
  outbound_wireguard_vlans: # Enterprise only; Define the VLANs that the router VM will route traffic for. This key is required if outbound_wireguard_config is defined.
    - 10
  inbound_wireguard:             # Enterprise only; Must be used with users that have portforwarding enabled at creation time
    enabled: true                # Enable or disable the WireGuard server on the router (default: false)
    server_cidr: 10.254.254.0/24 # The CIDR of the WireGuard server (default: 10.254.254.0/24)
    port: 51820                  # The port the WireGuard server is listening on (UDP) (default: 51820). Note: This must be 51820 to work with port forwarding.
    allowed_vlans:               # The VLANs that WireGuard clients are allowed to connect to (default: all)
      - 10
  iptables_commands: # These commands are run after the firewall is configured. Make sure you understand what these commands do as they could allow traffic that should otherwise be blocked by Ludus features!
    - iptables -I LUDUS_DEFAULTS -i ens18 -s 192.0.2.103 -j ACCEPT # A full iptables command to run at the end of router setup

# This key defines network rules in your range. It is optional, and by default all traffic is allowed
network: 
  inter_vlan_default: REJECT     # The default rule to apply to traffic between VLANs. Default: ACCEPT
  external_default: ACCEPT       # The default rule to apply to traffic leaving the range out to the internet. Default: ACCEPT
  wireguard_vlan_default: ACCEPT # The default rule to apply to traffic leaving the range to clients connected via WireGuard. Default: ACCEPT
  always_blocked_networks:       # Define any networks that ranges should never be able to reach (i.e. the LAN where the Ludus host is located)
    - 192.168.1.0/24             # entries must be in CIDR format
  rules: # Specify rules to restrict or allow based on inter_vlan_default. Default: allow all traffic
    - name: Only allow windows to kali on 443 # The rule name will be added as a comment in iptables
      vlan_src: 10   # Traffic source VLAN. Special value 'public' can be used which is converted to '! 10.ID.0.0/16' in the iptables rule, 'all' is '10.ID.0.0/16', and 'wireguard' is '198.51.100.0/24'
      vlan_dst: 99   # Traffic destination VLAN. Special value 'public' can be used which is converted to '! 10.ID.0.0/16' in the iptables rule, 'all' is '10.ID.0.0/16', and 'wireguard' is '198.51.100.0/24'
      protocol: tcp  # Protocol (tcp|udp|icmp|all)
      ports: 443     # A single port, a range in the format start:end, or 'all'
      action: ACCEPT # ACCEPT|REJECT|DROP
    - name: Allow kali to the DC
      vlan_src: 99
      ip_last_octet_src: 1 # The single machine from the vlan_src to apply the rule to
      vlan_dst: 10
      ip_last_octet_dst: 11 # The single machine from the vlan_dst to apply the rule to
      protocol: all
      ports: all
      action: ACCEPT

# These values control the values Ludus uses when deploying ranges and Windows domains.
# The values shown here are the defaults that will be set if this key is not defined
# If you define the defaults key, you must set every value as it overrides the server set defaults dict
# Users may wish to change these values to emulate environments (functional level, domain admin username and password, etc)
defaults:
  snapshot_with_RAM: true                  # When entering testing mode, capture the RAM state which allows reverting to a running VM
  stale_hours: 0                           # How many hours until a pre-existing snapshot should be deleted and retaken (if entering and exiting testing mode quickly)
  ad_domain_functional_level: Win2012R2    # The functional level of each Windows domain created by Ludus - options are: "Win2003", "Win2008", "Win2008R2", "Win2012", "Win2012R2", "WinThreshold", or "Win2025"
  ad_forest_functional_level: Win2012R2    # The functional level of each Windows forest created by Ludus - options are: "Win2003", "Win2008", "Win2008R2", "Win2012", "Win2012R2", "WinThreshold", or "Win2025"
  ad_domain_admin: domainadmin             # The domain admin username for every Windows domain
  ad_domain_admin_password: password       # The domain admin password for every Windows domain
  ad_domain_user: domainuser               # The domain user username for every Windows domain
  ad_domain_user_password: password        # The domain user password for every Windows domain
  ad_domain_safe_mode_password: password   # The domain safe mode password for every Windows domain
  timezone: America/New_York               # The timezone for all VMs, use the TZ identifier format from https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
  enable_dynamic_wallpaper: true           # Enable dynamic wallpaper (red/green) for all Windows VMs in the range

# Use the notify key to send a notification when a range deployment finishes or fails.
# Notification "urls" look like the following. For more information about service specific configuration see
# Shoutrrr's documentation: https://containrrr.dev/shoutrrr/services/overview/
#
# Note: usernames and passwords containing special characters will need to be urlencoded.
# If your username is: "myname@example.com" and your password is "124@34$1"
# your shoutrrr url will look like: "smtp://myname%40example%2Ecom:124%4034%241@ms.my.domain.com:587"
notify:
 urls:
   - "discord://token@webhookid"
   - "telegram://token@telegram?channels=channel-1[,channel-2,...]"
   - "pushover://shoutrrr:apiToken@userKey/?priority=1&devices=device1[,device2, ...]"
   - "slack://[botname@]token-a/token-b/token-c"
   - "smtp://username:password@host:port/?fromAddress=fromAddress&toAddresses=recipient1[,recipient2,...]"
   - "teams://token-a/token-b/token-c"
   - "gotify://gotify-host/token"
   - "pushbullet://api-token[/device/#channel/email]"
   - "ifttt://key/?events=event1[,event2,...]&value1=value1&value2=value2&value3=value3"
   - "mattermost://[username@]mattermost-host/token[/channel]"
   - "ntfy://username:password@host:port/topic"
   - "hangouts://chat.googleapis.com/v1/spaces/FOO/messages?key=bar&token=baz"
   - "zulip://bot-mail:bot-key@zulip-domain/?stream=name-or-id&topic=name"
   - "join://shoutrrr:api-key@join/?devices=device1[,device2, ...][&icon=icon][&title=title]"
   - "script:///file/path/on/disk"
   - "https://www.example.com/path"
```
