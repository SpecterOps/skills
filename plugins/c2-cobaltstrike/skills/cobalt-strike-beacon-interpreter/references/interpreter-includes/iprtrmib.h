#ifndef BUILTINS_IPRTRMIB_H
#define BUILTINS_IPRTRMIB_H

#include <winnt.h>
#include <ipifcons.h>
#include <tcpmib.h>
#include <udpmib.h>

#ifndef ANY_SIZE
#define ANY_SIZE 1
#endif

#ifndef FIELD_OFFSET
#define FIELD_OFFSET(type, field) ((LONG)(LONG_PTR)&(((type *)0)->field))
#endif

#ifndef ALIGN_SIZE
#define ALIGN_SIZE (sizeof(DWORD))
#endif

#ifndef MAX_INTERFACE_NAME_LEN
#define MAX_INTERFACE_NAME_LEN 256
#endif

#ifndef BUILTINS_IF_INDEX_DEFINED
#define BUILTINS_IF_INDEX_DEFINED
typedef ULONG IF_INDEX;
#endif

#define IPRTRMGR_PID 10000

#define IF_NUMBER           0
#define IF_TABLE            (IF_NUMBER + 1)
#define IF_ROW              (IF_TABLE + 1)
#define IP_STATS            (IF_ROW + 1)
#define IP_ADDRTABLE        (IP_STATS + 1)
#define IP_ADDRROW          (IP_ADDRTABLE + 1)
#define IP_FORWARDNUMBER    (IP_ADDRROW + 1)
#define IP_FORWARDTABLE     (IP_FORWARDNUMBER + 1)
#define IP_FORWARDROW       (IP_FORWARDTABLE + 1)
#define IP_NETTABLE         (IP_FORWARDROW + 1)
#define IP_NETROW           (IP_NETTABLE + 1)
#define ICMP_STATS          (IP_NETROW + 1)
#define TCP_STATS           (ICMP_STATS + 1)
#define TCP_TABLE           (TCP_STATS + 1)
#define TCP_ROW             (TCP_TABLE + 1)
#define UDP_STATS           (TCP_ROW + 1)
#define UDP_TABLE           (UDP_STATS + 1)
#define UDP_ROW             (UDP_TABLE + 1)
#define MCAST_MFE           (UDP_ROW + 1)
#define MCAST_MFE_STATS     (MCAST_MFE + 1)
#define BEST_IF             (MCAST_MFE_STATS + 1)
#define BEST_ROUTE          (BEST_IF + 1)
#define PROXY_ARP           (BEST_ROUTE + 1)
#define MCAST_IF_ENTRY      (PROXY_ARP + 1)
#define MCAST_GLOBAL        (MCAST_IF_ENTRY + 1)
#define IF_STATUS           (MCAST_GLOBAL + 1)
#define MCAST_BOUNDARY      (IF_STATUS + 1)
#define MCAST_SCOPE         (MCAST_BOUNDARY + 1)
#define DEST_MATCHING       (MCAST_SCOPE + 1)
#define DEST_LONGER         (DEST_MATCHING + 1)
#define DEST_SHORTER        (DEST_LONGER + 1)
#define ROUTE_MATCHING      (DEST_SHORTER + 1)
#define ROUTE_LONGER        (ROUTE_MATCHING + 1)
#define ROUTE_SHORTER       (ROUTE_LONGER + 1)
#define ROUTE_STATE         (ROUTE_SHORTER + 1)
#define MCAST_MFE_STATS_EX  (ROUTE_STATE + 1)
#define IP6_STATS           (MCAST_MFE_STATS_EX + 1)
#define UDP6_STATS          (IP6_STATS + 1)
#define TCP6_STATS          (UDP6_STATS + 1)
#define NUMBER_OF_EXPORTED_VARIABLES (TCP6_STATS + 1)

typedef struct _MIB_OPAQUE_QUERY {
    DWORD dwVarId;
    DWORD rgdwVarIndex[ANY_SIZE];
} MIB_OPAQUE_QUERY, *PMIB_OPAQUE_QUERY;

typedef enum _TCP_TABLE_CLASS {
    TCP_TABLE_BASIC_LISTENER,
    TCP_TABLE_BASIC_CONNECTIONS,
    TCP_TABLE_BASIC_ALL,
    TCP_TABLE_OWNER_PID_LISTENER,
    TCP_TABLE_OWNER_PID_CONNECTIONS,
    TCP_TABLE_OWNER_PID_ALL,
    TCP_TABLE_OWNER_MODULE_LISTENER,
    TCP_TABLE_OWNER_MODULE_CONNECTIONS,
    TCP_TABLE_OWNER_MODULE_ALL
} TCP_TABLE_CLASS, *PTCP_TABLE_CLASS;

typedef enum _UDP_TABLE_CLASS {
    UDP_TABLE_BASIC,
    UDP_TABLE_OWNER_PID,
    UDP_TABLE_OWNER_MODULE
} UDP_TABLE_CLASS, *PUDP_TABLE_CLASS;

typedef enum _TCPIP_OWNER_MODULE_INFO_CLASS {
    TCPIP_OWNER_MODULE_INFO_BASIC
} TCPIP_OWNER_MODULE_INFO_CLASS, *PTCPIP_OWNER_MODULE_INFO_CLASS;

typedef struct _TCPIP_OWNER_MODULE_BASIC_INFO {
    PWSTR pModuleName;
    PWSTR pModulePath;
} TCPIP_OWNER_MODULE_BASIC_INFO, *PTCPIP_OWNER_MODULE_BASIC_INFO;

typedef struct _MIB_IPMCAST_BOUNDARY {
    DWORD dwIfIndex;
    DWORD dwGroupAddress;
    DWORD dwGroupMask;
    DWORD dwStatus;
} MIB_IPMCAST_BOUNDARY, *PMIB_IPMCAST_BOUNDARY;

typedef struct _MIB_IPMCAST_BOUNDARY_TABLE {
    DWORD dwNumEntries;
    MIB_IPMCAST_BOUNDARY table[ANY_SIZE];
} MIB_IPMCAST_BOUNDARY_TABLE, *PMIB_IPMCAST_BOUNDARY_TABLE;

#define SIZEOF_BOUNDARY_TABLE(X) (FIELD_OFFSET(MIB_IPMCAST_BOUNDARY_TABLE, table[0]) + ((X) * sizeof(MIB_IPMCAST_BOUNDARY)) + ALIGN_SIZE)

typedef struct _MIB_BOUNDARYROW {
    DWORD dwGroupAddress;
    DWORD dwGroupMask;
} MIB_BOUNDARYROW, *PMIB_BOUNDARYROW;

typedef struct _MIB_MCAST_LIMIT_ROW {
    DWORD dwTtl;
    DWORD dwRateLimit;
} MIB_MCAST_LIMIT_ROW, *PMIB_MCAST_LIMIT_ROW;

#define MAX_SCOPE_NAME_LEN 255
#define SN_UNICODE
typedef WCHAR SN_CHAR;
typedef SN_CHAR *SCOPE_NAME;

typedef struct _MIB_IPMCAST_SCOPE {
    DWORD dwGroupAddress;
    DWORD dwGroupMask;
    SN_CHAR snNameBuffer[MAX_SCOPE_NAME_LEN + 1];
    DWORD dwStatus;
} MIB_IPMCAST_SCOPE, *PMIB_IPMCAST_SCOPE;

typedef enum _MIB_IPFORWARD_TYPE {
    MIB_IPROUTE_TYPE_OTHER    = 1,
    MIB_IPROUTE_TYPE_INVALID  = 2,
    MIB_IPROUTE_TYPE_DIRECT   = 3,
    MIB_IPROUTE_TYPE_INDIRECT = 4
} MIB_IPFORWARD_TYPE;

typedef DWORD MIB_IPFORWARD_PROTO;

typedef struct _MIB_IPFORWARDROW {
    DWORD dwForwardDest;
    DWORD dwForwardMask;
    DWORD dwForwardPolicy;
    DWORD dwForwardNextHop;
    IF_INDEX dwForwardIfIndex;
    DWORD dwForwardType;
    DWORD dwForwardProto;
    DWORD dwForwardAge;
    DWORD dwForwardNextHopAS;
    DWORD dwForwardMetric1;
    DWORD dwForwardMetric2;
    DWORD dwForwardMetric3;
    DWORD dwForwardMetric4;
    DWORD dwForwardMetric5;
} MIB_IPFORWARDROW, *PMIB_IPFORWARDROW;

#define MIB_IPROUTE_METRIC_UNUSED ((DWORD)-1)

typedef struct _MIB_IPDESTROW {
    MIB_IPFORWARDROW ForwardRow;
    DWORD dwForwardPreference;
    DWORD dwForwardViewSet;
} MIB_IPDESTROW, *PMIB_IPDESTROW;

typedef struct _MIB_IPDESTTABLE {
    DWORD dwNumEntries;
    MIB_IPDESTROW table[ANY_SIZE];
} MIB_IPDESTTABLE, *PMIB_IPDESTTABLE;

typedef struct _MIB_BEST_IF {
    DWORD dwDestAddr;
    DWORD dwIfIndex;
} MIB_BEST_IF, *PMIB_BEST_IF;

typedef struct _MIB_PROXYARP {
    DWORD dwAddress;
    DWORD dwMask;
    DWORD dwIfIndex;
} MIB_PROXYARP, *PMIB_PROXYARP;

typedef struct _MIB_IFSTATUS {
    DWORD dwIfIndex;
    DWORD dwAdminStatus;
    DWORD dwOperationalStatus;
    BOOL bMHbeatActive;
    BOOL bMHbeatAlive;
} MIB_IFSTATUS, *PMIB_IFSTATUS;

typedef struct _MIB_ROUTESTATE {
    BOOL bRoutesSetToStack;
} MIB_ROUTESTATE, *PMIB_ROUTESTATE;

typedef struct _MIB_OPAQUE_INFO {
    DWORD dwId;
    BYTE rgbyData[1];
} MIB_OPAQUE_INFO, *PMIB_OPAQUE_INFO;

#define MAX_MIB_OFFSET 8

#define MIB_INFO_SIZE(S) (MAX_MIB_OFFSET + sizeof(S))
#define MIB_INFO_SIZE_IN_DWORDS(S) ((MIB_INFO_SIZE(S)) / sizeof(DWORD) + 1)

#define CAST_MIB_INFO(X, Y, Z) Z = (Y)(X->rgbyData)

#endif
