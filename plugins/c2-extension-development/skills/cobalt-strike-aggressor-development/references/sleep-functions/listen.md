# listen

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/listen.html

---

## Synopsis

```sleep
$ listen(port, [timeout], [$host], [&closure], [option => value, ...])
```

Instantiates a server socket to listen for TCP/IP connections on the specified port and accepts a connection.

## Parameters

`port` - the port number to listen on

`timeout` - the number of milliseconds to wait for a connection before returning $null

`$host` - a variable to place the hostname of the connecting host into.

`&closure` - if &closure is specified, this function call will not block. &closure will be called when a connection is established.
When called, the closure receives the following arguments:

ArgumentDescription
$1a $handle for the connected socket

`option => value` - various socket options that can be set:

`linger => n` - the value of SO_LONGER (how long (in milliseconds) the socket waits for a TCP reset before closing)

`lport => n` - the local port to bind to

`laddr => "127.0.0.1"` - the local address to bind to

`backlog => n` - the number of connections to queue while waiting for a subsequent call of [&listen](listen.md) to accept a connection.

## Returns

A $handle to a TCP/IP socket. This handle can be read from and written to using Sleep's IO functions.

## Side Effects / Notes

- The variable passed in to contain the hostname is altered. Otherwise this function has no side effects on any of its other parameters.

- Not really a side effect but the first time listen is called for a specific port a server socket listening on that port is created in the background. Each subsequent call to listen references this same server socket. To force the current Sleep process to release this background listening socket use [&closef](closef.md).

## Errors

- This function does flag errors that can be caught using [&checkError](checkError.md). I just need to document them.

## Examples

**Example:**
```sleep
# A simple "Hello World" server

$socket = listen(5001);

if (checkError($error))
{
println("Error occured: $error");
}
else
{
println($socket, "Hello World!");
}

closef($socket);

```

**Output:**
```
$ telnet 127.0.0.1 5001
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Hello World!
Connection closed by foreign host.

```

## See Also

[&allocate](allocate.md); [&connect](connect.md); [&exec](exec.md); [&fork](fork.md); [&getConsole](getConsole.md); [&openf](openf.md); [&setEncoding](setEncoding.md)
