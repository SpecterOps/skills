# Cookbook

Common analysis recipes and patterns for working with Binary Ninja.

## Loading & Navigation

### Load a binary (headless)
```python
from binaryninja import load
with load('/bin/ls') as bv:
    print(f"{bv.arch.name}: {hex(bv.entry_point)}")
```

### Get all functions
```python
for func in bv.functions:
    print(func.name, hex(func.start), func.return_type)
```

### Find a function
```python
func = bv.get_functions_by_name("main")[0]     # by name (may return multiple)
func = bv.get_function_at(addr)                 # exact start address
func = bv.get_functions_containing(addr)[0]     # contains address
```

### Largest function
```python
max(bv.functions, key=lambda x: x.total_bytes)
```

## IL & Decompilation

### Access all IL forms
```python
for func in bv.functions:
    llil     = func.llil          # Low Level IL
    llil_ssa = func.llil.ssa_form # LLIL SSA
    mlil     = func.mlil          # Medium Level IL
    mlil_ssa = func.mlil.ssa_form # MLIL SSA
    hlil     = func.hlil          # High Level IL (decompilation)
    hlil_ssa = func.hlil.ssa_form # HLIL SSA
```

### Iterate all decompiled instructions
```python
for func in bv.functions:
    for inst in func.hlil.instructions:
        print(f"{inst.address} : {inst}")

# Or across entire binary:
for inst in bv.hlil_instructions:
    print(f"{inst.address} : {inst}")
```

### Map between IL levels
```python
hlil_inst = func.hlil[0]
hlil_inst.mlil    # approximate single MLIL mapping
hlil_inst.mlils   # all contributing MLIL instructions (most accurate)
hlil_inst.llil    # approximate single LLIL mapping
hlil_inst.llils   # all contributing LLIL instructions
```

## Call Graph Analysis

### Callers and callees
```python
func.callers    # list of functions that call this function
func.callees    # list of functions called by this function
```

### All call sites into a function
```python
for site in func.caller_sites:
    print(site.address, site.hlil)
```

### All calls made by a function
```python
for site in func.call_sites:
    print(site.address, site.hlil)
```

### Most connected function
```python
max(bv.functions, key=lambda x: len(x.callers + x.callees))
```

## Cross-References
```python
# HLIL cross-references of a function's callers
for ref in func.caller_sites:
    print(ref.hlil)
```

## Variables & Parameters

### Access variables
```python
all_vars      = func.vars               # all variables
hlil_vars     = func.hlil.vars          # variables used in HLIL
aliased_vars  = func.hlil.aliased_vars  # aliased variables
param_vars    = func.parameter_vars     # function parameters
```

### Stack variable info
```python
var = hlil_vars[0]
if var.source_type == StackVariableSourceType:
    print(var.storage)                    # stack offset
    print(var.offset_to_next_variable)    # distance to next var
    print(abs(var.type.width))            # type-based size
```

### SSA: find definition and uses
```python
ssa_vars = func.hlil.ssa_vars
def_inst = func.hlil.ssa_form.get_ssa_var_definition(ssa_vars[0])
use_insts = func.hlil.ssa_form.get_ssa_var_uses(ssa_vars[0])
```

### Query possible values of a call parameter
```python
for ref in func.caller_sites:
    if isinstance(ref.hlil, Call) and len(ref.hlil.params) >= 3:
        print(ref.hlil.params[2].possible_values)
```

## Pattern Matching with Traverse

### Find all calls to a specific function
```python
def find_calls(i, target_addr) -> str:
    match i:
        case HighLevelILCall(dest=HighLevelILConstPtr(constant=c)) if c == target_addr:
            return str(i)

for result in current_hlil.traverse(find_calls, target_addr):
    print(result)
```

### Collect all call targets
```python
def collect_targets(i) -> int:
    match i:
        case HighLevelILCall(dest=HighLevelILConstPtr(constant=c)):
            return c

targets = set(hex(a) for a in current_hlil.traverse(collect_targets))
```

### Count parameters per call
```python
def param_counter(i) -> int:
    match i:
        case HighLevelILCall():
            return len(i.params)

list(current_hlil.traverse(param_counter))
```

## Annotations & Types

### Rename a function
```python
func.name = "newName"
```

### Change function type signature
```python
func.type = Type.function(Type.void(), [])
func.type = Type.function(Type.int(4), [('buf', Type.pointer(bv.arch, Type.char())), ('len', Type.int(4))])
```

### Change parameter type
```python
func.parameter_vars[0].type = Type.pointer(bv.arch, Type.char())
```

### Create and apply a struct
```python
bv.define_user_type('MyStruct', Type.structure(members=[
    (Type.int(4), 'field_0'),
    (Type.pointer(bv.arch, Type.char()), 'name'),
    (Type.int(8), 'size')
]))
```

### Apply type to data variable
```python
bv.define_user_data_var(addr, "char*")
bv.get_data_var_at(addr).type = Type.int(4)
```

### Tags and bookmarks
```python
bv.add_tag(addr, "Crashes", "buffer overflow here")
func.add_tag("Important", "needs code-review")
func.add_tag("Bug", "off-by-one", addr)
```
