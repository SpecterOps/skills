getAggressorClientType

Returns the type of client that is executing the current script. This function is useful when sharing a script between different client types but you want to limit some capabilities in the script to a particular client type. For example, UI elements should only be executed for the ui client type.

#### Returns

One of the following strings will be returned:

`ui `- Returned when the Cobalt Strike UI client is executing the script.

`headless `- Returned when the Headless Cobalt Strike client is executing the script.

`restapi `- Returned when the Cobalt Strike Rest API service is executing the script.

#### Examples

Print the aggressor client type that is executing this code.

```
println("The aggressor client type is set to: " . getAggressorClientType());```

Use in a CNA script to help control behavior when it is executed by any of the client types.

```
# Use in a CNA script that may be used by any of the client types.
if (getAggressorClientType() eq "ui") {
   show_message("I am a UI client, safe to show dialog boxes.");
} else {
   println("I am not a UI client, print message to stdout.");
}```
