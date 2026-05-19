# Introduction

I. What is Sleep?

The java world currently has Jacl for TCL, Jython for Python, and JRuby for Ruby. One offering is missing from this bunch: what Java scripting language exists for the Perl hackers of the world?

Sleep is a Java-based scripting language heavily inspired by Perl. Sleep started out as a weekend long hack fest in April 2002. When nothing like Perl was available to build a scriptable Internet Relay Chat client, I set out to build the scripting language I wanted.

Sleep has evolved beyond its beginnings as a scripting engine for a chat program. Today Sleep primitives include strings, doubles, integers, and containers for holding objects and functions. Arrays and hashes can combine these primitives into complex data structures. Closures that respond to "messages" act as a flexible means of abstraction. Also The entire Java API is accessible as if the Java Objects were functions that respond to "messages".

## Sleep Language Overview

Sleep's syntax, operators, and idioms are similar to the Perl scripting language. There is one major difference that catches new programmers. Sleep requires whitespace between operators and their terms. The following code is not valid:

```
$x=1+2; # this will not parse!!
```

This statement is valid though:

```
$x = 1 + 2;
```

Sleep variables are called scalars and scalars hold strings, numbers in various formats, Java object references, functions, arrays, and dictionaries. Here are several assignments in Sleep

```
$x = "Hello World";
$y = 3;
$z = @(1, 2, 3, "four");
$a = %(a => "apple", b => "bat", c => "awesome language", d => 4);
```

Arrays and dictionaries are created with the @ and % functions. Arrays and dictionaries may reference other arrays and dictionaries. Arrays and dictionaries may even reference themselves.

Comments begin with a # and go until the end of the line.

Sleep interpolates double-quoted strings. This means that any white-space separated token beginning with a $ sign is replaced with its value. The special variable $+ concatenates an interpolated string with another value.

```
println("\$a is: $a and \n\$x joined with \$y is: $x $+ $y");
```

This will print out:

```
$a is: %(d => 4, b => 'bat', c => 'awesome language', a => 'apple') and 
$x joined with $y is: Hello World3
```

There's a function called &warn. It works like &println, except it includes the current script name and a line number too. This is a great function to debug code with.

Sleep functions are declared with the sub keyword. Arguments to functions are labeled $1, $2, all the way up to $n. Functions will accept any number of arguments. The variable @_ is an array containing all of the arguments too. Changes to $1, $2, etc. will alter the contents of @_.

```
sub addTwoValues {
   println($1 + $2);
}
 
addTwoValues("3", 55.0);
```

This script prints out:

```
58.0
```


In Sleep, a function is a first-class type like any other object. Here are a few things that you may see:

```
$addf = &addTwoValues;
```

The $addf variable now references the &addTwoValues function. To call a function enclosed in a variable, use:

```
[$addf : "3", 55.0];
```

This bracket notation is also used to manipulate Java objects. I recommend reading the Sleep manual if you're interested in learning more about this. The following statements are equivalent and they do the same thing:

```
[$addf : "3", 55.0];
[&addTwoValues : "3", 55.0];
[{ println($1 + $2); } : "3", 55.0];
addTwoValues("3", 55.0);
```

Sleep has three variable scopes: global, closure-specific, and local. The Sleep manual covers this in more detail. If you see local('$x $y $z') in an example, it means that $x, $y, and $z are local to the current function and their values will disappear when the function returns. Sleep uses lexical scoping for its variables.

Sleep has all of the other basic constructs you'd expect in a scripting language. You should read the manual to learn more about it.

## Sleep Manual

The full sleep manual can be found [here](https://sleep.dashnine.org/manual/).