# putAll

**Category:** Arrays

**Source:** https://sleep.dashnine.org/manual/putAll.html

---

## Synopsis

```sleep
% putAll(%hash, @|&keys, @|&values)
```

Populates the hash with data obtained from iterating over the key and value sources simultaneously.

```sleep
% putAll(%hash, @|&source)
```

Populates the hash with data obtained from iterating over the specified source for key and value valuies.

```sleep
@ putAll(@array, @|&source)
```

Puts all elements obtained from iterating over the specified source into the array.

## Parameters

`@|&keys` - an iterator source containing keys to populate the hash with.

`@|&values` - an iterator source containing values to populate the hash with.

`@|&source` - an iterator source iterated over using a value and its neighor as a key, value pair to populate the hash with.

## Returns

The specified hash (or array) with copies of the new data.

## Side Effects / Notes

- New values are placed into the hash or array.

## Examples

**Example:**
```sleep
# get list of file names
@files = `ls -1`;

# get file permissions from ls output
@perms = map({ return split(' ', $1)[0]; }, sublist(`ls -1l`, 1));

# create a hash with all of this information.
%permissions = putAll(ohash(), @files, @perms);

println(%permissions);

```

**Output:**
```
$ java -jar sleep.jar ../putAll.sl
%(Untitled.graffle => '-rw-r--r--', binary.graffle => '-rw-r--r--',
invoke.graffle => '-rw-r--r--', parsetree.graffle => '-rw-r--r--',
thisscope.graffle => '-rw-r--r--')

```
