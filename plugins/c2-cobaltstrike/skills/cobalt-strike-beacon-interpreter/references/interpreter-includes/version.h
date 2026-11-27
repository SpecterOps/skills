#ifndef BUILTINS_VERSION_H
#define BUILTINS_VERSION_H

VERSION$VerFindFileA: u32 (u32, ptr, ptr, ptr, ptr, ptr, ptr, ptr);
VERSION$VerFindFileW: u32 (u32, ptr, ptr, ptr, ptr, ptr, ptr, ptr);
VERSION$VerInstallFileA: u32 (u32, ptr, ptr, ptr, ptr, ptr, ptr, ptr);
VERSION$VerInstallFileW: u32 (u32, ptr, ptr, ptr, ptr, ptr, ptr, ptr);
VERSION$GetFileVersionInfoSizeA: u32 (cstr, ptr);
VERSION$GetFileVersionInfoSizeW: u32 (ptr, ptr);
VERSION$GetFileVersionInfoSizeExA: u32 (u32, cstr, ptr);
VERSION$GetFileVersionInfoSizeExW: u32 (u32, ptr, ptr);
VERSION$GetFileVersionInfoA: u32 (cstr, u32, u32, ptr);
VERSION$GetFileVersionInfoW: u32 (ptr, u32, u32, ptr);
VERSION$GetFileVersionInfoExA: u32 (u32, cstr, u32, u32, ptr);
VERSION$GetFileVersionInfoExW: u32 (u32, ptr, u32, u32, ptr);
VERSION$VerLanguageNameA: u32 (u32, ptr, u32);
VERSION$VerLanguageNameW: u32 (u32, ptr, u32);
VERSION$VerQueryValueA: u32 (ptr, cstr, ptr, ptr);
VERSION$VerQueryValueW: u32 (ptr, ptr, ptr, ptr);

#endif /* BUILTINS_VERSION_H */
