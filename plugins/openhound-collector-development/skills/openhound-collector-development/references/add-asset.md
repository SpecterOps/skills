# OpenHound Add Asset

Use this reference when adding a new resource model under `src/<pkg>/models/` or changing how a model emits nodes and edges.

## Files Usually Touched

- `src/<pkg>/models/<name>.py`
- `src/<pkg>/models/__init__.py`
- `src/<pkg>/kinds/nodes.py`
- `src/<pkg>/kinds/edges.py`
- `src/<pkg>/source.py`
- `src/<pkg>/main.py` if lookup/preproc table registration is required
- `src/<pkg>/transforms.py` and `src/<pkg>/lookup.py` if cross-table lookup is required

## Model Structure

Every collected asset should define two things:

1. A dataclass named `<Name>Properties` extending the extension base `<PREFIX>NodeProperties`.
2. A Pydantic `BaseAsset` subclass named `<Name>` decorated with `@app.asset(...)`.

The raw fields on the `BaseAsset` class should mirror the collected JSONL schema. The dataclass properties should describe the OpenGraph node properties emitted during conversion.

## Property Dataclasses

Every OpenGraph property field must be documented in the class docstring's `Attributes` section:

```python
from dataclasses import dataclass

from openhound_<pkg>.graph import EXNodeProperties


@dataclass
class AssetProperties(EXNodeProperties):
    """Properties for the Asset node.
    
    Attributes:
        hostname: The asset hostname.
    """
    hostname: str
```

Prefer nullable types over placeholder sentinels when data can be absent:

```python
group_name: str | None = None
```

Do not use empty strings to mean missing data unless the upstream API explicitly distinguishes empty string from null.

## Asset Classes

Use `@app.asset(...)` with `NodeDef` for node-bearing assets and `EdgeDef` for relationships emitted by that same class.

```python
from openhound.core.asset import BaseAsset, EdgeDef, NodeDef
from openhound.core.models.entries import Edge, EdgePath

from openhound_<pkg>.graph import EXNode
from openhound_<pkg>.kinds import edges as ek
from openhound_<pkg>.kinds import nodes as nk
from openhound_<pkg>.main import app


@app.asset(
    node=NodeDef(kind=nk.ASSET, properties=AssetProperties, description="Example asset", icon="cog"),
    edges=[
        EdgeDef(
            start=nk.ASSET,
            end=nk.GROUP,
            kind=ek.MEMBER_OF,
            description="Asset belongs to group",
        )
    ],
)
class Asset(BaseAsset):
    id: str
    name: str
    groups: list[str]

    @property
    def as_node(self) -> EXNode:
        properties = AssetProperties(
            node_id=self.id,
            name=self.name,
            displayname=self.name,
            environmentid=self._extras["environmentid"],
        )
        return EXNode(properties=properties, kinds=[nk.ASSET])

    @property
    def edges(self):
        for group_id in self.groups:
            yield Edge(
                kind=ek.MEMBER_OF,
                start=EdgePath(value=self.as_node.id, match_by="id"),
                end=EdgePath(value=group_id, match_by="id"),
            )
```

## Edge Definition Alignment

Only declare `EdgeDef(...)` entries on the asset class that emits those edges from its `edges` property.

If a node-bearing asset creates only a node, use only `node=NodeDef(...)` and emit no edges. If relationships are represented by a separate edge-only asset, put the `EdgeDef(...)` declarations on that edge-only asset.

If a helper emits a shared edge, such as a root/environment containment edge, declare the matching `EdgeDef(...)` on every asset that yields it.

## Edge Emission Style

Prefer generators:

```python
@property
def _access_edges(self):
    for target_id in self.target_ids:
        yield Edge(...)

@property
def edges(self):
    yield from self._access_edges
```

Avoid building `edges = []`, appending items, and returning the list unless there is a specific reason.

## Conditional Edge Paths

Prefer `ConditionalEdgePath` when creating an edge to an existing node that should be resolved by node properties instead of a known OpenGraph ID.

Use `PropertyMatch` entries for the stable property constraints needed to uniquely identify the target node. Avoid weak matchers, such as only `name`, unless the upstream domain guarantees uniqueness.

Use `EdgePath(value=..., match_by="id")` when the exact stable node ID is already known.

```python
from openhound.core.models.entries import ConditionalEdgePath, Edge, EdgePath, PropertyMatch
from openhound.core.models.entries_dataclass import EdgeProperties


yield Edge(
    kind=ek.MEMBERSHIP_SYNC,
    start=ConditionalEdgePath(
        kind=nk.GROUP,
        property_matchers=[
            PropertyMatch(key="tenant_domain", value=source_domain),
            PropertyMatch(key="type", value="OKTA_GROUP"),
            PropertyMatch(key="name", value=self.profile.name.upper()),
        ],
    ),
    end=EdgePath(value=self.id, match_by="id"),
    properties=EdgeProperties(traversable=True),
)
```

## Lookup Usage

Use `self._lookup` inside `as_node` or `edges` only when `preproc` creates and registers the required lookup data.

```python
@property
def as_node(self) -> EXNode:
    org_node_id = self._lookup.org_id_for(self.org_name)
    properties = AssetProperties(node_id=self.id, org_id=org_node_id)
    return EXNode(properties=properties, kinds=[nk.ASSET])
```

## Checklist

- Create or update `src/<pkg>/models/<name>.py`.
- Add node kind constants to `kinds/nodes.py` if the asset emits nodes.
- Add edge kind constants to `kinds/edges.py` if the asset emits edges.
- Assets returning a node must pass the emitted property dataclass into `NodeDef(properties=...)`.
- Export the model from `src/<pkg>/models/__init__.py`.
- Add or update a resource or transformer in `source.py`.
- Wire the resource or transformer into the source return tuple.
- If lookup data is needed, update `transforms.py`, `lookup.py`, and the `preproc` table map in `main.py`.
- Read `references/validate-extension.md` before finishing.
