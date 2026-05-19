bdllspawn

Spawn a Reflective DLL as a Beacon post-exploitation job.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the local path to the Reflective DLL

`$3` - a parameter to pass to the DLL

`$4` - a short description of this post exploitation job (shows up in **jobs** output)

`$5` - wait time for returned data specified in milliseconds (5000 = 5 seconds)

`$6` - true/false; use impersonated token when running this post-ex job?

`$7` - (optional) callback function with the results. Arguments to the callback are: $1 = beacon ID, $2 = results, $3 = information map

#### Notes

- This function will spawn an x86 process if the Reflective DLL is an x86 DLL. Likewise, if the Reflective DLL is an x64 DLL, this function will spawn an x64 process.
- A well-behaved Reflective DLL follows these rules:  - Receives a parameter via the reserved DllMain parameter when the DLL_PROCESS_ATTACH reason is specified.
  - Prints messages to STDOUT
  - Calls `fflush(stdout)` to flush STDOUT
  - Calls `ExitProcess(0)` when done. This kills the spawned process to host the capability.


#### Example (ReflectiveDll.c)

This example is based on Stephen Fewer's Reflective DLL Injection Project:

```
BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD dwReason, LPVOID lpReserved ) {
   BOOL bReturnValue = TRUE;
   switch( dwReason ) {
      case DLL_QUERY_HMODULE:
         if( lpReserved != NULL )
            *(HMODULE *)lpReserved = hAppInstance;
         break;
      case DLL_PROCESS_ATTACH:
         hAppInstance = hinstDLL;
   
         /* print some output to the operator */
         if (lpReserved != NULL) {
            printf("Hello from test.dll. 
            Parameter is '%s'\n", (char *)lpReserved);
         }
         else {
            printf("Hello from test.dll. There is no parameter\n");
         }

         /* flush STDOUT */
         fflush(stdout);

         /* we're done, so let's exit */
         ExitProcess(0);
         break;
      case DLL_PROCESS_DETACH:
      case DLL_THREAD_ATTACH:
      case DLL_THREAD_DETACH:
         break;
   }
   return bReturnValue;
}```

#### Example (Aggressor Script)

```
alias hello {
   bdllspawn($1, script_resource("reflective_dll.dll"), $2, 
   "test dll", 5000, false);
}```

