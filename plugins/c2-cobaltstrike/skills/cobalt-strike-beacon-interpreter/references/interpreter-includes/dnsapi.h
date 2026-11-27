#ifndef BUILTINS_DNSAPI_H
#define BUILTINS_DNSAPI_H

DNSAPI$DnsQueryConfig: u32 (u32, u32, ptr, ptr, ptr, ptr);
DNSAPI$DnsRecordCopyEx: ptr (ptr, u32, u32);
DNSAPI$DnsRecordSetCopyEx: ptr (ptr, u32, u32);
DNSAPI$DnsRecordCompare: u32 (ptr, ptr);
DNSAPI$DnsRecordSetCompare: u32 (ptr, ptr, ptr, ptr);
DNSAPI$DnsFree: void (ptr, u32);
DNSAPI$DnsRecordListFree: void (ptr, u32);
DNSAPI$DnsQuery_A: u32 (cstr, u16, u32, ptr, ptr, ptr);
DNSAPI$DnsQuery_UTF8: u32 (cstr, u16, u32, ptr, ptr, ptr);
DNSAPI$DnsQuery_W: u32 (ptr, u16, u32, ptr, ptr, ptr);
DNSAPI$DnsAcquireContextHandle_W: u32 (u32, ptr, ptr);
DNSAPI$DnsAcquireContextHandle_A: u32 (u32, ptr, ptr);
DNSAPI$DnsReleaseContextHandle: void (ptr);
DNSAPI$DnsModifyRecordsInSet_W: u32 (ptr, ptr, u32, ptr, ptr, ptr);
DNSAPI$DnsModifyRecordsInSet_A: u32 (ptr, ptr, u32, ptr, ptr, ptr);
DNSAPI$DnsModifyRecordsInSet_UTF8: u32 (ptr, ptr, u32, ptr, ptr, ptr);
DNSAPI$DnsReplaceRecordSetW: u32 (ptr, u32, ptr, ptr, ptr);
DNSAPI$DnsReplaceRecordSetA: u32 (ptr, u32, ptr, ptr, ptr);
DNSAPI$DnsReplaceRecordSetUTF8: u32 (ptr, u32, ptr, ptr, ptr);
DNSAPI$DnsNameCompare_A: u32 (ptr, ptr);
DNSAPI$DnsNameCompare_W: u32 (ptr, ptr);
DNSAPI$DnsWriteQuestionToBuffer_W: u32 (ptr, ptr, ptr, u16, u16, u32);
DNSAPI$DnsWriteQuestionToBuffer_UTF8: u32 (ptr, ptr, ptr, u16, u16, u32);
DNSAPI$DnsExtractRecordsFromMessage_W: u32 (ptr, u16, ptr);
DNSAPI$DnsExtractRecordsFromMessage_UTF8: u32 (ptr, u16, ptr);

#endif /* BUILTINS_DNSAPI_H */
