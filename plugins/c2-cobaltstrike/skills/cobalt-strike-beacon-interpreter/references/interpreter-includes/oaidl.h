#ifndef BUILTINS_OAIDL_H
#define BUILTINS_OAIDL_H

#include <winnt.h>

#define FAILED(hr) ((HRESULT)(hr) < 0)
#define SUCCEEDED(hr) ((HRESULT)(hr) >= 0)
#define COINIT_APARTMENTTHREADED 0x2
#define CLSCTX_INPROC_SERVER 0x1

typedef SHORT VARIANT_BOOL;
typedef int FLOAT; // float is not supported by the VM but this will allow the VARIANT struct to line up correctly
typedef DWORD64 DOUBLE; // double is also not supported by the VM but this will keep VARIANT struct aligned
typedef DOUBLE DATE;
typedef LONG DISPID;
typedef GUID* REFIID;
typedef WCHAR OLECHAR;
typedef OLECHAR *BSTR;
typedef OLECHAR *LPOLESTR;
typedef BSTR *LPBSTR;
typedef unsigned short VARTYPE;
enum VARENUM {
    VT_EMPTY = 0,
    VT_NULL = 1,
    VT_I2 = 2,
    VT_I4 = 3,
    VT_R4 = 4,
    VT_R8 = 5,
    VT_CY = 6,
    VT_DATE = 7,
    VT_BSTR = 8,
    VT_DISPATCH = 9,
    VT_ERROR = 10,
    VT_BOOL = 11,
    VT_VARIANT = 12,
    VT_UNKNOWN = 13,
    VT_DECIMAL = 14,
    VT_I1 = 16,
    VT_UI1 = 17,
    VT_UI2 = 18,
    VT_UI4 = 19,
    VT_I8 = 20,
    VT_UI8 = 21,
    VT_INT = 22,
    VT_UINT = 23,
    VT_VOID = 24,
    VT_HRESULT = 25,
    VT_PTR = 26,
    VT_SAFEARRAY = 27,
    VT_CARRAY = 28,
    VT_USERDEFINED = 29,
    VT_LPSTR = 30,
    VT_LPWSTR = 31,
    VT_RECORD = 36,
    VT_INT_PTR = 37,
    VT_UINT_PTR = 38,
    VT_FILETIME = 64,
    VT_BLOB = 65,
    VT_STREAM = 66,
    VT_STORAGE = 67,
    VT_STREAMED_OBJECT = 68,
    VT_STORED_OBJECT = 69,
    VT_BLOB_OBJECT = 70,
    VT_CF = 71,
    VT_CLSID = 72,
    VT_VERSIONED_STREAM = 73,
    VT_BSTR_BLOB = 0xfff,
    VT_VECTOR = 0x1000,
    VT_ARRAY = 0x2000,
    VT_BYREF = 0x4000,
    VT_RESERVED = 0x8000,
    VT_ILLEGAL = 0xffff,
    VT_ILLEGALMASKED = 0xfff,
    VT_TYPEMASK = 0xfff
};

typedef union tagCY {
    struct {
        unsigned long Lo;
        long Hi;
    };
    LONGLONG int64;
} CY;
typedef struct tagDEC {
    USHORT wReserved;
    union {
        struct {
            BYTE scale;
            BYTE sign;
        };
        USHORT signscale;
    };
    ULONG Hi32;
    union {
        struct {
            ULONG Lo32;
            ULONG Mid32;
        };
        ULONGLONG Lo64;
    };
} DECIMAL;

typedef LONG SCODE;

typedef struct tagSAFEARRAYBOUND {
    ULONG cElements;
    LONG lLbound;
} SAFEARRAYBOUND;

typedef struct tagSAFEARRAY {
    USHORT cDims;
    USHORT fFeatures;
    ULONG cbElements;
    ULONG cLocks;
    PVOID pvData;
    SAFEARRAYBOUND rgsabound[1];
} SAFEARRAY;

typedef struct tagDISPPARAMS {
    void *rgvarg;
    DISPID *rgdispidNamedArgs;
    UINT cArgs;
    UINT cNamedArgs;
} DISPPARAMS;

typedef struct IUnknownVtbl {
    /*** IUnknown methods ***/
    HRESULT (stdcall *QueryInterface)(
        void* This,
        REFIID riid,
        void **ppvObject);

    ULONG (stdcall *AddRef)(
        void* This);

    ULONG (stdcall *Release)(
        void* This);
} IUnknownVtbl;
struct IUnknown {
   IUnknownVtbl* lpVtbl;
};

typedef struct IDispatchVtbl {
    /*** IUnknown methods ***/
    HRESULT (stdcall *QueryInterface)(
        void *This,
        REFIID riid,
        void **ppvObject);

    ULONG (stdcall *AddRef)(
        void *This);

    ULONG (stdcall *Release)(
        void *This);

    /*** IDispatch methods ***/
    HRESULT (stdcall *GetTypeInfoCount)(
        void *This,
        UINT *pctinfo);

    HRESULT (stdcall *GetTypeInfo)(
        void *This,
        UINT iTInfo,
        LCID lcid,
        void **ppTInfo);

    HRESULT (stdcall *GetIDsOfNames)(
        void *This,
        REFIID riid,
        LPOLESTR *rgszNames,
        UINT cNames,
        LCID lcid,
        DISPID *rgDispId);

    HRESULT (stdcall *Invoke)(
        void *This,
        DISPID dispIdMember,
        REFIID riid,
        LCID lcid,
        WORD wFlags,
        void *pDispParams,
        void *pVarResult,
        void *pExcepInfo,
        UINT *puArgErr);

} IDispatchVtbl;

struct IDispatch {
    IDispatchVtbl* lpVtbl;
};

typedef struct tagVARIANT {
    union {
        struct {
            VARTYPE vt;
            WORD wReserved1;
            WORD wReserved2;
            WORD wReserved3;
            union {
                LONGLONG llVal;
                LONG lVal;
                BYTE bVal;
                SHORT iVal;
                FLOAT fltVal;
                DOUBLE dblVal;
                VARIANT_BOOL boolVal;
                SCODE scode;
                CY cyVal;
                DATE date;
                BSTR bstrVal;
                struct IUnknown *punkVal;
                struct IDispatch *pdispVal;
                SAFEARRAY *parray;
                BYTE *pbVal;
                SHORT *piVal;
                LONG *plVal;
                LONGLONG *pllVal;
                FLOAT *pfltVal;
                DOUBLE *pdblVal;
                VARIANT_BOOL *pboolVal;
                SCODE *pscode;
                CY *pcyVal;
                DATE *pdate;
                BSTR *pbstrVal;
                struct IUnknown **ppunkVal;
                struct IDispatch **ppdispVal;
                SAFEARRAY **pparray;
                void *pvarVal;
                PVOID byref;
                CHAR cVal;
                USHORT uiVal;
                ULONG ulVal;
                ULONGLONG ullVal;
                INT intVal;
                UINT uintVal;
                DECIMAL *pdecVal;
                CHAR *pcVal;
                USHORT *puiVal;
                ULONG *pulVal;
                ULONGLONG *pullVal;
                INT *pintVal;
                UINT *puintVal;
                struct {
                    PVOID pvRecord;
                    void *pRecInfo;
                };
            };
        };
        DECIMAL decVal;
    };
} VARIANT;

typedef VARIANT *LPVARIANT;
typedef VARIANT VARIANTARG;
typedef VARIANT *LPVARIANTARG;

#endif
