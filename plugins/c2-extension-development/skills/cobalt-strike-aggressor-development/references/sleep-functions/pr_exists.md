# pr_exists

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/pr_exists.html

---

## Synopsis

```sleep
-exists "file"
```

A predicate to check if a file exists

## Parameters

`"file"` - the file to check.

## Returns

True or false and this operator is only usable in a comparison context.

## Examples

**Example:**
```sleep
if (-exists "/var/www/secret_files")
{
`tar zvf my_secrets_now.tgz`;
}

```

## See Also

[-isDir](pr_isDir.md); [-isFile](pr_isFile.md); [-isHidden](pr_isHidden.md); [&lof](lof.md)
