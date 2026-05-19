bspawnto

Change the default program Beacon spawns to inject capabilities into.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the architecture we're modifying the spawnto setting for (x86, x64)

`$3` - the program to spawn

#### Notes

The value you specify for spawnto must work from x86->x86, x86->x64, x64->x86, and x64->x86 contexts. This is tricky. Follow these rules and you'll be OK:

1. Always specify the full path to the program you want Beacon to spawn for its post-ex jobs.

2. Environment variables (e.g., %windir%) are OK within these paths.

3. Do not specify `%windir%\system32` or `c:\windows\system32` directly. Always use syswow64 (x86) and sysnative (x64). Beacon will adjust these values to system32 if it's necessary.

4. For an x86 spawnto value, you must specify an x86 program. For an x64 spawnto value, you must specify an x64 program.

#### Example

```
# let's make everything lame.
on beacon_initial {
   binput($1, "prep session with new spawnto values.");
   bspawnto($1, "x86", "%windir%\\syswow64\\notepad.exe");
   bspawnto($1, "x64", "%windir%\\sysnative\\notepad.exe");
}```
