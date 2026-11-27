#ifndef BUILTINS_WTSAPI32_H
#define BUILTINS_WTSAPI32_H

#include <winnt.h>

/* Current server/session sentinels */
#define WTS_CURRENT_SERVER         ((HANDLE)NULL)
#define WTS_CURRENT_SERVER_HANDLE  ((HANDLE)NULL)
#define WTS_CURRENT_SERVER_NAME    (NULL)
#define WTS_CURRENT_SESSION        ((DWORD)-1)
#define WTS_ANY_SESSION            ((DWORD)-2)

/* WTSSendMessage response values */
#ifndef IDTIMEOUT
#define IDTIMEOUT 32000
#endif
#ifndef IDASYNC
#define IDASYNC   32001
#endif

#ifndef __HYDRIX_H__
#define USERNAME_LENGTH      20
#define CLIENTNAME_LENGTH    20
#define CLIENTADDRESS_LENGTH 30
#endif

/* Shutdown flags */
#define WTS_WSD_LOGOFF      0x00000001
#define WTS_WSD_SHUTDOWN    0x00000002
#define WTS_WSD_REBOOT      0x00000004
#define WTS_WSD_POWEROFF    0x00000008
#define WTS_WSD_FASTREBOOT  0x00000010

#define MAX_ELAPSED_TIME_LENGTH 15
#define MAX_DATE_TIME_LENGTH    56
#define WINSTATIONNAME_LENGTH   32
#define DOMAIN_LENGTH           17

#define WTS_DRIVE_LENGTH         3
#define WTS_LISTENER_NAME_LENGTH 32
#define WTS_COMMENT_LENGTH       60

/* Listener creation flags */
#define WTS_LISTENER_CREATE 0x00000001
#define WTS_LISTENER_UPDATE 0x00000010

/* Listener access values */
#define WTS_SECURITY_QUERY_INFORMATION 0x00000001
#define WTS_SECURITY_SET_INFORMATION   0x00000002
#define WTS_SECURITY_RESET             0x00000004
#define WTS_SECURITY_VIRTUAL_CHANNELS  0x00000008
#define WTS_SECURITY_REMOTE_CONTROL    0x00000010
#define WTS_SECURITY_LOGON             0x00000020
#define WTS_SECURITY_LOGOFF            0x00000040
#define WTS_SECURITY_MESSAGE           0x00000080
#define WTS_SECURITY_CONNECT           0x00000100
#define WTS_SECURITY_DISCONNECT        0x00000200

#define WTS_SECURITY_GUEST_ACCESS (WTS_SECURITY_LOGON)
#define WTS_SECURITY_CURRENT_GUEST_ACCESS (WTS_SECURITY_VIRTUAL_CHANNELS | WTS_SECURITY_LOGOFF)
#define WTS_SECURITY_USER_ACCESS (WTS_SECURITY_CURRENT_GUEST_ACCESS | WTS_SECURITY_QUERY_INFORMATION | WTS_SECURITY_CONNECT)
#define WTS_SECURITY_CURRENT_USER_ACCESS (WTS_SECURITY_SET_INFORMATION | WTS_SECURITY_RESET | WTS_SECURITY_VIRTUAL_CHANNELS | WTS_SECURITY_LOGOFF | WTS_SECURITY_DISCONNECT)
#define WTS_SECURITY_ALL_ACCESS (STANDARD_RIGHTS_REQUIRED | WTS_SECURITY_QUERY_INFORMATION | WTS_SECURITY_SET_INFORMATION | WTS_SECURITY_RESET | WTS_SECURITY_VIRTUAL_CHANNELS | WTS_SECURITY_REMOTE_CONTROL | WTS_SECURITY_LOGON | WTS_SECURITY_MESSAGE | WTS_SECURITY_CONNECT | WTS_SECURITY_DISCONNECT)

typedef enum _WTS_CONNECTSTATE_CLASS {
    WTSActive,
    WTSConnected,
    WTSConnectQuery,
    WTSShadow,
    WTSDisconnected,
    WTSIdle,
    WTSListen,
    WTSReset,
    WTSDown,
    WTSInit
} WTS_CONNECTSTATE_CLASS;

typedef struct _WTS_SERVER_INFOW {
    LPWSTR pServerName;
} WTS_SERVER_INFOW, *PWTS_SERVER_INFOW;

typedef struct _WTS_SERVER_INFOA {
    LPSTR pServerName;
} WTS_SERVER_INFOA, *PWTS_SERVER_INFOA;

typedef WTS_SERVER_INFOA WTS_SERVER_INFO;
typedef PWTS_SERVER_INFOA PWTS_SERVER_INFO;

typedef struct _WTS_SESSION_INFOW {
    DWORD SessionId;
    LPWSTR pWinStationName;
    WTS_CONNECTSTATE_CLASS State;
} WTS_SESSION_INFOW, *PWTS_SESSION_INFOW;

typedef struct _WTS_SESSION_INFOA {
    DWORD SessionId;
    LPSTR pWinStationName;
    WTS_CONNECTSTATE_CLASS State;
} WTS_SESSION_INFOA, *PWTS_SESSION_INFOA;

typedef struct _WTS_SESSION_INFO_1W {
    DWORD ExecEnvId;
    WTS_CONNECTSTATE_CLASS State;
    DWORD SessionId;
    LPWSTR pSessionName;
    LPWSTR pHostName;
    LPWSTR pUserName;
    LPWSTR pDomainName;
    LPWSTR pFarmName;
} WTS_SESSION_INFO_1W, *PWTS_SESSION_INFO_1W;

typedef struct _WTS_SESSION_INFO_1A {
    DWORD ExecEnvId;
    WTS_CONNECTSTATE_CLASS State;
    DWORD SessionId;
    LPSTR pSessionName;
    LPSTR pHostName;
    LPSTR pUserName;
    LPSTR pDomainName;
    LPSTR pFarmName;
} WTS_SESSION_INFO_1A, *PWTS_SESSION_INFO_1A;

typedef WTS_SESSION_INFOA WTS_SESSION_INFO;
typedef PWTS_SESSION_INFOA PWTS_SESSION_INFO;
typedef WTS_SESSION_INFO_1A WTS_SESSION_INFO_1;
typedef PWTS_SESSION_INFO_1A PWTS_SESSION_INFO_1;

typedef struct _WTS_PROCESS_INFOW {
    DWORD SessionId;
    DWORD ProcessId;
    LPWSTR pProcessName;
    PSID pUserSid;
} WTS_PROCESS_INFOW, *PWTS_PROCESS_INFOW;

typedef struct _WTS_PROCESS_INFOA {
    DWORD SessionId;
    DWORD ProcessId;
    LPSTR pProcessName;
    PSID pUserSid;
} WTS_PROCESS_INFOA, *PWTS_PROCESS_INFOA;

typedef WTS_PROCESS_INFOA WTS_PROCESS_INFO;
typedef PWTS_PROCESS_INFOA PWTS_PROCESS_INFO;

#define WTS_PROTOCOL_TYPE_CONSOLE 0
#define WTS_PROTOCOL_TYPE_ICA     1
#define WTS_PROTOCOL_TYPE_RDP     2

typedef enum _WTS_INFO_CLASS {
    WTSInitialProgram,
    WTSApplicationName,
    WTSWorkingDirectory,
    WTSOEMId,
    WTSSessionId,
    WTSUserName,
    WTSWinStationName,
    WTSDomainName,
    WTSConnectState,
    WTSClientBuildNumber,
    WTSClientName,
    WTSClientDirectory,
    WTSClientProductId,
    WTSClientHardwareId,
    WTSClientAddress,
    WTSClientDisplay,
    WTSClientProtocolType,
    WTSIdleTime,
    WTSLogonTime,
    WTSIncomingBytes,
    WTSOutgoingBytes,
    WTSIncomingFrames,
    WTSOutgoingFrames,
    WTSClientInfo,
    WTSSessionInfo,
    WTSSessionInfoEx,
    WTSConfigInfo,
    WTSValidationInfo,
    WTSSessionAddressV4,
    WTSIsRemoteSession
} WTS_INFO_CLASS;

typedef struct _WTSCONFIGINFOW {
    ULONG version;
    ULONG fConnectClientDrivesAtLogon;
    ULONG fConnectPrinterAtLogon;
    ULONG fDisablePrinterRedirection;
    ULONG fDisableDefaultMainClientPrinter;
    ULONG ShadowSettings;
    WCHAR LogonUserName[USERNAME_LENGTH + 1];
    WCHAR LogonDomain[DOMAIN_LENGTH + 1];
    WCHAR WorkDirectory[MAX_PATH + 1];
    WCHAR InitialProgram[MAX_PATH + 1];
    WCHAR ApplicationName[MAX_PATH + 1];
} WTSCONFIGINFOW, *PWTSCONFIGINFOW;

typedef struct _WTSCONFIGINFOA {
    ULONG version;
    ULONG fConnectClientDrivesAtLogon;
    ULONG fConnectPrinterAtLogon;
    ULONG fDisablePrinterRedirection;
    ULONG fDisableDefaultMainClientPrinter;
    ULONG ShadowSettings;
    CHAR LogonUserName[USERNAME_LENGTH + 1];
    CHAR LogonDomain[DOMAIN_LENGTH + 1];
    CHAR WorkDirectory[MAX_PATH + 1];
    CHAR InitialProgram[MAX_PATH + 1];
    CHAR ApplicationName[MAX_PATH + 1];
} WTSCONFIGINFOA, *PWTSCONFIGINFOA;

typedef struct _WTSINFOW {
    WTS_CONNECTSTATE_CLASS State;
    DWORD SessionId;
    DWORD IncomingBytes;
    DWORD OutgoingBytes;
    DWORD IncomingFrames;
    DWORD OutgoingFrames;
    DWORD IncomingCompressedBytes;
    DWORD OutgoingCompressedBytes;
    WCHAR WinStationName[WINSTATIONNAME_LENGTH];
    WCHAR Domain[DOMAIN_LENGTH];
    WCHAR UserName[USERNAME_LENGTH + 1];
    LARGE_INTEGER ConnectTime;
    LARGE_INTEGER DisconnectTime;
    LARGE_INTEGER LastInputTime;
    LARGE_INTEGER LogonTime;
    LARGE_INTEGER CurrentTime;
} WTSINFOW, *PWTSINFOW;

typedef struct _WTSINFOA {
    WTS_CONNECTSTATE_CLASS State;
    DWORD SessionId;
    DWORD IncomingBytes;
    DWORD OutgoingBytes;
    DWORD IncomingFrames;
    DWORD OutgoingFrames;
    DWORD IncomingCompressedBytes;
    DWORD OutgoingCompressedBy;
    CHAR WinStationName[WINSTATIONNAME_LENGTH];
    CHAR Domain[DOMAIN_LENGTH];
    CHAR UserName[USERNAME_LENGTH + 1];
    LARGE_INTEGER ConnectTime;
    LARGE_INTEGER DisconnectTime;
    LARGE_INTEGER LastInputTime;
    LARGE_INTEGER LogonTime;
    LARGE_INTEGER CurrentTime;
} WTSINFOA, *PWTSINFOA;

#define WTS_SESSIONSTATE_UNKNOWN 0xFFFFFFFF
#define WTS_SESSIONSTATE_LOCK    0x00000000
#define WTS_SESSIONSTATE_UNLOCK  0x00000001

typedef struct _WTSINFOEX_LEVEL1_W {
    ULONG SessionId;
    WTS_CONNECTSTATE_CLASS SessionState;
    LONG SessionFlags;
    WCHAR WinStationName[WINSTATIONNAME_LENGTH + 1];
    WCHAR UserName[USERNAME_LENGTH + 1];
    WCHAR DomainName[DOMAIN_LENGTH + 1];
    LARGE_INTEGER LogonTime;
    LARGE_INTEGER ConnectTime;
    LARGE_INTEGER DisconnectTime;
    LARGE_INTEGER LastInputTime;
    LARGE_INTEGER CurrentTime;
    DWORD IncomingBytes;
    DWORD OutgoingBytes;
    DWORD IncomingFrames;
    DWORD OutgoingFrames;
    DWORD IncomingCompressedBytes;
    DWORD OutgoingCompressedBytes;
} WTSINFOEX_LEVEL1_W, *PWTSINFOEX_LEVEL1_W;

typedef struct _WTSINFOEX_LEVEL1_A {
    ULONG SessionId;
    WTS_CONNECTSTATE_CLASS SessionState;
    LONG SessionFlags;
    CHAR WinStationName[WINSTATIONNAME_LENGTH + 1];
    CHAR UserName[USERNAME_LENGTH + 1];
    CHAR DomainName[DOMAIN_LENGTH + 1];
    LARGE_INTEGER LogonTime;
    LARGE_INTEGER ConnectTime;
    LARGE_INTEGER DisconnectTime;
    LARGE_INTEGER LastInputTime;
    LARGE_INTEGER CurrentTime;
    DWORD IncomingBytes;
    DWORD OutgoingBytes;
    DWORD IncomingFrames;
    DWORD OutgoingFrames;
    DWORD IncomingCompressedBytes;
    DWORD OutgoingCompressedBytes;
} WTSINFOEX_LEVEL1_A, *PWTSINFOEX_LEVEL1_A;

typedef union _WTSINFOEX_LEVEL_W {
    WTSINFOEX_LEVEL1_W WTSInfoExLevel1;
} WTSINFOEX_LEVEL_W, *PWTSINFOEX_LEVEL_W;

typedef union _WTSINFOEX_LEVEL_A {
    WTSINFOEX_LEVEL1_A WTSInfoExLevel1;
} WTSINFOEX_LEVEL_A, *PWTSINFOEX_LEVEL_A;

typedef struct _WTSINFOEXW {
    DWORD Level;
    WTSINFOEX_LEVEL_W Data;
} WTSINFOEXW, *PWTSINFOEXW;

typedef struct _WTSINFOEXA {
    DWORD Level;
    WTSINFOEX_LEVEL_A Data;
} WTSINFOEXA, *PWTSINFOEXA;

typedef struct _WTSCLIENTW {
    WCHAR ClientName[CLIENTNAME_LENGTH + 1];
    WCHAR Domain[DOMAIN_LENGTH + 1];
    WCHAR UserName[USERNAME_LENGTH + 1];
    WCHAR WorkDirectory[MAX_PATH + 1];
    WCHAR InitialProgram[MAX_PATH + 1];
    BYTE EncryptionLevel;
    ULONG ClientAddressFamily;
    USHORT ClientAddress[CLIENTADDRESS_LENGTH + 1];
    USHORT HRes;
    USHORT VRes;
    USHORT ColorDepth;
    WCHAR ClientDirectory[MAX_PATH + 1];
    ULONG ClientBuildNumber;
    ULONG ClientHardwareId;
    USHORT ClientProductId;
    USHORT OutBufCountHost;
    USHORT OutBufCountClient;
    USHORT OutBufLength;
    WCHAR DeviceId[MAX_PATH + 1];
} WTSCLIENTW, *PWTSCLIENTW;

typedef struct _WTSCLIENTA {
    CHAR ClientName[CLIENTNAME_LENGTH + 1];
    CHAR Domain[DOMAIN_LENGTH + 1];
    CHAR UserName[USERNAME_LENGTH + 1];
    CHAR WorkDirectory[MAX_PATH + 1];
    CHAR InitialProgram[MAX_PATH + 1];
    BYTE EncryptionLevel;
    ULONG ClientAddressFamily;
    USHORT ClientAddress[CLIENTADDRESS_LENGTH + 1];
    USHORT HRes;
    USHORT VRes;
    USHORT ColorDepth;
    CHAR ClientDirectory[MAX_PATH + 1];
    ULONG ClientBuildNumber;
    ULONG ClientHardwareId;
    USHORT ClientProductId;
    USHORT OutBufCountHost;
    USHORT OutBufCountClient;
    USHORT OutBufLength;
    CHAR DeviceId[MAX_PATH + 1];
} WTSCLIENTA, *PWTSCLIENTA;

#define PRODUCTINFO_COMPANYNAME_LENGTH 256
#define PRODUCTINFO_PRODUCTID_LENGTH   4

typedef struct _WTS_PRODUCT_INFOA {
    CHAR CompanyName[PRODUCTINFO_COMPANYNAME_LENGTH];
    CHAR ProductID[PRODUCTINFO_PRODUCTID_LENGTH];
} PRODUCT_INFOA;

typedef struct _WTS_PRODUCT_INFOW {
    WCHAR CompanyName[PRODUCTINFO_COMPANYNAME_LENGTH];
    WCHAR ProductID[PRODUCTINFO_PRODUCTID_LENGTH];
} PRODUCT_INFOW;

#define VALIDATIONINFORMATION_LICENSE_LENGTH    16384
#define VALIDATIONINFORMATION_HARDWAREID_LENGTH 20

typedef struct _WTS_VALIDATION_INFORMATIONA {
    PRODUCT_INFOA ProductInfo;
    BYTE License[VALIDATIONINFORMATION_LICENSE_LENGTH];
    DWORD LicenseLength;
    BYTE HardwareID[VALIDATIONINFORMATION_HARDWAREID_LENGTH];
    DWORD HardwareIDLength;
} WTS_VALIDATION_INFORMATIONA, *PWTS_VALIDATION_INFORMATIONA;

typedef struct _WTS_VALIDATION_INFORMATIONW {
    PRODUCT_INFOW ProductInfo;
    BYTE License[VALIDATIONINFORMATION_LICENSE_LENGTH];
    DWORD LicenseLength;
    BYTE HardwareID[VALIDATIONINFORMATION_HARDWAREID_LENGTH];
    DWORD HardwareIDLength;
} WTS_VALIDATION_INFORMATIONW, *PWTS_VALIDATION_INFORMATIONW;

typedef WTSCONFIGINFOA WTSCONFIGINFO;
typedef PWTSCONFIGINFOA PWTSCONFIGINFO;
typedef PRODUCT_INFOA PRODUCT_INFO;
typedef WTS_VALIDATION_INFORMATIONA WTS_VALIDATION_INFORMATION;
typedef PWTS_VALIDATION_INFORMATIONA PWTS_VALIDATION_INFORMATION;
typedef WTSINFOA WTSINFO;
typedef PWTSINFOA PWTSINFO;
typedef WTSINFOEXA WTSINFOEX;
typedef PWTSINFOEXA PWTSINFOEX;
typedef WTSINFOEX_LEVEL_A WTSINFOEX_LEVEL;
typedef PWTSINFOEX_LEVEL_A PWTSINFOEX_LEVEL;
typedef WTSINFOEX_LEVEL1_A WTSINFOEX_LEVEL1;
typedef PWTSINFOEX_LEVEL1_A PWTSINFOEX_LEVEL1;
typedef WTSCLIENTA WTSCLIENT;
typedef PWTSCLIENTA PWTSCLIENT;

typedef struct _WTS_CLIENT_ADDRESS {
    DWORD AddressFamily;
    BYTE Address[20];
} WTS_CLIENT_ADDRESS, *PWTS_CLIENT_ADDRESS;

typedef struct _WTS_CLIENT_DISPLAY {
    DWORD HorizontalResolution;
    DWORD VerticalResolution;
    DWORD ColorDepth;
} WTS_CLIENT_DISPLAY, *PWTS_CLIENT_DISPLAY;

typedef enum _WTS_CONFIG_CLASS {
    WTSUserConfigInitialProgram,
    WTSUserConfigWorkingDirectory,
    WTSUserConfigfInheritInitialProgram,
    WTSUserConfigfAllowLogonTerminalServer,
    WTSUserConfigTimeoutSettingsConnections,
    WTSUserConfigTimeoutSettingsDisconnections,
    WTSUserConfigTimeoutSettingsIdle,
    WTSUserConfigfDeviceClientDrives,
    WTSUserConfigfDeviceClientPrinters,
    WTSUserConfigfDeviceClientDefaultPrinter,
    WTSUserConfigBrokenTimeoutSettings,
    WTSUserConfigReconnectSettings,
    WTSUserConfigModemCallbackSettings,
    WTSUserConfigModemCallbackPhoneNumber,
    WTSUserConfigShadowingSettings,
    WTSUserConfigTerminalServerProfilePath,
    WTSUserConfigTerminalServerHomeDir,
    WTSUserConfigTerminalServerHomeDirDrive,
    WTSUserConfigfTerminalServerRemoteHomeDir,
    WTSUserConfigUser
} WTS_CONFIG_CLASS;

typedef enum _WTS_CONFIG_SOURCE {
    WTSUserConfigSourceSAM
} WTS_CONFIG_SOURCE;

typedef struct _WTSUSERCONFIGA {
    DWORD Source;
    DWORD InheritInitialProgram;
    DWORD AllowLogonTerminalServer;
    DWORD TimeoutSettingsConnections;
    DWORD TimeoutSettingsDisconnections;
    DWORD TimeoutSettingsIdle;
    DWORD DeviceClientDrives;
    DWORD DeviceClientPrinters;
    DWORD ClientDefaultPrinter;
    DWORD BrokenTimeoutSettings;
    DWORD ReconnectSettings;
    DWORD ShadowingSettings;
    DWORD TerminalServerRemoteHomeDir;
    CHAR InitialProgram[MAX_PATH + 1];
    CHAR WorkDirectory[MAX_PATH + 1];
    CHAR TerminalServerProfilePath[MAX_PATH + 1];
    CHAR TerminalServerHomeDir[MAX_PATH + 1];
    CHAR TerminalServerHomeDirDrive[WTS_DRIVE_LENGTH + 1];
} WTSUSERCONFIGA, *PWTSUSERCONFIGA;

typedef struct _WTSUSERCONFIGW {
    DWORD Source;
    DWORD InheritInitialProgram;
    DWORD AllowLogonTerminalServer;
    DWORD TimeoutSettingsConnections;
    DWORD TimeoutSettingsDisconnections;
    DWORD TimeoutSettingsIdle;
    DWORD DeviceClientDrives;
    DWORD DeviceClientPrinters;
    DWORD ClientDefaultPrinter;
    DWORD BrokenTimeoutSettings;
    DWORD ReconnectSettings;
    DWORD ShadowingSettings;
    DWORD TerminalServerRemoteHomeDir;
    WCHAR InitialProgram[MAX_PATH + 1];
    WCHAR WorkDirectory[MAX_PATH + 1];
    WCHAR TerminalServerProfilePath[MAX_PATH + 1];
    WCHAR TerminalServerHomeDir[MAX_PATH + 1];
    WCHAR TerminalServerHomeDirDrive[WTS_DRIVE_LENGTH + 1];
} WTSUSERCONFIGW, *PWTSUSERCONFIGW;

typedef WTSUSERCONFIGA WTSUSERCONFIG;
typedef PWTSUSERCONFIGA PWTSUSERCONFIG;

#define WTS_EVENT_NONE        0x00000000
#define WTS_EVENT_CREATE      0x00000001
#define WTS_EVENT_DELETE      0x00000002
#define WTS_EVENT_RENAME      0x00000004
#define WTS_EVENT_CONNECT     0x00000008
#define WTS_EVENT_DISCONNECT  0x00000010
#define WTS_EVENT_LOGON       0x00000020
#define WTS_EVENT_LOGOFF      0x00000040
#define WTS_EVENT_STATECHANGE 0x00000080
#define WTS_EVENT_LICENSE     0x00000100
#define WTS_EVENT_ALL         0x7fffffff
#define WTS_EVENT_FLUSH       0x80000000

#define REMOTECONTROL_KBDSHIFT_HOTKEY 0x1
#define REMOTECONTROL_KBDCTRL_HOTKEY  0x2
#define REMOTECONTROL_KBDALT_HOTKEY   0x4

typedef enum _WTS_VIRTUAL_CLASS {
    WTSVirtualClientData,
    WTSVirtualFileHandle
} WTS_VIRTUAL_CLASS;

typedef struct _WTS_SESSION_ADDRESS {
    DWORD AddressFamily;
    BYTE Address[20];
} WTS_SESSION_ADDRESS, *PWTS_SESSION_ADDRESS;

#define WTS_CHANNEL_OPTION_DYNAMIC             0x00000001
#define WTS_CHANNEL_OPTION_DYNAMIC_PRI_LOW     0x00000000
#define WTS_CHANNEL_OPTION_DYNAMIC_PRI_MED     0x00000002
#define WTS_CHANNEL_OPTION_DYNAMIC_PRI_HIGH    0x00000004
#define WTS_CHANNEL_OPTION_DYNAMIC_PRI_REAL    0x00000006
#define WTS_CHANNEL_OPTION_DYNAMIC_NO_COMPRESS 0x00000008

#define NOTIFY_FOR_ALL_SESSIONS 1
#define NOTIFY_FOR_THIS_SESSION 0

#define WTS_PROCESS_INFO_LEVEL_0 0
#define WTS_PROCESS_INFO_LEVEL_1 1

typedef struct _WTS_PROCESS_INFO_EXW {
    DWORD SessionId;
    DWORD ProcessId;
    LPWSTR pProcessName;
    PSID pUserSid;
    DWORD NumberOfThreads;
    DWORD HandleCount;
    DWORD PagefileUsage;
    DWORD PeakPagefileUsage;
    DWORD WorkingSetSize;
    DWORD PeakWorkingSetSize;
    LARGE_INTEGER UserTime;
    LARGE_INTEGER KernelTime;
} WTS_PROCESS_INFO_EXW, *PWTS_PROCESS_INFO_EXW;

typedef struct _WTS_PROCESS_INFO_EXA {
    DWORD SessionId;
    DWORD ProcessId;
    LPSTR pProcessName;
    PSID pUserSid;
    DWORD NumberOfThreads;
    DWORD HandleCount;
    DWORD PagefileUsage;
    DWORD PeakPagefileUsage;
    DWORD WorkingSetSize;
    DWORD PeakWorkingSetSize;
    LARGE_INTEGER UserTime;
    LARGE_INTEGER KernelTime;
} WTS_PROCESS_INFO_EXA, *PWTS_PROCESS_INFO_EXA;

typedef WTS_PROCESS_INFO_EXA WTS_PROCESS_INFO_EX;
typedef PWTS_PROCESS_INFO_EXA PWTS_PROCESS_INFO_EX;

typedef enum _WTS_TYPE_CLASS {
    WTSTypeProcessInfoLevel0,
    WTSTypeProcessInfoLevel1,
    WTSTypeSessionInfoLevel1
} WTS_TYPE_CLASS;

/* interpreter does not support array typedef syntax; wrap in structs instead. */
typedef struct _WTSLISTENERNAMEW {
    WCHAR Value[WTS_LISTENER_NAME_LENGTH + 1];
} WTSLISTENERNAMEW, *PWTSLISTENERNAMEW;

typedef struct _WTSLISTENERNAMEA {
    CHAR Value[WTS_LISTENER_NAME_LENGTH + 1];
} WTSLISTENERNAMEA, *PWTSLISTENERNAMEA;

typedef WTSLISTENERNAMEA WTSLISTENERNAME;
typedef PWTSLISTENERNAMEA PWTSLISTENERNAME;

typedef struct _WTSLISTENERCONFIGW {
    ULONG version;
    ULONG fEnableListener;
    ULONG MaxConnectionCount;
    ULONG fPromptForPassword;
    ULONG fInheritColorDepth;
    ULONG ColorDepth;
    ULONG fInheritBrokenTimeoutSettings;
    ULONG BrokenTimeoutSettings;
    ULONG fDisablePrinterRedirection;
    ULONG fDisableDriveRedirection;
    ULONG fDisableComPortRedirection;
    ULONG fDisableLPTPortRedirection;
    ULONG fDisableClipboardRedirection;
    ULONG fDisableAudioRedirection;
    ULONG fDisablePNPRedirection;
    ULONG fDisableDefaultMainClientPrinter;
    ULONG LanAdapter;
    ULONG PortNumber;
    ULONG fInheritShadowSettings;
    ULONG ShadowSettings;
    ULONG TimeoutSettingsConnection;
    ULONG TimeoutSettingsDisconnection;
    ULONG TimeoutSettingsIdle;
    ULONG SecurityLayer;
    ULONG MinEncryptionLevel;
    ULONG UserAuthentication;
    WCHAR Comment[WTS_COMMENT_LENGTH + 1];
    WCHAR LogonUserName[USERNAME_LENGTH + 1];
    WCHAR LogonDomain[DOMAIN_LENGTH + 1];
    WCHAR WorkDirectory[MAX_PATH + 1];
    WCHAR InitialProgram[MAX_PATH + 1];
} WTSLISTENERCONFIGW, *PWTSLISTENERCONFIGW;

typedef struct _WTSLISTENERCONFIGA {
    ULONG version;
    ULONG fEnableListener;
    ULONG MaxConnectionCount;
    ULONG fPromptForPassword;
    ULONG fInheritColorDepth;
    ULONG ColorDepth;
    ULONG fInheritBrokenTimeoutSettings;
    ULONG BrokenTimeoutSettings;
    ULONG fDisablePrinterRedirection;
    ULONG fDisableDriveRedirection;
    ULONG fDisableComPortRedirection;
    ULONG fDisableLPTPortRedirection;
    ULONG fDisableClipboardRedirection;
    ULONG fDisableAudioRedirection;
    ULONG fDisablePNPRedirection;
    ULONG fDisableDefaultMainClientPrinter;
    ULONG LanAdapter;
    ULONG PortNumber;
    ULONG fInheritShadowSettings;
    ULONG ShadowSettings;
    ULONG TimeoutSettingsConnection;
    ULONG TimeoutSettingsDisconnection;
    ULONG TimeoutSettingsIdle;
    ULONG SecurityLayer;
    ULONG MinEncryptionLevel;
    ULONG UserAuthentication;
    CHAR Comment[WTS_COMMENT_LENGTH + 1];
    CHAR LogonUserName[USERNAME_LENGTH + 1];
    CHAR LogonDomain[DOMAIN_LENGTH + 1];
    CHAR WorkDirectory[MAX_PATH + 1];
    CHAR InitialProgram[MAX_PATH + 1];
} WTSLISTENERCONFIGA, *PWTSLISTENERCONFIGA;

typedef WTSLISTENERCONFIGA WTSLISTENERCONFIG;
typedef PWTSLISTENERCONFIGA PWTSLISTENERCONFIG;

WTSAPI32$WTSEnumerateServersW: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSEnumerateServersA: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSOpenServerW: ptr (ptr);
WTSAPI32$WTSOpenServerA: ptr (ptr);
WTSAPI32$WTSCloseServer: void (ptr);
WTSAPI32$WTSEnumerateSessionsW: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSEnumerateSessionsA: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSEnumerateProcessesW: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSEnumerateProcessesA: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSTerminateProcess: u32 (ptr, u32, u32);
WTSAPI32$WTSQuerySessionInformationW: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSQuerySessionInformationA: u32 (ptr, u32, u32, ptr, ptr);
WTSAPI32$WTSQueryUserConfigW: u32 (ptr, ptr, u32, ptr, ptr);
WTSAPI32$WTSQueryUserConfigA: u32 (ptr, ptr, u32, ptr, ptr);
WTSAPI32$WTSSetUserConfigW: u32 (ptr, ptr, u32, ptr, u32);
WTSAPI32$WTSSetUserConfigA: u32 (ptr, ptr, u32, ptr, u32);
WTSAPI32$WTSSendMessageW: u32 (ptr, u32, ptr, u32, ptr, u32, u32, u32, ptr, u32);
WTSAPI32$WTSSendMessageA: u32 (ptr, u32, ptr, u32, ptr, u32, u32, u32, ptr, u32);
WTSAPI32$WTSDisconnectSession: u32 (ptr, u32, u32);
WTSAPI32$WTSLogoffSession: u32 (ptr, u32, u32);
WTSAPI32$WTSShutdownSystem: u32 (ptr, u32);
WTSAPI32$WTSWaitSystemEvent: u32 (ptr, u32, ptr);
WTSAPI32$WTSVirtualChannelOpen: ptr (ptr, u32, ptr);
WTSAPI32$WTSVirtualChannelClose: u32 (ptr);
WTSAPI32$WTSVirtualChannelRead: u32 (ptr, u32, ptr, u32, ptr);
WTSAPI32$WTSVirtualChannelWrite: u32 (ptr, ptr, u32, ptr);
WTSAPI32$WTSVirtualChannelPurgeInput: u32 (ptr);
WTSAPI32$WTSVirtualChannelPurgeOutput: u32 (ptr);
WTSAPI32$WTSVirtualChannelQuery: u32 (ptr, u32, ptr, ptr);
WTSAPI32$WTSFreeMemory: void (ptr);
WTSAPI32$WTSRegisterSessionNotification: u32 (ptr, u32);
WTSAPI32$WTSUnRegisterSessionNotification: u32 (ptr);
WTSAPI32$WTSQueryUserToken: u32 (u32, ptr);
WTSAPI32$WTSConnectSessionA: u32 (u32, u32, ptr, u32);
WTSAPI32$WTSConnectSessionW: u32 (u32, u32, ptr, u32);
WTSAPI32$WTSRegisterSessionNotificationEx: u32 (ptr, ptr, u32);
WTSAPI32$WTSStartRemoteControlSessionA: u32 (ptr, u32, u32, u16);
WTSAPI32$WTSStartRemoteControlSessionW: u32 (ptr, u32, u32, u16);
WTSAPI32$WTSStopRemoteControlSession: u32 (u32);
WTSAPI32$WTSUnRegisterSessionNotificationEx: u32 (ptr, ptr);
WTSAPI32$WTSVirtualChannelOpenEx: ptr (u32, ptr, u32);

#endif
