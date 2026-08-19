# Checking for Errors

Cobalt Strike’s Linux package includes a c2lint program. This program will check the syntax of a communication profile, apply a few extra checks, and even unit test your profile with random data. It’s highly recommended that you check your profiles with this tool before you load them into Cobalt Strike.

`./c2lint [/path/to/my.profile]`

c2lint returns and logs the following result codes for the specified profile file:

- A result of 0 is returned if c2lint completes with no errors
- A result of 1 is returned if c2lint completes with only warnings
- A result of 2 is returned if c2lint completes with only errors
- A result of 3 is returned if c2lint completes with both errors and warnings.

The last lines of the c2lint output display a count of detected errors and warnings. No message is displayed if none are found. There can be more error messages displayed in the output than the count represents because a single error may produce more than 1 error message. This is the same possibility for warnings however less likely. For example:

- [!] Detected 1 warning.
- [-] Detected 3 errors.
