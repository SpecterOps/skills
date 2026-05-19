# ls

**Category:** FileSystem

**Source:** https://sleep.dashnine.org/manual/ls.html

---

## Synopsis

```sleep
@ ls("path")
```

Lists all of the files/directories within the specified path.

## Parameters

`"path"` - the path to list files/directories from.

## Returns

An array of strings with the full paths of all of the files/directories within the specified path.

## Examples

**Example:**
```sleep
# print out a directory listing.

@files = ls('/Users/raffi/sleepdev/dist/sleep');
printAll(@files);

```

**Output:**
```
/Users/raffi/sleepdev/dist/sleep/bin
/Users/raffi/sleepdev/dist/sleep/build.xml
/Users/raffi/sleepdev/dist/sleep/docs
/Users/raffi/sleepdev/dist/sleep/license.txt
/Users/raffi/sleepdev/dist/sleep/readme.txt
/Users/raffi/sleepdev/dist/sleep/sleep.jar
/Users/raffi/sleepdev/dist/sleep/src
/Users/raffi/sleepdev/dist/sleep/tests
/Users/raffi/sleepdev/dist/sleep/whatsnew.txt

```

## See Also

[-isDir](pr_isDir.md); [&listRoots](listRoots.md); [&mkdir](mkdir.md)
