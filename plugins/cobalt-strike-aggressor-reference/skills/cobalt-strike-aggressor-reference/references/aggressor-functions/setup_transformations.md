setup_transformations

Apply the transformations rules defined in the Malleable C2 profile to the beacon payload.

#### Arguments

`$1` – Beacon payload to modify

`$2` – Beacon architecture (x86/x64)

#### Returns

The updated beacon payload with the transformations applied to the payload.

#### Example

See BEACON_RDLL_GENERATE hook

```
# Apply the transformations to the beacon payload.
$temp_dll = setup_transformations($temp_dll, $arch);```

