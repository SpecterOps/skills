# OpenHound Preproc And Lookup

Use this reference when relationships or node properties require data from multiple collected tables.

## Purpose

`preproc` loads selected raw JSONL tables into DuckDB, runs optional SQL transforms and produces lookup data used during `convert` through `self._lookup`.

Use this path when a model needs to resolve information that is not present in its own raw row.

## Files Usually Touched

- `src/<pkg>/transforms.py`
- `src/<pkg>/lookup.py`
- `src/<pkg>/main.py`
- `src/<pkg>/models/<name>.py`
- `src/<pkg>/source.py` if new raw tables must be collected

## Transforms

`transforms.py` should contain plain DuckDB SQL functions. Keep each transform focused and call them from a top-level `transforms` function.

```python
import duckdb


def create_joined_tables(con: duckdb.DuckDBPyConnection, schema: str = "myservice") -> None:
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {schema}.asset_groups AS
        SELECT asset_id, group_id
        FROM {schema}.asset_memberships
        """
    )


def transforms(con: duckdb.DuckDBPyConnection, schema: str = "myservice") -> None:
    create_joined_tables(con, schema)
```

Use parameter binding for values. Schema and table names are often interpolated because DuckDB does not bind identifiers; keep those values internal and trusted.

Use DuckDB JSON operators for JSON object fields loaded from raw resources:

```sql
SELECT metadata->>'name' AS name
FROM myservice.assets
```

## Preproc Registration

The `preproc` function in `main.py` returns a mapping of DuckDB table name to JSONL table name. Only listed tables are loaded into the lookup DB.

```python
@app.preproc(transformer=transforms)
def preproc(ctx: PreProcContext) -> dict[str, str]:
    return {
        "assets": "assets",
        "asset_memberships": "asset_memberships",
    }
```

If no SQL transforms are needed, the transformer can be omitted. If lookup methods depend on transformed tables, ensure the transformer is registered.

If `lookup.py` reads a table created by `transforms.py`, use `@app.preproc(transformer=transforms)`.

## Lookup Manager

`lookup.py` should define one extension lookup class extending `LookupManager`. Use `@lru_cache` for repeated lookups.

```python
from functools import lru_cache

from openhound.core.lookup import LookupManager


class EXLookup(LookupManager):
    
    def __init__(self, client: DuckDBPyConnection, schema: str = "myservice"):
        super().__init__(client, schema)
        self.schema = schema
        self.client = client
        
    @lru_cache
    def group_id_for(self, name: str) -> str | None:
        return self._find_single_object(
            f"SELECT node_id FROM {self.schema}.groups WHERE name = ?",
            [name],
        )


    @lru_cache
    def all_assets_domain(self, domain: str) -> list:
        return self._find_all_objects(
            f"SELECT * FROM {self.schema}.assets WHERE domain = ?",
            [domain],
        )
```

Prefer small lookup methods with clear names. The `_find_single_object` method will return `None` if no results are found.

## Convert Registration

Register the lookup class on `@app.convert(...)`:

```python
@app.convert(lookup=EXLookup)
def convert(ctx: ConvertContext) -> DltSource:
    from .source import source as myservice_source

    return myservice_source(), {}
```

The lookup is injected into each `BaseAsset` as `self._lookup` during convert.

## Model Usage

Use lookup methods from `as_node` or `edges` when needed:

```python
@property
def edges(self):
    group_id = self._lookup.group_id_for(self.group_name)
    if group_id is None:
        return

    yield Edge(
        kind=ek.MEMBER_OF,
        start=EdgePath(value=self.as_node.id, match_by="id"),
        end=EdgePath(value=group_id, match_by="id"),
    )
```

Document in the collector README when users must run `preproc` before `convert`.

## Rules

- Do not call `self._lookup` unless `convert` is registered with the lookup class.
- Do not assume raw tables are available in DuckDB unless they are returned by `preproc`.
- Keep transform output table names stable; lookup methods may depend on them.
- Avoid loading unnecessary raw tables into preproc.
- Cache deterministic lookup methods with `@lru_cache` or `@cache`.

## Checklist

- Required raw tables are collected by `source.py` and match with the defined resource/transformer name.
- Required raw tables are included in `main.py`'s `preproc` mapping.
- SQL transforms create any derived tables used by lookup methods.
- `@app.preproc(transformer=transforms)` is used when transforms are required.
- `@app.preproc(transformer=transforms)` is used when lookup reads transformed tables.
- `lookup.py` contains cached lookup methods.
- `@app.convert(lookup=<PREFIX>Lookup)` is registered.
- Models handle missing lookup results.
- Read `references/validate-extension.md` before finishing.
