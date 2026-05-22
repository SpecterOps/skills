# Important Concepts

## BinaryView

The top-level analysis object in Binary Ninja, representing a loaded binary. Think of it as what an OS does when loading an executable: memory mappings, sections, segments, functions, and metadata.

Key hierarchy: `BinaryView` -> `Function` -> `BasicBlock` -> `Instruction`

Some BinaryViews have parent views -- the analysis view includes memory mappings via segments/sections, while `parent_view` is the raw on-disk file.

## Walking ILs

### Iterating Instructions

LLIL and MLIL can be iterated linearly with reasonable safety:
```python
for func in bv.functions:
    for block in func.mlil:
        for instr in block:
            print(instr)
```

Or more directly:
```python
for inst in bv.mlil_instructions:
    if isinstance(inst, Localcall):
        print(inst.params)
```

### HLIL Tree Traversal

HLIL is heavily tree-based. Simple iteration **will miss nested expressions**. Use `traverse`:
```python
def find_strcpy(i, targets) -> str:
    match i:
        case HighLevelILCall(dest=HighLevelILConstPtr(constant=c)) if c in targets:
            return str(i.params[1].constant_data.data)

for result in current_hlil.traverse(find_strcpy, target_addrs):
    print(result)
```

## Mapping Between ILs

Translation between each IL layer is **many-to-many**. One assembly instruction may produce multiple LLIL instructions, and multiple MLIL instructions may collapse into one HLIL expression.

- `hlil_inst.llil` -- single (approximate) mapping down
- `hlil_inst.llils` -- **all** LLIL instructions that contributed (most correct)
- `hlil_inst.mlil` -- single mapping down
- `hlil_inst.mlils` -- all contributing MLIL instructions

Addresses in ILs are approximate and can change between analysis runs.

## Operating on IL vs Native

Scripts should operate on ILs (richer information). However, some operations (comments, tags) work on native addresses:
```python
bv.set_comment_at(address, "my comment")  # native address, IL-agnostic
```

## Instruction Index vs Expression Index

Both are integers, both unique per-function and per-IL level, but they are **distinct**:
- **Instruction Index** -- unique index for top-level IL instructions
- **Expression Index** -- unique index for expressions (including nested sub-expressions in the tree)

They start at 0 independently and must not be confused.

## Static Single Assignment (SSA)

In SSA form, variables are write-once. Each modification creates a new **version** (shown as `var#N`).

- `eax#1 = 5` -- version 1
- `eax#2 = eax#1 + 3` -- version 2 references version 1

When paths merge, a **PHI function** (`Phi`) aggregates versions:
- `eax#3 = Phi(eax#1, eax#2)` -- could be either version

### SSA Use Cases
- **Uninitialized variable detection**: SSA var read at version 0 that isn't a function argument
- **Data flow tracing**: Walk back through SSA definitions to find where a value originated
- **Inter-procedural analysis**: Build on SSA to trace values across function boundaries

### SSA API
```python
hlil_ssa_vars = func.hlil.ssa_vars
def_inst = func.hlil.ssa_form.get_ssa_var_definition(ssa_var)  # single definition
use_insts = func.hlil.ssa_form.get_ssa_var_uses(ssa_var)       # potentially many uses
```

## When IL APIs Return None

Binary Ninja caches generated IL (configurable via `analysis.limits.cacheSize`). Normally accessing `.llil` transparently generates IL if not cached. However, `None` is returned when analysis limits are triggered.

- `func.llil_if_available` -- returns IL only if already cached (no generation)
- `func.analysis_skip_reason` -- query why analysis was skipped
- `func.analysis_skip_override` -- override limits (**dangerous**)

## Function Sizing

No explicit `.size` property on functions. Two approaches:
- `func.total_bytes` -- sum of all basic block lengths (may double-count overlapping bytes)
- `func.highest_address - func.lowest_address` -- address range span

Functions end when all basic blocks terminate via: return, noreturn call, invalid instruction, branch to existing block, or interrupt.

## Auto vs User

API methods with `_auto_` are for automatic analysis (re-run on each open). Methods with `_user_` persist in the database and survive re-analysis. User actions are undoable. When annotating interactively or via scripts, use `_user_` variants.
