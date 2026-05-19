# Roles

How to use Ansible roles with Ludus, add roles, configure role variables, and a table of Ludus-specific community roles.

## How to use Roles

**Tip:** Looking to create your own roles? Check out the role developer page in the Ludus docs.

Roles are Ansible roles that are applied to VMs in Ludus after they are deployed and configured. It's easy to add a role to a Ludus VM, simply add the role to Ludus and then define the `roles` key in the config.

Roles are unique to each user on a Ludus host, which allows users to have different versions of roles, custom roles, etc without overwriting or breaking each other's roles.

**Tip:** Any ansible role (35,000+) can be used with Ludus, as long as it is compatible with the OS of the VM and the roles pre-requisites are met. You can search for roles on [Ansible Galaxy](https://galaxy.ansible.com/ui/standalone/roles/).

To add a role to Ludus, use the client as the user that will deploy the role (optionally specify the user/range that will use the role with `--user`)

```bash
# Add directly from Ansible Galaxy
ludus ansible role add badsectorlabs.ludus_adcs

# Add from a local directory
ludus ansible role add -d ./ludus_child_domain

# Add a role for another user/range (as an admin)
ludus ansible role add badsectorlabs.luds_adcs --user USER2
```

After roles have been added to Ludus, you can modify the range config to use them:

```yaml
# range-config.yml
ludus:
  - vm_name: "{{ range_id }}-docker-host"
    hostname: "{{ range_id }}-docker"
    template: debian-12-x64-server-template
    vlan: 10
    ip_last_octet: 11
    ram_gb: 8
    cpus: 4
    linux: true
    roles:                  # This key is an array of user-defined roles that will be installed on this VM. Roles must exist on the Ludus server and can be installed with `ludus ansible role add`
      - geerlingguy.docker  # Arbitrary role name, as it appears in `ludus ansible roles list`
    role_vars:              # This key contains `key: value` pairs of variables that are passed to ALL user-defined roles.
      docker_edition: ce    # Arbitrary variables for user-defined roles. Do *not* use hyphens to prefix these variables, the role_vars key *must* be a dictionary!
      docker_users:         # You can use lists or dicts here
        - localuser
```

You can define any variables that will be passed to the role with `role_vars` as seen above. Note that all variable in `role_vars` will be passed to all roles.

## Ludus Specific Roles

While most existing ansible roles will work with Ludus, this page contains a table of roles specifically designed for Ludus.

| Role | Description | Author | Notes |
| ---- | ----------- | ------ | ----- |
| [badsectorlabs.ludus_vulhub](https://github.com/badsectorlabs/ludus_vulhub) | Runs [Vulhub](https://vulhub.org/) environments on a Linux system. | Bad Sector Labs | |
| [badsectorlabs.ludus_adcs](https://github.com/badsectorlabs/ludus_adcs) | Installs ADCS on Windows Server and optionally configures Certified Preowned templates. | Bad Sector Labs | |
| [badsectorlabs.ludus_bloodhound_ce](https://github.com/badsectorlabs/ludus_bloodhound_ce) | Installs Bloodhound CE on a Debian based system. | Bad Sector Labs | |
| [badsectorlabs.ludus_mssql](https://github.com/badsectorlabs/ludus_mssql) | Installs MSSQL on Windows systems. | Bad Sector Labs | |
| [badsectorlabs.ludus_elastic_container](https://github.com/badsectorlabs/ludus_elastic_container) | Installs "The Elastic Container Project" on a Linux system. | Bad Sector Labs | |
| [badsectorlabs.ludus_elastic_agent](https://github.com/badsectorlabs/ludus_elastic_agent) | Installs an Elastic Agent on a Windows, Debian, or Ubuntu system | Bad Sector Labs | |
| [badsectorlabs.ludus_xz_backdoor](https://github.com/badsectorlabs/ludus_xz_backdoor) | Installs the xz backdoor (CVE-2024-3094) on a Debian host and optionally installs the xzbot tool. | Bad Sector Labs | |
| [badsectorlabs.ludus_commandovm](https://github.com/badsectorlabs/ludus_commandovm) | Sets up Commando VM on Windows >= 10 hosts | Bad Sector Labs | Available as a template |
| [badsectorlabs.ludus_flarevm](https://github.com/badsectorlabs/ludus_flarevm) | Installs Flare VM on Windows >= 10 hosts | Bad Sector Labs | Available as a template |
| [badsectorlabs.ludus_remnux](https://github.com/badsectorlabs/ludus_remnux) | Installs REMnux on Ubuntu 20.04 systems | Bad Sector Labs | Available as a template |
| [badsectorlabs.ludus_emux](https://github.com/badsectorlabs/ludus_emux) | Installs EMUX and runs an emulated device on Debian based hosts | Bad Sector Labs | |
| [aleemladha.wazuh_server_install](https://github.com/aleemladha/wazuh_server_install) | Install Wazuh SIEM Unified XDR and SIEM protection with SOC Fortress Rules | @LadhaAleem | |
| [aleemladha.ludus_wazuh_agent](https://github.com/aleemladha/ludus_wazuh_agent) | Deploys Wazuh Agents to Windows systems | @LadhaAleem | |
| [aleemladha.ludus_exchange](https://github.com/aleemladha/ludus_exchange) | Installs Microsoft Exchange Server on a Windows Server host | @LadhaAleem | |
| [ludus_child_domain](https://github.com/ChoiSG/ludus_ansible_roles) | Create a child domain and domain controller | @_choisec | Must install from directory |
| [ludus_child_domain_join](https://github.com/ChoiSG/ludus_ansible_roles) | Join a machine to the child domain created from ludus_child_domain | @_choisec | Must install from directory |
| [ludus-local-users](https://github.com/Cyblex-Consulting/ludus-local-users) | Manages local users and groups for Windows or Linux | @tigrebleu | Must install from directory |
| [ludus-gitlab-ce](https://github.com/Cyblex-Consulting/ludus-gitlab-ce) | Handles the installation of a Gitlab instance | @tigrebleu | Must install from directory |
| [ludus-ad-content](https://github.com/Cyblex-Consulting/ludus-ad-content) | Creates content in an Active Directory (OUs, Groups, Users) | @tigrebleu | Must install from directory |
| [ludus_tailscale](https://github.com/NocteDefensor/ludus_tailscale) | Provision or remove a device to/from a Tailnet | @__Mastadon | |
| [ludus_velociraptor_client](https://github.com/fmurer/ludus_velociraptor_client) | Install a Velociraptor Agent on a System in Ludus | @f_Murer | Must install from directory |
| [ludus_velociraptor_server](https://github.com/fmurer/ludus_velociraptor_server) | Install a Velociraptor Server in Ludus | @f_Murer | Must install from directory |
| [bagelByt3s.ludus_adfs](https://github.com/bagelByt3s/ludus_adfs) | Installs an ADFS deployment with optional configurations. | Beyviel David | Must install from directory |
| [ludus_caldera_server](https://github.com/frack113/ludus_caldera_server) | Installs Caldera Server main branch on linux | @frack113 | |
| [ludus_caldera_agent](https://github.com/frack113/ludus_caldera_agent) | Installs Caldera Agent on Windows | @frack113 | |
| [ludus_aurora_agent](https://github.com/frack113/ludus_aurora_agent) | Installs Aurora Agent on Windows | @frack113 | Requires package and valid license |
| [ludus_graylog_server](https://github.com/frack113/my-ludus-roles) | Installs Graylog server on Ubuntu 22.04 | @frack113 | Must install from directory |
| [ludus_filigran_opencti](https://github.com/frack113/ludus_filigran_opencti) | Installs OpenCTI | @frack113 | |
| [ludus_ghosts_server](https://github.com/frack113/ludus_ghosts_server) | Installs Ghosts on a Linux server | @frack113 | |
| [jasonmull.ludus_ghosts_client](https://github.com/jasonmull/ludus_ghosts_client) | Installs Ghosts client on a Windows endpoint | @jasonmull | |
| [jasonmull.empire_c2_docker](https://github.com/jasonmull/empire_docker_ansible) | Deploy Empire C2 via Docker | @jasonmull | |
| [0xRedpoll.ludus_cobaltstrike_teamserver](https://github.com/0xRedpoll/ludus_cobaltstrike_teamserver) | Install and provision a Cobalt Strike teamserver in Ludus | @0xRedpoll | |
| [0xRedpoll.ludus_mythic_teamserver](https://github.com/0xRedpoll/ludus_mythic_teamserver) | Installs and spins up a Mythic Teamserver on a Debian or Ubuntu server | @0xRedpoll | |
| [ludus-ad-vulns](https://github.com/Primusinterp/ludus-ad-vulns) | Adds vulnerabilities in an Active Directory. | @Primusinterp | Must install from directory |
| [ludus_juiceshop](https://github.com/xurger/ludus_juiceshop) | Installs OWASP Juice Shop | xurger | Must install from directory |
| [netpenguins.ludus_sliver](https://github.com/NetPenguins/ludus_sliver) | Installs SliverC2 | NetPenguins | |
| [netpenguins.ludus_redirector](https://github.com/NetPenguins/ludus_redirector) | Sets up an Apache2 redirector for adversarial simulation ranges | NetPenguins | |
| [netpenguins.ludus_k3s](https://github.com/NetPenguins/ludus_k3s) | Deploys a k3s cluster in ludus ranges | NetPenguins | |
| [ludus_enable_asr](https://github.com/curi0usJack/Ludus-MDE-MDI-Roles/tree/main/ludus_enable_asr) | Enables many Attack Surface Reduction rules on a Windows host | @curi0usJack | Must install from directory |
| [ludus_enable_mdi_gpo](https://github.com/curi0usJack/Ludus-MDE-MDI-Roles/tree/main/ludus_enable_mdi_gpo) | Creates GPOs and adds recommended auditing settings for Microsoft Defender for Identity | @curi0usJack | Must install from directory |
| [ludus_badblood](https://github.com/curi0usJack/ludus_badblood) | Outfits your ludus AD domain with BadBlood info | @curi0usJack | Must install from directory |
| [ludus_splunk_universalforwarder](https://github.com/curi0usJack/ludus_splunk_universalforwarder) | Installs Splunk Universal Forwarder on Windows endpoints | @curi0usJack | Must install from directory |
| [ludus_splunk](https://github.com/curi0usJack/ludus_splunk) | Installs Splunk Enterprise on Linux | @curi0usJack | Must install from directory |
| [ludus_adtimeline_syncthing](https://github.com/mojeda101/ludus_adtimeline_syncthing) | Installs ADTimeline Splunk app with Syncthing for automatic ingestion | mojeda101 | |
| [ludus_litterbox](https://github.com/professor-moody/ludus_litterbox_role) | Installs Litterbox controlled sandbox environment for payload development/testing | professor-moody | |
| [professor_moody.scorch.ludus](https://github.com/professor-moody/ludus_scorch) | Sets up a full SCORCH deployment with various common misconfigurations | professor-moody | collection |
| [5tuk0v.ludus_wsus](https://github.com/5tuk0v/ludus_wsus) | Installs Windows Server Update Services (WSUS) on Windows Server | @stuk0v_ | |
| [5tuk0v.ludus_vectr](https://github.com/5tuk0v/ludus_vectr) | Installs VECTR threat tracking and campaign management tool on Ubuntu 22.04 | @stuk0v_ | |
| [5tuk0v.ludus_ghostwritter](https://github.com/5tuk0v/ludus_ghostwriter) | Installs Ghostwriter on a Linux-based host | @stuk0v_ | |
| [5tuk0v.ludus_zeek](https://github.com/5tuk0v/ludus_zeek/) | Installs Zeek on Debian and Ubuntu hosts | @stuk0v_ | |
| [inf0junki3.ludus.netbox](https://galaxy.ansible.com/ui/repo/published/inf0junki3/ludus/content/role/netbox/) | Sets up the Netbox network & infrastructure management solution | inf0junki3 | Part of the inf0junki3.ludus collection |
| [inf0junki3.ludus.vectr](https://galaxy.ansible.com/ui/repo/published/inf0junki3/ludus/content/role/vectr/) | Sets up the VECTR red/purple team platform | inf0junki3 | Part of the inf0junki3.ludus collection |
| [brmkit.ludus_nemesis](https://github.com/brmkit/ludus_nemesis) | Installs Nemesis by SpecterOps | @_brmkit | |
| [brmkit.ludus_guacamole](https://github.com/brmkit/ludus_guacamole) | Installs Guacamole on Linux and optionally configures connections | @_brmkit | |
