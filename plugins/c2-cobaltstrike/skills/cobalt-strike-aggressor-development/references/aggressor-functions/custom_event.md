custom_event

Broadcast a custom event to all Cobalt Strike clients.

#### Arguments

`$1` - the topic name

`$2` - the event data

#### Example

```
custom_event("my-topic", %(foo => 42, bar => "hello"));```
