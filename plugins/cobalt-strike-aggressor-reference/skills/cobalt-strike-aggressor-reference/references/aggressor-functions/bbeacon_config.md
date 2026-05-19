bbeacon_config

Use this script function with the **host** command to view and update beacon status and configuration . Use the **failover_notification** command to control beacon failover notifications

### Failover_Notification Command

Use this command to retrieve the current notification setting from a beacon [HTTP|DNS]. Use the [true|false] arguments to enable/disable notifications from a beacon [HTTP|DNS] when host rotation occurs from failover events.

bbeacon_config failover_notification [true | false]

#### Example

```
$beacon_id = $1;
bbeacon_config($beacon_id, "failover_notification");
bbeacon_config($beacon_id, "failover_notification", "true");
bbeacon_config($beacon_id, "failover_notification", "false");```

### Host Command

Use this command to view and update beacon status and configuration of the beacons callback host list.

bbeacon_config [host] [action] [arguments]

where Action and Arguments can be:

| Description | Arguments |  |
| --- | --- | --- |
| Add a host/uri to the beacons callback host list. The uri must be known by the server. A maximum of 32 hosts may be defined. Multiple hosts and uris can be used by way of a comma-separated list. | [hostname] [uri] |  |
| Retrieve host callback information from a beacon. |  |  |
| Hold a host in the callback host list [Random and Round-Robin rotation only]. Multiple hosts can be used by way of a comma-separated list. | [hostname] |  |
| List the host profiles available in the beacon config. |  |  |
| Release a host in the callback host list [Random and Round-Robin rotation only]. Multiple hosts can be used by way of a comma-separated list. | [hostname] |  |
| Remove a host from the beacons callback host list. Multiple hosts can be used by way of a comma-separated list. | [hostname] |  |
| Reset the status and/or statistics for callback hosts. | [all|status|statistics] [hostname] |  |
| Change the host/uri of an existing host/uri in the host list. The uri must be known by the server. Multiple hosts and uris can be used by way of a comma-separated list. | [original-hostname] [new-hostname] [new-uri] |  |

#### Examples

**Add a host to host list**

```
$beacon_id = $1;
bbeacon_config($beacon_id, "host", "add", [hostname], [uri]);
bbeacon_config($beacon_id, "host", "add", [hostname1,hostname2], [uri1,uri2]);
```

**Remove a host**

```
$beacon_id = $1;
bbeacon_config($beacon_id, "host", "remove", [hostname]);
bbeacon_config($beacon_id, "host", "remove", [hostname1,hostname2]);
```

**Change a host name**

```
$beacon_id = $1;
bbeacon_config($beacon_id, "host", "update", [original-hostname], [new-hostname]);
bbeacon_config($beacon_id, "host", "update", [original-hostname1,original-hostname2], [new-hostname1,new-hostname2]);
bbeacon_config($beacon_id, "host", "update", [original-hostname], [new-hostname], [new-uri]);
bbeacon_config($beacon_id, "host", "update", [original-hostname1,original-hostname2], [new-hostname1,new-hostname2], [new-uri1,new-uri2]);```

**List defined host profile host names**

```
$beacon_id = $1;
bbeacon_config($beacon_id, "host", "profiles");```

**Retrieve host callback information**

```
$beacon_id = $1;
bbeacon_config($beacon_id, "host", "info");```

**Reset status/statistics**

```
$beacon_id = $1;
bbeacon_config($beacon_id, "host", "reset", "[all|status|statistics]");
bbeacon_config($beacon_id, "host", "reset", "[all|status|statistics]", [hostname]);
bbeacon_config($beacon_id, "host", "reset", "[all|status|statistics]", [hostname1,hostname2]);
```

NOTE: **Resetting status will reset**:

- Host held setting



**Resetting statistics will reset**:

- Last successful connection timestamp

- Last failed connection timestamp

- Successful connection count

- Failed connection count

