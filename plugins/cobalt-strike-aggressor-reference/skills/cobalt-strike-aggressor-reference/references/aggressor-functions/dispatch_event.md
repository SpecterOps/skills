dispatch_event

Call a function in Java Swing's Event Dispatch Thread. Java's Swing Library is not thread safe. All changes to the user interface should happen from the Event Dispatch Thread.

#### Arguments

`$1` - the function to call

#### Example

```
dispatch_event({
   println("Hello World"); 
});```

