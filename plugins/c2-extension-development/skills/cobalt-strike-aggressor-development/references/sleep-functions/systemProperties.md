# systemProperties

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/systemProperties.html

---

## Synopsis

```sleep
% systemProperties()
```

Returns a hash of the available system properties.

## Returns

A read-only hash of all the available system properties.

## Examples

**Example:**
```sleep
# list properties of your system...

foreach $property => $value (systemProperties()) {
println("$property : $value");
}

```

**Output:**
```
java.runtime.name : Java(TM) 2 Runtime Environment, Standard Edition
java.vm.version : 1.5.0_07-87
java.vm.vendor : "Apple Computer, Inc."
java.runtime.version : 1.5.0_07-164
os.arch : ppc
os.name : Mac OS X
os.version : 10.4.8
user.home : /Users/raffi
user.name : raffi
java.version : 1.5.0_07

```

**Example:**
```sleep
%props = systemProperties();
println("My userid is: " . %props["user.name"]);
println("I belong at: " . %props["user.home"]);

```

**Output:**
```
My userid is: raffi
I belong at: /Users/raffi

```

**Example:**
```sleep
# set a system property

[System setProperty: "test.prop", "foo"];

# retreive it:

println(systemProperties()["test.prop"]);

```

**Output:**
```
foo

```
