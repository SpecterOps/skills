# inline

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/inline.html

---

## Synopsis

```sleep
inline(&closure)
```

Dynamically invokes the specified closure as if it was an inline function occuring within the local scope.

## Parameters

`&closure` - the closure to invoke.

## Side Effects / Notes

- When a closure is invoked inline its $this scope and local variables all come from the calling function.

## Examples

**Example:**
```sleep
inline form
{
println('<form action="'.$1.'">');
inline($2);
println(' <input type="submit" value="Submit to '.$title.'">');
println('</form>');
}

inline select
{
println(' <select name="'.$1.'">');
foreach $item ($2)
{
println(' <option>'.$item.'</option>');
}
println(' </select>');
}

sub buildPage
{
local('$title');
$title = "My Website!!";

form("favorites",
{
println('<br>Colors? ');
select('colors', @("#FF0000", "#00FF00", "#0000FF"));
});
}

buildPage();

```

**Output:**
```
<form action="favorites">
<br>Colors?
<select name="colors">
<option>#FF0000</option>
<option>#00FF00</option>
<option>#0000FF</option>
</select>
<input type="submit" value="Submit to My Website!!">
</form>

```

## See Also

[&function](function.md); [&invoke](invoke.md); [&setf](setf.md)
