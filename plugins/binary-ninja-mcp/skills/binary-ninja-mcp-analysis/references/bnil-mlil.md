# MLIL Instruction Reference

Medium Level IL translates registers to variables, associates types, resolves call parameters, propagates constants, and eliminates some dead code. Stack operations are abstracted away.

## Key Differences from LLIL

1. Registers are now **variables** (with names like `rax`, `var_260`)
2. Stack concept is removed -- stack accesses become variable references
3. Variables have **types** associated with them
4. Call sites have inferred **parameters** and **return values**
5. Constants are **propagated** through data flow
6. Some **dead code** is eliminated

## The Variable Object

Variables represent a single storage location within a function scope.

### Properties
- `source_type` -- Storage location: `StackVariableSourceType`, `RegisterVariableSourceType`, or `FlagVariableSourceType`
- `storage` -- For register vars: register index. For stack vars: stack offset.
- `index` -- Unique identifier across analysis passes
- `type` -- The `Type` object associated with this variable

### Variable Naming Convention
- `RegisterVariableSourceType` -> register name (e.g., `rax`, `rbx`)
- `StackVariableSourceType` -> `var_` + hex of negative stack offset (e.g., `var_260`)
- Reuse of a storage location appends a version counter (e.g., `rax_1`, `rax_2`)

## The Type System

Type objects have a `type_class` property from the `TypeClass` enumeration:

| TypeClass | Description |
|-----------|-------------|
| `VoidTypeClass` | Unknown/void type |
| `BoolTypeClass` | Boolean (0 or !0) |
| `IntegerTypeClass` | Integer with sign, width, display type |
| `FloatTypeClass` | IEEE754 floating point (up to 10 bytes) |
| `PointerTypeClass` | Pointer with `target`/`element_type` property |
| `ArrayTypeClass` | Array with `element_type`, `count`, `width` |
| `FunctionTypeClass` | Function with `return_value`, `parameters`, `calling_convention`, `can_return` |
| `StructureTypeClass` | Struct/class/union with `members` list (each has `name`, `offset`, `type`) |
| `EnumerationTypeClass` | Enumeration with `members` (each has `name`, `value`) |
| `NamedTypeReferenceClass` | Symbolic reference to another type (like C typedef) |
| `WideCharTypeClass` | Unicode character |
| `VarArgsTypeClass` | Variadic function parameter marker |
| `ValueTypeClass` | Constant value (used in demangling) |

All types have a `confidence` property used for type inference.

## Control Flow Instructions

- `MLIL_JUMP` -- Branch to `dest` address
- `MLIL_JUMP_TO` -- Jump table: `dest` expression + `targets` list
- `MLIL_CALL` -- Call `dest` with `params`, returning `output`
- `MLIL_CALL_UNTYPED` -- Call where stack resolution failed (no params/output list)
- `MLIL_TAILCALL` -- Tail call to `dest` with `params` and `output`
- `MLIL_TAILCALL_UNTYPED` -- Tail call without resolved params
- `MLIL_RET` -- Return to caller
- `MLIL_NORET` -- Unreachable (after non-returning call)
- `MLIL_IF` -- Conditional: `condition` -> `true`/`false` branch
- `MLIL_GOTO` -- Branch to IL instruction id
- `MLIL_SYSCALL` -- System call with `params` and `output`
- `MLIL_SYSCALL_UNTYPED` -- System call without resolved params
- `MLIL_CALL_OUTPUT` -- Return values `dest` from a call
- `MLIL_CALL_PARAM` -- Parameter set `src` for a call
- `MLIL_RET_HINT` -- Indirect jump (internal analysis only)

## Variable Reads and Writes

- `MLIL_SET_VAR` -- Set variable `dest` to expression `src`
- `MLIL_SET_VAR_FIELD` -- Set variable `dest` at `offset` to `src`
- `MLIL_SET_VAR_SPLIT` -- Set pair `high`:`low` to `src`
- `MLIL_SET_VAR_ALIASED` -- Set aliased variable `prev` to `src`
- `MLIL_SET_VAR_ALIASED_FIELD` -- Set field at `offset` of aliased variable
- `MLIL_VAR` -- Variable reference `src`
- `MLIL_VAR_FIELD` -- Variable + offset: `src`, `offset`
- `MLIL_VAR_SPLIT` -- Split pair `high`:`low` as single expression
- `MLIL_VAR_ALIASED` -- Aliased variable reference
- `MLIL_VAR_ALIASED_FIELD` -- Aliased variable field
- `MLIL_VAR_PHI` -- PHI node combining variable versions at block merge
- `MLIL_MEM_PHI` -- Memory PHI for memory modifications across paths
- `MLIL_LOAD` -- Read `size` bytes from memory address `src`
- `MLIL_LOAD_STRUCT` -- Read from struct: `src` + `offset`
- `MLIL_STORE` -- Store `src` to memory at `dest`
- `MLIL_STORE_STRUCT` -- Store to struct: `dest` + `offset` from `src`
- `MLIL_ADDRESS_OF` -- Address of variable `src`
- `MLIL_ADDRESS_OF_FIELD` -- Address of variable `src` at `offset`
- `MLIL_LOW_PART` -- `size` bytes from low end of `src`

## Constants

- `MLIL_CONST` -- Constant integer
- `MLIL_CONST_DATA` -- Constant data reference
- `MLIL_CONST_PTR` -- Constant used as pointer
- `MLIL_EXTERN_PTR` -- External symbol: `constant` + `offset`
- `MLIL_FLOAT_CONST` -- Floating point constant
- `MLIL_IMPORT` -- Imported address constant

## Arithmetic Operations

- `MLIL_ADD` / `MLIL_ADC` -- Add / Add with carry
- `MLIL_SUB` / `MLIL_SBB` -- Subtract / Subtract with borrow
- `MLIL_AND` / `MLIL_OR` / `MLIL_XOR` -- Bitwise AND/OR/XOR
- `MLIL_LSL` / `MLIL_LSR` / `MLIL_ASR` -- Shifts
- `MLIL_ROL` / `MLIL_ROR` / `MLIL_RLC` / `MLIL_RRC` -- Rotations
- `MLIL_MUL` / `MLIL_MULU_DP` / `MLIL_MULS_DP` -- Multiply (single/double precision)
- `MLIL_DIVU` / `MLIL_DIVS` / `MLIL_DIVU_DP` / `MLIL_DIVS_DP` -- Divide
- `MLIL_MODU` / `MLIL_MODS` / `MLIL_MODU_DP` / `MLIL_MODS_DP` -- Modulus
- `MLIL_NEG` / `MLIL_NOT` -- Negate/Complement
- `MLIL_SX` / `MLIL_ZX` -- Sign/Zero extend
- `MLIL_ADD_OVERFLOW` -- Overflow of addition
- `MLIL_BOOL_TO_INT` -- Bool to integer conversion

## Floating Point

- `MLIL_FADD` / `MLIL_FSUB` / `MLIL_FMUL` / `MLIL_FDIV` -- FP arithmetic
- `MLIL_FSQRT` / `MLIL_FNEG` / `MLIL_FABS` -- FP operations
- `MLIL_FLOAT_TO_INT` / `MLIL_INT_TO_FLOAT` / `MLIL_FLOAT_CONV` -- Conversions
- `MLIL_ROUND_TO_INT` / `MLIL_FLOOR` / `MLIL_CEIL` / `MLIL_FTRUNC` -- Rounding

## Comparisons

- `MLIL_CMP_E` / `MLIL_CMP_NE` -- Equal / Not equal
- `MLIL_CMP_SLT` / `MLIL_CMP_ULT` -- Signed/Unsigned less than
- `MLIL_CMP_SLE` / `MLIL_CMP_ULE` -- Signed/Unsigned less than or equal
- `MLIL_CMP_SGE` / `MLIL_CMP_UGE` -- Signed/Unsigned greater than or equal
- `MLIL_CMP_SGT` / `MLIL_CMP_UGT` -- Signed/Unsigned greater than
- `MLIL_TEST_BIT` -- Test if bit `right` is set in `left`
- `MLIL_FCMP_E` / `MLIL_FCMP_NE` / `MLIL_FCMP_LT` / `MLIL_FCMP_LE` / `MLIL_FCMP_GE` / `MLIL_FCMP_GT` -- FP comparisons
- `MLIL_FCMP_O` (ordered) / `MLIL_FCMP_UO` (unordered)

## Miscellaneous

- `MLIL_NOP` -- No operation
- `MLIL_BP` -- Breakpoint
- `MLIL_TRAP` -- Trap with `vector`
- `MLIL_INTRINSIC` -- Architecture intrinsic
- `MLIL_FREE_VAR_SLOT` -- Free register stack slot
- `MLIL_UNDEF` -- Undefined behavior
- `MLIL_UNIMPL` / `MLIL_UNIMPL_MEM` -- Unimplemented (with optional memory access)
