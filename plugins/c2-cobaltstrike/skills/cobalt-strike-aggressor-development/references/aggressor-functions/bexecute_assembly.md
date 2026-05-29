bexecute_assembly

Spawns a local .NET executable assembly as a Beacon post-exploitation job.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the local path to the .NET executable assembly

`$3` - parameters to pass to the assembly

`$4` - (optional) the "PATCHES:" argument can modify functions in memory for the process. Up to 4 "patch-rule" rules can be specified (space delimited).

`$5` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

**"patch-rule" syntax (comma delimited):**` [library],[function],[offset],[hex-patch-value]`

**library **- 1-260 characters
**function **- 1-256 characters
**offset **- 0-65535 (The offset from the start of the executable function)
**hex-patch-value** - 2-200 hex characters (0-9,A-F). Length must be even number (hex pairs).

#### Notes

- This command accepts a valid .NET executable and calls its entry point.
- This post-exploitation job inherits Beacon's thread token.
- Compile your custom .NET programs with a .NET 3.5 compiler for compatibility with systems that don't have .NET 4.0 and later.

#### Example

```
alias myutil {
   bexecute_assembly($1, script_resource("myutil.exe"), "arg1 arg2 \"arg 3\"");
}```
