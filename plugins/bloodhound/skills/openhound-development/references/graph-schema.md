# OpenHound Graph Schema

Use this reference when editing `src/<pkg>/graph.py` or changing extension-wide OpenGraph node and edge property behavior.

## Purpose

`graph.py` defines the OpenHound extension's base dataclass types for nodes, node properties, and edge properties. These types are imported by model files and lookup-related code.

## Naming

Use the extension prefix consistently:

- `<PREFIX>NodeProperties`
- `<PREFIX>Node`
- `<PREFIX>EdgeProperties`

For example, GitHub might use `GHNodeProperties`, `GHNode`, and `GHEdgeProperties`.

## Base Node Properties

The base properties class should extend `NodeProperties` from `openhound.core.models.entries_dataclass`.

Add only fields that every node in the extension should have.

```python
from dataclasses import dataclass

from openhound.core.models.entries_dataclass import NodeProperties as BaseProperties


@dataclass
class EXNodeProperties(BaseProperties):
    """Base properties for all nodes in the extension.
    
    Attributes:
        node_id: The platform native unique identifier.
    """
    node_id: str
```

Every field must include docstrings specifying the attributes with a description because this is used for generated documentation.

Every collector should have one root/environment node. When a collector emits multiple resource nodes, include `environmentid` in the base node properties and set it to the OpenGraph ID of that root/environment node.

## Node Class

The node class should extend `Node` from `openhound.core.models.entries_dataclass` and set `self.id` in `__post_init__`.

```python
from dataclasses import dataclass, field

from openhound.core.models.entries_dataclass import Node as BaseNode


@dataclass
class EXNode(BaseNode):
    properties: EXNodeProperties
    kinds: list[str]
    id: str = field(init=False)

    def __post_init__(self):
        self.id = self.properties.node_id
```

## Node ID Rules

Prefer the platform's native opaque/global node ID when available and only when the native ID is consistent and unique.

Do not use raw integer primary keys as OpenGraph node IDs. They are not stable enough across systems and can collide across extensions.

If the platform does not expose a suitable ID, derive one from stable properties with `BaseNode.guid(...)`:

```python
def __post_init__(self):
    self.id = self.guid(self.properties.tenant_id, self.properties.slug)
```

Use reproducible values only. Do not include timestamps, random values, pagination offsets or mutable display names unless they are the best stable identifier the service provides.

## Edge Properties

The extension edge property class should extend `EdgeProperties`.

```python
from dataclasses import dataclass

from openhound.core.models.entries_dataclass import EdgeProperties


@dataclass
class EXEdgeProperties(EdgeProperties):
    reason: str | None = None
```

Add shared fields only when they apply broadly across extension edges. Entity-specific relationship fields can stay closer to the emitting model when appropriate.

## Graph Schema Rules

- Keep `graph.py` generic to the extension, not specific to one entity.
- Avoid importing model classes into `graph.py`.
- Avoid importing `app` into `graph.py`.
- Do not define kind strings in `graph.py`; use `kinds/nodes.py` and `kinds/edges.py`.
- Do not add compatibility aliases unless there is persisted data, shipped behavior, external consumers, or an explicit requirement.

## Checklist

- Prefix classes match the service prefix.
- Base node properties extend the OpenHound base properties class.
- Node class extends the OpenHound base node class.
- `id` is assigned in `__post_init__`.
- Node ID is stable and string-compatible.
- Base node properties include `environmentid` when the collector emits a root/environment node.
- Every graph property contains docstrings with an "Attributes" section describing each field.
- Read `references/validate-extension.md` before finishing.
