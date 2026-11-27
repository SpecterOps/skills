#ifndef BUILTINS_LIMITS_H
#define BUILTINS_LIMITS_H

#define CHAR_BIT      8
#define SCHAR_MIN   (-128)
#define SCHAR_MAX     127
#define UCHAR_MAX     0xff

#define CHAR_MIN    SCHAR_MIN
#define CHAR_MAX    SCHAR_MAX

#define MB_LEN_MAX    5
#define SHRT_MIN    (-32768)
#define SHRT_MAX      32767
#define USHRT_MAX     0xffff
#define INT_MIN     (-2147483647 - 1)
#define INT_MAX       2147483647
#define UINT_MAX      0xffffffffU
#define LONG_MIN    (-2147483647L - 1)
#define LONG_MAX      2147483647L
#define ULONG_MAX     0xffffffffUL
#define LLONG_MAX     9223372036854775807LL
#define LLONG_MIN   (-9223372036854775807LL - 1)
#define ULLONG_MAX    18446744073709551615ULL

#define _I8_MIN     (-127 - 1)
#define _I8_MAX       127
#define _UI8_MAX      0xffU

#define _I16_MIN    (-32767 - 1)
#define _I16_MAX      32767
#define _UI16_MAX     0xffffU

#define _I32_MIN    (-2147483647 - 1)
#define _I32_MAX      2147483647
#define _UI32_MAX     0xffffffffU

#define _I64_MIN    (-9223372036854775807LL - 1)
#define _I64_MAX      9223372036854775807LL
#define _UI64_MAX     18446744073709551615ULL

#ifndef SIZE_MAX
#ifndef _WIN32
#define SIZE_MAX 18446744073709551615ULL
#else
#define SIZE_MAX 0xffffffffU
#endif
#endif

#ifndef RSIZE_MAX
#define RSIZE_MAX (SIZE_MAX >> 1)
#endif

#endif
