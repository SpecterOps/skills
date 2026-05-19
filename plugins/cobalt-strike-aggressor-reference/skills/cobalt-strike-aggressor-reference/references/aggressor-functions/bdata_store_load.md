bdata_store_load

Load post-ex items to Beacon. This provides a mechanism to upload data and then query it via BOFs using APIs such as BeaconStoreGetItem().

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - item type [bof|dotnet|file]

`$3` - file path

`$4` - (optional) item name (If omitted, the file name is used).

#### Example

```
alias "data_store_load" {
    blog($1, "Loading data store...");
    bdata_store_load($1, "bof", "/home/someone/file.bof");
    bdata_store_load($1, "dotnet", "/home/someone/file.dotnet");
    bdata_store_load($1, "file", "/home/someone/file.data");
    blog($1, "Loaded data store...");
}
 
alias "data_store_load_with_name" {
    blog($1, "Loading data store with names...");
    bdata_store_load($1, "bof", "/home/someone/file.bof", "myBof");
    bdata_store_load($1, "dotnet", "/home/someone/file.dotnet", "myDotNet");
    bdata_store_load($1, "file", "/home/someone/file.data", "myData");
    blog($1, "Loaded data store with names...");
}```