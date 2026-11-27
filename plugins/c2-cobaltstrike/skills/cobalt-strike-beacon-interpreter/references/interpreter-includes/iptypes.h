#ifndef BUILTINS_IPTYPES_H
#define BUILTINS_IPTYPES_H

#include <winnt.h>
#include <ipifcons.h>

#define MAX_ADAPTER_DESCRIPTION_LENGTH  128
#define MAX_ADAPTER_NAME_LENGTH         256
#define MAX_ADAPTER_ADDRESS_LENGTH      8
#define DEFAULT_MINIMUM_ENTITIES        32
#define MAX_HOSTNAME_LEN                128
#define MAX_DOMAIN_NAME_LEN             128
#define MAX_SCOPE_ID_LEN                256
#define MAX_DHCPV6_DUID_LENGTH          130
#define MAX_DNS_SUFFIX_STRING_LENGTH    256

#define BROADCAST_NODETYPE              1
#define PEER_TO_PEER_NODETYPE           2
#define MIXED_NODETYPE                  4
#define HYBRID_NODETYPE                 8

typedef unsigned char UINT8;

#ifndef _TIME_T_DEFINED
/* Match UCRT behavior: 64-bit by default, optional 32-bit override. */
#ifdef _USE_32BIT_TIME_T
typedef long time_t;
#else
typedef long long time_t;
#endif
#define _TIME_T_DEFINED
#endif

#ifndef BUILTINS_IF_INDEX_DEFINED
#define BUILTINS_IF_INDEX_DEFINED
typedef ULONG IF_INDEX;
#endif
typedef ULONG IF_OPER_STATUS;
typedef ULONGLONG IF_LUID;
typedef ULONG NET_IF_COMPARTMENT_ID;
typedef GUID NET_IF_NETWORK_GUID;
typedef ULONG NET_IF_CONNECTION_TYPE;
typedef ULONG TUNNEL_TYPE;
typedef ULONG IP_PREFIX_ORIGIN;
typedef ULONG IP_SUFFIX_ORIGIN;
typedef ULONG IP_DAD_STATE;

#ifndef BUILTINS_SOCKADDR_DEFINED
#define BUILTINS_SOCKADDR_DEFINED
typedef struct _SOCKADDR {
    USHORT sa_family;
    CHAR sa_data[14];
} SOCKADDR, *PSOCKADDR, *LPSOCKADDR;
#endif

#ifndef BUILTINS_SOCKET_ADDRESS_DEFINED
#define BUILTINS_SOCKET_ADDRESS_DEFINED
typedef struct _SOCKET_ADDRESS {
    LPSOCKADDR lpSockaddr;
    INT iSockaddrLength;
} SOCKET_ADDRESS, *PSOCKET_ADDRESS;
#endif

typedef struct {
    CHAR String[4 * 4];
} IP_ADDRESS_STRING, *PIP_ADDRESS_STRING, IP_MASK_STRING, *PIP_MASK_STRING;

typedef struct _IP_ADDR_STRING {
    struct _IP_ADDR_STRING *Next;
    IP_ADDRESS_STRING IpAddress;
    IP_MASK_STRING IpMask;
    DWORD Context;
} IP_ADDR_STRING, *PIP_ADDR_STRING;

typedef struct _IP_ADAPTER_INFO {
    struct _IP_ADAPTER_INFO *Next;
    DWORD ComboIndex;
    CHAR AdapterName[MAX_ADAPTER_NAME_LENGTH + 4];
    CHAR Description[MAX_ADAPTER_DESCRIPTION_LENGTH + 4];
    UINT AddressLength;
    BYTE Address[MAX_ADAPTER_ADDRESS_LENGTH];
    DWORD Index;
    UINT Type;
    UINT DhcpEnabled;
    PIP_ADDR_STRING CurrentIpAddress;
    IP_ADDR_STRING IpAddressList;
    IP_ADDR_STRING GatewayList;
    IP_ADDR_STRING DhcpServer;
    BOOL HaveWins;
    IP_ADDR_STRING PrimaryWinsServer;
    IP_ADDR_STRING SecondaryWinsServer;
    time_t LeaseObtained;
    time_t LeaseExpires;
} IP_ADAPTER_INFO, *PIP_ADAPTER_INFO;

typedef struct _IP_ADAPTER_UNICAST_ADDRESS {
    ULONG Length;
    DWORD Flags;
    struct _IP_ADAPTER_UNICAST_ADDRESS *Next;
    SOCKET_ADDRESS Address;
    IP_PREFIX_ORIGIN PrefixOrigin;
    IP_SUFFIX_ORIGIN SuffixOrigin;
    IP_DAD_STATE DadState;
    ULONG ValidLifetime;
    ULONG PreferredLifetime;
    ULONG LeaseLifetime;
    UINT8 OnLinkPrefixLength;
} IP_ADAPTER_UNICAST_ADDRESS, *PIP_ADAPTER_UNICAST_ADDRESS;

typedef struct _IP_ADAPTER_ANYCAST_ADDRESS {
    ULONG Length;
    DWORD Flags;
    struct _IP_ADAPTER_ANYCAST_ADDRESS *Next;
    SOCKET_ADDRESS Address;
} IP_ADAPTER_ANYCAST_ADDRESS, *PIP_ADAPTER_ANYCAST_ADDRESS;

typedef struct _IP_ADAPTER_MULTICAST_ADDRESS {
    ULONG Length;
    DWORD Flags;
    struct _IP_ADAPTER_MULTICAST_ADDRESS *Next;
    SOCKET_ADDRESS Address;
} IP_ADAPTER_MULTICAST_ADDRESS, *PIP_ADAPTER_MULTICAST_ADDRESS;

typedef struct _IP_ADAPTER_DNS_SERVER_ADDRESS {
    ULONG Length;
    DWORD Reserved;
    struct _IP_ADAPTER_DNS_SERVER_ADDRESS *Next;
    SOCKET_ADDRESS Address;
} IP_ADAPTER_DNS_SERVER_ADDRESS, *PIP_ADAPTER_DNS_SERVER_ADDRESS;

typedef struct _IP_ADAPTER_WINS_SERVER_ADDRESS {
    ULONG Length;
    DWORD Reserved;
    struct _IP_ADAPTER_WINS_SERVER_ADDRESS *Next;
    SOCKET_ADDRESS Address;
} IP_ADAPTER_WINS_SERVER_ADDRESS, *PIP_ADAPTER_WINS_SERVER_ADDRESS;

typedef struct _IP_ADAPTER_GATEWAY_ADDRESS {
    ULONG Length;
    DWORD Reserved;
    struct _IP_ADAPTER_GATEWAY_ADDRESS *Next;
    SOCKET_ADDRESS Address;
} IP_ADAPTER_GATEWAY_ADDRESS, *PIP_ADAPTER_GATEWAY_ADDRESS;

typedef struct _IP_ADAPTER_PREFIX {
    ULONG Length;
    DWORD Flags;
    struct _IP_ADAPTER_PREFIX *Next;
    SOCKET_ADDRESS Address;
    ULONG PrefixLength;
} IP_ADAPTER_PREFIX, *PIP_ADAPTER_PREFIX;

typedef struct _IP_ADAPTER_DNS_SUFFIX {
    struct _IP_ADAPTER_DNS_SUFFIX *Next;
    WCHAR String[MAX_DNS_SUFFIX_STRING_LENGTH];
} IP_ADAPTER_DNS_SUFFIX, *PIP_ADAPTER_DNS_SUFFIX;

#define IP_ADAPTER_ADDRESS_DNS_ELIGIBLE        0x01
#define IP_ADAPTER_ADDRESS_TRANSIENT           0x02

#define IP_ADAPTER_DDNS_ENABLED                0x00000001
#define IP_ADAPTER_REGISTER_ADAPTER_SUFFIX     0x00000002
#define IP_ADAPTER_DHCP_ENABLED                0x00000004
#define IP_ADAPTER_RECEIVE_ONLY                0x00000008
#define IP_ADAPTER_NO_MULTICAST                0x00000010
#define IP_ADAPTER_IPV6_OTHER_STATEFUL_CONFIG  0x00000020
#define IP_ADAPTER_NETBIOS_OVER_TCPIP_ENABLED  0x00000040
#define IP_ADAPTER_IPV4_ENABLED                0x00000080
#define IP_ADAPTER_IPV6_ENABLED                0x00000100
#define IP_ADAPTER_IPV6_MANAGE_ADDRESS_CONFIG  0x00000200

typedef struct _IP_ADAPTER_ADDRESSES {
    ULONG Length;
    IF_INDEX IfIndex;
    struct _IP_ADAPTER_ADDRESSES *Next;
    PCHAR AdapterName;
    PIP_ADAPTER_UNICAST_ADDRESS FirstUnicastAddress;
    PIP_ADAPTER_ANYCAST_ADDRESS FirstAnycastAddress;
    PIP_ADAPTER_MULTICAST_ADDRESS FirstMulticastAddress;
    PIP_ADAPTER_DNS_SERVER_ADDRESS FirstDnsServerAddress;
    PWCHAR DnsSuffix;
    PWCHAR Description;
    PWCHAR FriendlyName;
    BYTE PhysicalAddress[MAX_ADAPTER_ADDRESS_LENGTH];
    ULONG PhysicalAddressLength;
    ULONG Flags;
    ULONG Mtu;
    IFTYPE IfType;
    IF_OPER_STATUS OperStatus;
    IF_INDEX Ipv6IfIndex;
    ULONG ZoneIndices[16];
    PIP_ADAPTER_PREFIX FirstPrefix;
    ULONGLONG TransmitLinkSpeed;
    ULONGLONG ReceiveLinkSpeed;
    PIP_ADAPTER_WINS_SERVER_ADDRESS FirstWinsServerAddress;
    PIP_ADAPTER_GATEWAY_ADDRESS FirstGatewayAddress;
    ULONG Ipv4Metric;
    ULONG Ipv6Metric;
    IF_LUID Luid;
    SOCKET_ADDRESS Dhcpv4Server;
    NET_IF_COMPARTMENT_ID CompartmentId;
    NET_IF_NETWORK_GUID NetworkGuid;
    NET_IF_CONNECTION_TYPE ConnectionType;
    TUNNEL_TYPE TunnelType;
    SOCKET_ADDRESS Dhcpv6Server;
    BYTE Dhcpv6ClientDuid[MAX_DHCPV6_DUID_LENGTH];
    ULONG Dhcpv6ClientDuidLength;
    ULONG Dhcpv6Iaid;
    PIP_ADAPTER_DNS_SUFFIX FirstDnsSuffix;
} IP_ADAPTER_ADDRESSES, *PIP_ADAPTER_ADDRESSES;

#define GAA_FLAG_SKIP_UNICAST                  0x0001
#define GAA_FLAG_SKIP_ANYCAST                  0x0002
#define GAA_FLAG_SKIP_MULTICAST                0x0004
#define GAA_FLAG_SKIP_DNS_SERVER               0x0008
#define GAA_FLAG_INCLUDE_PREFIX                0x0010
#define GAA_FLAG_SKIP_FRIENDLY_NAME            0x0020
#define GAA_FLAG_INCLUDE_WINS_INFO             0x0040
#define GAA_FLAG_INCLUDE_GATEWAYS              0x0080
#define GAA_FLAG_INCLUDE_ALL_INTERFACES        0x0100
#define GAA_FLAG_INCLUDE_ALL_COMPARTMENTS      0x0200
#define GAA_FLAG_INCLUDE_TUNNEL_BINDINGORDER   0x0400
#define GAA_FLAG_SKIP_DNS_INFO                 0x0800

typedef struct _IP_PER_ADAPTER_INFO {
    UINT AutoconfigEnabled;
    UINT AutoconfigActive;
    PIP_ADDR_STRING CurrentDnsServer;
    IP_ADDR_STRING DnsServerList;
} IP_PER_ADAPTER_INFO, *PIP_PER_ADAPTER_INFO;

typedef struct _FIXED_INFO {
    CHAR HostName[MAX_HOSTNAME_LEN + 4];
    CHAR DomainName[MAX_DOMAIN_NAME_LEN + 4];
    PIP_ADDR_STRING CurrentDnsServer;
    IP_ADDR_STRING DnsServerList;
    UINT NodeType;
    CHAR ScopeId[MAX_SCOPE_ID_LEN + 4];
    UINT EnableRouting;
    UINT EnableProxy;
    UINT EnableDns;
} FIXED_INFO, *PFIXED_INFO;

typedef struct _IP_INTERFACE_NAME_INFO {
    ULONG Index;
    ULONG MediaType;
    UCHAR ConnectionType;
    UCHAR AccessType;
    GUID DeviceGuid;
    GUID InterfaceGuid;
} IP_INTERFACE_NAME_INFO, *PIP_INTERFACE_NAME_INFO;

#endif
