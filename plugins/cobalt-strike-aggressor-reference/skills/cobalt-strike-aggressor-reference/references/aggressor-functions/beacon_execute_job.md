beacon_execute_job

Run a command and report its output to the user. 

#### Arguments

`$1` - the Beacon ID

`$2` - the command to run (environment variables are resolved)

`$3` - the command arguments (environment variables are not resolved).

`$4` - flags that change how the job is launched (e.g., 1 = disable WOW64 file system redirection)

#### Notes

- The string $2 and $3 are combined as-is into a command line. Make sure you begin $3 with a space!
- This is the mechanism Cobalt Strike uses for its shell and powershell commands.

#### Example

```
alias shell {
   local('$args');
   $args = substr($0, 6);
   btask($1, "Tasked beacon to run: $args", "T1059");
   beacon_execute_job($1, "%COMSPEC%", " /C $args", 0);
}```

