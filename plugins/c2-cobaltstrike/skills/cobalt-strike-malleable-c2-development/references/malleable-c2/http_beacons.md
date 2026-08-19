# HTTP Beacons

Allows you to specify general attributes for the http(s) beacons.

The default beacon library can subsequently be overridden on UI Dialogs and Aggressor Commands that generate beacons as needed.

```
http-beacon {
    set library "winhttp";
    set data_required "false";'
}

http-beacon "variant-x" {
    set library "wininet";
}
```

The settings are:

| Option               | Default Value                                           | Description                                                                                                                                                                                                                                                                                                                               |
| -------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| library              | wininet                                                 | Allows user to specify the default library used by the generated beacons used by the profile.<br><br>The library defaults to `"wininet"`, which is the only type of beacon prior to version 4.9. The library value can be `"wininet"` or `"winhttp"`.                                                                                     |
| data_required        | false                                                   | Set to send data in all beacon check-in/callbacks. The Team Server will expect data in valid communication. This helps determine the configurations that return response code 200 (OK) without data and appear to be valid `"nothing to do"` beacon responses when they are not.<br><br>Valid values are `[true \| false]`.               |
| data_required_length | 0 (a small header will be sent with no additional data) | Specify how much data will be included in `"nothing to do"` responses.<br><br>Valid values are:<br>**number** - A fixed length number [1 through 2048].<br>**min-max** - A range of lengths to randomly use [1-2048].<br>**R[number]** - Random length up to the number [max 2048].<br>**F[number]** - fixed length of number [max 2048]. |
