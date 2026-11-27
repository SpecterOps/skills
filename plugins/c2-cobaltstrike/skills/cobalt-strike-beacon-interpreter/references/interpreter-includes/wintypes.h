#ifndef BUILTINS_WINTYPES_H
#define BUILTINS_WINTYPES_H

typedef void VOID;
typedef char *PSZ;
typedef int BOOL;
typedef char CHAR;
typedef unsigned char UCHAR;
typedef UCHAR *PUCHAR;
typedef short SHORT;
typedef unsigned short USHORT;
typedef int HRESULT;
typedef int INT;
typedef int INT32;
typedef unsigned int UINT;
typedef unsigned int UINT32;
typedef long LONG;
typedef unsigned long ULONG;
typedef long long LONGLONG;
typedef unsigned long long ULONGLONG;
typedef unsigned char BYTE;
typedef unsigned short WORD;
typedef unsigned long DWORD;
typedef unsigned long long DWORD64;
typedef BYTE *PBYTE;
typedef BYTE *LPBYTE;
typedef int *PINT;
typedef int *PINT32;
typedef int *LPINT;
typedef WORD *PWORD;
typedef WORD *LPWORD;
typedef LONG *LPLONG;
typedef DWORD *PDWORD;
typedef DWORD *LPDWORD;
typedef DWORD64 *PDWORD64;
typedef ULONGLONG DWORDLONG;
typedef LONG *PLONG;
typedef ULONG *PULONG;
typedef UINT *PUINT;
typedef UINT32 *PUINT32;
typedef BOOL *PBOOL;
typedef VOID *PVOID;
typedef VOID *HWND;
typedef VOID *LPVOID;
typedef VOID *LPCVOID;
typedef VOID *FARPROC;
typedef VOID *NEARPROC;
typedef VOID *PROC;
typedef CHAR *PCHAR;
typedef CHAR *LPSTR;
typedef CHAR *LPCSTR;

#ifndef BUILTINS_WCHAR_DEFINED
#define BUILTINS_WCHAR_DEFINED
typedef unsigned short WCHAR;
typedef WCHAR *PWCHAR;
typedef WCHAR *LPWCH;
typedef WCHAR *PWCH;
typedef WCHAR *LPCWCH;
typedef WCHAR *PCWCH;
typedef WCHAR *PWSTR;
typedef WCHAR *LPWSTR;
typedef WCHAR *LPCWSTR;
typedef WCHAR *PCWSTR;
typedef LPWSTR *PZPWSTR;
#endif

#ifndef BUILTINS_TCHAR_DEFINED
#define BUILTINS_TCHAR_DEFINED
#ifdef UNICODE
typedef WCHAR TCHAR;
#else
typedef CHAR TCHAR;
#endif
typedef TCHAR *PTSTR;
typedef TCHAR *LPTSTR;
typedef TCHAR *LPCTSTR;
#endif

#ifndef _WIN32
typedef long long INT_PTR;
typedef long long LONG_PTR;
typedef unsigned long long UINT_PTR;
typedef unsigned long long ULONG_PTR;
#else
typedef int INT_PTR;
typedef long LONG_PTR;
typedef unsigned int UINT_PTR;
typedef unsigned long ULONG_PTR;
#endif
typedef ULONG_PTR DWORD_PTR;
typedef ULONG_PTR SIZE_T;
typedef UINT_PTR WPARAM;
typedef LONG_PTR LPARAM;
typedef LONG_PTR LRESULT;
typedef PVOID HANDLE;
typedef HANDLE *SPHANDLE;
typedef HANDLE *LPHANDLE;
typedef HANDLE HGLOBAL;
typedef HANDLE HLOCAL;
typedef HANDLE GLOBALHANDLE;
typedef HANDLE LOCALHANDLE;
typedef HANDLE HINSTANCE;
typedef HINSTANCE HMODULE;
typedef WORD ATOM;
typedef int HFILE;

typedef struct _FILETIME {
    DWORD dwLowDateTime;
    DWORD dwHighDateTime;
} FILETIME, *PFILETIME, *LPFILETIME;

typedef union _LARGE_INTEGER {
    struct {
        DWORD LowPart;
        LONG HighPart;
    } u;
    LONGLONG QuadPart;
} LARGE_INTEGER, *PLARGE_INTEGER;

typedef struct _SYSTEMTIME {
    WORD wYear;
    WORD wMonth;
    WORD wDayOfWeek;
    WORD wDay;
    WORD wHour;
    WORD wMinute;
    WORD wSecond;
    WORD wMilliseconds;
} SYSTEMTIME, *PSYSTEMTIME, *LPSYSTEMTIME;

#define _FILETIME_
#define MAX_PATH 260
#define TRUE 1
#define FALSE 0
#define NULL 0
#define IN
#define OUT
#define OPTIONAL
#define far
#define near
#define pascal
#define cdecl
#define NEAR
#define FAR
#define CALLBACK
#define WINAPI
#define WINAPIV
#define APIENTRY WINAPI
#define APIPRIVATE
#define CDECL
#define PASCAL
#define CONST
#define max(a,b) (((a) > (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))
#define MAKEWORD(a, b) ((WORD)(((BYTE)(((DWORD_PTR)(a)) & 0xff)) | ((WORD)((BYTE)(((DWORD_PTR)(b)) & 0xff))) << 8))
#define MAKELONG(a, b) ((LONG)(((WORD)(((DWORD_PTR)(a)) & 0xffff)) | ((DWORD)((WORD)(((DWORD_PTR)(b)) & 0xffff))) << 16))
#define LOWORD(l) ((WORD)(((DWORD_PTR)(l)) & 0xffff))
#define HIWORD(l) ((WORD)((((DWORD_PTR)(l)) >> 16) & 0xffff))
#define LOBYTE(w) ((BYTE)(((DWORD_PTR)(w)) & 0xff))
#define HIBYTE(w) ((BYTE)((((DWORD_PTR)(w)) >> 8) & 0xff))
#ifndef CONTAINING_RECORD
#define CONTAINING_RECORD(address, type, field) ((type *)((PCHAR)(address) - (ULONG_PTR)__builtin_offsetof(type, field)))
#endif
#define WIN32
#define STRICT 1

#endif
