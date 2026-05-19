tokenToEmail

Covert a phishing token to an email address.

#### Arguments

`$1` - the phishing token

#### Returns

The email address or "unknown" if the token is not associated with an email.

#### Example

```
set PROFILER_HIT {
   local('$out $app $ver $email');
   $email = tokenToEmail($5);         
   $out = "\c9[+]\o $1 $+ / $+ $2 [ $+ $email $+ ] Applications";
   foreach $app => $ver ($4) {
      $out .= "\n\t $+ $[25]app $ver";
   }
   return "$out $+ \n\n";
}```

