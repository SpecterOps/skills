# LLIL Instruction Reference

Low Level IL is the closest IL to native assembly. Registers, flags, and memory operations are preserved. Instructions form expression trees -- operands can be composed of sub-operations.

Example tree for `eax = eax + ecx * 4`:
```
    =
   / \
 eax  +
     / \
   eax  *
       / \
     ecx  4
```

## Key Properties of LowLevelILInstruction

- `address` -- virtual address of the corresponding assembly instruction
- `instr_index` -- unique index of this IL instruction (distinct from address due to many-to-many mapping)
- `operation` -- enumeration value (e.g., `LowLevelILOperation.LLIL_SET_REG`)
- `operands` -- list of all operands
- `src` -- source operand
- `dest` -- destination operand
- `size` -- size of operation in bytes

## Registers, Constants & Flags

- `LLIL_REG` -- Register terminal
- `LLIL_CONST` -- Constant integer terminal
- `LLIL_SET_REG` -- Set register to result of `src` expression
- `LLIL_SET_REG_SPLIT` -- Set a pair of registers as one double-sized register
- `LLIL_SET_FLAG` -- Set flag to result of `src` expression

## Memory Load & Store

- `LLIL_LOAD` -- Load value from memory
- `LLIL_STORE` -- Store value to memory
- `LLIL_PUSH` -- Store to stack, adjust stack pointer by sizeof(value)
- `LLIL_POP` -- Load from stack, adjust stack pointer by sizeof(value)

## Control Flow & Conditionals

- `LLIL_JUMP` -- Branch to address from IL expression
- `LLIL_JUMP_TO` -- Jump table: expression + list of possible targets
- `LLIL_CALL` -- Call function at address from IL expression
- `LLIL_TAILCALL` -- Tail call with `dest`, `params`, `output`
- `LLIL_RET` -- Return to caller
- `LLIL_NORET` -- Marks unreachable code after non-returning call
- `LLIL_SYSCALL` -- System call
- `LLIL_IF` -- Conditional: if `condition` then true_label else false_label
- `LLIL_GOTO` -- Branch to IL label (not address)
- `LLIL_FLAG_COND` -- Flag condition expression

### Comparison Operations
- `LLIL_CMP_E` -- equal
- `LLIL_CMP_NE` -- not equal
- `LLIL_CMP_SLT` / `LLIL_CMP_ULT` -- signed/unsigned less than
- `LLIL_CMP_SLE` / `LLIL_CMP_ULE` -- signed/unsigned less than or equal
- `LLIL_CMP_SGE` / `LLIL_CMP_UGE` -- signed/unsigned greater than or equal
- `LLIL_CMP_SGT` / `LLIL_CMP_UGT` -- signed/unsigned greater than

## Arithmetic & Logical

- `LLIL_ADD` / `LLIL_ADC` -- Add / Add with carry
- `LLIL_SUB` / `LLIL_SBB` -- Subtract / Subtract with borrow
- `LLIL_AND` / `LLIL_OR` / `LLIL_XOR` -- Bitwise AND/OR/XOR
- `LLIL_LSL` / `LLIL_LSR` / `LLIL_ASR` -- Logical shift left/right, Arithmetic shift right
- `LLIL_ROL` / `LLIL_ROR` -- Rotate left/right
- `LLIL_RLC` / `LLIL_RRC` -- Rotate left/right with carry
- `LLIL_MUL` -- Multiply (single precision)
- `LLIL_MULU_DP` / `LLIL_MULS_DP` -- Unsigned/Signed multiply (double precision)
- `LLIL_DIVU` / `LLIL_DIVS` -- Unsigned/Signed divide (single precision)
- `LLIL_DIVU_DP` / `LLIL_DIVS_DP` -- Unsigned/Signed divide (double precision)
- `LLIL_MODU` / `LLIL_MODS` -- Unsigned/Signed modulus (single precision)
- `LLIL_MODU_DP` / `LLIL_MODS_DP` -- Unsigned/Signed modulus (double precision)
- `LLIL_NEG` -- Sign negation
- `LLIL_NOT` -- Bitwise complement
- `LLIL_TEST_BIT` -- Test if bit `right` is set in `left`
- `LLIL_BOOL_TO_INT` -- Convert bool to integer

## Floating Point

- `LLIL_FLOAT_CONST` -- FP constant
- `LLIL_FADD` / `LLIL_FSUB` / `LLIL_FMUL` / `LLIL_FDIV` -- FP arithmetic
- `LLIL_FSQRT` / `LLIL_FNEG` / `LLIL_FABS` -- FP square root/negate/absolute
- `LLIL_FLOAT_TO_INT` / `LLIL_INT_TO_FLOAT` / `LLIL_FLOAT_CONV` -- FP conversions
- `LLIL_ROUND_TO_INT` / `LLIL_FLOOR` / `LLIL_CEILING` / `LLIL_FTRUNC` -- FP rounding

### FP Comparisons
- `LLIL_FCMP_E` / `LLIL_FCMP_NE` / `LLIL_FCMP_LT` / `LLIL_FCMP_LE` / `LLIL_FCMP_GE` / `LLIL_FCMP_GT`
- `LLIL_FCMP_O` (ordered) / `LLIL_FCMP_UO` (unordered)

## Special Instructions

- `LLIL_NOP` -- No operation
- `LLIL_BP` -- Breakpoint
- `LLIL_TRAP` -- Trap/interrupt
- `LLIL_SX` -- Sign extend
- `LLIL_ZX` -- Zero extend
- `LLIL_LOW_PART` -- `size` bytes from the low end of `src`
- `LLIL_UNDEF` -- Undefined behavior
- `LLIL_UNIMPL` -- Unimplemented instruction
- `LLIL_UNIMPL_MEM` -- Unimplemented memory access
- `LLIL_EXTERN_PTR` -- Synthesized pointer to external data
- `LLIL_INTRINSIC` -- Architecture intrinsic (e.g., AES instructions) with `output`, `params`, `intrinsic`
- `LLIL_MEM_PHI` -- Memory PHI for SSA (memory modifications across basic block merges)
