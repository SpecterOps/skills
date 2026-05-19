# Default Passwords

Ludus templates use default credentials for provisioning with Ansible.

If your use case requires hardened machines, Ludus Enterprise enables key based SSH and certificate based WinRM provisioning.

## Default Machine Credentials

- Kali
  - `kali:kali` (OS)
  - `kali:password` (KasmVNC - https port 8444)
- Windows
  - `localuser:password` (local Administrator)
  - `LUDUS\domainuser:password`
  - `LUDUS\domainadmin:password` (Domain Admin)
- Debian based boxes
  - `debian:debian`
- Others
  - `localuser:password`

## Changing the default Windows domain accounts and passwords

It's possible to change the default Windows domain accounts and passwords by editing the `defaults.ad_domain_admin`, `defaults.ad_domain_admin_password`, `defaults.ad_domain_user`, and `defaults.ad_domain_user_password` keys in the Ludus config file.

**Note:** You must set all keys in the `defaults` object if you define any of them.

```yaml
defaults:
  ...
  ad_domain_admin: DA-John.Doe
  ad_domain_admin_password: CorrectHorseBatteryStaple
  ad_domain_user: John.Doe
  ad_domain_user_password: letmein
  ...
```

These values are used by the `setup-win-domain.yml` playbook to create the domain admin and domain user accounts.
