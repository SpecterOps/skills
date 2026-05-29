# Sleep Quick Reference Guide

A fast reference for the most commonly used Sleep functions and concepts.

## Essential Functions

### Output
- `println($text)` - Print text with newline
- `print($text)` - Print text without newline
- `warn($message)` - Print warning message

### Variables
- `local('$var')` - Declare local variable
- `global('$var')` - Declare global variable
- `$null` - Null/empty scalar

### Arrays
- `@array = @(1, 2, 3)` - Create array
- `push(@array, $item)` - Add to end
- `pop(@array)` - Remove from end
- `size(@array)` - Get size
- `foreach $item (@array) { }` - Iterate

### Hashes
- `%hash = %(key => "value")` - Create hash
- `%hash["key"]` - Access value
- `keys(%hash)` - Get all keys
- `values(%hash)` - Get all values

### Strings
- `strlen($str)` - Get length
- `substr($str, $start, $len)` - Get substring
- `split($delim, $str)` - Split into array
- `join($delim, @array)` - Join array
- `uc($str)` - Uppercase
- `lc($str)` - Lowercase

### Control Flow
- `if ($condition) { }` - Conditional
- `while ($condition) { }` - Loop
- `for ($i = 0; $i < 10; $i++) { }` - For loop
- `foreach $item (@array) { }` - For each

### Functions
- `sub name { }` - Define function
- `return $value` - Return from function
- `lambda({ code }, $var => $val)` - Anonymous function

### File I/O
- `openf($filename)` - Open file for reading
- `openf(">$filename")` - Open for writing
- `readln($handle)` - Read line
- `println($handle, $text)` - Write line
- `closef($handle)` - Close file

### Regular Expressions
- `"string" ismatch 'pattern'` - Test match
- `"string" hasmatch 'pattern'` - Find match
- `matched()` - Get match results
- `replace($str, 'pattern', 'replacement')` - Replace

### Math
- `int($value)` - Convert to integer
- `double($value)` - Convert to double
- `rand()` - Random number
- `sqrt($n)`, `sin($n)`, `cos($n)` - Math functions

### Objects (Java Integration)
- `[new ClassName]` - Create object
- `[object method: arg1, arg2]` - Call method
- `[ClassName staticMethod: arg]` - Static method
- `import package.*` - Import Java package

## Common Patterns

### Reading a File
```sleep
$handle = openf("file.txt");
while $line (readln($handle)) {
    println($line);
}
closef($handle);
```

### Writing a File
```sleep
$handle = openf(">output.txt");
println($handle, "Line 1");
println($handle, "Line 2");
closef($handle);
```

### Iterating Arrays
```sleep
@items = @("a", "b", "c");
foreach $item (@items) {
    println($item);
}
```

### Iterating Hashes
```sleep
%data = %(key1 => "val1", key2 => "val2");
foreach $key => $value (%data) {
    println("$key = $value");
}
```

### Try-Catch
```sleep
try {
    # risky code
} catch $error {
    warn("Error: $error");
}
```

### Creating Threads
```sleep
$thread = fork({
    println("In thread!");
}, $var => $value);
wait($thread);
```

## Operators

### Comparison
- `==` - Numeric equality
- `eq` - String equality
- `<`, `>`, `<=`, `>=` - Numeric comparison
- `lt`, `gt` - String comparison

### Logical
- `&&` - AND
- `||` - OR
- `!` - NOT

### Assignment
- `=` - Assign
- `+=`, `-=`, `*=`, `/=` - Modify and assign

### String
- `.` - Concatenate
- `x` - Repeat

## Predicates

### Type Testing
- `-isnumber $x` - Is number
- `-isarray $x` - Is array
- `-ishash $x` - Is hash
- `-isfunction $x` - Is function

### File Testing
- `-exists $path` - File exists
- `-isDir $path` - Is directory
- `-isFile $path` - Is file
- `-canread $path` - Can read
- `-canwrite $path` - Can write

### Stream Testing
- `-eof $handle` - End of file

## Special Variables

- `@_` - Anonymous arguments in function
- `$1, $2, $3` - Positional arguments
- `$0` - Message name in closure
- `$null` - Null value
- `$this` - Current closure
- `@ARGV` - Command line arguments
- `$__SCRIPT__` - Current script name

## Common Idioms

### Default Value
```sleep
$value = iff($x is $null, "default", $x);
```

### Safe Array Access
```sleep
$item = iff(size(@array) > 0, @array[0], $null);
```

### String Formatting
```sleep
println("Value is $value");
println("Format: $[10]value");  # Right-align in 10 chars
```

### Array Slicing
```sleep
@slice = sublist(@array, $start, $end);
```

## Quick Tips

1. **Variables start with symbols:** `$scalar`, `@array`, `%hash`, `&function`
2. **Arrays are 0-indexed:** First element is `@array[0]`
3. **Negative indices work:** `@array[-1]` is last element
4. **Functions use &:** Reference with `&functionName`
5. **Pass by reference:** Arrays, hashes, objects pass by reference
6. **Closures have scope:** Use `lambda()` to create isolated scope
7. **Regex anchored:** `ismatch` anchors to start/end, `hasmatch` doesn't
8. **Whitespace matters:** Operators need whitespace: `$x = 1 + 2`

## Getting Help

- **Full Documentation:** See INDEX.md for complete function reference
- **Tutorials:** See intro.md, functions.md, regex.md, etc.
- **Examples:** Most function files include usage examples
- **Online:** http://sleep.dashnine.org/

## Most Used Functions (Top 20)

1. `println` - Output text
2. `openf` - Open file
3. `readln` - Read line
4. `closef` - Close handle
5. `size` - Get array/hash size
6. `foreach` - Iterate collection
7. `push` - Add to array
8. `pop` - Remove from array
9. `split` - Split string
10. `join` - Join array
11. `substr` - Get substring
12. `ismatch` - Regex match
13. `if/else` - Conditional
14. `while` - Loop
15. `local` - Declare variable
16. `return` - Return value
17. `keys` - Hash keys
18. `iff` - Conditional operator
19. `lambda` - Anonymous function
20. `eval` - Evaluate code

---

For complete documentation, see **INDEX.md**
