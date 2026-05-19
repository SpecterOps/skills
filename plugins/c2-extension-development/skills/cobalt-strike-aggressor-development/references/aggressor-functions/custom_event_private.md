custom_event_private

Send a custom event to one specific Cobalt Strike client.

#### Arguments

`$1` - who to send the custom event to

`$2` - the topic name

`$3` - the event data

#### Example

```
custom_event_private("neo", "my-topic", 42);```
