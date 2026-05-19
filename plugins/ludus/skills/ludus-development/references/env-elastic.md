# Elastic Security Lab

Deploy an Elastic Security server on Ludus with agents on multiple endpoints. Agents are set to use a pre-configured policy with all detections and logging enabled.

1. Add the `badsectorlabs.ludus_elastic_container` and `badsectorlabs.ludus_elastic_agent` roles to your Ludus server

```shell-session
ludus ansible roles add badsectorlabs.ludus_elastic_container
ludus ansible roles add badsectorlabs.ludus_elastic_agent
```

2. Modify your ludus config to add the `badsectorlabs.ludus_elastic_container` role to a Debian or Ubuntu VM and the `badsectorlabs.ludus_elastic_agent` on Debian-based or Windows VMs

```shell-session
ludus range config get > config.yml
```

```yaml
ludus:
  - vm_name: "{{ range_id }}-elastic"
    hostname: "{{ range_id }}-elastic"
    template: debian-12-x64-server-template
    vlan: 20
    ip_last_octet: 1
    ram_gb: 8
    cpus: 4
    linux: true
    testing:
      snapshot: false
      block_internet: false
    roles:
      - badsectorlabs.ludus_elastic_container
    role_vars:
      ludus_elastic_password: "thisisapassword"

  - vm_name: "{{ range_id }}-debian"
    hostname: "{{ range_id }}-debian"
    template: debian-12-x64-server-template
    vlan: 20
    ip_last_octet: 20
    ram_gb: 4
    cpus: 2
    linux: true
    testing:
      snapshot: false
      block_internet: false
    roles:
      - badsectorlabs.ludus_elastic_agent

  - vm_name: "{{ range_id }}-win11-22h2-enterprise-x64-1"
    hostname: "{{ range_id }}-WIN11-22H2-1"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 21
    ram_gb: 8
    cpus: 4
    windows:
      install_additional_tools: false
    roles:
      - badsectorlabs.ludus_elastic_agent
```

```shell-session
ludus range config set -f config.yml
```

**Note:** The `badsectorlabs.ludus_elastic_agent` will automatically find the enrollment token and URL for the elastic server and enroll the agent. You can set the token and URL manually using role_vars if you wish. See [the README](https://github.com/badsectorlabs/ludus_elastic_agent) for more info.

3. Deploy the range

```shell-session
ludus range deploy
```

4. Enjoy your Elastic Security server with agents enrolled and detections enabled! You can access the elastic web interface via HTTPS on port 5601 or the VM with the `badsectorlabs.ludus_elastic_container` role. The creds are `elastic:elasticpassword` unless you set the password with role variables.
