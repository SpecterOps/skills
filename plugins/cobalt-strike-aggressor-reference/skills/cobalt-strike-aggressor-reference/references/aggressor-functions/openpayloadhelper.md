openPayloadHelper

Open a payload chooser dialog.

#### Arguments

`$1` - a callback function. Arguments: $1 - the selected listener.

#### Example

```
openPayloadHelper(lambda({
   bspawn($bid, $1);
}, $bid => $1));```

