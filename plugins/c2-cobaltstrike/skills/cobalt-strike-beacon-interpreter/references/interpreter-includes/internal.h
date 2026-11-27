#ifndef BUILTINS_ADVAPI_H
#define BUILTINS_ADVAPI_H

/* emits debug string via OutputDebugStringA */ 
INTERNAL$DbgPrintf: cdecl void (cstr, ...);

#endif
