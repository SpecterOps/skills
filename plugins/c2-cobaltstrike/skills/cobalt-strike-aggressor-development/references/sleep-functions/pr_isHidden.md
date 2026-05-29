# pr_isHidden

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/pr_isHidden.html

---

## Synopsis

```sleep
-isHidden "file"
```

A predicate to check if a file is hidden

## Parameters

`"file"` - the file to check.

## Returns

True or false and this operator is only usable in a comparison context.

## Examples

**Example:**
```sleep
foreach $user_dir (ls("/Users/"))
{
$file = getFileProper($user_dir, ".porn");
if (-exists $file && -isHidden $file)
{
$user = matches($user_dir, '/Users/(.*)')[0];
println("User $user is trying to hide porn!");
}
}

```

**Output:**
```
User parsoff is trying to hide porn!

```

## See Also

[-exists](pr_exists.md); [-isDir](pr_isDir.md); [-isFile](pr_isFile.md); [&lof](lof.md)
