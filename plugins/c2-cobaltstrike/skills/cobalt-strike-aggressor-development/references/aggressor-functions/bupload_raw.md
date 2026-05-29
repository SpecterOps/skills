bupload_raw

Ask a Beacon to upload a file

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the remote file name of the file

`$3` - the raw content of the file

`$4` - (optional) the local path to the file (if there is one)

#### Example

```
$data = artifact("my-listener", "exe");
bupload_raw($1, "\\\\DC\\C$\\foo.exe", $data);```
