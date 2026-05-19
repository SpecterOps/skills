iprange

Generate an array of IPv4 addresses based on a string description

#### Arguments

`$1` - a string with a description of IPv4 ranges

| Result |  |
| --- | --- |
| The IP4 address 192.168.1.2 |  |
| The IPv4 addresses 192.168.1.1 and 192.168.1.2 |  |
| The IPv4 addresses 192.168.1.0 through 192.168.1.255 |  |
| The IPv4 addresses 192.168.1.18 through 192.168.1.29 |  |
| The IPv4 addresses 192.168.1.18 through 192.168.1.29 |  |

#### Returns

An array of IPv4 addresses within the specified ranges.

#### Example

```
printAll(iprange("192.168.1.0/25"));```
