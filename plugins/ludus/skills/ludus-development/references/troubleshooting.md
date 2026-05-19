# Ludus Troubleshooting Reference

## Proxmox Issues

### Proxmox Web Interface is blank or returns 500 errors

In the web console this is shown as an error loading `/PVE/StdWorkspace.js`.

If the Proxmox web interface is blank after accepting the certificate warning, try to run `apt install --reinstall proxmox-widget-toolkit` as root on your Ludus host, then reload the web page.

This is an issue some users have with Proxmox and has been reported on the Proxmox forum as well as the Ludus issue tracker.

### Proxmox API returns 596 timeout errors

On massive deployments (500+ VMs) some API calls may exceed the hardcoded 30 second timeout that `pveproxy` imposes.

Either use `pvesh` from a root shell as it bypasses `pveproxy`, or modify `/usr/share/perl5/PVE/APIServer/AnyEvent.pm` and change line 833

```plain
         $w = http_request(
             $method => $target,
             headers => $headers,
             timeout => 90, # was previously 30
             proxy => undef, # avoid use of $ENV{HTTP_PROXY}
             persistent => $persistent,
```

then restart `pveproxy` with `systemctl restart pveproxy`.

## Template Issues

### ISO downloads fail - Use pre-downloaded ISOs for templates

If your Ludus host is unable to download ISOs but your local machine can, you can upload the ISO files to the Ludus host and modify the packer files to point to the existing ISO files.

To do this:

1. Download the ISO file locally, then upload it to your Ludus host. You can do this via the GUI or via SCP. The template should end up in a data pool. By default, if using the `local` pool, the ISO should end up at `/var/lib/vz/template/iso`.

2. Locate the template packer file. Built-in templates are at `/opt/ludus/packer/<template>/<template>.pkr.hcl`, user added templates are at `/opt/ludus/users/<username>/packer/<template>/<template>.pkr.hcl`

3. Edit the template packer file and change the `iso_url` value to `iso_file`. The format for pool is `<poolname>:iso/<isoname>.iso`. For example:

Change

```
variable "iso_url" {
  type    = string
  default = "https://software-static.download.prss.microsoft.com/sg/download/888969d5-f34g-4e03-ac9d-1f9786c66749/SERVER_EVAL_x64FRE_en-us.iso"
}
```

to

```
variable "iso_file" {
  type    = string
  default = "local:iso/SERVER_EVAL_x64FRE_en-us.iso"
}
```

4. Build the template with ludus, and it will use the local ISO. `ludus template build -n <template name>`

Assuming your iso is stored in the `local` pool.

### Linux template stuck on `Configuring apt - scanning the mirror`

The MTU of your Ludus host may be less than the standard 1500, which is the MTU for the `vmbr100` "WAN" network and each range network.

If this is the case, you can add `mtu 1420` (or the value of your WAN interface's MTU) to `/etc/network/interfaces`. To make this change apply to users created in the future, edit the template in `/opt/ludus/ansible/user-management/vmbr-management.yml` to add the MTU value to the interface block.

## Network Issues

### Templates cannot connect to the internet

If your templates cannot connect to the internet or are getting Automatic Private IP Addressing (APIPA) addresses that start with `169.254`, your Ludus nat interface may be down or dnsmasq may not be running (or running but not listening).

Before proceeding, try restarting the `dnsmasq` service on the Ludus server:

```shell
systemctl restart dnsmasq
```

Even if dnsmasq was already running, there have been multiple cases where it was not listening and restarting it fixed the issue.

If that didn't solve your issue, get your `ludus_nat_interface` value from `/opt/ludus/config.yml`

```plain
root@ludus:~# cat /opt/ludus/config.yml
---
proxmox_node: ludus
proxmox_interface: vmbr0
proxmox_local_ip: 10.98.108.3
proxmox_public_ip: 10.98.108.3
proxmox_gateway: 10.98.108.1
proxmox_netmask: 255.255.255.0
proxmox_vm_storage_pool: local
proxmox_vm_storage_format: qcow2
proxmox_iso_storage_pool: local
ludus_nat_interface: vmbr1000
prevent_user_ansible_add: false
```

To check if this interface is up, run the following command on the Ludus host:

```plain
root@ludus:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: ens18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master vmbr0 state UP group default qlen 1000
    link/ether bc:24:11:de:d2:b0 brd ff:ff:ff:ff:ff:ff
    altname enp0s18
3: vmbr0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether bc:24:11:de:d2:b0 brd ff:ff:ff:ff:ff:ff
    inet 10.98.108.3/24 scope global vmbr0
       valid_lft forever preferred_lft forever
    inet6 fe80::be24:11ff:fede:d2b0/64 scope link
       valid_lft forever preferred_lft forever
5: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 198.51.100.1/24 scope global wg0
       valid_lft forever preferred_lft forever
10: vmbr1000: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether 82:a4:7a:9a:10:35 brd ff:ff:ff:ff:ff:ff
    inet 192.0.2.254/24 scope global ludus
       valid_lft forever preferred_lft forever
    inet6 fe80::80a4:7aff:fe9a:1035/64 scope link
       valid_lft forever preferred_lft forever
11: vmbr1002: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether fa:04:2a:a5:84:d0 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::f804:2aff:fea5:84d0/64 scope link
       valid_lft forever preferred_lft forever
```

If the line that corresponds with your ludus_nat_interface shows `DOWN` inside the angle brackets for the ludus interface, run the following command to bring the interface `UP`:

```plain
ifup vmbr1000
```

Run `ip a` again to verify the interface is up. Next, check that the MASQUERADE rule is in place:

```plain
root@proxtest:~# iptables -nvL -t nat
Chain PREROUTING (policy ACCEPT 236 packets, 14443 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 226 packets, 13898 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 328 packets, 22056 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 328 packets, 22056 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 MASQUERADE  0    --  *      vmbr0   192.0.2.0/24         0.0.0.0/0
```

The MASQUERADE rule should be in place for the Ludus network range of 192.0.2.0/24. Ludus VMs should now have internet access.

If VMs still are unable to obtain an IP in the 192.0.2.0/24 after this, check the status of the `dnsmasq` service on the Ludus server.

```
systemctl status dnsmasq
```

In some cases, other programs such as `conmand` listen on port 53 which causes a conflict with `dnsmasq`.
Resolve this conflict and restart `dnsmasq`.
Once `dnsmasq` is running, VMs should be able to get an IP address via DHCP and access the internet.

### Unable to access a range after granting access

If you have granted a user access to a range but they are unable to access the range try the following:

1. Make sure the user has an up to date WireGuard configuration file that includes the destination range subnet. You can always pull an up to date configuration with `ludus --user <userID> user wireguard`

2. Re-deploy the networking rules for the target range with `ludus --user <target range ID> range deploy -t network`. This will force a recreation of the firewall rules and should include a rule to allow the user access.

## Ansible Issues

### General Ansible Errors

Just up arrow and hit enter!

But really, Ludus actions are idempotent, and these VMs are complex beasts. Sometimes things don't work on the first try. No harm in trying again!

Ansible errors can be parsed and made more readable with the `ludus range errors` command.

### Ansible "Failed to create temporary directory" Error

```
TASK [Gathering Facts] *********************************************************
fatal: [JD-ad-dc-win2019-server-x64]: UNREACHABLE! => {"changed": false, "msg":
"Failed to create temporary directory. In some cases, you may have been able to
authenticate and did not have permissions on the target directory. Consider
changing the remote tmp path in ansible.cfg to a path rooted in \"/tmp\",
for more error information use -vvv. Failed command was: ( umask 77 &&
mkdir -p \"` echo /home/ludus/.ansible/tmp `\"&& mkdir \"`
echo /home/ludus/.ansible/tmp/ansible-tmp-1704235290.5345225-913183-44415051184218 `\"
&& echo ansible-tmp-1704235290.5345225-913183-44415051184218=\"`
echo /home/ludus/.ansible/tmp/ansible-tmp-1704235290.5345225-913183-44415051184218 `\" ),
exited with result 1", "unreachable": true}
```

This is a long error message, but the key is `"unreachable": true`.

Check that the VM that failed is powered on and reachable. Power cycle the VM if needed. Re-run the ansible that caused this error.

### Unable to retrieve API task ID from node

**Error:**
`Unable to retrieve API task ID from node <node name> HTTPSConnectionPool(host='<node name>', port=8006): Read timed out. (read timeout=5)`

**Resolution:**

This issue has been seen on existing Proxmox installs.

Try to `curl https://<node name>:8006/`

If you get an ssl error (`SSL certificate problem: unable to get local issuer certificate`) try copying the `/etc/pve/pve-root-ca.pem` file to `/usr/local/share/ca-certificates/pve-root-ca.crt` (make sure to change the `.pem` extension to `.crt` and run `update-ca-certificates`).

Then try again to `curl https://<node name>:8006/`. If the ssl error issue is gone, chances are ansible API task ID error will be resolved.

### Multiple VMs with name found

**Error:**

`Multiple VMs with name ... found, provide vmid instead`

**Resolution:**

This issue occurs when there are multiple VMs accessible to the user with the exact same name. This has been seen when a duplicate VM template was created but never fully converted to template (failed build). Make sure that all VM names are unique in both the `SHARED` pool (templates) and the user's range pool.

## WireGuard Issues

### Debugging WireGuard

#### Enable Debug in the kernel on the Ludus host
```
echo module wireguard +p > /sys/kernel/debug/dynamic_debug/control
```

#### Watch logs
```
dmesg -HwT | grep wireguard
```

#### Disable debug
```
echo module wireguard -p > /sys/kernel/debug/dynamic_debug/control
```

### Issues and remediation

#### Client sees: `Error: Invalid handshake initiation from ...`

1. Comment out the user's peer details from `/etc/wireguard/wg0.conf`
2. Sync the config with the kernel module with `wg syncconf wg0 <(wg-quick strip wg0)`
3. Uncomment the user's peer details from `/etc/wireguard/wg0.conf`
4. Sync the config with the kernel module with `wg syncconf wg0 <(wg-quick strip wg0)`

The user should be able to reconnect immediately.

#### TCP connections hang

This can be an issue if you are running your Ludus wireguard tunnel inside another VPN (not recommended).

Run this on the Ludus server to enable MSS clamping:

```
/sbin/iptables -t mangle -A FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
```

If that alone does not solve the problem, lower the WireGuard MTU values on both the server and client until TCP is functional.
You'll want to use the largest MTU values that works in order to limit packet fragmentation.

```
root@ludus:~# cat /etc/wireguard/wg0.conf
# Ansible managed
[Interface]
PrivateKey = ODcsR+U927qnFnAeREoCUAMfcuGlZwcLpOxttSCI33o=
Address = 198.51.100.1/24
ListenPort = 51820
MTU = 1284 # Add this line and edit the value (default is 1400)
```

## Kali Issues

### Kali APT `undefined symbol` error

```
Traceback (most recent call last):
  File "/usr/lib/cnf-update-db", line 3, in <module>
    import apt_pkg
ImportError: /usr/lib/python3/dist-packages/apt_pkg.cpython-312-x86_64-linux-gnu.so: undefined symbol: _ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_replaceEmmPKcm, version APTPKG_6.0
Error: Problem executing scripts APT::Update::Post-Invoke-Success 'if /usr/bin/test - /var/1ib/command-not-found/ -a -e /usr/1ib/cnf-update-db; then /usr/1ib/cnf-update-db > /dev/null; fi'
Error: Sub-process returned an error code
```

As of 2024-12-05 there is an APT error with Kali that prevents any packages from being installed after initial install.

A bug has been reported and is being tracked by the Kali maintainers.

In the meantime, you can comment out the provisioner part of the kali hcl at `/opt/ludus/packer/kali/kali.pkr.hcl`

```
build {
  sources = ["source.proxmox-iso.kali"]

//  provisioner "ansible" {
//    user               = "${var.ssh_username}"
//    use_proxy          = false
//    extra_arguments    = ["--extra-vars", "{ansible_python_interpreter: /usr/bin/python3, ansible_password: ${var.ssh_password}, ansible_sudo_pass: ${var.ssh_password}}"]
//    playbook_file      = "./kali.yml"
//    ansible_env_vars   = ["ANSIBLE_HOME=${var.ansible_home}", "ANSIBLE_LOCAL_TEMP=${var.ansible_home}/tmp", "ANSIBLE_PERSISTENT_CONTROL_PATH_DIR=${var.ansible_home}/pc", "ANSIBLE_SSH_CONTROL_PATH_DIR=${var.ansible_home}/cp"]
//    skip_version_check = true
//  }

}
```

That at least gets you a base Kali template, but without KasmVNC.
You can install the KasmVNC manually, but ansible won't go past the error.

### Kali GRUB install error

Your Kali install may fail with a GRUB boot loader error (as of 2024-02-08).

Packer will wait 30 minutes from boot for SSH to become available, so you need to perform the following steps to complete the installation until the `dpkg` package is fixed by the Kali maintainers.

1. Log into your Ludus host's Proxmox web interface (https://<ludus IP>:8006), click on the Kali VM, and click on Console. Click the noVNC tab in the center left of the screen. Click the "A" icon and then click "Alt" and press F2 on your keyboard.

2. Press enter at the new screen to get a console

3. Click "ALT" again to deselect it

4. Type the following commands:

```
chroot /target bash
echo -e "#!/bin/bash\nexec true" > /sbin/start-stop-daemon
chmod +x /sbin/start-stop-daemon
```

5. Run `apt reinstall dpkg`

6. Activate "Alt" again and press F1 on your keyboard

7. This will bring you back to the red screen. Deselect "Alt" and press Enter to continue.

8. Press enter with "Install the GRUB boot loader" highlighted to finish the Kali install. Packer will pick up on reboot and complete the template creation process.

## Flare-VM Issues

### Disable Defender 1 Error (Blocked by antivirus)

```
 TASK [badsectorlabs.ludus_flarevm : Disable Defender 1] ************************
fatal: [flare]: FAILED! => {"changed": true, ... "fully_qualified_error_id": "ScriptContainedMaliciousContent", ...}
```

If you encounter this issue when following the malware lab tutorial, here is the solution:

1. Use flare-vm template instead of win11-xxx-template.

```bash
git clone https://gitlab.com/badsectorlabs/ludus.git
cd ludus/templates
ludus templates add -d flare-vm
ludus templates build
# Wait for the template to successfully build
# You can watch the logs with `ludus template logs -f`
# Or check the status with `ludus template status` and `ludus templates list`
```

2. After successfully building, change the template value in `config.yml` to `flare-vm-template`

```yaml
# config.yml
- vm_name: "{{ range_id }}-flare"
    hostname: "{{ range_id }}-FLARE"
    template: flare-vm-template
    vlan: 99
    ip_last_octet: 3
    ram_gb: 4
    cpus: 2
    windows:
      install_additional_tools: false
    testing:
      snapshot: true
      block_internet: true
    roles:
      - badsectorlabs.ludus_flarevm
```

3. Set this config and force deploy it.

```bash
ludus range config set -f config.yml
ludus range deploy
# Wait for the range to successfully deploy
# You can watch the logs with `ludus range logs -f`
# Or check the status with `ludus range status`
```

Issue reference: [Issue 86](https://gitlab.com/badsectorlabs/ludus/-/issues/86)

## KasmVNC Issues

### No stylesheet loaded

This is a known bug (https://github.com/kasmtech/KasmVNC/issues/207).
Opening the web inspector and clicking the network tab, reloading the page, and double clicking the style.dist.css file (which opens it in a new window), then reloading the KasmVNC page seems to fix it.

## Client Issues

If you encounter errors while using the Ludus CLI, the `--verbose` flag will print the full details of the request and response.
This data includes all the configuration file, environmental variables, and CLI arguments that are read and processed.
API keys are redacted after the `.` which shows the userID but nothing else. These command outputs are safe to share in issues or other documents.
The output will leak your username in the path to the configuration file if no configuration file is specified on the command line.

```plain
$ ludus users list all --verbose
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:101 Using config file: /Users/user/.config/ludus/config.yml
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:105 --- Configuration from cli and read from file ---
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:107 	url = https://10.98.108.227:8080
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:107 	proxy =
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:107 	verify = %!s(bool=false)
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:107 	user =
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:107 	verbose = %!s(bool=true)
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:107 	json = %!s(bool=false)
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:116 ---
[DEBUG] 2024/01/26 15:49:09 ludus/cmd.initConfig:root.go:130 Got API key: CI.***REDACTED***
[DEBUG] 2024/01/26 15:49:09 ludus/rest.InitClient:restapi.go:46 Endpoint URL:  https://10.98.108.227:8080
[DEBUG] 2024/01/26 15:49:09 ludus/rest.InitClient:restapi.go:56 Endpoint SSL Verify:  false
...
+------------------------+--------+------------------+------------------+-------+
|          NAME          | USERID |     CREATED      |   LAST ACTIVE    | ADMIN |
+------------------------+--------+------------------+------------------+-------+
| root                   | ROOT   | 2024-01-19 17:28 | 2024-01-25 19:46 | true  |
| Continuous Integration | CI     | 2024-01-19 17:30 | 2024-01-26 15:49 | true  |
+------------------------+--------+------------------+------------------+-------+
```

## API Key Issues

### Recover an API key for a user if an admin key is known

1. Run `ludus user apikey --user <userID>`

### Recover an API key using the `ROOT` key (no admin key is known)

1. SSH into the Ludus host as root and run `ludus-install-status` which will print the `ROOT` key
2. Use the `ROOT` key with the client to reset the api key of the user with the lost key

```
LUDUS_API_KEY='ROOT.o>T3BMm!^\As_0Fhve8B\VrD&zqc#kCk&B&?e|aF' ludus user apikey --user <userID>
```

## Packer Cache Cleanup

### Introduction

This guide proposes one possible approach to address the issue of accumulating ISO files in the Ludus Packer cache directory. The suggestion uses a time-based file rotation tool called Rotafile, though similar solutions could be implemented using other tools or custom scripts.

### Problem Overview

The Ludus Packer cache directory (typically at `/opt/ludus/users/USERNAME/packer/packer_cache`, where USERNAME is your Ludus username) accumulates:
- ISO files ranging from ~400MB to ~6.9GB each
- Significant disk space usage that grows over time

### Installing a Time-Based File Rotation Tool

For this example, we'll use Rotafile, but similar functionality could be achieved with standard Linux tools like `find` with `cron` jobs, or other utilities:

```bash
# Clone the repository
git clone https://github.com/aancw/rotafile.git
cd rotafile

# Make scripts executable
chmod +x rotafile.sh install.sh

# Install the script (optional)
sudo ./install.sh
```

If you prefer not to install external tools, you could also use built-in Linux commands like `find` with the `-mtime` option to achieve similar results.

### Understanding File Rotation Parameters

If using Rotafile, it uses this syntax:

```
rotafile [directory] [time_period] [file_pattern] [options]
```

Similar approaches with standard Linux tools would look like:

```bash
# Using find to locate and delete files older than 30 days
find /path/to/directory -type f -name "*.iso" -mtime +30 -delete

# Using find with exec to implement a dry-run
find /path/to/directory -type f -name "*.iso" -mtime +30 -exec ls -la {} \;
```

### Basic Approaches for Ludus Cache Cleanup

#### Analyzing the Cache (Preview First)

Before implementing any deletion, it's always wise to first see what would be affected:

```bash
# Determine your Ludus username
LUDUS_USER="USERNAME_HERE"

# Using Rotafile to analyze without deleting
./rotafile.sh /opt/ludus/users/$LUDUS_USER/packer/packer_cache 30d "*.iso" --dry-run

# Alternative with standard find command
find /opt/ludus/users/$LUDUS_USER/packer/packer_cache -type f -name "*.iso" -mtime +30 -ls
```

This will show which files would be deleted and how much space would be freed, but won't actually delete anything.

#### Manual Cleanup Options

To manually clean up the cache:

```bash
# Determine your Ludus username
LUDUS_USER="USERNAME_HERE"

# Option 1: Using Rotafile
./rotafile.sh /opt/ludus/users/$LUDUS_USER/packer/packer_cache 30d "*.iso"

# Option 2: Using standard find command
find /opt/ludus/users/$LUDUS_USER/packer/packer_cache -type f -name "*.iso" -mtime +30 -delete
```

#### Logging for Auditing Purposes

It's advisable to maintain logs of cleanup operations:

```bash
# Determine your Ludus username
LUDUS_USER="USERNAME_HERE"

# Option 1: Using Rotafile with built-in logging
./rotafile.sh /opt/ludus/users/$LUDUS_USER/packer/packer_cache 30d "*.iso" --log=/var/log/ludus/packer-cache-iso.log

# Option 2: Using find with redirection to log file
find /opt/ludus/users/$LUDUS_USER/packer/packer_cache -type f -name "*.iso" -mtime +30 -ls > /var/log/ludus/find-log.txt
find /opt/ludus/users/$LUDUS_USER/packer/packer_cache -type f -name "*.iso" -mtime +30 -delete >> /var/log/ludus/find-log.txt
```

### Setting Up Automated Cleanup

For regular maintenance, automated cleanup can be implemented using cron:

```bash
# Edit crontab
sudo crontab -e
```

Add a line to run weekly cleanup (using either approach):

```
# Get your Ludus username
LUDUS_USER="USERNAME_HERE"

# Option 1: Using Rotafile
0 2 * * 0 /path/to/rotafile.sh /opt/ludus/users/$LUDUS_USER/packer/packer_cache 30d "*.iso" --force --log=/var/log/ludus/packer-cache-$(date +\%Y\%m\%d).log

# Option 2: Using find directly
0 2 * * 0 find /opt/ludus/users/$LUDUS_USER/packer/packer_cache -type f -name "*.iso" -mtime +30 -ls > /var/log/ludus/packer-cache-$(date +\%Y\%m\%d).log 2>&1 && find /opt/ludus/users/$LUDUS_USER/packer/packer_cache -type f -name "*.iso" -mtime +30 -delete >> /var/log/ludus/packer-cache-$(date +\%Y\%m\%d).log 2>&1
```

Replace `/path/to/rotafile.sh` with the actual path where Rotafile is installed.

### Monitoring Cleanup Results

To verify cleanup operations:

```bash
# View the logs
cat /var/log/ludus/packer-cache-*.log

# Determine your Ludus username
LUDUS_USER="USERNAME_HERE"

# Check current cache size
du -sh /opt/ludus/users/$LUDUS_USER/packer/packer_cache
```

Whether implemented with specialized tools or built-in commands, this approach provides a practical solution to the Packer cache growth issue while ensuring necessary files remain available during active development periods.

Issue Reference: [issues#97](https://gitlab.com/badsectorlabs/ludus/-/issues/97)

## Uninstall Ludus

Run the following as root on the Ludus host to uninstall Ludus.

```
ludus users list all
# Repeat the next command for all users
ludus range rm --user <USER ID>
export LUDUS_API_KEY=$(cat /opt/ludus/install/root-api-key)
ludus users list all
# Repeat the next command for all users
ludus --url https://127.0.0.1:8081 user rm -i <USER ID>
systemctl stop ludus
systemctl stop ludus-admin
pveum group delete ludus_users
pveum group delete ludus_admins
pvesh delete /pools/SHARED
pvesh delete /pools/ADMIN # if created
rm -rf /opt/ludus
# Remove vmbr1000 (and any other vmbr1000+ interfaces) using the Proxmox GUI
```
