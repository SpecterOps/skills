bexit

Ask a Beacon to exit.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

#### Example

```
item "&Die" {
   binput($1, "exit");
   bexit($1);
}    ```
