#ifndef BUILTINS_WINREG_H
#define BUILTINS_WINREG_H

#include <winnt.h>

#ifndef __cdecl
#define __cdecl cdecl
#endif

#ifndef WINVER
#define WINVER 0x0500
#endif

#ifndef BUILTINS_ACCESS_MASK_DEFINED
#define BUILTINS_ACCESS_MASK_DEFINED
typedef DWORD ACCESS_MASK;
typedef ACCESS_MASK *PACCESS_MASK;
#endif

typedef LONG LSTATUS;
typedef ACCESS_MASK REGSAM;
typedef HANDLE HKEY;
typedef HKEY *PHKEY;

/* RRF - Registry Routine Flags (for RegGetValue) */
#define RRF_RT_REG_NONE        0x00000001
#define RRF_RT_REG_SZ          0x00000002
#define RRF_RT_REG_EXPAND_SZ   0x00000004
#define RRF_RT_REG_BINARY      0x00000008
#define RRF_RT_REG_DWORD       0x00000010
#define RRF_RT_REG_MULTI_SZ    0x00000020
#define RRF_RT_REG_QWORD       0x00000040
#define RRF_RT_DWORD           (RRF_RT_REG_BINARY | RRF_RT_REG_DWORD)
#define RRF_RT_QWORD           (RRF_RT_REG_BINARY | RRF_RT_REG_QWORD)
#define RRF_RT_ANY             0x0000ffff
#define RRF_SUBKEY_WOW6464KEY  0x00010000
#define RRF_SUBKEY_WOW6432KEY  0x00020000
#define RRF_WOW64_MASK         0x00030000
#define RRF_NOEXPAND           0x10000000
#define RRF_ZEROONFAILURE      0x20000000

/* Flags for RegLoadAppKey */
#define REG_PROCESS_APPKEY                  0x00000001
#define REG_USE_CURRENT_SECURITY_CONTEXT    0x00000002

/* Reserved key handles */
#define HKEY_CLASSES_ROOT                ((HKEY)(ULONG_PTR)((LONG)0x80000000))
#define HKEY_CURRENT_USER                ((HKEY)(ULONG_PTR)((LONG)0x80000001))
#define HKEY_LOCAL_MACHINE               ((HKEY)(ULONG_PTR)((LONG)0x80000002))
#define HKEY_USERS                       ((HKEY)(ULONG_PTR)((LONG)0x80000003))
#define HKEY_PERFORMANCE_DATA            ((HKEY)(ULONG_PTR)((LONG)0x80000004))
#define HKEY_PERFORMANCE_TEXT            ((HKEY)(ULONG_PTR)((LONG)0x80000050))
#define HKEY_PERFORMANCE_NLSTEXT         ((HKEY)(ULONG_PTR)((LONG)0x80000060))
#define HKEY_CURRENT_CONFIG              ((HKEY)(ULONG_PTR)((LONG)0x80000005))
#define HKEY_DYN_DATA                    ((HKEY)(ULONG_PTR)((LONG)0x80000006))
#define HKEY_CURRENT_USER_LOCAL_SETTINGS ((HKEY)(ULONG_PTR)((LONG)0x80000007))

/* Common aliases */
#define HKCR HKEY_CLASSES_ROOT
#define HKCU HKEY_CURRENT_USER
#define HKLM HKEY_LOCAL_MACHINE
#define HKU  HKEY_USERS
#define HKCC HKEY_CURRENT_CONFIG

/* Registry specific access rights */
#define KEY_QUERY_VALUE         (0x0001)
#define KEY_SET_VALUE           (0x0002)
#define KEY_CREATE_SUB_KEY      (0x0004)
#define KEY_ENUMERATE_SUB_KEYS  (0x0008)
#define KEY_NOTIFY              (0x0010)
#define KEY_CREATE_LINK         (0x0020)
#define KEY_WOW64_32KEY         (0x0200)
#define KEY_WOW64_64KEY         (0x0100)
#define KEY_WOW64_RES           (0x0300)

#define KEY_READ ((STANDARD_RIGHTS_READ | KEY_QUERY_VALUE | KEY_ENUMERATE_SUB_KEYS | KEY_NOTIFY) & (~SYNCHRONIZE))
#define KEY_WRITE ((STANDARD_RIGHTS_WRITE | KEY_SET_VALUE | KEY_CREATE_SUB_KEY) & (~SYNCHRONIZE))
#define KEY_EXECUTE ((KEY_READ) & (~SYNCHRONIZE))
#define KEY_ALL_ACCESS ((STANDARD_RIGHTS_ALL | KEY_QUERY_VALUE | KEY_SET_VALUE | KEY_CREATE_SUB_KEY | KEY_ENUMERATE_SUB_KEYS | KEY_NOTIFY | KEY_CREATE_LINK) & (~SYNCHRONIZE))

/* Open/Create options */
#define REG_OPTION_RESERVED             (0x00000000L)
#define REG_OPTION_NON_VOLATILE         (0x00000000L)
#define REG_OPTION_VOLATILE             (0x00000001L)
#define REG_OPTION_CREATE_LINK          (0x00000002L)
#define REG_OPTION_BACKUP_RESTORE       (0x00000004L)
#define REG_OPTION_OPEN_LINK            (0x00000008L)
#define REG_OPTION_DONT_VIRTUALIZE      (0x00000010L)

#define REG_LEGAL_OPTION (REG_OPTION_RESERVED | REG_OPTION_NON_VOLATILE | REG_OPTION_VOLATILE | REG_OPTION_CREATE_LINK | REG_OPTION_BACKUP_RESTORE | REG_OPTION_OPEN_LINK | REG_OPTION_DONT_VIRTUALIZE)
#define REG_OPEN_LEGAL_OPTION (REG_OPTION_RESERVED | REG_OPTION_BACKUP_RESTORE | REG_OPTION_OPEN_LINK | REG_OPTION_DONT_VIRTUALIZE)

/* Key creation/open disposition */
#define REG_CREATED_NEW_KEY         (0x00000001L)
#define REG_OPENED_EXISTING_KEY     (0x00000002L)

/* Hive format for RegSaveKeyEx */
#define REG_STANDARD_FORMAT     1
#define REG_LATEST_FORMAT       2
#define REG_NO_COMPRESSION      4

/* Key restore & hive load flags */
#define REG_WHOLE_HIVE_VOLATILE         (0x00000001L)
#define REG_REFRESH_HIVE                (0x00000002L)
#define REG_NO_LAZY_FLUSH               (0x00000004L)
#define REG_FORCE_RESTORE               (0x00000008L)
#define REG_APP_HIVE                    (0x00000010L)
#define REG_PROCESS_PRIVATE             (0x00000020L)
#define REG_START_JOURNAL               (0x00000040L)
#define REG_HIVE_EXACT_FILE_GROWTH      (0x00000080L)
#define REG_HIVE_NO_RM                  (0x00000100L)
#define REG_HIVE_SINGLE_LOG             (0x00000200L)
#define REG_BOOT_HIVE                   (0x00000400L)
#define REG_LOAD_HIVE_OPEN_HANDLE       (0x00000800L)
#define REG_FLUSH_HIVE_FILE_GROWTH      (0x00001000L)
#define REG_OPEN_READ_ONLY              (0x00002000L)
#define REG_IMMUTABLE                   (0x00004000L)
#define REG_NO_IMPERSONATION_FALLBACK   (0x00008000L)
#define REG_APP_HIVE_OPEN_READ_ONLY     (REG_OPEN_READ_ONLY)

/* Unload flags */
#define REG_FORCE_UNLOAD            1
#define REG_UNLOAD_LEGAL_FLAGS      (REG_FORCE_UNLOAD)

/* Notify filter values */
#define REG_NOTIFY_CHANGE_NAME          (0x00000001L)
#define REG_NOTIFY_CHANGE_ATTRIBUTES    (0x00000002L)
#define REG_NOTIFY_CHANGE_LAST_SET      (0x00000004L)
#define REG_NOTIFY_CHANGE_SECURITY      (0x00000008L)
#define REG_NOTIFY_THREAD_AGNOSTIC      (0x10000000L)

#define REG_LEGAL_CHANGE_FILTER (REG_NOTIFY_CHANGE_NAME | REG_NOTIFY_CHANGE_ATTRIBUTES | REG_NOTIFY_CHANGE_LAST_SET | REG_NOTIFY_CHANGE_SECURITY | REG_NOTIFY_THREAD_AGNOSTIC)

/* Predefined value types */
#define REG_NONE                     (0ul)
#define REG_SZ                       (1ul)
#define REG_EXPAND_SZ                (2ul)
#define REG_BINARY                   (3ul)
#define REG_DWORD                    (4ul)
#define REG_DWORD_LITTLE_ENDIAN      (4ul)
#define REG_DWORD_BIG_ENDIAN         (5ul)
#define REG_LINK                     (6ul)
#define REG_MULTI_SZ                 (7ul)
#define REG_RESOURCE_LIST            (8ul)
#define REG_FULL_RESOURCE_DESCRIPTOR (9ul)
#define REG_RESOURCE_REQUIREMENTS_LIST (10ul)
#define REG_QWORD                    (11ul)
#define REG_QWORD_LITTLE_ENDIAN      (11ul)

#define PROVIDER_KEEPS_VALUE_LENGTH 0x1

struct val_context {
    int valuelen;
    LPVOID value_context;
    LPVOID val_buff_ptr;
};
typedef struct val_context *PVALCONTEXT;

typedef struct pvalueA {
    LPSTR pv_valuename;
    int pv_valuelen;
    LPVOID pv_value_context;
    DWORD pv_type;
} PVALUEA, *PPVALUEA;

typedef struct pvalueW {
    LPWSTR pv_valuename;
    int pv_valuelen;
    LPVOID pv_value_context;
    DWORD pv_type;
} PVALUEW, *PPVALUEW;

typedef PVOID PQUERYHANDLER;

typedef struct provider_info {
    PQUERYHANDLER pi_R0_1val;
    PQUERYHANDLER pi_R0_allvals;
    PQUERYHANDLER pi_R3_1val;
    PQUERYHANDLER pi_R3_allvals;
    DWORD pi_flags;
    LPVOID pi_key_context;
} REG_PROVIDER, *PPROVIDER;

typedef struct value_entA {
    LPSTR ve_valuename;
    DWORD ve_valuelen;
    DWORD_PTR ve_valueptr;
    DWORD ve_type;
} VALENTA, *PVALENTA;

typedef struct value_entW {
    LPWSTR ve_valuename;
    DWORD ve_valuelen;
    DWORD_PTR ve_valueptr;
    DWORD ve_type;
} VALENTW, *PVALENTW;

#ifdef UNICODE
typedef PVALUEW PVALUE;
typedef PPVALUEW PPVALUE;
typedef VALENTW VALENT;
typedef PVALENTW PVALENT;
#else
typedef PVALUEA PVALUE;
typedef PPVALUEA PPVALUE;
typedef VALENTA VALENT;
typedef PVALENTA PVALENT;
#endif

#define WIN31_CLASS             NULL
#define REG_MUI_STRING_TRUNCATE 0x00000001
#define REG_SECURE_CONNECTION   1

#endif
