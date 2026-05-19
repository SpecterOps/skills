# HLIL Instruction Reference

High Level IL is Binary Ninja's decompiler output. It recovers high-level language constructs (if/while/for/switch), folds expressions, and eliminates dead code. Tree-based with significant nesting.

## Key Differences from MLIL

1. **Control flow recovery** -- while, do-while, for, switch/case, break, continue
2. **Expression folding** -- multiple MLIL statements collapsed into single expressions
3. **No `.output` on HLIL_CALL** -- return values appear as `inst.right` of `HighLevelILVarInit` or `HighLevelILVarAssign`
4. **Struct fields and array indexing** -- `HLIL_STRUCT_FIELD`, `HLIL_ARRAY_INDEX`, `HLIL_DEREF_FIELD`

## Important: Tree Structure

HLIL is heavily tree-based. Naive iteration over top-level instructions will miss nested calls, comparisons, and operations. Use the `traverse` API or `visit` methods for thorough analysis.

## Control Flow

- `HLIL_JUMP` -- Branch to `dest` address
- `HLIL_CALL` -- Call `dest` with `params` (no `output` -- returns via assignment)
- `HLIL_TAILCALL` -- Tail call to `dest` with `params`
- `HLIL_SYSCALL` -- System call with `params`
- `HLIL_RET` -- Return to caller
- `HLIL_NORET` -- Unreachable code marker
- `HLIL_IF` -- Conditional: `condition` -> `true`/`false` branch
- `HLIL_GOTO` -- Branch to IL label
- `HLIL_WHILE` -- While loop
- `HLIL_DO_WHILE` -- Do-while loop
- `HLIL_FOR` -- For loop
- `HLIL_SWITCH` -- Switch statement
- `HLIL_CASE` -- Case within switch
- `HLIL_BREAK` -- Break from loop/switch
- `HLIL_CONTINUE` -- Continue to next loop iteration

## Variable Reads and Writes

- `HLIL_VAR_DECLARE` -- Declaration of `var`
- `HLIL_VAR_INIT` -- Initialize `dest` variable with `src` expression
- `HLIL_ASSIGN` -- Set `dest` to `src` expression
- `HLIL_ASSIGN_UNPACK` -- Destructuring assignment
- `HLIL_VAR` -- Variable reference
- `HLIL_VAR_PHI` -- PHI node for variable versions
- `HLIL_MEM_PHI` -- Memory PHI
- `HLIL_ADDRESS_OF` -- Address of variable `src`

## Memory Access

- `HLIL_DEREF` -- Dereference `src` (pointer read)
- `HLIL_DEREF_FIELD` -- Dereference with field offset
- `HLIL_STRUCT_FIELD` -- Access struct field
- `HLIL_ARRAY_INDEX` -- Array element access
- `HLIL_SPLIT` -- Split pair `high`:`low`

## Constants

- `HLIL_CONST` -- Constant integer
- `HLIL_CONST_DATA` -- Constant data reference
- `HLIL_CONST_PTR` -- Constant pointer
- `HLIL_EXTERN_PTR` -- External symbol pointer
- `HLIL_FLOAT_CONST` -- Floating point constant
- `HLIL_IMPORT` -- Imported address
- `HLIL_LOW_PART` -- `size` bytes from low end of `src`

## Arithmetic Operations

- `HLIL_ADD` / `HLIL_ADC` -- Add / Add with carry
- `HLIL_SUB` / `HLIL_SBB` -- Subtract / Subtract with borrow
- `HLIL_AND` / `HLIL_OR` / `HLIL_XOR` -- Bitwise AND/OR/XOR
- `HLIL_LSL` / `HLIL_LSR` / `HLIL_ASR` -- Shifts
- `HLIL_ROL` / `HLIL_ROR` / `HLIL_RLC` / `HLIL_RRC` -- Rotations
- `HLIL_MUL` / `HLIL_MULU_DP` / `HLIL_MULS_DP` -- Multiply
- `HLIL_DIVU` / `HLIL_DIVS` / `HLIL_DIVU_DP` / `HLIL_DIVS_DP` -- Divide
- `HLIL_MODU` / `HLIL_MODS` / `HLIL_MODU_DP` / `HLIL_MODS_DP` -- Modulus
- `HLIL_NEG` / `HLIL_NOT` -- Negate/Complement
- `HLIL_SX` / `HLIL_ZX` -- Sign/Zero extend
- `HLIL_ADD_OVERFLOW` -- Overflow of addition
- `HLIL_BOOL_TO_INT` -- Bool to integer

## Floating Point

- `HLIL_FADD` / `HLIL_FSUB` / `HLIL_FMUL` / `HLIL_FDIV` -- FP arithmetic
- `HLIL_FSQRT` / `HLIL_FNEG` / `HLIL_FABS` -- FP operations
- `HLIL_FLOAT_TO_INT` / `HLIL_INT_TO_FLOAT` / `HLIL_FLOAT_CONV` -- Conversions
- `HLIL_ROUND_TO_INT` / `HLIL_FLOOR` / `HLIL_CEIL` / `HLIL_FTRUNC` -- Rounding

## Comparisons

- `HLIL_CMP_E` / `HLIL_CMP_NE` -- Equal / Not equal
- `HLIL_CMP_SLT` / `HLIL_CMP_ULT` -- Signed/Unsigned less than
- `HLIL_CMP_SLE` / `HLIL_CMP_ULE` -- Signed/Unsigned less than or equal
- `HLIL_CMP_SGE` / `HLIL_CMP_UGE` -- Signed/Unsigned greater than or equal
- `HLIL_CMP_SGT` / `HLIL_CMP_UGT` -- Signed/Unsigned greater than
- `HLIL_TEST_BIT` -- Test if bit
- `HLIL_FCMP_E` / `HLIL_FCMP_NE` / `HLIL_FCMP_LT` / `HLIL_FCMP_LE` / `HLIL_FCMP_GE` / `HLIL_FCMP_GT`
- `HLIL_FCMP_O` (ordered) / `HLIL_FCMP_UO` (unordered)

## Miscellaneous

- `HLIL_NOP` -- No operation
- `HLIL_BP` -- Breakpoint
- `HLIL_TRAP` -- Trap with `vector`
- `HLIL_INTRINSIC` -- Architecture intrinsic
- `HLIL_UNDEF` -- Undefined behavior
- `HLIL_UNIMPL` / `HLIL_UNIMPL_MEM` -- Unimplemented
- `HLIL_BLOCK` -- Block of statements
- `HLIL_LABEL` -- Label target
- `HLIL_UNREACHABLE` -- Unreachable code
