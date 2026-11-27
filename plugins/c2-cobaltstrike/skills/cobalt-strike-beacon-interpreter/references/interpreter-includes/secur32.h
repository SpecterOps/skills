#ifndef BUILTINS_SECUR32_H
#define BUILTINS_SECUR32_H

SECUR32$LsaRegisterLogonProcess: i32 (ptr, ptr, ptr);
SECUR32$LsaLogonUser: i32 (ptr, ptr, u32, u32, ptr, u32, ptr, ptr, ptr, ptr, ptr, ptr, ptr, ptr);
SECUR32$LsaLookupAuthenticationPackage: i32 (ptr, ptr, ptr);
SECUR32$LsaFreeReturnBuffer: i32 (ptr);
SECUR32$LsaCallAuthenticationPackage: i32 (ptr, u32, ptr, u32, ptr, ptr, ptr);
SECUR32$LsaDeregisterLogonProcess: i32 (ptr);
SECUR32$LsaConnectUntrusted: i32 (ptr);
SECUR32$LsaEnumerateLogonSessions: i32 (ptr, ptr);
SECUR32$LsaGetLogonSessionData: i32 (ptr, ptr);
SECUR32$LsaRegisterPolicyChangeNotification: i32 (u32, ptr);
SECUR32$LsaUnregisterPolicyChangeNotification: i32 (u32, ptr);

#endif /* BUILTINS_SECUR32_H */
