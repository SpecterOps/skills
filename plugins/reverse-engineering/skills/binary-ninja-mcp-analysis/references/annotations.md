# Annotations Reference

## Symbols

Rename a function:
```python
func.name = "newName"
```

Create and apply a symbol:
```python
sym = Symbol(SymbolType.FunctionSymbol, addr, "myName")
bv.define_user_symbol(sym)
```

Symbol types:
| Type | Description |
|------|-------------|
| `FunctionSymbol` | Function in current binary |
| `ImportAddressSymbol` | Import Address Table entry |
| `ImportedFunctionSymbol` | Function not in current binary |
| `DataSymbol` | Data in current binary |
| `ImportedDataSymbol` | Data not in current binary |
| `ExternalSymbol` | External data/code |
| `LibraryFunctionSymbol` | Shared library function |
| `SymbolicFunctionSymbol` | Abstract function |
| `LocalLabelSymbol` | Local label |

## Tags

### Create a tag type
```python
bv.create_tag_type("Vulnerability", "!!")
```

### Data tags (at any address)
```python
bv.add_tag(addr, "Vulnerabilities", "buffer overflow")
```

### Function tags (labels entire function)
```python
func.add_tag("Important", "needs code-review")
```

### Address tags (labels specific instruction)
```python
func.add_tag("Bug", "off-by-one error", addr)
```

## Types

### Creating Types

**Via parser (convenient but slow):**
```python
bv.parse_type_string("uint64_t")  # returns (Type, name)
```

**Integer types:**
```python
Type.int(4)              # 4-byte signed
Type.int(8, False)       # 8-byte unsigned
```

**Pointer types:**
```python
Type.pointer(bv.arch, Type.int(4))
Type.pointer(bv.arch, Type.void(), const=True)
```

**Array types:**
```python
Type.array(Type.int(4), 10)  # array of 10 ints
```

**Function types:**
```python
Type.function(Type.void(), [])
Type.function(Type.int(4), [('buf', Type.pointer(bv.arch, Type.char())), ('len', Type.int(4))])
```

**Structures:**
```python
# Anonymous
Type.structure(members=[(Type.int(4), 'x'), (Type.int(4), 'y')])

# Named (registered with BinaryView)
bv.define_user_type('Point', Type.structure(members=[
    (Type.int(4), 'x'),
    (Type.int(4), 'y')
]))

# Reference a named type
ntr = Type.named_type_from_registered_type(bv, 'Point')
bv.define_user_type('Line', Type.structure(members=[
    (ntr, 'start'),
    (ntr, 'end')
]))
```

**Unions:**
```python
Type.structure(members=[(Type.int(4), 'i'), (Type.float(4), 'f')],
               type=StructureVariant.UnionStructureType)
```

**Enumerations:**
```python
Type.enumeration(members=[('NONE', 0), ('READ', 1), ('WRITE', 2)])
bv.define_user_type('Access', Type.enumeration(members=[('NONE', 0), ('READ', 1), ('WRITE', 2)]))
```

### Modifying Existing Types
```python
with Type.builder(bv, 'MyStruct') as s:
    s.append(Type.int(2))  # add new field
```

### Applying Types

**To a function:**
```python
func.type = Type.function(Type.void(), [])
```

**To a parameter:**
```python
func.parameter_vars[0].type = Type.pointer(bv.arch, Type.char())
```

**To a data variable:**
```python
bv.get_data_var_at(addr).type = Type.int(4)
# Or create one if none exists:
bv.define_user_data_var(addr, "char*")
```

### Accessing Types
```python
bv.types['Elf64_Header']                    # lookup by name
bv.get_type_by_name('Elf64_Header')         # alternative lookup
header = bv.get_data_var_at(bv.start)       # typed data variable
header['ident']['signature'].value           # access struct fields
```

### Named Type References

In Binary Ninja, struct/enum names are separate from definitions (like C). To reference a named type inside another type:
```python
ntr = Type.named_type_from_registered_type(bv, 'ExistingType')
# Use ntr as a member type in another struct
```

## Signature Libraries

Binary Ninja matches statically-compiled functions against signature libraries, auto-renaming matched functions. Signatures load from:
- `$INSTALL_DIR/signatures/$PLATFORM`
- `$USER_DIR/signatures/$PLATFORM`

The signature matcher runs automatically after analysis (configurable via `analysis.signatureMatcher.autorun`).
