# Sharing

Range sharing between Ludus users, including workshops and single user with multiple ranges.

**Note:** NetPenguins has created [ludus-impersonator.sh](https://gist.github.com/NetPenguins/277babc21a74fcccc083e00174569fb6) which could help you if you often impersonate users.

There are two main use cases for sharing ranges between users:

1. Multiple users sharing a Ludus server wish to access one or more shared ranges (i.e. a team collaborating, a workshop)

2. One user of Ludus wishes to have separate ranges but control them all with the same WireGuard config and Ludus API key (i.e. a Ludus host dedicated to a single user but with many ranges).

## Multiple users sharing ranges (team/workshop)

In this scenario, a team member will set up a custom EDR range or a proctor will build a range and wants to share it with his team/class, but not allow them to modify it with Ludus.

1. A Ludus admin user must create a user that will be the shared range user:

```bash
# Assumes a tunnel set up in another shell with: ssh -L 8081:127.0.0.1:8081 user@<Ludus IP>
ludus --url https://127.0.0.1:8081 user add -n 'Workshop Range 1' -i WKSHP1
+--------+------------------+-------+-------------------------------------------------+
| USERID | PROXMOX USERNAME | ADMIN |                     API KEY                     |
+--------+------------------+-------+-------------------------------------------------+
| WKSHP1 | workshop-range-1 | false | WKSHP1.yRG8m_dYoHAa47D3P2BkNlObFFqVz++lT8C2dSjS |
+--------+------------------+-------+-------------------------------------------------+
```

2. This API key can be used by the proctor directly, or, if they are an admin, the range can be controlled with impersonation.

### Using User Impersonation

Use the `--user` flag to control another user's range:

```shell
ludus --user WKSHP1 range config set -f my-custom-config.yml
ludus --user WKSHP1 range deploy
```

### Using the API Key Directly

Use the API key of the new user directly:

```shell
ludus apikey
[INFO]  Enter your Ludus API Key for https://198.51.100.1:8080:
WKSHP1.yRG8m_dYoHAa47D3P2BkNlObFFqVz++lT8C2dSjS
[INFO]  Ludus API key set successfully
ludus range config set -f my-custom-config.yml
[INFO]  Your range config has been successfully updated.
ludus range deploy
[INFO]  range deploy started
```

3. The Ludus admin user shares the range to users who will use it

```shell
ludus range access grant --target WKSHP1 --source USER1
[INFO]  Range access to Workshop Range 1's range granted to User 1. Have User 1 pull an updated wireguard config.
ludus range access grant --target WKSHP1 --source USER2
[INFO]  Range access to Workshop Range 1's range granted to User 2. Have User 2 pull an updated wireguard config.
...
ludus range access list
+----------------------+-----------------+
| TARGET RANGE USER ID | SOURCE USER IDS |
+----------------------+-----------------+
|        WKSHP1        |   USER1,USER2   |
+----------------------+-----------------+
```

4. Users who had access granted to the shared range pull and load their updated WireGuard config and access the range directly

```bash
ludus user wireguard
# User loads and connects to the new config
ping 10.x.x.x # a machine in the shared range
```

**Important:** Ludus does nothing to prevent users from modifying VMs they have access to (either intentionally or via exploitation). As credentials are simple by default on purpose, consider this situation for your workshops and make adjustments as necessary. Having a snapshot of the VMs before unleashing users on them is a good idea!

## One user with multiple ranges

In this scenario, a Ludus host is used by a user who wishes to control and modify multiple separate ranges.

1. The Ludus admin user (ADMUSER) creates a user for each distinct range they wish to control

```bash
# Assumes a tunnel set up in another shell with: ssh -L 8081:127.0.0.1:8081 user@<Ludus IP>
ludus --url https://127.0.0.1:8081 user add -n 'SCCM Range' -i SCCM
...
ludus --url https://127.0.0.1:8081 user add -n 'GOAD Range' -i GOAD
```

2. The Ludus admin user sets and deploys ranges as the new range users

```shell
ludus --user SCCM range config set -f sccm-range.yml
[INFO]  Your range config has been successfully updated.
ludus --user SCCM range deploy
[INFO]  range deploy started
...
ludus --user GOAD range config set -f goad-range.yml
[INFO]  Your range config has been successfully updated.
ludus --user GOAD range deploy
[INFO]  range deploy started
```

3. The Ludus admin user grants himself access to all the new ranges

```shell
ludus range access grant --target SCCM --source ADMUSER
[INFO]  Range access to SCCM Range's range granted to Admin user. Have Admin user pull an updated wireguard config.

...
ludus range access grant --target GOAD --source ADMUSER
[INFO]  Range access to GOAD Range's range granted to Admin user. Have Admin user pull an updated wireguard config.
ludus range access list
+----------------------+-----------------+
| TARGET RANGE USER ID | SOURCE USER IDS |
+----------------------+-----------------+
|        SCCM          |     ADMUSER     |
|        GOAD          |     ADMUSER     |
+----------------------+-----------------+
```

4. The Ludus admin user pulls an updated WireGuard config and has access to all ranges

```bash
ludus user wireguard
# Admin user loads and connects to the new config
ping 10.x.x.x # a machine in the SCCM or GOAD range
```
