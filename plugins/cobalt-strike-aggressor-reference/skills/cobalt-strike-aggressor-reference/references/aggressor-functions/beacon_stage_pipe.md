beacon_stage_pipe

This function handles the staging process for a bind pipe stager. This is an optional stager for lateral movement. You can stage any x86 payload/listener through this stager. Use &stager_bind_pipe to generate this stager.

#### Arguments

`$1` - the id of the beacon to stage through

`$2` - the target host

`$3` - the listener name

`$4` - the architecture of the payload to stage. x86 is the only option right now.

#### Example

```
# step 1. generate our stager
$stager = stager_bind_pipe("my-listener");

# step 2. do something to run our stager

# step 3. stage a payload via this stager
beacon_stage_pipe($bid, $target, "my-listener", "x86");

# step 4. assume control of the payload (if needed)
beacon_link($bid, $target, "my-listener");```

