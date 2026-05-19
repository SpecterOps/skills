# Workshop and Conference Environment Guides

This document contains Ludus configurations for various workshops and conference labs.

## SANS Shadow Steps Workshop

### Understanding and Detecting User Impersonation and Lateral Movement in Active Directory

**Props!** Huge shout out to [@ladhaAleem](https://twitter.com/LadhaAleem) converting the "SANS Workshop: Shadow Steps: Understanding and Detecting User Impersonation and Lateral Movement in Active Directory" workshop created by [Jean-Francois Maes](https://www.sans.org/profiles/jeanfrancois-maes/) to an ansible playbook and making it work with Ludus as well!

### Description from SANS Workshop: Shadow Steps: Understanding and Detecting User Impersonation and Lateral Movement in Active Directory

This hands-on, scenario-driven workshop delves into how attackers move stealthily through Active Directory environments using user impersonation and lateral movement techniques. Participants will explore how attackers exploit credentials and trust relationships to expand their access, and how defenders can detect, prevent, and respond to such threats.

Through simulated exercises and guided labs, participants will walk through real-world attack paths such as (over)Pass-the-Hash, Kerberoasting, and token impersonation.

Learning Objectives:

- Understand the key mechanisms behind user impersonation in Active Directory.
- Demonstrate how attackers perform lateral movement via tools and techniques such as:
- Pass-the-Hash
- Pass-the-Ticket/Overpass-the-Hash
- Remote Services Abuse (SMB, WMI, RDP, WinRM)
- SOCKS PTH
- Kerberoasting
- Token Impersonation
- Token Creation
- This hands-on workshop is ideal for Penetration Testers with limited knowledge about AD internals.

Have fun !

### Access the workbook here:

- https://logout.gitbook.io/lateral-movement-in-ad-with-empire

### Deployment

#### 1. Add roles

Add the `badsectorlabs.ludus_elastic_container` and `badsectorlabs.ludus_elastic_agent` roles to your Ludus server

```shell-session
ludus ansible roles add badsectorlabs.ludus_elastic_container
ludus ansible roles add badsectorlabs.ludus_elastic_agent
```

#### 2. Deploy the VMs

Set and deploy the configuration for the lab.

```bash
git clone https://github.com/aleemladha/SANS-Workshop-LateralMovement
ludus range config set -f SANS-Workshop-LateralMovement/ad/SANS/providers/ludus/config.yml
ludus range deploy
# Wait for the range to successfully deploy
# You can watch the logs with `ludus range logs -f`
# Or check the status with `ludus range status`
```

#### 3. Install requirements

Install ansible and its requirements for the lab on your local machine.

```shell-session
# You can use a virtualenv here if you would like
python3 -m venv sans-lat-ludus
source sans-lat-ludus/bin/activate
python3 -m pip install ansible-core
python3 -m pip install pywinrm
ansible-galaxy install -r SANS-Workshop-LateralMovement/ansible/requirements.yml
```

#### 4. Setup the inventory files

The inventory file is already present in the providers folder and replace RANGENUMBER with your range number with sed (commands provided below)

**Linux:**

```bash
cd SANS-Workshop-LateralMovement/ansible
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `sudo apt install jq` if you don't have jq
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/SANS/providers/ludus/inventory.yml
```

**macOS:**

```bash
cd SANS-Workshop-LateralMovement/ansible
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `brew install jq` if you don't have jq
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/SANS/providers/ludus/inventory.yml
```

#### 5. Deploy the SANS Workshop

**Note:** If not running on the Ludus host, you must be connected to your Ludus wireguard VPN for these commands to work

**Linux:**

```bash
# in the SANS-Workshop-LateralMovement/ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/SANS/data/inventory -i ../ad/SANS/providers/ludus/inventory.yml"
export LAB="SANS"
chmod +x ../scripts/provisionning.sh
../scripts/provisionning.sh
```

**macOS:**

```bash
# In the SANS-Workshop-LateralMovement/ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/SANS/data/inventory -i ../ad/SANS/providers/ludus/inventory.yml"
export LAB="SANS"
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
../scripts/provisionning.sh
```

Now you wait. `[WARNING]` lines are ok, and some steps may take a long time, don't panic!

This will take a few hours. You'll know it is done when you see:

```
The Empire's dominion is complete! But Rebel operatives remain hidden. Your mission: eliminate them.
```

#### 6. Snapshot VMs

**Note:** You must be connected to your Ludus wireguard VPN for these commands to work

Take snapshots via the proxmox web UI or SSH run the following ludus command:

```bash
ludus snapshot create clean-setup -d "Clean SANS Lab setup after ansible run"
```

#### 7. Hack!

Access your Kali machine at `https://10.RANGENUMBER.50.99:8444` using the creds `kali:password`.

Access your Elastic SIEM at `https://10.RANGENUMBER.20.1:5601` using the creds `elastic:elasticpassword`

Then [Setup Empire & Starkiller](https://logout.gitbook.io/lateral-movement-in-ad-with-empire/installing-the-environment/empire).

Once done, follow lab 2 in the workbook above, without the need to use any OpenVPN configuration.

**Note:** Replace this part with your RANGENUMBER `xfreerdp /v:10.RANGENUMBER.20.11 /u:Administrator /p:'AnsibleAutomation123!' +clipboard /dynamic-resolution`

You can also use a standard RDP client on your local machine if your WireGuard is connected.

If you want a challenge and want to do the lab with defender enabled, edit the `ad/SANS/data/inventory` file and change the last part to look like this

```
; allow defender
; usage : security.yml
[defender_on]
dc01
dc02
dc03
srv02

; disable defender
; usage : security.yml
[defender_off]
```

## BarbHack CTF 2024

### BarbHack CTF 2024 (Gotham City - Active Directory Lab)

**Props!** Huge shout out to [@ladhaAleem](https://twitter.com/LadhaAleem) converting the "BarbHack CTF 2024 (Gotham City - Active Directory Lab)" workshop created by [@mpgn_x64](https://x.com/mpgn_x64) to an ansible playbook and making it work with Ludus as well!

### Description from BarbHack CTF 2024

Welcome to the NetExec Active Directory Lab! This lab is designed to teach you how to exploit Active Directory (AD) environments using the powerful tool NetExec.

Originally featured in the Barbhack 2024 CTF, this lab is now available for free to everyone! In this lab, you'll explore how to use the powerful tool NetExec to efficiently compromise an Active Directory domain during an internal pentest.

The ultimate goal? Become Domain Administrator by following various attack paths, using nothing but NetExec! and Maybe BloodHound (Why not?)

Obviously do not cheat by looking at the passwords and flags in the recipe files, the lab must start without user to full compromise.

**Note:** Use nothing but NetExec! and Maybe BloodHound (Why not?)

Have fun !

### Deployment

#### 1. Deploy VMs

Set and deploy the configuration for the lab.

```bash
git clone https://github.com/Pennyw0rth/NetExec-Lab
ludus range config set -f NetExec-Lab/BARBHACK-2024/ad/BARBHACK/providers/ludus/config.yml
ludus range deploy
# Wait for the range to successfully deploy
# You can watch the logs with `ludus range logs -f`
# Or check the status with `ludus range status`
```

#### 2. Install requirements

**Warning:** If you are running this guide on the Ludus host you can skip this step, it already has all the requirements.

Install ansible and its requirements for the BarbHack lab on your local machine.

```shell-session
# You can use a virtualenv here if you would like
python3 -m pip install ansible-core
python3 -m pip install pywinrm
cd NetExec-Lab/BARBHACK-2024/ansible
ansible-galaxy install -r requirements.yml
```

#### 4. Setup the inventory files

The inventory file is already present in the providers folder and replace RANGENUMBER with your range number with sed (commands provided below)

**Linux or Ludus host:**

```bash
cd NetExec-Lab/BARBHACK-2024/ansible
# go the the ansible directory as above
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `sudo apt install jq` if you don't have jq
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/BARBHACK/providers/ludus/inventory.yml
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/BARBHACK/providers/ludus/inventory_disableludus.yml
```

**macOS:**

```bash
cd NetExec-Lab/BARBHACK-2024/ansible
# paste in the inventory file above
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `brew install jq` if you don't have jq
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/BARBHACK/providers/ludus/inventory.yml
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/BARBHACK/providers/ludus/inventory_disableludus.yml
```

#### 5. Deploy the BarbHack Workshop

**Note:** If not running on the Ludus host, you must be connected to your Ludus wireguard VPN for these commands to work

**Linux or Ludus host:**

```bash
# in the ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/BARBHACK/data/inventory -i ../ad/BARBHACK/providers/ludus/inventory.yml"
export LAB="BARBHACK"
chmod +x ../scripts/provisionning.sh
../scripts/provisionning.sh
```

**macOS:**

```bash
# In the ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/BARBHACK/data/inventory -i ../ad/BARBHACK/providers/ludus/inventory.yml"
export LAB="BARBHACK"
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
../scripts/provisionning.sh
```

Now you wait. `[WARNING]` lines are ok, and some steps may take a long time, don't panic!

This will take a few hours. You'll know it is done when you see:

```
Gotham needs you! A villain is still at large in the shadows. It's your mission to track them down!
```

#### 5. Disable localuser

Once install has finished disable localuser user to avoid using it and avoid unintended secrets stored (*I'm looking at you Lsassy*).

**Note:** If not running on the Ludus host, you must be connected to your Ludus wireguard VPN for this command to work

```bash
# Still in the BARBHACK-2024/ansible directory
ansible-playbook -i ../ad/BARBHACK/providers/ludus/inventory_disableludus.yml disable_localuser.yml reboot.yml
```

#### 5. Snapshot VMs

Take snapshots via the proxmox web UI or run the following ludus command

```bash
ludus snapshot create clean-setup -d "Clean BarbHack Lab setup after ansible run"
```

#### 6. Hack!

Access your Kali machine at `https://10.RANGENUMBER.10.99:8444` using the creds `kali:password` (sudo password is `kali`).

If you want a challange and want to do the lab with defender enabled, edit the `ad/BARBHACK/data/inventory` file and change the last part to look like this

```
; allow defender
; usage : security.yml
[defender_on]
dc01
srv01
srv02

; disable defender
; usage : security.yml
[defender_off]
```

## NetExec Workshop leHACK 2024

### Netexec Workshop (leHACK 2024)

**Props!** Huge shout out to [@ladhaAleem](https://twitter.com/LadhaAleem) for creating this project and converting the leHACK 2024 workshop created by [@mpgn_x64](https://x.com/mpgn_x64) to an ansible playbook and making it work with Ludus as well!

### Description from leHACK 2024

Welcome to the NetExec Active Directory Lab! This lab is designed to teach you how to exploit Active Directory (AD) environments using the powerful tool [NetExec](https://github.com/Pennyw0rth/NetExec).

Originally featured in the leHACK 2024 Workshop, this lab is now available for free to everyone! In this lab, you'll explore how to use the powerful tool NetExec to efficiently compromise an Active Directory domain during an internal pentest.

The ultimate goal? Become Domain Administrator by following various attack paths, using nothing but NetExec and maybe BloodHound (Why not :P).

Obviously do not cheat by looking at the passwords and flags in the recipe files, the lab must start without user to full compromise

**Note**: One change has been made on this lab regarding the workshop, the part using msol module on nxc is replaced with a dump of lsass. The rest is identical.

### Scenario

The Gallic camp was attacked by the Romans and it seems that a traitor made this attack possible! Two domains must be compromised to find it

### Public Writeups

- https://www.rayanle.cat/lehack-2024-netexec-workshop-writeup/ by [@rayanlecat](https://x.com/rayanlecat)
- https://blog.lasne.pro/posts/netexec-workshop-lehack2024/ by [@0xFalafel](https://x.com/0xFalafel)

### Deployment

#### 1. Add the Windows 2019 template to Ludus

```bash
git clone https://gitlab.com/badsectorlabs/ludus
cd ludus/templates
ludus templates add -d win2019-server-x64
[INFO]  Successfully added template
ludus templates build
[INFO]  Template building started - this will take a while. Building 1 template(s) at a time.
# Wait until the templates finish building, you can monitor them with `ludus templates logs -f` or `ludus templates status`
ludus templates list
+----------------------------------------+-------+
|                TEMPLATE                | BUILT |
+----------------------------------------+-------+
| debian-11-x64-server-template          | TRUE  |
| debian-12-x64-server-template          | TRUE  |
| kali-x64-desktop-template              | TRUE  |
| win11-22h2-x64-enterprise-template     | TRUE  |
| win2022-server-x64-template            | TRUE  |
| win2019-server-x64-template            | TRUE  |
+----------------------------------------+-------+
```

#### 2. Deploy VMs

Set and deploy the configuration for the lab.

```bash
git clone https://github.com/Pennyw0rth/NetExec-Lab
ludus range config set -f NetExec-Lab/LeHack-2024/ad/LEHACK/providers/ludus/config.yml
ludus range deploy
# Wait for the range to successfully deploy
# You can watch the logs with `ludus range logs -f`
# Or check the status with `ludus range status`
```

#### 3. Install requirements

Install ansible and its requirements for the NetExec lab on your local machine.

```shell-session
# You can use a virtualenv here if you would like
python3 -m pip install ansible-core
python3 -m pip install pywinrm
git clone https://github.com/Pennyw0rth/NetExec-Lab
cd LeHack-2024/ansible
ansible-galaxy install -r requirements.yml
```

#### 4. Setup the inventory files

The inventory file is already present in the providers folder and replace RANGENUMBER with your range number with sed (commands provided below)

**Linux:**

```bash
cd LeHack-2024/ansible
# go the the ansible directory as above
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `sudo apt install jq` if you don't have jq
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory.yml
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory_disableludus.yml
```

**macOS:**

```bash
cd LeHack-2024/ansible
# paste in the inventory file above
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `brew install jq` if you don't have jq
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory.yml
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory_disableludus.yml
```

#### 5. Deploy the NetExec Workshop

**Note:** If not running on the Ludus host, you must be connected to your Ludus wireguard VPN for these commands to work

**Linux:**

```bash
cd LeHack-2024/ansible
# in the ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/LEHACK/data/inventory -i ../ad/LEHACK/providers/ludus/inventory.yml"
export LAB="LEHACK"
chmod +x ../scripts/provisionning.sh
../scripts/provisionning.sh
```

**macOS:**

```bash
cd LeHack-2024/ansible
# In the ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/LEHACK/data/inventory -i ../ad/LEHACK/providers/ludus/inventory.yml"
export LAB="LEHACK"
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
../scripts/provisionning.sh
```

Now you wait. `[WARNING]` lines are ok, and some steps may take a long time, don't panic!

This will take a few hours. You'll know it is done when you see:

```
May the gods of Gaul guide you as you embark on this dangerous quest!
```

#### 5. Disable localuser

Once install has finished disable localuser user to avoid using it and avoid unintended secrets stored (*I'm looking at you Lsassy*).

**Note:** You must be connected to your Ludus wireguard VPN for these commands to work

```bash
# Still in the LeHack-2024/ansible directory
ansible-playbook -i ../ad/LEHACK/providers/ludus/inventory_disableludus.yml disable_localuser.yml reboot.yml
```

#### 6. Snapshot VMs

Take snapshots via the proxmox web UI or SSH run the following ludus command:

```bash
ludus snapshot create clean-setup -d "Clean setup of the netexec lab after ansible run"
```

#### 7. Hack!

Access your Kali machine at `https://10.RANGENUMBER.10.99:8444` using the creds `kali:password`.

## NetExec Workshop leHACK 2025

### Netexec Workshop (leHACK 2025)

**Props!** Huge shout out to [@ladhaAleem](https://twitter.com/LadhaAleem) for creating this project and converting the leHACK 2025 workshop created by [@mpgn_x64](https://x.com/mpgn_x64) to an ansible playbook and making it work with Ludus as well!

### Description from leHACK 2025

Welcome to the NetExec Active Directory Lab! This lab is designed to teach you how to exploit Active Directory (AD) environments using the powerful tool [NetExec](https://github.com/Pennyw0rth/NetExec).

Originally featured in the leHACK 2025 Workshop, this lab is now available for free to everyone! In this lab, you'll explore how to use the powerful tool NetExec to efficiently compromise an Active Directory domain during an internal pentest.

The ultimate goal? Become Domain Administrator by following various attack paths, using nothing but NetExec and maybe BloodHound (Why not :P).

Obviously do not cheat by looking at the passwords and flags in the recipe files, the lab must start without user to full compromise

**Note**: One change has been made on this lab regarding the workshop, the part using msol module on nxc is replaced with a dump of lsass. The rest is identical.

### Public Writeups

- https://blog.anh4ckin.ch/posts/netexec-workshop2k25/ by [@LeandreOnizuka](https://x.com/LeandreOnizuka)

### Deployment

#### 1. Add the Windows 2019 template to Ludus

```bash
git clone https://gitlab.com/badsectorlabs/ludus
cd ludus/templates
ludus templates add -d win2019-server-x64
[INFO]  Successfully added template
ludus templates build
[INFO]  Template building started - this will take a while. Building 1 template(s) at a time.
# Wait until the templates finish building, you can monitor them with `ludus templates logs -f` or `ludus templates status`
ludus templates list
+----------------------------------------+-------+
|                TEMPLATE                | BUILT |
+----------------------------------------+-------+
| debian-11-x64-server-template          | TRUE  |
| debian-12-x64-server-template          | TRUE  |
| kali-x64-desktop-template              | TRUE  |
| win11-22h2-x64-enterprise-template     | TRUE  |
| win2022-server-x64-template            | TRUE  |
| win2019-server-x64-template            | TRUE  |
+----------------------------------------+-------+
```

#### 2. Deploy VMs

Set and deploy the configuration for the lab.

```bash
git clone https://github.com/Pennyw0rth/NetExec-Lab
ludus range config set -f NetExec-Lab/LeHack-2025/ad/LEHACK/providers/ludus/config.yml
ludus range deploy
# Wait for the range to successfully deploy
# You can watch the logs with `ludus range logs -f`
# Or check the status with `ludus range status`
```

#### 3. Install requirements

Install ansible and its requirements for the NetExec lab on your local machine.

```shell-session
# You can use a virtualenv here if you would like
python3 -m pip install ansible-core
python3 -m pip install pywinrm
git clone https://github.com/Pennyw0rth/NetExec-Lab
cd LeHack-2025/ansible
ansible-galaxy install -r requirements.yml
```

#### 4. Setup the inventory files

The inventory file is already present in the providers folder and replace RANGENUMBER with your range number with sed (commands provided below)

**Linux:**

```bash
cd LeHack-2025/ansible
# go the the ansible directory as above
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `sudo apt install jq` if you don't have jq
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory.yml
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory_disableludus.yml
```

**macOS:**

```bash
cd LeHack-2025/ansible
# paste in the inventory file above
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `brew install jq` if you don't have jq
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory.yml
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/LEHACK/providers/ludus/inventory_disableludus.yml
```

#### 5. Deploy the NetExec Workshop

**Note:** If not running on the Ludus host, you must be connected to your Ludus wireguard VPN for these commands to work

**Linux:**

```bash
cd LeHack-2025/ansible
# in the ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/LEHACK/data/inventory -i ../ad/LEHACK/providers/ludus/inventory.yml"
export LAB="LEHACK"
chmod +x ../scripts/provisionning.sh
../scripts/provisionning.sh
```

**macOS:**

```bash
cd LeHack-2025/ansible
# In the ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/LEHACK/data/inventory -i ../ad/LEHACK/providers/ludus/inventory.yml"
export LAB="LEHACK"
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
../scripts/provisionning.sh
```

Now you wait. `[WARNING]` lines are ok, and some steps may take a long time, don't panic!

This will take a few hours. You'll know it is done when you see:

```
May the gods of Gaul guide you as you embark on this dangerous quest!
```

#### 5. Disable localuser

Once install has finished disable localuser user to avoid using it and avoid unintended secrets stored (*I'm looking at you Lsassy*).

**Note:** You must be connected to your Ludus wireguard VPN for these commands to work

```bash
# Still in the LEHACK-2025/ansible directory
ansible-playbook -i ../ad/LEHACK/providers/ludus/inventory_disableludus.yml disable_localuser.yml reboot.yml rebootsrv01.yml
```

#### 6. Snapshot VMs

Take snapshots via the proxmox web UI or SSH run the following ludus command:

```bash
ludus snapshot create clean-setup -d "Clean setup of the netexec lab after ansible run"
```

#### 7. Hack!

Access your Kali machine at `https://10.RANGENUMBER.10.99:8444` using the creds `kali:password`.

## SANS AD Privilege Escalation with Empire

### SANS Workshop: Active Directory Privilege Escalation with Empire!

**Props!** Huge shout out to [@ladhaAleem](https://twitter.com/LadhaAleem) converting the "SANS Workshop: Active Directory Privilege Escalation with Empire" workshop created by [Jean-Francois Maes](https://www.sans.org/profiles/jeanfrancois-maes/) to an ansible playbook and making it work with Ludus as well!

### Description from SANS Workshop: Active Directory Privilege Escalation with Empire

Welcome to this workshop where we are going to dive into a core active directory component - Kerberos!

This lab is a self-guided Active Directory security exercise designed to help participants understand Kerberos-based privilege escalation attacks. Originally part of a SANS workshop, this lab is now freely available for local deployment on VMware, VirtualBox, and Ludus.

Participants will build their own AD lab, configure attack tools, and execute real-world attack techniques to escalate privileges in an Active Directory environment.

This workshop is ideally suited for blue teamers that want to peek behind the curtain and understand how adversaries attack AD and pentesters that may not be as familiar with AD environments yet.

Attacks Covered:

- Kerberoasting - Extracting service tickets to crack passwords
- DCSyncing - Extracting credentials by simulating a domain controller
- SID History Abuse - Hopping across parent/child domain trusts
- Unconstrained Delegation Abuse - Capturing privileged credentials

**Note:** The following lab only uses of Empire & Starkiller and no other tools

Have fun !

### Access the workbook here:

- https://logout.gitbook.io/ad-privesc-with-empire

### Deployment

#### 1. Deploy the VMs

Set and deploy the configuration for the lab.

```bash
git clone https://github.com/aleemladha/SANS-Workshop-Lab
ludus range config set -f SANS-Workshop-Lab/ad/SANS/providers/ludus/config.yml
ludus range deploy
# Wait for the range to successfully deploy
# You can watch the logs with `ludus range logs -f`
# Or check the status with `ludus range status`
```

#### 2. Install requirements

Install ansible and its requirements for the lab on your local machine.

```shell-session
# You can use a virtualenv here if you would like
python3 -m venv sans-ludus
source sans-ludus/bin/activate
python3 -m pip install ansible-core
python3 -m pip install pywinrm
ansible-galaxy install -r SANS-Workshop-Lab/ansible/requirements.yml
```

#### 3. Setup the inventory files

The inventory file is already present in the providers folder and replace RANGENUMBER with your range number with sed (commands provided below)

**Linux:**

```bash
cd SANS-Workshop-Lab/ansible
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `sudo apt install jq` if you don't have jq
sed -i "s/RANGENUMBER/$RANGENUMBER/g" ../ad/SANS/providers/ludus/inventory.yml
```

**macOS:**

```bash
cd SANS-Workshop-Lab/ansible
export RANGENUMBER=$(ludus range list --json | jq '.rangeNumber')
# `brew install jq` if you don't have jq
sed -i '' "s/RANGENUMBER/$RANGENUMBER/g" ../ad/SANS/providers/ludus/inventory.yml
```

#### 4. Deploy the SANS Workshop

**Note:** If not running on the Ludus host, you must be connected to your Ludus wireguard VPN for these commands to work

**Linux:**

```bash
# in the SANS-Workshop-Lab/ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/SANS/data/inventory -i ../ad/SANS/providers/ludus/inventory.yml"
export LAB="SANS"
chmod +x ../scripts/provisionning.sh
../scripts/provisionning.sh
```

**macOS:**

```bash
# In the SANS-Workshop-Lab/ansible folder perform the following
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/SANS/data/inventory -i ../ad/SANS/providers/ludus/inventory.yml"
export LAB="SANS"
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
../scripts/provisionning.sh
```

Now you wait. `[WARNING]` lines are ok, and some steps may take a long time, don't panic!

This will take a few hours. You'll know it is done when you see:

```
The Empire's dominion is complete! But Rebel operatives remain hidden. Your mission: eliminate them.
```

**Note:** You must be connected to your Ludus wireguard VPN for these commands to work

#### 5. Snapshot VMs

Take snapshots via the proxmox web UI or SSH run the following ludus command:

```bash
ludus snapshot create clean-setup -d "Clean SANS Lab setup after ansible run"
```

#### 6. Hack!

Access your Kali machine at `https://10.RANGENUMBER.50.99:8444` using the creds `kali:password`.

Then [Setup Empire & Starkiller](https://logout.gitbook.io/ad-privesc-with-empire/installing-the-environment/empire).

Once done, follow lab 2 in the workbook above, without the need to use any OpenVPN configuration.

**Note:** Replace this part with your RANGENUMBER `xfreerdp /v:10.RANGENUMBER.20.10 /u:jross /p:'0nz2xQ44GumoWpl' +clipboard`

You can also use a standard RDP client on your local machine if your WireGuard is connected.

If you want a challange and want to do the lab with defender enabled, edit the `ad/SANS/data/inventory` file and change the last part to look like this

```
; allow defender
; usage : security.yml
[defender_on]
dc01
dc02
dc03
srv02

; disable defender
; usage : security.yml
[defender_off]
```
