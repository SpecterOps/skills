# connect

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/connect.html

---

## Synopsis

```sleep
$ connect("host", port, [timeout], [&closure], [option => value, ...])
```

connects to the specified host:port and returns a $handle. Check for issues connecting to a host with checkError(). If &closure is specified, this call will not block. &closure will be called when a connection is established.

## Parameters

`"host"` - the hostname or IP address to connect to

`port` - the port number to connect to

`timeout` - the desired timeout (in milliseconds), 0 specifies an indefinite timeout, default is 60 seconds

`&closure` - if a closure is specified, this function will not block, instead when the connection is established, &closure will be called.
When called, the closure receives the following arguments:

ArgumentDescription
$1a $handle for the connected socket

`option => value` - various socket options.

`linger => n` - the value of SO_LONGER (how long (in milliseconds) the socket waits for a TCP reset before closing)

`lport => n` - the local port to bind to

`laddr => "127.0.0.1"` - the local address to bind to

## Returns

A $handle to a socket. This handle can be read from and written to using Sleep's IO functions.

## Errors

- This function does flag errors that can be caught using [&checkError](checkError.md). I just need to document them.

## Examples

**Example:**
```sleep
$handle = connect(@ARGV[0], 31337);

println($handle, "hello echo server");

$text = readln($handle);
println("Read: $text");
	
closef($handle);

```

**Output:**
```
$ java -jar sleep.jar echocl.sl 127.0.0.1
Read: PONG! hello echo server

```

## See Also

[&allocate](allocate.md); [&exec](exec.md); [&fork](fork.md); [&getConsole](getConsole.md); [&listen](listen.md); [&openf](openf.md); [&setEncoding](setEncoding.md)
