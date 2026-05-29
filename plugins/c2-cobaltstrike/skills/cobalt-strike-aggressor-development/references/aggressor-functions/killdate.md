killdate

Get the Beacon kill date configured on the teamserver.

####  Returns

A string with the teamserver's kill date in the format “YYYY-MM-DD” (where YYYY is year, MM is month and DD is the day). For example, a returned value of 2024-07-05 is the date 5 July 2024.

NOTE:  A kill date is optional. If a teamserver does not have a kill date set then an empty string is returned.

#### Example

```
println("Kill date: " . killdate());```
