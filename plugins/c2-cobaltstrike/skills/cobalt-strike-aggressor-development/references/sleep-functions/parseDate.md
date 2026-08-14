# parseDate

**Category:** DateTime

**Source:** https://sleep.dashnine.org/manual/parseDate.html

---

## Synopsis

```sleep
$ parseDate('format', "date string")
```

parses the specified date string into a scalar long.

## Parameters

`format` - the date/time format.

- 2.1 Scalars: Time and Date Values - summary of the date/time format

`"date string"` - a string that follows the specified format

## Returns

returns a scalar long containing the number of milliseconds since the epoch represented by the specified date string.

## Examples

**Example:**
```sleep
# lets do a little 'date' arithmetic

$event = "14/Oct/2006:12:24:00 -0500";
$a = parseDate('dd/MMM/yyyy:kk:mm:ss Z', $event);

$now = "2006.10.14 at 13:40:00 EDT";
$b = parseDate("yyyy.MM.dd 'at' HH:mm:ss z", $now);

# keep in mind we are dealing with milliseconds
# i.e. 60 * 1000 = 1 minute
$diff = $b - $a;
println("event occured " . ($diff / 60000) . " minutes ago");

# subtract the difference from our "now" value
$when = $b - $diff;

println("event occured " . formatDate($when, "yyyy.MM.dd 'at' HH:mm:ss z"));

```

**Output:**
```
event occured 16 minutes ago
event occured 2006.10.14 at 13:24:00 EDT

```

## See Also

[&formatDate](formatDate.md); [&ticks](ticks.md)
