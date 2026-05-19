bsyscall_method

Ask Beacon to change its syscall method.

#### Arguments

**$1** - the id for the beacon. This may be an array or a single ID.

**$2** - the syscall method. Supported methods are:

**None**: Use the standard Windows API function.**Direct**: Use the Nt* version of the function.

**Indirect**: Jump to the appropriate instruction within the Nt* version of the function.

NOTE: If the $2 argument is empty, Beacon is tasked to query the currently used syscall method.

#### Example

```
alias syscall_method {
   bsyscall_method($1, $2);
}```

