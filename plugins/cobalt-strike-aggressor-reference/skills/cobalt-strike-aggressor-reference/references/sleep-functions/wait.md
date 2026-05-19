# wait

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/wait.html

---

## Synopsis

```sleep
$ wait($handle, [timeout])
```

Blocks and waits for the callback, process, or fork associated with $handle to finish. if $handle is a fork, the return value of the fork will be returned by &wait. if $handle is a process, the return value of the process will be returned by &wait. If the specified timeout is reached $null will be returned.

## Parameters

`$handle` - the handle to wait for.

`timeout` - the number of milliseconds to wait for. default is 0 which means to wait forever.

## Returns

The data returned depends on the type of the handle. If the handle is a [&fork](fork.md) then the return value of the fork is used. If the handle is a process opened with [&exec](exec.md) then the exit value of the process is used. If the timeout is reached then $null is returned.

## Examples

**Example:**
```sleep
sub factorial
{
sub calculateFactorial
{
return iff($1 == 0, 1, $1 * calculateFactorial($1 - 1));
}

$result = calculateFactorial($value);
println("fact( $+ $value $+ ) is ready");
return $result;
}

$fact12 = fork(&factorial, $value => 120.0);
$fact11 = fork(&factorial, $value => 110.0);
$fact10 = fork(&factorial, $value => 100.0);

println("fact(120) = " . wait($fact12));
println("fact(110) = " . wait($fact11));
println("fact(100) = " . wait($fact10));

```

**Output:**
```
fact(120.0) is ready
fact(110.0) is ready
fact(100.0) is ready
fact(120) = 6.689502913449124E198
fact(110) = 1.5882455415227421E178
fact(100) = 9.33262154439441E157

```

## See Also

[&available](available.md); [&closef](closef.md); [&consume](consume.md); [&mark](mark.md); [&printEOF](printEOF.md); [&reset](reset.md); [&setEncoding](setEncoding.md); [&skip](skip.md)
