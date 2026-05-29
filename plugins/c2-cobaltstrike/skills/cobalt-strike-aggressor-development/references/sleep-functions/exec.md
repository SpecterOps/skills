# exec

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/exec.html

---

## Synopsis

```sleep
$ exec("command", [%env], ["directory"])
```

executes the specified command and returns a $handle.

```sleep
$ exec(@command, [%env], ["directory"])
```

executes the first element of the command array and returns a $handle. this form of exec is useful for passing arguments that have whitespace in them.

## Parameters

`"command"` - the comamnd to execute. this string is split apart by whitespace. the first token represents the command. the rest of the string is split by whitespace and passed as arguments.

`@command` - an array containing the command to execute as element 0. The rest of the array is passed as the argument array for the command.

`%env` - a scalar hash specifying the environment for the executed command. (default is $null which uses the default environment).

`"directory"` - the directory to execute the command from. default is the current working directory.

## Returns

A $handle to stdin/stdout for the executed process. This handle can be read from and written to using Sleep's IO functions.

## Errors

- This function does flag errors that can be caught using [&checkError](checkError.md). I just need to document them.

## Examples

**Example:**
```sleep
$process = exec("ls -al");
@data = readAll($process);
closef($process);

```

## See Also

[&allocate](allocate.md); [&connect](connect.md); [&fork](fork.md); [&getConsole](getConsole.md); [&listen](listen.md); [&openf](openf.md); [&setEncoding](setEncoding.md)
