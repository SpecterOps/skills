setup_reflective_loader

DEPRECATED**This hook is no longer needed as the stomp loader style reflective loader is no longer supported.**

Insert the reflective loader executable code into a beacon payload.

#### Arguments

`$1` - Original beacon executable payload.

`$2` - User defined Reflective Loader executable data.

#### Returns

The beacon executable payload updated with the user defined reflective loader. $null if there is an error.

#### Notes

The user defined Reflective Loader must be less than 5k.

#### Example

See BEACON_RDLL_GENERATE hook

```
# ---------------------------------------------------------------------
# Replace the beacons default loader with '$loader'.
# ---------------------------------------------------------------------
$temp_dll = setup_reflective_loader($2, $loader);```
