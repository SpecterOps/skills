# formatDate

**Category:** DateTime

**Source:** https://sleep.dashnine.org/manual/formatDate.html

---

## Synopsis

```sleep
$ formatDate([date], 'format')
```

formats the specified date as a string with the specified format.

## Parameters

`date` - a scalar long representing the number of milliseconds since the epoch. defaults to the current date/time if not specified.

`format` - the date/time format.

- [2.1 Scalars: Time and Date Values](fundamentals.md#datetime) - summary of the date/time format

## Returns

returns the specified date parameter formatted as a string.

## Examples

**Example:**
```sleep
# show the current time...

println("The current time is: " . formatDate("yyyy.MM.dd 'at' HH:mm:ss z"));

# show the time 3 hours ago...

$time = ticks() - (1000 * 60 * 60 * 3);
println("The time was: " . formatDate($time, "yyyy.MM.dd 'at' HH:mm:ss z"));

```

**Output:**
```
The current time is: 2009.04.29 at 17:09:47 EDT
The time was: 2009.04.29 at 14:09:47 EDT

```

## See Also

[&parseDate](parseDate.md); [&ticks](ticks.md)
