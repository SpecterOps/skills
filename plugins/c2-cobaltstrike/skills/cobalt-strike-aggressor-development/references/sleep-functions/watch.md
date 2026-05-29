# watch

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/watch.html

---

## Synopsis

```sleep
watch('$var @ar')
```

Declares all ovariables in the string as "watch" variables. Any attempt to set a value in a watched container will print out a warning. The warning does not prevent the setting of the variable. The value will change as normal.

## Parameters

`'$var @ar'` - a string containing a space separated list of variables to watch. These vars must already exist.

## Side Effects / Notes

- Takes all of the specified scalars and turns them into watch scalars. One limitation of this function is that it can only watch individual scalars, it is not capable of watching array/hash elements.

## Errors

- The function might complain if you try to watch a variable that doesn't exist yet.

## Examples

**Example:**
```sleep
sub test
{
$1 = "bar";
}

$fluffy = "foo";
watch('$fluffy');

test($fluffy);

println("The value of \$fluffy is $fluffy");

```

**Output:**
```
Warning: watch(): $fluffy = 'bar' at fluffy2.sl:3
The value of $fluffy is bar

```

## See Also

[&checkError](checkError.md); [&debug](debug.md); [&getStackTrace](getStackTrace.md); [&profile](profile.md); [&taint](taint.md); [&warn](warn.md)
