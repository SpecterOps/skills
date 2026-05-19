# SCCM Lab

Deploy a full SCCM (Configuration Manager) environment on Ludus with agents on multiple endpoints. Uses the `synzack.ludus_sccm` Ansible collection.

**Props:** Shout out to Zach Stein ([@synzack21](https://twitter.com/synzack21)) for collaborating to create the Ludus SCCM Ansible collection!

This guide will create a [Configuration Manager](https://learn.microsoft.com/en-us/mem/configmgr/core/understand/introduction) environment and install Configuration Manager agents on multiple endpoints.
For more information, see the [blog post](https://posts.specterops.io/automating-sccm-with-ludus-a-configuration-manager-for-your-configuration-manager-c8f4d8e40473) by Zach Stein ([@synzack21](https://twitter.com/synzack21)).


1. Add the `synzack.ludus_sccm` collection to your Ludus server 

```shell-session
ludus ansible collection add synzack.ludus_sccm
```

2. Modify your ludus config to add the appropriate SCCM roles to servers.

**Caution:**

- Due to unknown issues with SCCM, .local domain suffixes will not work properly. We recommend using something else such as .domain or .lab for your domain suffix
- If you wish to add client push to the DC, you will need to enable Remote Scheduled Tasks Management firewall rules or use the disable_firewall role
- At this time, all 4 site server roles are needed to deploy SCCM, there is no standalone option yet
- All SCCM VM hostnames MUST be 15 characters or less

```shell-session
ludus range config get > config.yml
```

```yaml
ludus:
  - vm_name: "{{ range_id }}-DC01"
    hostname: "DC01"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 10
    ram_gb: 4
    ram_min_gb: 1
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: ludus.domain
      role: primary-dc
    roles:
      - synzack.ludus_sccm.install_adcs
      - synzack.ludus_sccm.disable_firewall

  - vm_name: "{{ range_id }}-Workstation"
    hostname: "Workstation"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 11
    ram_gb: 4
    ram_min_gb: 1
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: ludus.domain
      role: member
    roles:
      - synzack.ludus_sccm.disable_firewall

  - vm_name: "{{ range_id }}-sccm-distro"
    hostname: "sccm-distro"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 12
    ram_gb: 4
    ram_min_gb: 1
    cpus: 4
    windows:
      sysprep: true
    domain:
      fqdn: ludus.domain
      role: member
    roles:
      - synzack.ludus_sccm.ludus_sccm_distro
    role_vars:
      ludus_sccm_site_server_hostname: 'sccm-sitesrv' 

  - vm_name: "{{ range_id }}-sccm-sql"
    hostname: "sccm-sql"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 13
    ram_gb: 4
    ram_min_gb: 1
    cpus: 4
    windows:
      sysprep: true
    domain:
      fqdn: ludus.domain
      role: member
    roles:
      - synzack.ludus_sccm.ludus_sccm_sql
    role_vars:
      ludus_sccm_site_server_hostname: 'sccm-sitesrv'    
      ludus_sccm_sql_server_hostname: 'sccm-sql'         
      ludus_sccm_sql_svc_account_username: 'sqlsccmsvc'  
      ludus_sccm_sql_svc_account_password: 'Password123' 

  - vm_name: "{{ range_id }}-sccm-mgmt"
    hostname: "sccm-mgmt"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 14
    ram_gb: 4
    ram_min_gb: 1
    cpus: 4
    windows:
      sysprep: true
    domain:
      fqdn: ludus.domain
      role: member
    roles:
      - synzack.ludus_sccm.ludus_sccm_mgmt
    role_vars:
      ludus_sccm_site_server_hostname: "sccm-sitesrv" 

  - vm_name: "{{ range_id }}-sccm-sitesrv"
    hostname: "sccm-sitesrv" 
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 15
    ram_gb: 4
    ram_min_gb: 1
    cpus: 4
    windows:
      sysprep: true
      autologon_user: domainadmin
      autologon_password: password
    domain:
      fqdn: ludus.domain
      role: member
    roles:
      - synzack.ludus_sccm.ludus_sccm_siteserver
      - synzack.ludus_sccm.enable_webdav
    role_vars:
      ludus_sccm_sitecode: 123           
      ludus_sccm_sitename: Primary Site  
      ludus_sccm_site_server_hostname: 'sccm-sitesrv'
      ludus_sccm_distro_server_hostname: 'sccm-distro'
      ludus_sccm_mgmt_server_hostname: 'sccm-mgmt'
      ludus_sccm_sql_server_hostname: 'sccm-sql'
      # --------------------------NAA Account-------------------------------------------------
      ludus_sccm_configure_naa: true
      ludus_sccm_naa_username: 'sccm_naa'
      ludus_sccm_naa_password: 'Password123'
      # --------------------------Client Push Account-----------------------------------------
      ludus_sccm_configure_client_push: true
      ludus_sccm_client_push_username: 'sccm_push'
      ludus_sccm_client_push_password: 'Password123'
      ludus_sccm_enable_automatic_client_push_installation: true
      ludus_sccm_enable_system_type_configuration_manager: true
      ludus_sccm_enable_system_type_server: true
      ludus_sccm_enable_system_type_workstation: true
      ludus_sccm_install_client_to_domain_controller: false  # "true" Requires Remote Scheduled Tasks Management Firewall Enabled on the DCs (or no firewall)
      ludus_sccm_allow_NTLM_fallback: true
      # ---------------------------Discovery Methods------------------------------------------
      ludus_sccm_enable_active_directory_forest_discovery: true
      ludus_sccm_enable_active_directory_boundary_creation: true
      ludus_sccm_enable_subnet_boundary_creation: true
      ludus_sccm_enable_active_directory_group_discovery: true
      ludus_sccm_enable_active_directory_system_discovery: true
      ludus_sccm_enable_active_directory_user_discovery: true
      # ----------------------------------PXE-------------------------------------------------
      ludus_sccm_enable_pxe: true
      ludus_enable_pxe_password: false
      ludus_pxe_password: 'Password123'
      ludus_domain_join_account: domainadmin
      ludus_domain_join_password: 'password'
```

```shell-session
ludus range config set -f config.yml
```

3. Deploy the range

```bash
ludus range deploy
# Wait for the range to successfully deploy
# You can watch the logs with `ludus range logs -f`
# Or check the status with `ludus range status`
```

**Tip:** If you'd like to watch the progress of the SCCM install, open a console or RDP into the sccm-sitesrv VM and run:

```
Get-Content C:\ConfigMgrSetup.log -Wait
```

This will "tail" the log file as SCCM installs.


4. Use [Misconfiguration Manager](https://github.com/subat0mik/Misconfiguration-Manager) to explore all the ways to pwn SCCM!

Our favorite SCCM tools are [SharpSCCM](https://github.com/Mayyhem/SharpSCCM) by [@_Mayyhem](https://twitter.com/_Mayyhem) and [SCCMHunter](https://github.com/garrettfoster13/sccmhunter) by [@garrfoster](https://x.com/garrfoster).

The main way to access SCCM is on the Site Server (sccm-sitesrv) with the Configuration Manager Console.

**Tip:** Using the configuration above, the `domainadmin` user is the user that has permissions in SCCM. To access the Configuration Manager Console. Log into the sccm-sitesrv VM as `domainadmin` (which should be the user that automatically logs in to the Site Server).
