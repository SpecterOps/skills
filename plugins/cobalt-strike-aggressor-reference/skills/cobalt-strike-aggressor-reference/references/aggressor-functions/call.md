call

Issue a call to the team server.

#### Arguments

`$1` - the command name

`$2` - a callback to receive a response to this request. The callback will receive two arguments. The first is the call name. The second is the response.

`...` - one or more arguments to pass into this call.

#### Example

```
call("aggressor.ping", { warn(@_); }, "this is my value");```

