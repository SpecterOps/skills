# BNIL Overview

The Binary Ninja Intermediate Language (BNIL) is a family of tree-based, architecture-independent intermediate representations used throughout Binary Ninja.

## IL Hierarchy

The analysis pipeline lifts native instructions through progressively higher abstractions:

```
Native Assembly
  -> Lifted IL (raw translation from native semantics)
    -> LLIL (NOPs removed, flags folded into conditionals)
      -> LLIL SSA
        -> Mapped MLIL (translation layer, rarely needed)
          -> MLIL (registers -> variables, types, constants propagated)
            -> MLIL SSA
              -> HLIL (control flow recovery, dead code elimination, expression folding)
                -> HLIL SSA
```

Each layer can have different instructions -- an instruction present at one level may not exist at another.

## When to Use Each Level

| Level | Use When |
|-------|----------|
| **HLIL** | Understanding logic, vulnerability analysis, initial triage. Recovers if/while/for/switch. Tree-based with heavy folding. |
| **MLIL** | Precise data flow analysis. Variables have types, call parameters resolved, constants propagated. Less nesting than HLIL. |
| **LLIL** | Low-level semantics: register operations, flag behavior, stack manipulation. One-to-many mapping from assembly. |
| **Disassembly** | Raw instructions. Specific encodings, alignment, instruction-level detail. |

## Reading IL Notation

### Comparisons
All comparisons are explicitly signed or unsigned:
- `s<=`, `s>=`, `s<`, `s>` -- signed comparisons
- `u<=`, `u>=`, `u<`, `u>` -- unsigned comparisons

### Bitwise Operations
- `&&` -- standard bitwise operators
- `sx` -- sign-extend
- `zx` -- zero-extend

### Size Specifiers

Integer sizes:
- `.b` -- Byte (1 byte)
- `.w` -- Word (2 bytes)
- `.d` -- Dword (4 bytes)
- `.q` -- Qword (8 bytes)

Floating point sizes:
- `.h` -- Half (2 bytes)
- `.s` -- Single (4 bytes)
- `.d` -- Double (8 bytes)
- `.t` -- Ten (10 bytes)
- `.o` -- Oword (16 bytes)

Floating point operations are prefixed with `f`: `f*`, `f/`, `f+`, `f-`

### Variable Offsets
`:$offset` syntax indicates how many bits from the bottom of a variable the expression references.

Example: `sx.q(rax_2:0.d)` = lower 32 bits of variable `rax_2`, sign-extended to 64-bit.

### Macros

- `COMBINE(a, b)` -- Value twice the width, upper half `a`, lower half `b`. For 32-bit a,b: `(a << 32) | b`
- `LOWx(a)` -- Lower `x` bits of value `a` (size `2*x`). E.g., `LOWD(a)` = `a & 0xFFFFFFFF`
- `HIGHx(a)` -- Upper `x` bits of value `a`. E.g., `HIGHD(a)` = `a >> 32`
- `ROR(a, b)`, `ROL(a, b)` -- Rotate right/left value `a` by `b` bits
- `RRC(a, b)`, `RLC(a, b)` -- Rotate right/left with carry
- `TEST_BIT(a, b)` -- Test if bit `b` is set in `a`, equivalent to `(a & b) == b`
- `FCMP_O(a, b)` -- Floating point ordered comparison (both not NaN)
- `FCMP_UO(a, b)` -- Floating point unordered comparison (either is NaN)

## Using the API with ILs

### Checking Instruction Types
Use `isinstance()` with IL instruction classes:

```python
for h in current_hlil.instructions:
    if isinstance(h, Call):
        print(f"{h} is a Call")
    if isinstance(h, LocalCall):
        print(f"{h} has {len(h.params)} parameters")
```

### Visitors (for tree-based ILs)
Because BNIL is tree-based, naive iteration can miss nested expressions. Use visitor APIs:

- `visit` -- visits instructions only (not operands)
- `visit_all` -- visits instructions and their operands
- `visit_operands` -- visits operands only

Visitor callback receives: `(operand_name, inst, instr_type_name, parent)`

```python
def visitor(operand_name, inst, instr_type_name, parent):
    match inst:
        case Arithmetic(right=Constant()):
            print(f"{inst.address:#x} {inst}")

current_hlil.root.visit(visitor)
```

### Traverse API (HLIL)
The `traverse` API is preferred for HLIL pattern matching:

```python
def find_calls(i) -> int:
    match i:
        case HighLevelILCall():
            return len(i.params)

list(current_hlil.traverse(find_calls))
```
