openFileBrowser

Open the file browser for a Beacon

#### Arguments

`$1` - the Beacon ID to apply this feature to

#### Example

```
item "Browse Files" {
   local('$bid');
   foreach $bid ($1) {
      openFileBrowser($bid);
   }
}```

