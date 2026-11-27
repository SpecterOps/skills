#include <windows.h>
#include <beacon.h>

#define SCALE3(x) ((x) * 3)
#define PICK_MAX(a, b) ((a) > (b) ? (a) : (b))

/* Custom signature example not currently covered in built-in interpreter-includes. */
USER32$GetDesktopWindow: ptr ();

enum DemoPhase {
    DEMO_INIT = 1,
    DEMO_RUN = 2,
    DEMO_DONE = 3
};

union U32Bytes {
    unsigned int u;
    unsigned char b[4];
};

struct DemoNode {
    int value;
    struct DemoNode *next;
};
typedef struct DemoNode DemoNode;

typedef unsigned int (stdcall *GETPID_FN)(void);

int fib(int n);
int sum_until_negative(int *vals, int count);
char *pick_first(char **items, int count, char *fallback);
int goto_countdown_sum(int start);
void run_demo(void);

int g_seed = 7;
int g_values[5] = {4, 5, 6, 7, 8};
char g_banner[] = "vm-demo";
wchar_t g_wbanner[] = L"VM";

int fib(int n)
{
    if (n <= 1)
        return n;
    return fib(n - 1) + fib(n - 2);
}

int sum_until_negative(int *vals, int count)
{
    int i;
    int total;
    total = 0;
    for (i = 0; i < count; i++) {
        if (vals[i] == 0)
            continue;
        if (vals[i] < 0)
            break;
        total += vals[i];
    }
    return total;
}

char *pick_first(char **items, int count, char *fallback)
{
    if (count > 0 && items[0] != 0)
        return items[0];
    return fallback;
}

int goto_countdown_sum(int start)
{
    int total;
    total = 0;
loop:
    if (start <= 0)
        goto done;
    total += start;
    start--;
    goto loop;
done:
    return total;
}

void run_demo(void)
{
    int local_a;
    int local_b;
    int chain;
    int cmp;
    int logic;
    int bitmix;
    int shifted;
    int ternary_pick;
    int comma_value;
    int while_total;
    int do_count;
    int i;
    int matrix[4];
    int inferred[] = {9, 10, 11};
    int sum_checked_values;
    int ptr_third;
    int cast_first;
    int fib8;
    int goto_sum;
    int phase_value;
    int switch_score;
    int off_value;
    int node_sum;
    unsigned long long u64_value;
    long long i64_value;
    size_t banner_len;
    char *first_label;
    char *labels[2];
    void *vp;
    void *desktop_hwnd;
    void *kernel32_mod;
    void *getpid_proc;
    GETPID_FN getpid_fn;
    unsigned int pid_direct;
    unsigned int pid_from_ptr;
    union U32Bytes bytes;
    DemoNode n1;
    DemoNode n2;

    local_a = 3;
    local_b = 5;

    chain = local_a = local_b = g_seed;
    cmp = (chain == 7) + (chain != 6) + (chain >= 7) + (chain < 10);
    logic = (cmp > 0 && chain == 7) || (cmp < 0);
    bitmix = (local_a | local_b) ^ (local_a & local_b);
    shifted = SCALE3(3) + (64 >> 3);
    ternary_pick = (logic ? PICK_MAX(bitmix, shifted) : 0);
    comma_value = (local_a += 2, local_b += 3, local_a + local_b);

    while_total = 0;
    i = 0;
    while (i < 4) {
        while_total += i;
        i++;
    }

    do_count = 0;
    i = 0;
    do {
        do_count += 1;
        i++;
    } while (i < 3);

    matrix[0] = 1;
    matrix[1] = 2;
    matrix[2] = 3;
    matrix[3] = 4;

    sum_checked_values = sum_until_negative(g_values, 5);
    ptr_third = *(g_values + 2);

    vp = g_values;
    cast_first = ((int *)vp)[0];

    fib8 = fib(8);
    goto_sum = goto_countdown_sum(5);

    phase_value = DEMO_RUN;
    switch_score = 0;
    switch (phase_value) {
    case DEMO_INIT:
        switch_score = 1;
        break;
    case DEMO_RUN:
        switch_score = 2;
        break;
    default:
        switch_score = 3;
        break;
    }

    off_value = (int)__builtin_offsetof(struct DemoNode, next);

    n1.value = 11;
    n2.value = 22;
    n1.next = &n2;
    n2.next = 0;
    node_sum = n1.value + n1.next->value;

    bytes.u = 0x11223344u;

    u64_value = 0x100000001ULL;
    i64_value = -42LL;

    banner_len = strlen(g_banner);
    memset(g_banner + 2, 'X', (size_t)2);

    labels[0] = "alpha";
    labels[1] = "beta";
    first_label = pick_first(labels, 2, "none");

    pid_direct = GetCurrentProcessId();

    kernel32_mod = GetModuleHandleA("kernel32.dll");
    getpid_proc = GetProcAddress(kernel32_mod, "GetCurrentProcessId");
    getpid_fn = getpid_proc;
    pid_from_ptr = 0;
    if (getpid_fn != 0)
        pid_from_ptr = getpid_fn();

    desktop_hwnd = GetDesktopWindow();

    BeaconPrintf(CALLBACK_OUTPUT, "include+ffi: pid=%u ptrpid=%u desktop=%d\n",
        pid_direct, pid_from_ptr, (int)(desktop_hwnd != 0));
    BeaconPrintf(CALLBACK_OUTPUT, "ops: cmp=%d logic=%d bitmix=%d shift=%d ternary=%d comma=%d\n",
        cmp, logic, bitmix, shifted, ternary_pick, comma_value);
    BeaconPrintf(CALLBACK_OUTPUT, "flow: while=%d do=%d switch=%d goto=%d\n",
        while_total, do_count, switch_score, goto_sum);
    BeaconPrintf(CALLBACK_OUTPUT, "arrays+pointers: sum=%d third=%d cast0=%d m11=%d inf2=%d\n",
        sum_checked_values, ptr_third, cast_first, matrix[3], inferred[2]);
    BeaconPrintf(CALLBACK_OUTPUT, "types: fib8=%d node_sum=%d off_next=%d u64=%llu i64=%lld b0=%u wchar1=%u\n",
        fib8, node_sum, off_value, u64_value, i64_value,
        (unsigned int)bytes.b[0], (unsigned int)g_wbanner[1]);
    BeaconPrintf(CALLBACK_OUTPUT, "strings: len=%u first=%s banner=%s\n",
        (unsigned int)banner_len, first_label, g_banner);
}

run_demo();
