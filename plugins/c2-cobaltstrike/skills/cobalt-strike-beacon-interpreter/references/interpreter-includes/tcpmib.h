#ifndef BUILTINS_TCPMIB_H
#define BUILTINS_TCPMIB_H

#include <winnt.h>

#ifndef ANY_SIZE
#define ANY_SIZE 1
#endif

#ifndef FIELD_OFFSET
#define FIELD_OFFSET(type, field) ((LONG)(LONG_PTR)&(((type *)0)->field))
#endif

#ifndef ALIGN_SIZE
#define ALIGN_SIZE (sizeof(DWORD))
#endif

#ifndef TCPIP_OWNING_MODULE_SIZE
#define TCPIP_OWNING_MODULE_SIZE 16
#endif

typedef enum {
    MIB_TCP_STATE_CLOSED     = 1,
    MIB_TCP_STATE_LISTEN     = 2,
    MIB_TCP_STATE_SYN_SENT   = 3,
    MIB_TCP_STATE_SYN_RCVD   = 4,
    MIB_TCP_STATE_ESTAB      = 5,
    MIB_TCP_STATE_FIN_WAIT1  = 6,
    MIB_TCP_STATE_FIN_WAIT2  = 7,
    MIB_TCP_STATE_CLOSE_WAIT = 8,
    MIB_TCP_STATE_CLOSING    = 9,
    MIB_TCP_STATE_LAST_ACK   = 10,
    MIB_TCP_STATE_TIME_WAIT  = 11,
    MIB_TCP_STATE_DELETE_TCB = 12,
    MIB_TCP_STATE_RESERVED   = 100
} MIB_TCP_STATE;

typedef enum {
    TcpConnectionOffloadStateInHost = 0,
    TcpConnectionOffloadStateOffloading,
    TcpConnectionOffloadStateOffloaded,
    TcpConnectionOffloadStateUploading,
    TcpConnectionOffloadStateMax
} TCP_CONNECTION_OFFLOAD_STATE, *PTCP_CONNECTION_OFFLOAD_STATE;

typedef struct _MIB_TCPROW_LH {
    DWORD dwState;
    DWORD dwLocalAddr;
    DWORD dwLocalPort;
    DWORD dwRemoteAddr;
    DWORD dwRemotePort;
} MIB_TCPROW_LH, *PMIB_TCPROW_LH;

typedef struct _MIB_TCPROW_W2K {
    DWORD dwState;
    DWORD dwLocalAddr;
    DWORD dwLocalPort;
    DWORD dwRemoteAddr;
    DWORD dwRemotePort;
} MIB_TCPROW_W2K, *PMIB_TCPROW_W2K;

typedef MIB_TCPROW_LH MIB_TCPROW;
typedef MIB_TCPROW_LH *PMIB_TCPROW;

typedef struct _MIB_TCPTABLE {
    DWORD dwNumEntries;
    MIB_TCPROW table[ANY_SIZE];
} MIB_TCPTABLE, *PMIB_TCPTABLE;

#define SIZEOF_TCPTABLE(X) (FIELD_OFFSET(MIB_TCPTABLE, table[0]) + \
                            ((X) * sizeof(MIB_TCPROW)) + ALIGN_SIZE)

typedef struct _MIB_TCPROW2 {
    DWORD dwState;
    DWORD dwLocalAddr;
    DWORD dwLocalPort;
    DWORD dwRemoteAddr;
    DWORD dwRemotePort;
    DWORD dwOwningPid;
    TCP_CONNECTION_OFFLOAD_STATE dwOffloadState;
} MIB_TCPROW2, *PMIB_TCPROW2;

typedef struct _MIB_TCPTABLE2 {
    DWORD dwNumEntries;
    MIB_TCPROW2 table[ANY_SIZE];
} MIB_TCPTABLE2, *PMIB_TCPTABLE2;

#define SIZEOF_TCPTABLE2(X) (FIELD_OFFSET(MIB_TCPTABLE2, table[0]) + ((X) * sizeof(MIB_TCPROW2)) + ALIGN_SIZE)

typedef struct _MIB_TCPROW_OWNER_PID {
    DWORD dwState;
    DWORD dwLocalAddr;
    DWORD dwLocalPort;
    DWORD dwRemoteAddr;
    DWORD dwRemotePort;
    DWORD dwOwningPid;
} MIB_TCPROW_OWNER_PID, *PMIB_TCPROW_OWNER_PID;

typedef struct _MIB_TCPTABLE_OWNER_PID {
    DWORD dwNumEntries;
    MIB_TCPROW_OWNER_PID table[ANY_SIZE];
} MIB_TCPTABLE_OWNER_PID, *PMIB_TCPTABLE_OWNER_PID;

#define SIZEOF_TCPTABLE_OWNER_PID(X) (FIELD_OFFSET(MIB_TCPTABLE_OWNER_PID, table[0]) + ((X) * sizeof(MIB_TCPROW_OWNER_PID)) + ALIGN_SIZE)

typedef struct _MIB_TCPROW_OWNER_MODULE {
    DWORD dwState;
    DWORD dwLocalAddr;
    DWORD dwLocalPort;
    DWORD dwRemoteAddr;
    DWORD dwRemotePort;
    DWORD dwOwningPid;
    LARGE_INTEGER liCreateTimestamp;
    ULONGLONG OwningModuleInfo[TCPIP_OWNING_MODULE_SIZE];
} MIB_TCPROW_OWNER_MODULE, *PMIB_TCPROW_OWNER_MODULE;

typedef struct _MIB_TCPTABLE_OWNER_MODULE {
    DWORD dwNumEntries;
    MIB_TCPROW_OWNER_MODULE table[ANY_SIZE];
} MIB_TCPTABLE_OWNER_MODULE, *PMIB_TCPTABLE_OWNER_MODULE;

#define SIZEOF_TCPTABLE_OWNER_MODULE(X) (FIELD_OFFSET(MIB_TCPTABLE_OWNER_MODULE, table[0]) + ((X) * sizeof(MIB_TCPROW_OWNER_MODULE)) + ALIGN_SIZE)

#ifndef BUILTINS_IN6_ADDR_DEFINED
#define BUILTINS_IN6_ADDR_DEFINED
typedef struct _IN6_ADDR {
    UCHAR Byte[16];
} IN6_ADDR, *PIN6_ADDR;
#endif

typedef struct _MIB_TCP6ROW {
    MIB_TCP_STATE State;
    IN6_ADDR LocalAddr;
    DWORD dwLocalScopeId;
    DWORD dwLocalPort;
    IN6_ADDR RemoteAddr;
    DWORD dwRemoteScopeId;
    DWORD dwRemotePort;
} MIB_TCP6ROW, *PMIB_TCP6ROW;

typedef struct _MIB_TCP6TABLE {
    DWORD dwNumEntries;
    MIB_TCP6ROW table[ANY_SIZE];
} MIB_TCP6TABLE, *PMIB_TCP6TABLE;

#define SIZEOF_TCP6TABLE(X) (FIELD_OFFSET(MIB_TCP6TABLE, table[0]) + ((X) * sizeof(MIB_TCP6ROW)) + ALIGN_SIZE)

typedef struct _MIB_TCP6ROW2 {
    IN6_ADDR LocalAddr;
    DWORD dwLocalScopeId;
    DWORD dwLocalPort;
    IN6_ADDR RemoteAddr;
    DWORD dwRemoteScopeId;
    DWORD dwRemotePort;
    MIB_TCP_STATE State;
    DWORD dwOwningPid;
    TCP_CONNECTION_OFFLOAD_STATE dwOffloadState;
} MIB_TCP6ROW2, *PMIB_TCP6ROW2;

typedef struct _MIB_TCP6TABLE2 {
    DWORD dwNumEntries;
    MIB_TCP6ROW2 table[ANY_SIZE];
} MIB_TCP6TABLE2, *PMIB_TCP6TABLE2;

#define SIZEOF_TCP6TABLE2(X) (FIELD_OFFSET(MIB_TCP6TABLE2, table[0]) + ((X) * sizeof(MIB_TCP6ROW2)) + ALIGN_SIZE)

typedef struct _MIB_TCP6ROW_OWNER_PID {
    UCHAR ucLocalAddr[16];
    DWORD dwLocalScopeId;
    DWORD dwLocalPort;
    UCHAR ucRemoteAddr[16];
    DWORD dwRemoteScopeId;
    DWORD dwRemotePort;
    DWORD dwState;
    DWORD dwOwningPid;
} MIB_TCP6ROW_OWNER_PID, *PMIB_TCP6ROW_OWNER_PID;

typedef struct _MIB_TCP6TABLE_OWNER_PID {
    DWORD dwNumEntries;
    MIB_TCP6ROW_OWNER_PID table[ANY_SIZE];
} MIB_TCP6TABLE_OWNER_PID, *PMIB_TCP6TABLE_OWNER_PID;

#define SIZEOF_TCP6TABLE_OWNER_PID(X) (FIELD_OFFSET(MIB_TCP6TABLE_OWNER_PID, table[0]) + ((X) * sizeof(MIB_TCP6ROW_OWNER_PID)) + ALIGN_SIZE)

typedef struct _MIB_TCP6ROW_OWNER_MODULE {
    UCHAR ucLocalAddr[16];
    DWORD dwLocalScopeId;
    DWORD dwLocalPort;
    UCHAR ucRemoteAddr[16];
    DWORD dwRemoteScopeId;
    DWORD dwRemotePort;
    DWORD dwState;
    DWORD dwOwningPid;
    LARGE_INTEGER liCreateTimestamp;
    ULONGLONG OwningModuleInfo[TCPIP_OWNING_MODULE_SIZE];
} MIB_TCP6ROW_OWNER_MODULE, *PMIB_TCP6ROW_OWNER_MODULE;

typedef struct _MIB_TCP6TABLE_OWNER_MODULE {
    DWORD dwNumEntries;
    MIB_TCP6ROW_OWNER_MODULE table[ANY_SIZE];
} MIB_TCP6TABLE_OWNER_MODULE, *PMIB_TCP6TABLE_OWNER_MODULE;

#define SIZEOF_TCP6TABLE_OWNER_MODULE(X) (FIELD_OFFSET(MIB_TCP6TABLE_OWNER_MODULE, table[0]) + ((X) * sizeof(MIB_TCP6ROW_OWNER_MODULE)) + ALIGN_SIZE)

#define MIB_TCP_MAXCONN_DYNAMIC ((ULONG)-1)

typedef enum {
    TcpRtoAlgorithmOther    = 1,
    TcpRtoAlgorithmConstant = 2,
    TcpRtoAlgorithmRsre     = 3,
    TcpRtoAlgorithmVanj     = 4,
    MIB_TCP_RTO_OTHER       = 1,
    MIB_TCP_RTO_CONSTANT    = 2,
    MIB_TCP_RTO_RSRE        = 3,
    MIB_TCP_RTO_VANJ        = 4
} TCP_RTO_ALGORITHM, *PTCP_RTO_ALGORITHM;

typedef struct _MIB_TCPSTATS_LH {
    DWORD dwRtoAlgorithm;
    DWORD dwRtoMin;
    DWORD dwRtoMax;
    DWORD dwMaxConn;
    DWORD dwActiveOpens;
    DWORD dwPassiveOpens;
    DWORD dwAttemptFails;
    DWORD dwEstabResets;
    DWORD dwCurrEstab;
    DWORD dwInSegs;
    DWORD dwOutSegs;
    DWORD dwRetransSegs;
    DWORD dwInErrs;
    DWORD dwOutRsts;
    DWORD dwNumConns;
} MIB_TCPSTATS_LH, *PMIB_TCPSTATS_LH;

typedef struct _MIB_TCPSTATS_W2K {
    DWORD dwRtoAlgorithm;
    DWORD dwRtoMin;
    DWORD dwRtoMax;
    DWORD dwMaxConn;
    DWORD dwActiveOpens;
    DWORD dwPassiveOpens;
    DWORD dwAttemptFails;
    DWORD dwEstabResets;
    DWORD dwCurrEstab;
    DWORD dwInSegs;
    DWORD dwOutSegs;
    DWORD dwRetransSegs;
    DWORD dwInErrs;
    DWORD dwOutRsts;
    DWORD dwNumConns;
} MIB_TCPSTATS_W2K, *PMIB_TCPSTATS_W2K;

typedef MIB_TCPSTATS_LH MIB_TCPSTATS;
typedef MIB_TCPSTATS_LH *PMIB_TCPSTATS;

typedef struct _MIB_TCPSTATS2 {
    TCP_RTO_ALGORITHM RtoAlgorithm;
    DWORD dwRtoMin;
    DWORD dwRtoMax;
    DWORD dwMaxConn;
    DWORD dwActiveOpens;
    DWORD dwPassiveOpens;
    DWORD dwAttemptFails;
    DWORD dwEstabResets;
    DWORD dwCurrEstab;
    ULONGLONG dw64InSegs;
    ULONGLONG dw64OutSegs;
    DWORD dwRetransSegs;
    DWORD dwInErrs;
    DWORD dwOutRsts;
    DWORD dwNumConns;
} MIB_TCPSTATS2, *PMIB_TCPSTATS2;

#endif
