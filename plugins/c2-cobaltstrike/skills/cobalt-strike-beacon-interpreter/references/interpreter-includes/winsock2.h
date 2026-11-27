#ifndef BUILTINS_WINSOCK2_H
#define BUILTINS_WINSOCK2_H

#include <winnt.h>

typedef unsigned char u_char;
typedef unsigned short u_short;
typedef unsigned int u_int;
typedef unsigned long u_long;

typedef UINT_PTR SOCKET;

#ifndef FD_SETSIZE
#define FD_SETSIZE 64
#endif

typedef struct fd_set {
    u_int fd_count;
    SOCKET fd_array[FD_SETSIZE];
} fd_set;

#ifndef BUILTINS_TIMEVAL_DEFINED
#define BUILTINS_TIMEVAL_DEFINED
struct timeval {
    long tv_sec;
    long tv_usec;
};
#endif

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

typedef struct in_addr {
    u_long s_addr;
} IN_ADDR, *PIN_ADDR, *LPIN_ADDR;

typedef struct sockaddr_in {
    short sin_family;
    u_short sin_port;
    IN_ADDR sin_addr;
    CHAR sin_zero[8];
} SOCKADDR_IN, *PSOCKADDR_IN, *LPSOCKADDR_IN;

typedef struct _WSABUF {
    ULONG len;
    CHAR *buf;
} WSABUF, *LPWSABUF;

struct linger {
    u_short l_onoff;
    u_short l_linger;
};

#define WSADESCRIPTION_LEN 256
#define WSASYS_STATUS_LEN 128

typedef struct WSAData64 {
    WORD wVersion;
    WORD wHighVersion;
    unsigned short iMaxSockets;
    unsigned short iMaxUdpDg;
    CHAR *lpVendorInfo;
    CHAR szDescription[WSADESCRIPTION_LEN + 1];
    CHAR szSystemStatus[WSASYS_STATUS_LEN + 1];
} WSADATA64, *LPWSADATA64;

typedef struct WSAData32 {
    WORD wVersion;
    WORD wHighVersion;
    CHAR szDescription[WSADESCRIPTION_LEN + 1];
    CHAR szSystemStatus[WSASYS_STATUS_LEN + 1];
    unsigned short iMaxSockets;
    unsigned short iMaxUdpDg;
    CHAR *lpVendorInfo;
} WSADATA32, *LPWSADATA32;

#ifndef _WIN32
typedef WSADATA64 WSADATA;
typedef LPWSADATA64 LPWSADATA;
#else
typedef WSADATA32 WSADATA;
typedef LPWSADATA32 LPWSADATA;
#endif

#define WINSOCK_VERSION MAKEWORD(2, 2)

#define INVALID_SOCKET    ((SOCKET)(~0))
#define SOCKET_ERROR      (-1)
#define FROM_PROTOCOL_INFO (-1)

#define AF_UNSPEC 0
#define AF_INET   2
#define AF_INET6  23

#define PF_UNSPEC AF_UNSPEC
#define PF_INET   AF_INET
#define PF_INET6  AF_INET6

#define SOCK_STREAM    1
#define SOCK_DGRAM     2
#define SOCK_RAW       3
#define SOCK_RDM       4
#define SOCK_SEQPACKET 5

#define SOL_SOCKET     0xffff
#define SOMAXCONN      0x7fffffff

#define SO_DEBUG       0x0001
#define SO_REUSEADDR   0x0004
#define SO_KEEPALIVE   0x0008
#define SO_BROADCAST   0x0020
#define SO_LINGER      0x0080
#define SO_SNDBUF      0x1001
#define SO_RCVBUF      0x1002
#define SO_ERROR       0x1007
#define SO_TYPE        0x1008

#define IPPROTO_IP      0
#define IPPROTO_ICMP    1
#define IPPROTO_TCP     6
#define IPPROTO_UDP     17
#define IPPROTO_IPV6    41

#define INADDR_ANY        ((u_long)0x00000000)
#define INADDR_LOOPBACK   ((u_long)0x7f000001)
#define INADDR_BROADCAST  ((u_long)0xffffffff)

#define MSG_OOB         0x1
#define MSG_PEEK        0x2
#define MSG_DONTROUTE   0x4

#define SD_RECEIVE 0x00
#define SD_SEND    0x01
#define SD_BOTH    0x02

#define FIONREAD   0x4004667f
#define FIONBIO    0x8004667e

#define WSABASEERR            10000
#define WSAEINTR              (WSABASEERR + 4)
#define WSAEBADF              (WSABASEERR + 9)
#define WSAEACCES             (WSABASEERR + 13)
#define WSAEFAULT             (WSABASEERR + 14)
#define WSAEINVAL             (WSABASEERR + 22)
#define WSAEMFILE             (WSABASEERR + 24)
#define WSAEWOULDBLOCK        (WSABASEERR + 35)
#define WSAEINPROGRESS        (WSABASEERR + 36)
#define WSAEALREADY           (WSABASEERR + 37)
#define WSAENOTSOCK           (WSABASEERR + 38)
#define WSAEDESTADDRREQ       (WSABASEERR + 39)
#define WSAEMSGSIZE           (WSABASEERR + 40)
#define WSAEPROTOTYPE         (WSABASEERR + 41)
#define WSAENOPROTOOPT        (WSABASEERR + 42)
#define WSAEPROTONOSUPPORT    (WSABASEERR + 43)
#define WSAESOCKTNOSUPPORT    (WSABASEERR + 44)
#define WSAEOPNOTSUPP         (WSABASEERR + 45)
#define WSAEPFNOSUPPORT       (WSABASEERR + 46)
#define WSAEAFNOSUPPORT       (WSABASEERR + 47)
#define WSAEADDRINUSE         (WSABASEERR + 48)
#define WSAEADDRNOTAVAIL      (WSABASEERR + 49)
#define WSAENETDOWN           (WSABASEERR + 50)
#define WSAENETUNREACH        (WSABASEERR + 51)
#define WSAENETRESET          (WSABASEERR + 52)
#define WSAECONNABORTED       (WSABASEERR + 53)
#define WSAECONNRESET         (WSABASEERR + 54)
#define WSAENOBUFS            (WSABASEERR + 55)
#define WSAEISCONN            (WSABASEERR + 56)
#define WSAENOTCONN           (WSABASEERR + 57)
#define WSAETIMEDOUT          (WSABASEERR + 60)
#define WSAECONNREFUSED       (WSABASEERR + 61)
#define WSAEHOSTUNREACH       (WSABASEERR + 65)

#endif
