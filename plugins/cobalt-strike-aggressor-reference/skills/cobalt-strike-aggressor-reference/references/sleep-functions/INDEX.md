# Sleep Programming Language Documentation Index

This directory contains split documentation for the Sleep programming language, organized for efficient LLM ingestion.

**Source:** https://sleep.dashnine.org/manual/

---

## Tutorial Documentation

### Core Concepts
- [intro.md](intro.md) - Introduction to Sleep, support resources, and acknowledgements
- [started.md](started.md) - Getting started with stand-alone scripts and the Sleep console  
- [fundamentals.md](fundamentals.md) - Scalars, scalar expressions, numbers, and strings
- [datastruct.md](datastruct.md) - Arrays, stacks, lists, sets, and hashes
- [flowcontrol.md](flowcontrol.md) - Comparisons, loops, exceptions, and assertions
- [functions.md](functions.md) - Subroutines, scalar scope, closures, and continuations
- [regex.md](regex.md) - Regular expression patterns and matching
- [hoes.md](hoes.md) - Java object integration and object expressions
- [io.md](io.md) - Input/Output handles, files, network, threads, and buffers
- [embed.md](embed.md) - Sleep integration, extending Sleep, and working with scalars

---

## Reference Documentation

### Arrays (30 functions)
Operations for manipulating array data structures.

- [add.md](add.md) - Add elements to an array or hash
- [addAll.md](addAll.md) - Add all elements from one array to another
- [cast.md](cast.md) - Cast an array to a specific Java array type
- [clear.md](clear.md) - Clear all elements from an array or hash
- [concat.md](concat.md) - Concatenate arrays
- [copy.md](copy.md) - Create a copy of an array or hash
- [filter.md](filter.md) - Filter array elements using a function
- [flatten.md](flatten.md) - Flatten a nested array structure
- [identity.md](identity.md) - Test scalar identity (=~)
- [in.md](in.md) - Test if element is in array or hash
- [map.md](map.md) - Map a function over array elements
- [pop.md](pop.md) - Remove and return last element
- [push.md](push.md) - Add element to end of array
- [putAll.md](putAll.md) - Put all key-value pairs into a hash
- [reduce.md](reduce.md) - Reduce array using a function
- [remove.md](remove.md) - Remove element from array or hash
- [removeAll.md](removeAll.md) - Remove multiple elements
- [removeAt.md](removeAt.md) - Remove element at specific index
- [retainAll.md](retainAll.md) - Retain only specified elements
- [reverse.md](reverse.md) - Reverse array order
- [search.md](search.md) - Search for element in array
- [shift.md](shift.md) - Remove and return first element
- [size.md](size.md) - Get size of array or hash
- [sort.md](sort.md) - Sort array with custom comparator
- [sorta.md](sorta.md) - Sort array alphabetically
- [sortd.md](sortd.md) - Sort array as doubles
- [sortn.md](sortn.md) - Sort array numerically
- [splice.md](splice.md) - Remove/replace elements in array
- [sublist.md](sublist.md) - Get subarray slice
- [sum.md](sum.md) - Sum numeric array elements

### Date/Time (3 functions)
Functions for working with dates and times.

- [formatDate.md](formatDate.md) - Format a date/time value
- [parseDate.md](parseDate.md) - Parse a date/time string
- [ticks.md](ticks.md) - Get current time in milliseconds

### File System (21 functions)
Operations for working with files and directories.

- [chdir.md](chdir.md) - Change current directory
- [createNewFile.md](createNewFile.md) - Create a new file
- [cwd.md](cwd.md) - Get current working directory
- [deleteFile.md](deleteFile.md) - Delete a file
- [getFileName.md](getFileName.md) - Get filename from path
- [getFileParent.md](getFileParent.md) - Get parent directory
- [getFileProper.md](getFileProper.md) - Construct proper file path
- [lastModified.md](lastModified.md) - Get file modification time
- [listRoots.md](listRoots.md) - List filesystem roots
- [lof.md](lof.md) - Get length of file
- [ls.md](ls.md) - List directory contents
- [mkdir.md](mkdir.md) - Create directory
- [pr_canread.md](pr_canread.md) - Test if file can be read (-canread)
- [pr_canwrite.md](pr_canwrite.md) - Test if file can be written (-canwrite)
- [pr_exists.md](pr_exists.md) - Test if file exists (-exists)
- [pr_isDir.md](pr_isDir.md) - Test if path is directory (-isDir)
- [pr_isFile.md](pr_isFile.md) - Test if path is file (-isFile)
- [pr_isHidden.md](pr_isHidden.md) - Test if file is hidden (-isHidden)
- [rename.md](rename.md) - Rename a file
- [setLastModified.md](setLastModified.md) - Set file modification time
- [setReadOnly.md](setReadOnly.md) - Set file as read-only

### Hashes (6 functions)
Operations specific to hash/map data structures.

- [keys.md](keys.md) - Get array of hash keys
- [ohash.md](ohash.md) - Create ordered hash (insertion order)
- [ohasha.md](ohasha.md) - Create ordered hash (access order)
- [setMissPolicy.md](setMissPolicy.md) - Set policy for missing keys
- [setRemovalPolicy.md](setRemovalPolicy.md) - Set removal policy for hash
- [values.md](values.md) - Get array of hash values

### Input/Output (31 functions)
Functions for reading, writing, and managing I/O streams.

- [allocate.md](allocate.md) - Allocate a memory buffer
- [available.md](available.md) - Get bytes available for reading
- [bread.md](bread.md) - Binary read with pack template
- [bwrite.md](bwrite.md) - Binary write with pack template
- [closef.md](closef.md) - Close an I/O handle
- [connect.md](connect.md) - Connect to network host
- [exec.md](exec.md) - Execute external program
- [fork.md](fork.md) - Create new thread
- [getConsole.md](getConsole.md) - Get console I/O handle
- [listen.md](listen.md) - Listen for network connections
- [mark.md](mark.md) - Mark position in stream
- [openf.md](openf.md) - Open file for reading/writing
- [pr_eof.md](pr_eof.md) - Test for end-of-file (-eof)
- [print.md](print.md) - Print to stream
- [printAll.md](printAll.md) - Print all array elements
- [printEOF.md](printEOF.md) - Print EOF marker
- [println.md](println.md) - Print with newline
- [readAll.md](readAll.md) - Read all remaining data
- [readAsObject.md](readAsObject.md) - Read and deserialize object
- [readb.md](readb.md) - Read bytes
- [readc.md](readc.md) - Read character
- [readln.md](readln.md) - Read line
- [readObject.md](readObject.md) - Read serialized object
- [reset.md](reset.md) - Reset stream to marked position
- [setEncoding.md](setEncoding.md) - Set character encoding
- [sizeof.md](sizeof.md) - Get size of object in bytes
- [skip.md](skip.md) - Skip bytes in stream
- [wait.md](wait.md) - Wait for thread to complete
- [writeAsObject.md](writeAsObject.md) - Serialize and write object
- [writeb.md](writeb.md) - Write bytes
- [writeObject.md](writeObject.md) - Write serialized object

### Math (28 functions)
Mathematical operations and functions.

- [abs.md](abs.md) - Absolute value
- [acos.md](acos.md) - Arc cosine
- [asin.md](asin.md) - Arc sine
- [atan.md](atan.md) - Arc tangent
- [atan2.md](atan2.md) - Arc tangent of y/x
- [ceil.md](ceil.md) - Ceiling function
- [checksum.md](checksum.md) - Calculate checksum
- [cos.md](cos.md) - Cosine
- [degrees.md](degrees.md) - Convert radians to degrees
- [digest.md](digest.md) - Calculate cryptographic digest
- [double.md](double.md) - Convert to double
- [exp.md](exp.md) - Exponential (e^x)
- [floor.md](floor.md) - Floor function
- [formatNumber.md](formatNumber.md) - Format number as string
- [int.md](int.md) - Convert to integer
- [log.md](log.md) - Natural logarithm
- [long.md](long.md) - Convert to long
- [not.md](not.md) - Bitwise NOT
- [parseNumber.md](parseNumber.md) - Parse number from string
- [radians.md](radians.md) - Convert degrees to radians
- [rand.md](rand.md) - Random number
- [round.md](round.md) - Round to nearest integer
- [sin.md](sin.md) - Sine
- [spaceship.md](spaceship.md) - Three-way comparison (<=>)
- [sqrt.md](sqrt.md) - Square root
- [srand.md](srand.md) - Seed random number generator
- [tan.md](tan.md) - Tangent
- [uint.md](uint.md) - Convert to unsigned integer

### Strings (29 functions)
String manipulation and pattern matching.

- [asc.md](asc.md) - Get ASCII value of character
- [byteAt.md](byteAt.md) - Get byte at position
- [charAt.md](charAt.md) - Get character at position
- [chr.md](chr.md) - Convert ASCII value to character
- [cmp.md](cmp.md) - Compare strings
- [find.md](find.md) - Find string in array
- [hasmatch.md](hasmatch.md) - Test if string has regex match
- [indexOf.md](indexOf.md) - Find substring index
- [ismatch.md](ismatch.md) - Test if string matches regex
- [iswm.md](iswm.md) - Test wildcard match
- [join.md](join.md) - Join array elements into string
- [lc.md](lc.md) - Convert to lowercase
- [left.md](left.md) - Get leftmost characters
- [lindexOf.md](lindexOf.md) - Find last occurrence index
- [matched.md](matched.md) - Get regex match results
- [matches.md](matches.md) - Extract regex matches
- [mid.md](mid.md) - Get substring from middle
- [pack.md](pack.md) - Pack values into binary string
- [replace.md](replace.md) - Replace regex matches
- [replaceAt.md](replaceAt.md) - Replace substring at position
- [right.md](right.md) - Get rightmost characters
- [split.md](split.md) - Split string into array
- [strlen.md](strlen.md) - Get string length
- [strrep.md](strrep.md) - Repeat string
- [substr.md](substr.md) - Get substring
- [tr.md](tr.md) - Translate characters
- [uc.md](uc.md) - Convert to uppercase
- [unpack.md](unpack.md) - Unpack binary string into values

### Utility (39 functions)
General utility and meta-programming functions.

- [acquire.md](acquire.md) - Acquire semaphore
- [casti.md](casti.md) - Cast scalar to specific type
- [checkError.md](checkError.md) - Check for soft error
- [compile_closure.md](compile_closure.md) - Compile closure from code
- [debug.md](debug.md) - Set debug flags
- [eval.md](eval.md) - Evaluate Sleep code
- [exit.md](exit.md) - Exit script
- [expr.md](expr.md) - Evaluate expression
- [function.md](function.md) - Get function by name
- [getStackTrace.md](getStackTrace.md) - Get call stack trace
- [global.md](global.md) - Declare global variables
- [iff.md](iff.md) - Conditional operator
- [include.md](include.md) - Include another script
- [inline.md](inline.md) - Define inline subroutine
- [invoke.md](invoke.md) - Invoke function dynamically
- [is.md](is.md) - Test object reference equality
- [isa.md](isa.md) - Test if object is instance of class
- [lambda.md](lambda.md) - Create anonymous function
- [let.md](let.md) - Assign variables
- [local.md](local.md) - Declare local variables
- [newInstance.md](newInstance.md) - Create proxy instance
- [popl.md](popl.md) - Pop local scope
- [profile.md](profile.md) - Get profiling statistics
- [pushl.md](pushl.md) - Push new local scope
- [release.md](release.md) - Release semaphore
- [scalar.md](scalar.md) - Convert object to scalar
- [semaphore.md](semaphore.md) - Create semaphore
- [setf.md](setf.md) - Set function
- [setField.md](setField.md) - Set object field
- [sleep.md](sleep.md) - Pause execution
- [systemProperties.md](systemProperties.md) - Get system properties
- [taint.md](taint.md) - Mark data as tainted
- [this.md](this.md) - Access closure scope
- [typeOf.md](typeOf.md) - Get type of scalar
- [untaint.md](untaint.md) - Remove taint from data
- [use.md](use.md) - Load Java bridge
- [warn.md](warn.md) - Print warning message
- [watch.md](watch.md) - Watch variable for changes

---

## Quick Reference

### By Category
- **Arrays:** 30 functions for array manipulation
- **Date/Time:** 3 functions for date/time operations  
- **File System:** 21 functions for file operations
- **Hashes:** 6 functions for hash/map operations
- **Input/Output:** 31 functions for I/O operations
- **Math:** 28 mathematical functions
- **Strings:** 29 string manipulation functions
- **Utility:** 39 utility and meta-programming functions

### Total Functions: 187

---

## Usage Notes

- Each function page contains the full documentation from the Sleep manual
- Function pages include examples, parameters, return values, and related functions
- Tutorial pages provide comprehensive learning material
- All content sourced from https://sleep.dashnine.org/manual/

---

## License

Sleep is distributed under the LGPL (GNU Lesser General Public License).
Documentation © Raphael Mudge
