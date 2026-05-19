# Admin Notes

Administrative operations for Ludus server management.

## Promoting a user to admin

```
root@ludus:/opt/ludus# sqlite3 ludus.db
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
sqlite> UPDATE user_objects set is_admin = 1 WHERE user_id = '<USER ID>';
sqlite> .exit
root@ludus:/opt/ludus# pveum user modify {{ username }}@pam --groups ludus_admins --append
```

## Demoting a user from admin to regular user

```
root@ludus:/opt/ludus# sqlite3 ludus.db
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
sqlite> UPDATE user_objects set is_admin = 0 WHERE user_id = '<USER ID>';
sqlite> .exit
root@ludus:/opt/ludus# pveum user modify {{ username }}@pam --groups ludus_users
```

## Forcing a range out of testing mode

```
root@ludus:/opt/ludus# sqlite3 ludus.db
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
sqlite> UPDATE range_objects set testing_enabled = 0 WHERE range_number = <RANGE NUMBER>;
sqlite> UPDATE range_objects set allowed_domains = '' WHERE range_number = <RANGE NUMBER>;
sqlite> UPDATE range_objects set allowed_ips = '' WHERE range_number = <RANGE NUMBER>;
sqlite> .exit
```

## Get the total resources for a range config

```
yq '{"Total VMs": (.ludus.[] as $vm_item ireduce (0; . + 1)),"Total CPUs": (.ludus.[] as $vm_item ireduce (0; . + $vm_item.cpus)),"Total RAM (GB)": (.ludus.[] as $vm_item ireduce (0; . + $vm_item.ram_gb))}' range-config.yml
```
