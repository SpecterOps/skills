prompt_file_save

Show a file save dialog.

#### Arguments

`$1` - default value

`$2` - a callback function. Called when the user chooses a filename. The argument to the callback is the desired file.

#### Example

```
prompt_file_save($null, {
   local('$handle');
   $handle = openf("> $+ $1");
   println($handle, "I am content");
   closef($handle);
});```
