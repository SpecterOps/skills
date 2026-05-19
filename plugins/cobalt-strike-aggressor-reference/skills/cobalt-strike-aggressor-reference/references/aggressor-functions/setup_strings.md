setup_strings

Apply the strings defined in the Malleable C2 profile to the beacon payload.

#### Arguments

`$1` – beacon payload to modify

#### Returns

The updated beacon payload with the defined strings applied to the payload.

#### Example

See BEACON_RDLL_GENERATE hook

```
# Apply strings to the beacon payload.
$temp_dll = setup_strings($temp_dll);```

