archives

Returns a massive list of archived information about your activity from Cobalt Strike's data model. This information is leaned on heavily to reconstruct your activity timeline in Cobalt Strike's reports.

#### Returns

An array of dictionary objects with information about your team's activity.

#### Example

```
foreach $index => $entry (archives()) {
   println("\c3( $+ $index $+ )\o $entry");
}```

