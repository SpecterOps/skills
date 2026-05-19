data_keys

List the query-able keys from Cobalt Strike's data model

#### Returns

A list of keys that you may query with &data_query

#### Example

```
foreach $key (data_keys()) {
   println("\n\c4=== $key ===\n");
   println(data_query($key));
}```

