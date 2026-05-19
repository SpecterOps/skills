# use

**Category:** Utility

**Source:** https://sleep.dashnine.org/manual/use.html

---

## Synopsis

```sleep
use(^Class)
```

Installs the specified class (which is a sleep.interfaces.Loadable) into the current Sleep environment. This is a way of extending the Sleep language at runtime.

```sleep
use(['/path/to/file.jar'], 'Loadable')
```

Dynamically loads a specified Sleep bridge and installs it into the current Sleep environment. This is a way of extending the Sleep language at runtime with Sleep bridges.

## Parameters

`^Class` - the class to instantiate a new instance of and install into the current Sleep environment

`'/path/to/file.jar'` - optionally a jar file that contains the bridge classes can be specified. If no .jar file is specified then the bridge will be loaded from the sleep.classpath value.

`'Loadable'` - this is the fully qualified package+class name of the bridge class that implements sleep.interfaces.Loadable. This class will be dynamically instantiated and its scriptLoaded method will be called against the current script environment.

## Side Effects / Notes

- Loads a series of extensions into the current script environment.

## Errors

- Throws [java.lang.ClassNotFoundException](http://java.sun.com/javase/6/docs/api/java/lang/ClassNotFoundException.md) if the class cannot be located

- Throws other errors if class initialization fails.

## Examples

**Example:**
```sleep
# This example shows how to connect to a MySQL database and
# execute a simple query with Slumber by Andreas Ravnestad

import no.printf.slumber.JDBC from: slumber.jar;

use(^JDBC);

$handle = dbConnect('com.mysql.jdbc.Driver',
'jdbc:mysql://localhost/database',
'user', 'pass');

$result = dbQuery($handle, 'select * from table');

while (dbAssign($result, %row))
{
println(%row);
}

```

## See Also

[&include](include.md)
