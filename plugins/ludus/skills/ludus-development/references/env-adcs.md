# Active Directory Certificate Services Lab

Deploy an ADCS lab on Ludus with ESC1 through ESC15 attack paths using the `badsectorlabs.ludus_adcs` role.

1. Add the ludus_adcs role to your Ludus server

```shell-session
ludus ansible roles add badsectorlabs.ludus_adcs
```

2. Modify your ludus config to add the role to a Windows server VM

```shell-session
ludus range config get > config.yml
```

```yaml
ludus:
  - vm_name: "{{ range_id }}-ad-dc-win2022-server-x64-1"
    hostname: "{{ range_id }}-DC01-2022"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 11
    ram_gb: 6
    cpus: 4
    windows:
      sysprep: true
    domain:
      fqdn: ludus.domain
      role: primary-dc
    roles:
      - badsectorlabs.ludus_adcs
```

```shell-session
ludus range config set -f config.yml
```

3. Deploy the range

```shell-session
ludus range deploy
```

4. Enjoy your ESC1,2,3,4,5,6,7,8,9,11,13, and 15 attack paths!

---

## Included Attack Paths:

ESC1: Exploitable by `Domain Users` via the `ESC1` template.

ESC2: Exploitable by `Domain Users` via the `ESC2` template.

ESC3: Exploitable by `Domain Users` using a certificate from the `ESC3_CRA` template, which will allow requests on behalf of another user from the `User` or `ESC3` templates (for example).

ESC4: Exploitable by `Domain Users` via the ESC4 template.

ESC5: Exploitable by `esc5user` via local administrators group on the CA.

ESC6: Exploitable by `Domain Users`.

ESC7:
- `esc7_certmgr_user` has ManageCertificates rights and can exploit via the `ESC7_CertMgr` template.
- `esc7_camgr_user` has ManageCA rights and can exploit via the `SubCA` template (for example).

ESC8: Exploitable by `Domain Users`.

ESC9: Exploitable by the `Domain Users`, who have GenericAll rights over the `esc9user` account.

ESC11: Exploitable by `Domain Users`.

ESC13: Exploitable by `Domain Users` via the `ESC13` template. Users in `esc13group` have GenericAll over `Enterprise Admins`.

ESC15: Exploitable by `Domain Users` via the `WebServer` template.
