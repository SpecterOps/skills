# Ludus API Reference

The Ludus API (v1.9.6) controls user management, range deployment, power state, and testing state. All endpoints require API key authentication via the `X-API-KEY` header.

- **Base URL:** `https://198.51.100.1:8080` (default, over WireGuard)
- **Admin URL:** `https://127.0.0.1:8081` (for user management operations)
- **Auth:** API key in `X-API-KEY` header
- **License:** GNU AGPLv3

Common query parameter: `userID` (string, 1-20 alphanumeric chars, e.g. `JD`) - admins can pass this on most endpoints to act on behalf of another user.

---

## User Management

Actions to list and manage user accounts in Ludus and the underlying operating system.

### GET / - Retrieve Ludus version

Returns the Ludus server version string.

**Responses:**
- `200` - `{"result": "Ludus Server v1.0.0+abc123a"}`

---

### GET /user - List user details

Get a single user object. Defaults to the caller. Admins can specify another user via `userID` query param.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Response 200:**
```json
[
  {
    "name": "John Doe",
    "userID": "JD",
    "dateCreated": "2022-08-29T09:12:33.001Z",
    "dateLastActive": "2022-08-29T09:12:33.001Z",
    "isAdmin": true,
    "proxmoxUsername": "john-doe"
  }
]
```

**Responses:**
- `200` - User object array
- `400` - Bad input parameter

---

### POST /user - Add a user

Adds a user to the system. **Admin only.** The response contains the plaintext API key (not retrievable again except via `/user/apikey`).

**Request Body:**
```json
{
  "name": "John Doe",
  "userID": "JD",
  "isAdmin": true
}
```

**Response 201:**
```json
{
  "name": "John Doe",
  "userID": "JD",
  "isAdmin": true,
  "apiKey": "JD.Vf{M@GC:w}YQ=1zv@gLLnDH:j3nI]l7@:ct:qPy9",
  "proxmoxUsername": "john-doe"
}
```

**Responses:**
- `201` - User created (includes API key)
- `400` - Error (e.g. "User with that name already exists")

---

### DELETE /user/{userID} - Remove a user

Removes a user from the system. **Admin only.**

**Path Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | Yes | The user ID to delete |

**Responses:**
- `200` - User deleted
- `400` - userID not provided
- `404` - User not found

---

### GET /user/all - List all users

Get all users in Ludus. **Admin only.**

**Response 200:** Array of user objects (same schema as GET /user).

**Responses:**
- `200` - Array of user objects
- `400` - Bad input parameter

---

### GET /user/apikey - Reset and retrieve API key

Resets and returns the API key for the user. Defaults to the caller's key. Admins can reset other users' keys via `userID`.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Response 200:**
```json
{
  "result": {
    "apiKey": "G0rO+G+8Zlu%CAEDyYC2ZdW3pBWW+al,J2_tli1h"
  }
}
```

**Responses:**
- `200` - API key object
- `400` - Bad input parameter

---

### GET /user/credentials - Get proxmox credentials

Get proxmox credentials for a user.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Response 200:**
```json
{
  "result": {
    "proxmoxUsername": "john-doe",
    "proxmoxPassword": "5cy5@plhik4g&Yk12sG"
  }
}
```

**Responses:**
- `200` - Credential object
- `400` - Bad input parameter

---

### POST /user/credentials - Set proxmox credentials

Set the proxmox password for a user. Admins can set for other users via `userID` in body.

**Request Body:**
```json
{
  "userID": "JD",
  "proxmoxPassword": "5cy5@plhik4g&Yk12sG"
}
```

**Responses:**
- `200` - `{"result": "Your proxmox password has been successfully updated."}`
- `400` - Bad input parameter

---

### POST /user/passwordreset - Reset proxmox password

Resets a user's proxmox password. **Admin only.**

**Request Body:**
```json
{
  "userID": "JD"
}
```

**Responses:**
- `201` - User credentials updated
- `400` - Invalid input

---

### GET /user/wireguard - Get WireGuard config

Returns a WireGuard configuration file with appropriate values for the user's range.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Response 200:**
```json
{
  "result": {
    "wireGuardConfig": "[Interface]\nPrivateKey = ...\nAddress = 198.51.100.3/32\n\n[Peer]\nPublicKey = ...\nAllowedIPs = 10.3.0.0/16, 198.51.100.1/32\nEndpoint = 198.18.0.25:51820\nPersistentKeepalive = 25\n"
  }
}
```

---

## Range Management

Actions to list and manage range deployment.

### GET /range - List range VMs, power state, and testing state

Lists a range's VMs along with power state and testing state. Admins can query other users' ranges.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Response 200:**
```json
{
  "userID": "JD",
  "rangeNumber": 3,
  "lastDeployment": "2022-08-29T09:12:33.001Z",
  "numberOfVMs": 7,
  "testingEnabled": true,
  "allowedIPs": ["1.2.3.4"],
  "allowedDomains": ["example.com"],
  "rangeState": "SUCCESS",
  "VMs": [
    {
      "ID": 53,
      "proxmoxID": 146,
      "rangeNumber": 3,
      "name": "JD-ad-dc-win2019-server-x64",
      "poweredOn": true,
      "ip": "203.0.113.4"
    }
  ]
}
```

**Responses:**
- `200` - Range object
- `400` - Bad input parameter

---

### DELETE /range - Delete range

Stops and deletes all range VMs. Used to start fresh.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Responses:**
- `201` - `{"result": "Range destroy in progress"}`

---

### POST /range/abort - Abort deployment

Stops the range deployment by killing the ansible process for the user. Admins may specify another user ID.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Responses:**
- `201` - Range deploy aborted
- `400` - Invalid input
- `500` - Error with abort

---

### GET /range/all - List all ranges (admin)

Lists all ranges with VMs, power state, and testing state. **Admin only.**

**Response 200:** Array of range objects (same schema as GET /range).

**Responses:**
- `200` - Array of range objects
- `400` - Bad input parameter

---

### GET /range/config - Get range config

Returns the current YAML configuration for the range.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Response 200:**
```json
{
  "result": "ludus:\n  - vm_name: \"JD-ad-dc-win2019-server-x64\"\n    hostname: \"JD-DC01-2019\"\n    template: win2019-server-x64-template\n    ip_last_octet: 11\n    ..."
}
```

**Responses:**
- `200` - Range config YAML as string
- `400` - Bad input parameter

---

### PUT /range/config - Update range config

Updates the range configuration with a provided YAML file.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:** `multipart/form-data`
| Field | Type | Description |
|-------|------|-------------|
| `file` | binary | YAML config file |
| `force` | boolean | Force update (default: false) |

**Responses:**
- `200` - Successfully updated configuration
- `400` - Bad input parameter

---

### GET /range/config/example - Get example config

Returns an example range configuration with the user's userID in vm_name and hostname fields.

**Response 200:**
```json
{
  "result": "network:\n  inter_vlan_default: REJECT\n  rules:\n    - name: Only allow windows to kali on 443\n      ...\nludus:\n  - vm_name: \"{{ range_id }}-ad-dc-win2019-server-x64\"\n    ..."
}
```

**Responses:**
- `200` - Example config YAML
- `400` - Bad input parameter

---

### POST /range/deploy - Deploy range

Deploys a range with ansible. Can be called multiple times safely. Tags and force are optional.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "tags": "all",
  "force": false,
  "only_roles": ["badsectorlabs.ludus_bloodhound_ce"],
  "limit": "JD-kali1"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `tags` | string | Ansible tags to run (default: "all") |
| `force` | boolean | Force deploy even if testing enabled (default: false) |
| `only_roles` | string[] | Limit user-defined roles to this list |
| `limit` | string | Limit deploy to VMs matching pattern |

**Responses:**
- `201` - Range deployed
- `400` - Invalid input
- `500` - Error with deployment

---

### GET /range/logs - Get deployment logs

Returns the latest ansible logs for the range.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |
| `tail` | No | Number of lines to return |
| `cursor` | No | Line number to resume from |

**Response 200:**
```json
{
  "result": "2022-12-06 16:11:11,810 ... PLAY [Acquire a session ticket] ...",
  "cursor": 274
}
```

---

### GET /range/tags - List deploy tags

Lists all ansible tags available for use with the deploy command.

**Response 200:**
```json
"additional-tools, custom-choco, custom-tasks, dcs, debug, destroy-range, domain-join, etchosts, host-payload, install-office, install-visual-studio, nexus, opstations, redirectors, services, teamservers, test-range, user-management, win10, winrunner"
```

**Responses:**
- `200` - Comma-separated tag string
- `400` - Bad input parameter

---

### GET /range/etchosts - Get /etc/hosts file

Returns an /etc/hosts file with entries for the user's range VMs.

**Response 200:**
```json
{
  "result": "# Ludus /etc/hosts\n10.3.10.11     JD-ad-dc-win2019-server-x64\n..."
}
```

---

### GET /range/sshconfig - Get SSH config

Returns an SSH configuration file for the user's range.

**Response 200:**
```json
{
  "result": "Host teamserver1\n  HostName 10.3.30.11\n  User debian\n  Port 22\n  IdentityFile ~/.ssh/ludus.key\n..."
}
```

---

### GET /range/rdpconfigs - Get RDP configs zip

Returns a zip file containing RDP configuration files for Windows VMs in the range.

**Response 200:** `application/zip` binary data.

---

### GET /range/ansibleinventory - Get ansible inventory

Returns an ansible inventory file for the user's range.

**Response 200:**
```json
{
  "result": "all:\n  children:\n    ADMIN:\n      hosts:\n    JD:\n      hosts:\n        JD-ad-dc-win2019-server-x64:\n          ansible_connection: winrm\n          ..."
}
```

---

### GET /range/access - List range access

Returns an array of current cross-range access settings. **Admin only.**

**Response 200:**
```json
[
  {
    "targetUserID": "JD",
    "sourceUserIDs": ["JS"]
  }
]
```

**Responses:**
- `200` - Array of access settings
- `403` - Admin only

---

### POST /range/access - Grant/revoke access

Grant or revoke range access from one user to another. **Admin only.**

**Request Body:**
```json
{
  "action": "grant",
  "targetUserID": "JD",
  "sourceUserID": "JS",
  "force": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | `"grant"` or `"revoke"` |
| `targetUserID` | string | Range owner's userID |
| `sourceUserID` | string | User gaining/losing access |
| `force` | boolean | Force even if target router is inaccessible |

**Responses:**
- `200` - `{"result": "Range access to john doe's range granted to jane smith. Have jane smith pull an updated wireguard config."}`
- `403` - Admin only
- `404` - Access not found (for revoke)

---

## Power State Management

Actions to list VM power state and toggle VM power state.

### PUT /range/poweron - Power on VMs

Power on one, multiple, or all range VMs. Pass `"all"` in the machines array to operate on all VMs.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "machines": ["JD-ad-dc-win2019-server-x64"]
}
```

Use `["all"]` to power on all VMs.

**Responses:**
- `201` - `{"result": "range VM power on in progress"}`
- `500` - Error

---

### PUT /range/poweroff - Power off VMs

Power off one, multiple, or all range VMs. Pass `"all"` in the machines array to operate on all VMs.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "machines": ["JD-ad-dc-win2019-server-x64"]
}
```

Use `["all"]` to power off all VMs.

**Responses:**
- `201` - `{"result": "range VM power off in progress"}`
- `500` - Error

---

## Testing State Management

Actions to show range testing state and toggle range testing state.

### PUT /testing/start - Enter testing

Snapshots all test_range VMs and blocks all outbound traffic and DNS requests from the test range subnet.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Responses:**
- `201` - Testing state entered
- `400` - Invalid input
- `500` - Error

---

### PUT /testing/stop - Exit testing

Reverts all test_range VMs and allows all outbound traffic and DNS requests from the test range subnet.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "force": false
}
```

Setting `force` to true ignores errors when reverting snapshots but may leak telemetry about payloads.

**Responses:**
- `201` - Testing state exited
- `400` - Invalid input
- `500` - Error

---

### POST /testing/allow - Allow domain/IP

Looks up the domain and its HTTPS certificate CRL domains, adding all IPs to iptables allow and DNS allow list.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "domains": ["example.com"],
  "ips": ["203.0.113.4"]
}
```

**Response 200:**
```json
{
  "allowed": ["203.0.113.4"],
  "errors": [
    {"item": "example.com", "reason": "already allowed"}
  ]
}
```

**Responses:**
- `200` - Allowed results
- `400` - Invalid input
- `500` - Error

---

### POST /testing/deny - Deny domain/IP

Removes iptables and DNS rules that allow a domain/IP through the firewall. Does NOT deny CRL domains as they may be shared by multiple domains.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "domains": ["example.com"],
  "ips": ["203.0.113.4"]
}
```

**Response 200:**
```json
{
  "denied": ["203.0.113.4"],
  "errors": [
    {"item": "example.com", "reason": "was not allowed"}
  ]
}
```

**Responses:**
- `200` - Denied results
- `400` - Invalid input
- `500` - Error

---

### POST /testing/update - Update VM

Runs the ansible update routine on a VM or group of VMs. **Windows only.**

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "name": "JD-win10-21h2-enterprise-x64"
}
```

**Responses:**
- `200` - `{"result": "update process started"}`
- `500` - Error

---

## Ansible Management

Actions to manage Ansible roles and collections on the Ludus host.

### GET /ansible - List roles and collections

Returns available Ansible roles and collections installed for this user.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Response 200:**
```json
[
  {
    "name": "geerlingguy.java",
    "version": "2.3.2",
    "type": "role",
    "global": false
  }
]
```

---

### POST /ansible/role - Install/remove role

Install or remove an Ansible role by name or URL.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID (admin only for other users) |

**Request Body:**
```json
{
  "role": "geerlingguy.java",
  "version": "2.3.2",
  "force": true,
  "action": "install",
  "global": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Role name or URL |
| `version` | string | Version to install |
| `force` | boolean | Force reinstall |
| `action` | string | `"install"` or `"remove"` |
| `global` | boolean | Install globally |

**Responses:**
- `201` - `{"result": "Successfully installed: geerlingguy.java"}`
- `403` - Unauthorized
- `500` - Error installing role

---

### PUT /ansible/role/fromtar - Install role from tar

Install an Ansible role from a local directory (uploaded as tar).

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID (admin only for other users) |

**Request Body:** `multipart/form-data`
| Field | Type | Description |
|-------|------|-------------|
| `file` | binary | Tar file of the role |
| `force` | boolean | Force reinstall |

**Responses:**
- `201` - `{"result": "Successfully installed role"}`
- `400` - Bad request
- `403` - Unauthorized
- `500` - Error installing role

---

### POST /ansible/collection - Install collection

Install an Ansible collection by name or URL. Collections can only be removed by deleting their directories manually.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID (admin only for other users) |

**Request Body:**
```json
{
  "collection": "maxhoesel.smallstep",
  "version": "0.23.1",
  "force": true
}
```

**Responses:**
- `201` - `{"result": "Successfully installed: maxhoesel.smallstep"}`
- `409` - Collection already installed (use force to reinstall)
- `500` - Error installing collection

---

## Template Management

Actions to manage VM templates.

### GET /templates - List templates

Returns a list of VM templates that have been built in Ludus.

**Response 200:**
```json
[
  {
    "name": "debian-11-x64-server-template",
    "built": false
  }
]
```

**Responses:**
- `200` - Template status array
- `500` - Error

---

### POST /templates - Build templates

Starts the packer template build process. Specify a specific template name or `"all"`.

**Request Body:**
```json
{
  "template": "debian-12-x64-server-template",
  "parallel": 3,
  "verbose": false
}
```

**Responses:**
- `200` - `{"result": "Template building started - this will take a while. Building 3 template(s) at a time."}`
- `404` - Template not found
- `500` - Error starting build

---

### PUT /templates - Add a template

Add a template to Ludus from a tar file.

**Request Body:** `multipart/form-data`
| Field | Type | Description |
|-------|------|-------------|
| `file` | binary | Template tar file |
| `force` | boolean | Force overwrite |

**Responses:**
- `201` - `{"result": "Successfully added template"}`
- `400` - Bad request
- `500` - Error adding template

---

### DELETE /template/{name} - Delete a template

Delete a template. Users may not delete system templates.

**Path Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `name` | Yes | Template name to delete |

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Impersonate user (admin only) |

**Responses:**
- `201` - Template removed
- `400` - Template name not provided
- `403` - Cannot delete system templates
- `404` - Template not found
- `409` - Template in use by VMs

---

### POST /templates/abort - Abort template builds

Kills any running packer processes for the user.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID (admin only for other users) |

**Responses:**
- `200` - `{"result": "Packer process(es) aborted for user john-doe"}`
- `500` - No packer processes found

---

### GET /templates/logs - Get packer logs

Returns the latest packer build logs.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |
| `tail` | No | Number of lines to return |
| `cursor` | No | Line number to resume from |

**Response 200:**
```json
{
  "result": "2023/01/29 14:57:40 Build debug mode: false\n...",
  "cursor": 274
}
```

---

### GET /templates/status - Get build status

Returns a list of templates currently being built.

**Response 200:**
```json
[
  {
    "template": "debian-10-x64-server-template",
    "user": "john-doe"
  }
]
```

**Responses:**
- `200` - Array of builds in progress
- `500` - Error

---

## Snapshot Management

Actions to manage snapshots.

### GET /snapshots/list - List snapshots

Returns a list of snapshots for a range.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |
| `vmids` | No | Comma-separated list of VMIDs (e.g. `100,101`) |

**Response 200:**
```json
{
  "snapshots": [
    {
      "name": "My snapshot",
      "includesRAM": true,
      "description": "Took this snapshot before testing something",
      "snaptime": 1740779020,
      "parent": "Other snapshot",
      "vmid": 179,
      "vmname": "JD-ad-win11-22h2-enterprise-x64-1"
    }
  ],
  "errors": [
    {
      "vmid": 180,
      "vmname": "JD-ad-win11-22h2-enterprise-x64-2",
      "error": "Error parsing VM ID abc: ..."
    }
  ]
}
```

**Responses:**
- `200` - Snapshot list with errors
- `500` - Error

---

### POST /snapshots/create - Create snapshot

Takes a snapshot of one or more VMs by VMID. If `vmids` is empty, all VMs in the range are snapshotted.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "name": "My cool snapshot",
  "description": "Taking this snapshot before doing some testing",
  "vmids": [179, 180],
  "includeRAM": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Snapshot name |
| `description` | string | Snapshot description |
| `vmids` | int[] | VMIDs to snapshot (empty = all) |
| `includeRAM` | boolean | Include RAM (if false, VM powers off on restore) |

**Response 200:**
```json
{
  "success": [179],
  "errors": [{"vmid": 180, "vmname": "...", "error": "..."}]
}
```

**Responses:**
- `200` - Success/error arrays
- `500` - Internal error

---

### POST /snapshots/rollback - Rollback snapshot

Rolls back one or more VMs to a specified snapshot.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "name": "My cool snapshot",
  "vmids": [179, 180]
}
```

**Response 200:**
```json
{
  "success": [179],
  "errors": [{"vmid": 180, "vmname": "...", "error": "..."}]
}
```

**Responses:**
- `200` - Success/error arrays
- `500` - Internal error

---

### POST /snapshots/remove - Delete snapshot

Deletes a snapshot from one or more VMs.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "name": "My cool snapshot",
  "vmids": [179, 180]
}
```

**Response 200:**
```json
{
  "success": [179],
  "errors": [{"vmid": 180, "vmname": "...", "error": "..."}]
}
```

**Responses:**
- `200` - Success/error arrays
- `500` - Internal error

---

## KMS Management

Actions to manage the Key Management Service. **Enterprise only.**

### POST /kms/install - Install KMS server

Creates a KMS VM in the ADMIN pool at 192.0.2.1 and installs the KMS server.

**Responses:**
- `200` - `{"result": "KMS setup complete"}`
- `500` - `{"error": "Task failed: ..."}`

---

### POST /kms/license - License Windows VMs

License one or more Windows VMs using the KMS server.

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "productKey": "TVRH6-WHNXV-R9WG3-9XRFY-MY832",
  "vmids": [179, 180]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `productKey` | string | Volume license key (blank = auto-detect from Windows version) |
| `vmids` | int[] | VMIDs to license |

**Response 200:**
```json
{
  "success": [179],
  "errors": [{"item": "180", "reason": "Failed to run license-windows ansible playbook: ..."}]
}
```

**Responses:**
- `200` - Success/error arrays
- `500` - Internal error

---

## Anti-Sandbox Management

Actions to manage the Anti-Sandbox plugin. **Enterprise only.**

### POST /antisandbox/enable - Enable anti-sandbox

Modifies VM(s) to not look like virtualized sandbox hosts. **Enterprise and Windows only.**

**Query Parameters:**
| Name | Required | Description |
|------|----------|-------------|
| `userID` | No | Target user ID |

**Request Body:**
```json
{
  "vmIDs": "104,105",
  "registeredOwner": "Acme Corp IT",
  "registeredOrganization": "Acme Corp",
  "vendor": "Dell",
  "dropFiles": true,
  "processorName": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
  "processorVendor": "GenuineIntel",
  "processorSpeed": 2600,
  "processorIdentifier": "Intel64 Family 6 Model 142 Stepping 10",
  "systemBiosVersion": "1.18.0",
  "persist": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `vmIDs` | string | Comma-separated VM IDs or names |
| `registeredOwner` | string | RegisteredOwner registry value |
| `registeredOrganization` | string | RegisteredOrganization registry value |
| `vendor` | string | Hardware vendor (currently only `"Dell"`) |
| `dropFiles` | boolean | Drop random files on desktop/downloads |
| `processorName` | string | ProcessorNameString value |
| `processorVendor` | string | VendorIdentifier (e.g. `GenuineIntel`, `AuthenticAMD`) |
| `processorSpeed` | integer | CPU speed in MHz |
| `processorIdentifier` | string | Processor Identifier string |
| `systemBiosVersion` | string | SystemBiosVersion value |
| `persist` | boolean | Persist BIOS/CPU changes via scheduled task |

**Response 200:**
```json
{
  "success": [104],
  "errors": [{"item": 105, "reason": "Failed to get VM state no status found"}]
}
```

**Responses:**
- `200` - Success/error arrays
- `500` - Error

---

### POST /antisandbox/install-custom - Install custom QEMU/OVMF

Installs modified QEMU and OVMF packages that present as Dell hardware.

**Responses:**
- `200` - `{"result": "Anti-Sandbox QEMU and OVMF installed - will take effect on VM's next power cycle"}`
- `500` - Error

---

### POST /antisandbox/install-standard - Install standard QEMU/OVMF

Installs the standard (unmodified) QEMU and OVMF packages.

**Responses:**
- `200` - `{"result": "Standard QEMU and OVMF installed - will take effect on VM's next power cycle"}`
- `500` - Error
