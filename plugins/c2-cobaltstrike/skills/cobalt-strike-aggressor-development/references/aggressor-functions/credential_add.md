credential_add

Add a credential to the data model

#### Arguments

`$1` - username

`$2` - password

`$3` - realm

`$4` - source

`$5` - host

#### Example

```
command falsecreds {
   for ($x = 0; $x < 100; $x++) {
      credential_add("user $+ $x", "password $+ $x");
   }
}```
