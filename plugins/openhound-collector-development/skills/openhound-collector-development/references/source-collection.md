# OpenHound Source Collection

Use this reference when editing `src/<pkg>/source.py` or changing when/how upstream API data is collected.

## Source Pattern

`source.py` wires API collection into OpenHound/DLT. It usually contains:

- A `SourceContext` dataclass for the authenticated client and shared state.
- `@app.resource(...)` functions defining how resources are collected from the API.
- `@app.transformer(...)` functions for nested collection seeded by parent `@app.resource` resources.
- An `@app.source(...)` function that declares credentials, builds context and returns resources/transformers to be processed.

## Authentication

Credentials should come from DLT secrets under `[sources.source.<source>]` in `.dlt/secrets.toml` and should be declared with `dlt.secrets.value` parameters on the source function.

Example secrets file:

```toml
[sources.source.myservice]
token = "xxx"
host = "https://api.myservice.com"
org_name = "my-org"
```

Environment variables can also provide the same values, for example `SOURCES__SOURCE__MYSERVICE__TOKEN`.

If authentication is complex, add a dedicated `auth.py` module.

## Source Context

Use a context object to keep resource functions simple and consistent:

```python
from dataclasses import dataclass

from dlt.sources.rest_api import RESTClient


@dataclass
class SourceContext:
    client: RESTClient
```

Add shared identifiers, tenant/org names, rate limit helpers, or authenticated clients to this dataclass when needed.


## Rest API Client

Important: Prefer using `dlt.sources.rest_api.RESTClient` for API collection.  This client has built-in support for pagination, retries, rate limit handling and logging. If the API has specific needs, extend `RESTClient` with a custom client class in a dedicated `client.py` module.

## Resources And Transformers

Use `@app.resource(name=..., columns=<Model>)` for top-level collection. The `columns` model should reference the `BaseAsset` Pydantic class that validates yielded rows.

Use `@app.transformer(name=..., columns=<Model>)` for nested collection that depends on each parent item.

```python
@app.resource(name="assets", parallelized=True, columns=Asset)
def assets(ctx: SourceContext):
    for item in ctx.client.paginate("/assets"):
        yield item


@app.transformer(name="asset_users", parallelized=True, columns=AssetUser)
def asset_users(asset, ctx: SourceContext):
    for item in ctx.client.paginate(f"/assets/{asset.id}/users"):
        yield item
```

## DLT Source Function

Wrap the resources in an `@app.source(...)` function. Build the context once, create parent resources once, and use DLT's pipe operator for transformers.

```python
import dlt
from dlt.sources.rest_api import HeaderLinkPaginator, RESTClient
from dlt.sources.rest_api.auth import BearerTokenAuth


@app.source(name="myservice", max_table_nesting=0)
def source(token=dlt.secrets.value, host=dlt.secrets.value):
    ctx = SourceContext(
        client=RESTClient(
            base_url=host,
            auth=BearerTokenAuth(token=token),
            paginator=HeaderLinkPaginator(),
        )
    )

    assets_resource = assets(ctx)
    return (
        assets_resource,
        assets_resource | asset_users(ctx),
    )
```

Use `max_table_nesting=0` unless there is a concrete reason to let DLT infer nested tables.

## Collection Rules

- Yield raw dictionaries or objects shaped to match the `columns` model.
- Keep API pagination inside resource and transformer functions.
- Keep node/edge conversion logic out of `source.py`. Conversion belongs in model classes.
- Do not make resource functions reach into DuckDB lookup data.
- Avoid collecting fields that are not needed for graph conversion, lookup, metadata, or debugging.
- Do not collect or emit secrets, tokens, credentials, private keys, or credential-equivalent material.
- Name resources after the raw table they produce, using stable plural table names where practical.

## Checklist

- Credentials are declared with `dlt.secrets.value`.
- Source context contains authenticated clients and shared state.
- Each resource or transformer has the correct `columns=<Model>`.
- The Pydantic model should be saved under `models/` and exported from `models/__init__.py`.
- Parent resources reused by transformers are assigned to variables before piping.
- All resources/transformers are returned from the source function.
- Read `references/validate-extension.md` before finishing.
