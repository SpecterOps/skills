# fork

**Category:** InputOutput

**Source:** https://sleep.dashnine.org/manual/fork.html

---

## Synopsis

```sleep
$ fork(&closure, [$key => $value, ...])
```

Creates a new thread, a new script environment, and executes the specified &closure. The returned $handle acts as a pipe betweeen the thread and the new script environment. Within the script environment $source is available to act as an outward pipe.

## Parameters

`&closure` - the closure to execute. the this scope and everything else is dropped. only the closure block itself is executed. A variable named $source is installed into the new script environment to act as the other end of the pipe the returned handle is attached to.

`$key => $value` - installs the right hand side $value into the new script environment as $key. it is important that shared hashes/arrays/objects are synchronized using [&acquire](acquire.md) and [&release](release.md).

`...` - as many $key => $value pairs as you like may be specified.

## Returns

A $handle that acts as a pipe between the new script environment and the current script environment.

## Side Effects / Notes

- This function creates a new thread and executes the passed in closure.

- $source is available within the script environment containing &closure. Data written to $source can be read from the returned $handle. Data written to $handle can be read through $source.

## Errors

- This function does flag errors that can be caught using [&checkError](checkError.md). I just need to document them.

## Examples

**Example:**
```sleep
sub child
{
$calculation = readln($source);
println("Received $calculation");
$result = expr($calculation);
return $result;
}

$pipe = fork(&child);
println($pipe, "45 * 99");

$value = wait($pipe);
println("Result is: $value");

```

**Output:**
```
Received 45 * 99
Result is: 4455

```

## See Also

[&acquire](acquire.md); [&release](release.md); [&semaphore](semaphore.md)
