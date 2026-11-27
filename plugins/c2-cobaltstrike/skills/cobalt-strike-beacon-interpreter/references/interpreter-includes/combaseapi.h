/*
 * WINOLEAPI => HRESULT WINAPI, so these are modeled as stdcall i32.
 * Opaque/ref/pointer-style parameters are modeled as ptr.
 */
#ifndef BUILTINS_COMBASEAPI_H
#define BUILTINS_COMBASEAPI_H

typedef enum tagCOINITBASE {
    COINITBASE_MULTITHREADED = 0x0,
} COINITBASE;

typedef enum tagCOINIT {
    COINIT_APARTMENTTHREADED = 0x2,
    COINIT_MULTITHREADED = COINITBASE_MULTITHREADED,
    COINIT_DISABLE_OLE1DDE = 0x4,
    COINIT_SPEED_OVER_MEMORY = 0x8
} COINIT;

typedef enum tagCLSCTX {
    CLSCTX_INPROC_SERVER = 0x1,
    CLSCTX_INPROC_HANDLER = 0x2,
    CLSCTX_LOCAL_SERVER = 0x4,
    CLSCTX_INPROC_SERVER16 = 0x8,
    CLSCTX_REMOTE_SERVER = 0x10,
    CLSCTX_INPROC_HANDLER16 = 0x20,
    CLSCTX_RESERVED1 = 0x40,
    CLSCTX_RESERVED2 = 0x80,
    CLSCTX_RESERVED3 = 0x100,
    CLSCTX_RESERVED4 = 0x200,
    CLSCTX_NO_CODE_DOWNLOAD = 0x400,
    CLSCTX_RESERVED5 = 0x800,
    CLSCTX_NO_CUSTOM_MARSHAL = 0x1000,
    CLSCTX_ENABLE_CODE_DOWNLOAD = 0x2000,
    CLSCTX_NO_FAILURE_LOG = 0x4000,
    CLSCTX_DISABLE_AAA = 0x8000,
    CLSCTX_ENABLE_AAA = 0x10000,
    CLSCTX_FROM_DEFAULT_CONTEXT = 0x20000,
    CLSCTX_ACTIVATE_32_BIT_SERVER = 0x40000,
    CLSCTX_ACTIVATE_64_BIT_SERVER = 0x80000,
    CLSCTX_ENABLE_CLOAKING = 0x100000,
    CLSCTX_APPCONTAINER = 0x400000,
    CLSCTX_ACTIVATE_AAA_AS_IU = 0x800000,
    CLSCTX_PS_DLL = 0x80000000
} CLSCTX;

OLE32$CreateStreamOnHGlobal: stdcall i32 (ptr, u32, ptr);
OLE32$GetHGlobalFromStream: stdcall i32 (ptr, ptr);
OLE32$CoUninitialize: stdcall void ();
OLE32$CoInitializeEx: stdcall i32 (ptr, u32);
OLE32$CoGetCurrentLogicalThreadId: stdcall i32 (ptr);
OLE32$CoGetContextToken: stdcall i32 (ptr);
OLE32$CoGetApartmentType: stdcall i32 (ptr, ptr);
OLE32$CoGetObjectContext: stdcall i32 (ptr, ptr);
OLE32$CoRegisterClassObject: stdcall i32 (ptr, ptr, u32, u32, ptr);
OLE32$CoRevokeClassObject: stdcall i32 (u32);
OLE32$CoResumeClassObjects: stdcall i32 ();
OLE32$CoSuspendClassObjects: stdcall i32 ();
OLE32$CoGetMalloc: stdcall i32 (u32, ptr);
OLE32$CoGetCurrentProcess: stdcall u32 ();
OLE32$CoGetCallerTID: stdcall i32 (ptr);
OLE32$CoGetDefaultContext: stdcall i32 (i32, ptr, ptr);
OLE32$CoDecodeProxy: stdcall i32 (u32, u64, ptr);
OLE32$CoWaitForMultipleObjects: stdcall i32 (u32, u32, u32, ptr, ptr);
OLE32$CoAllowUnmarshalerCLSID: stdcall i32 (ptr);
OLE32$CoGetClassObject: stdcall i32 (ptr, u32, ptr, ptr, ptr);
OLE32$CoAddRefServerProcess: stdcall u32 ();
OLE32$CoReleaseServerProcess: stdcall u32 ();
OLE32$CoGetPSClsid: stdcall i32 (ptr, ptr);
OLE32$CoRegisterPSClsid: stdcall i32 (ptr, ptr);
OLE32$CoRegisterSurrogate: stdcall i32 (ptr);
OLE32$CoMarshalHresult: stdcall i32 (ptr, i32);
OLE32$CoUnmarshalHresult: stdcall i32 (ptr, ptr);
OLE32$CoLockObjectExternal: stdcall i32 (ptr, u32, u32);
OLE32$CoGetStdMarshalEx: stdcall i32 (ptr, u32, ptr);
OLE32$CoIncrementMTAUsage: stdcall i32 (ptr);
OLE32$CoDecrementMTAUsage: stdcall i32 (size_t);
OLE32$CoGetMarshalSizeMax: stdcall i32 (ptr, ptr, ptr, u32, ptr, u32);
OLE32$CoMarshalInterface: stdcall i32 (ptr, ptr, ptr, u32, ptr, u32);
OLE32$CoUnmarshalInterface: stdcall i32 (ptr, ptr, ptr);
OLE32$CoReleaseMarshalData: stdcall i32 (ptr);
OLE32$CoDisconnectObject: stdcall i32 (ptr, u32);
OLE32$CoGetStandardMarshal: stdcall i32 (ptr, ptr, u32, ptr, u32, ptr);
OLE32$CoMarshalInterThreadInterfaceInStream: stdcall i32 (ptr, ptr, ptr);
OLE32$CoGetInterfaceAndReleaseStream: stdcall i32 (ptr, ptr, ptr);
OLE32$CoCreateFreeThreadedMarshaler: stdcall i32 (ptr, ptr);
OLE32$CoFreeUnusedLibraries: stdcall void ();
OLE32$CoFreeUnusedLibrariesEx: stdcall void (u32, u32);
OLE32$CoInitializeSecurity: stdcall i32 (ptr, i32, ptr, ptr, u32, u32, ptr, u32, ptr);
OLE32$CoSwitchCallContext: stdcall i32 (ptr, ptr);
OLE32$CoCreateInstanceFromApp: stdcall i32 (ptr, ptr, u32, ptr, u32, ptr);
OLE32$CoIsHandlerConnected: stdcall u32 (ptr);
OLE32$CoDisconnectContext: stdcall i32 (u32);
OLE32$CoGetCallContext: stdcall i32 (ptr, ptr);
OLE32$CoQueryProxyBlanket: stdcall i32 (ptr, ptr, ptr, ptr, ptr, ptr, ptr, ptr);
OLE32$CoSetProxyBlanket: stdcall i32 (ptr, u32, u32, ptr, u32, u32, ptr, u32);
OLE32$CoCopyProxy: stdcall i32 (ptr, ptr);
OLE32$CoQueryClientBlanket: stdcall i32 (ptr, ptr, ptr, ptr, ptr, ptr, ptr);
OLE32$CoImpersonateClient: stdcall i32 ();
OLE32$CoRevertToSelf: stdcall i32 ();
OLE32$CoQueryAuthenticationServices: stdcall i32 (ptr, ptr);
OLE32$CoCreateInstance: stdcall i32 (ptr, ptr, u32, ptr, ptr);
OLE32$CoCreateInstanceEx: stdcall i32 (ptr, ptr, u32, ptr, u32, ptr);
OLE32$CoGetCancelObject: stdcall i32 (u32, ptr, ptr);
OLE32$CoSetCancelObject: stdcall i32 (ptr);
OLE32$CoCancelCall: stdcall i32 (u32, u32);
OLE32$CoTestCancel: stdcall i32 ();
OLE32$CoEnableCallCancellation: stdcall i32 (ptr);
OLE32$CoDisableCallCancellation: stdcall i32 (ptr);
OLE32$StringFromCLSID: stdcall i32 (ptr, ptr);
OLE32$CLSIDFromString: stdcall i32 (ptr, ptr);
OLE32$StringFromIID: stdcall i32 (ptr, ptr);
OLE32$IIDFromString: stdcall i32 (ptr, ptr);
OLE32$ProgIDFromCLSID: stdcall i32 (ptr, ptr);
OLE32$CLSIDFromProgID: stdcall i32 (ptr, ptr);
OLE32$StringFromGUID2: stdcall i32 (ptr, ptr, i32);
OLE32$CoCreateGuid: stdcall i32 (ptr);
OLE32$PropVariantCopy: stdcall i32 (ptr, ptr);
OLE32$PropVariantClear: stdcall i32 (ptr);
OLE32$FreePropVariantArray: stdcall i32 (u32, ptr);
OLE32$CoWaitForMultipleHandles: stdcall i32 (u32, u32, u32, ptr, ptr);
OLE32$CoGetTreatAsClass: stdcall i32 (ptr, ptr);
OLE32$CoInvalidateRemoteMachineBindings: stdcall i32 (ptr);
OLE32$CoTaskMemAlloc: stdcall ptr (size_t);
OLE32$CoTaskMemRealloc: stdcall ptr (ptr, size_t);
OLE32$CoTaskMemFree: stdcall void (ptr);

#endif /* BUILTINS_COMBASEAPI_H */
