stager_bind_pipe

Returns a bind_pipe stager for a specific Cobalt Strike listener. This stager is suitable for use in lateral movement actions that benefit from a small named pipe stager. Stage with &beacon_stage_pipe.

#### Arguments

`$1` - the listener name

#### Returns

A scalar containing x86 bind_pipe shellcode.

#### Example

```
# step 1. generate our stager
$stager = stager_bind_pipe("my-listener");

# step 2. do something to run our stager

# step 3. stage a payload via this stager
beacon_stage_pipe($bid, $target, "my-listener", "x86");

# step 4. assume control of the payload (if needed)
beacon_link($bid, $target, "my-listener");```

See also&artifact_general
