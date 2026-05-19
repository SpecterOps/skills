# Snapshots

Ludus provides snapshot functionality for VMs in your range. Snapshots allow you to save the state of a VM at a point in time and revert back to it later.

This functionality is also exposed in the Proxmox web UI. These Ludus commands are for convenience.

## Commands

### List Snapshots

The `list` command displays all snapshots for VMs in your range in a hierarchical tree format.

```bash
ludus snapshots list
```

This will show all snapshots for all VMs in your range, organized by VM and displaying the snapshot hierarchy.

Example output:
```
VM 104 (win10-client)
+-- pre-malware 2025-04-12 12:34:56 (Clean system before malware installation) [includes RAM]
    +-- post-malware 2025-04-12 14:23:45 (After malware installation)
        +-- current  (You are here!)

VM 105 (ubuntu-server)
+-- initial-setup 2025-04-12 09:12:34 (Fresh installation) [includes RAM]
    +-- configured 2025-04-12 11:45:23 (After service configuration)
        +-- current  (You are here!)
```

#### Options

You can filter the list to show snapshots for specific VMs:

```bash
ludus snapshots list --vmids 104,105
# or using the short flag
ludus snapshots list -n 104,105
```

### Create Snapshots

The `create` command (alias: `take`) creates a new snapshot for one or more VMs.

```bash
ludus snapshots create <snapshot-name>
```

By default, this creates a snapshot with RAM for all VMs in your range.

Example:
```bash
ludus snapshots create pre-attack
```

#### Options

You can specify which VMs to snapshot:

```bash
ludus snapshots create pre-attack --vmids 104,105
# or using the short flag
ludus snapshots create pre-attack -n 104,105
```

Add a description to your snapshot:

```bash
ludus snapshots create pre-attack --description "Clean system before attack simulation"
# or using the short flag
ludus snapshots create pre-attack -d "Clean system before attack simulation"
```

Create a snapshot without RAM (which saves space and is faster but upon revert your VM(s) will be powered off):

```bash
ludus snapshots create pre-attack --noRAM
# or using the short flag
ludus snapshots create pre-attack -r
```

### Revert to Snapshots

The `revert` command (alias: `rollback`) reverts VMs to a previous snapshot state.

```bash
ludus snapshots revert <snapshot-name>
```

Example:
```bash
ludus snapshots revert pre-attack
```

By default, this reverts all VMs in your range.

#### Options

You can specify which VMs to revert:

```bash
ludus snapshots revert pre-attack --vmids 104,105
# or using the short flag
ludus snapshots revert pre-attack -n 104,105
```

### Remove Snapshots

The `rm` command (aliases: `delete`, `remove`) deletes a snapshot from one or more VMs.

```bash
ludus snapshots rm <snapshot-name>
```

Example to remove a snapshot from specific VMs:
```bash
ludus snapshots rm old-snapshot --vmids 104,105
# or using the short flag
ludus snapshots rm old-snapshot -n 104,105
```

Example to remove a snapshot from all VMs in the range:
```bash
ludus snapshots rm old-snapshot
```

## Notes

- If you revert to a snapshot that does not include RAM (taken with `-r` or `--noRAM`), the VM will be powered off
- When ZFS storage is used for VMs, [snapshots must be reverted in the order they were taken](https://forum.proxmox.com/threads/cannt-get-snapshot-branches-task-error-cant-rollback-____-is-not-most-recent-snapshot.81416/). Directory (default) and LVM-thin storage types do not have this limitation and users can create "branching" snapshots.
- Testing mode uses the snapshot name `ludus_automated_clean_snapshot`. If you remove this snapshot while in testing mode, you will not be able to stop testing. Ludus does not prevent you from creating or modifying a snapshot with this name.
