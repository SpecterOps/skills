extract_reflective_loader

DEPRECATED**This hook is no longer needed as the stomp loader style reflective loader is no longer supported.**

Extract the executable code for a reflective loader from a Beacon Object File (BOF).

#### Arguments

`$1` - Beacon Object File data that contains a reflective loader.

#### Returns

The Reflective Loader binary executable code extracted from the Beacon Object File data.

#### Example

See BEACON_RDLL_GENERATE hook

```
# ---------------------------------------------------------------------
# extract loader from BOF.
# ---------------------------------------------------------------------
$loader = extract_reflective_loader($data);```

