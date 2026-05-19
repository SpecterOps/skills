# OpenHound Register Extension

Use this reference when editing `main.py`, `extension.yaml`, package entry points, or extension identity metadata.

## Phase Registration

`src/<pkg>/main.py` owns the single `OpenHound` app instance and registers all phases.

```python
from dlt.extract.source import DltSource
from openhound.core.app import OpenHound
from openhound.core.collect import CollectContext
from openhound.core.convert import ConvertContext
from openhound.core.preproc import PreProcContext

from .lookup import EXLookup
from .transforms import transforms


app = OpenHound("myservice", help="OpenGraph collector for MyService")


@app.collect()
def collect(ctx: CollectContext) -> DltSource:
    from .source import source as myservice_source

    return myservice_source()


@app.preproc(transformer=transforms)
def preproc(ctx: PreProcContext) -> dict[str, str]:
    return {
        "assets": "assets",
    }


@app.convert(lookup=EXLookup)
def convert(ctx: ConvertContext) -> DltSource:
    from .source import source as myservice_source

    return myservice_source(), {}
```

Import the DLT source function inside phase functions to avoid import cycles with models that import `app` from `main.py`.

## App Rules

- Define exactly one `app = OpenHound(...)` instance.
- Keep the app in `src/<pkg>/main.py`.
- Models should import `app` from `openhound_<pkg>.main`.
- Do not create local app instances in model, source, graph, lookup, or transform modules.

## Collect Phase

The collect phase should return the DLT source from `source.py`.

```python
@app.collect()
def collect(ctx: CollectContext) -> DltSource:
    from .source import source as myservice_source

    return myservice_source()
```

## Preproc Phase

The preproc phase maps DuckDB table names to JSONL table names. Only listed tables are loaded into the lookup DB.

Use a transformer only when `transforms.py` contains SQL transforms:

```python
@app.preproc(transformer=transforms)
def preproc(ctx: PreProcContext) -> dict[str, str]:
    return {"assets": "assets"}
```

The left side is the DuckDB table name used in lookup methods. The right side is the resource name as defined in the `source.py` resource/transformer definition. Keep these aligned with the actual source output and lookup usage.

## Convert Phase

The convert phase returns the DLT source and an extras dictionary. The extras dictionary can pass static values to assets during graph conversion through `self._extras`.

```python
@app.convert(lookup=EXLookup)
def convert(ctx: ConvertContext) -> DltSource:
    from .source import source as myservice_source

    return myservice_source(), {}
```

Omit `lookup=...` only when no model uses `self._lookup`.

## Extension Metadata

`extension.yaml` declares extension identity, credentials and parameters. This file is only used for metadata and does not affect runtime behavior, but credential and parameter names should stay aligned with `source.py` secrets parameters.

```yaml
name: myservice
version: 0.1.0
type: local
credentials:
  - name: token
    description: API token
    required: true
parameters:
  - name: org
    description: Organisation slug
    required: true
```


## Package Entry Point

`pyproject.toml` should expose the app through the `openhound.sources` entry point group.

```toml
[project.entry-points."openhound.sources"]
myservice = "openhound_myservice.main:app"
```

Optional: For the cookiecutter template, preserve template variables when editing generated paths and names.

## Checklist

- `main.py` has one `OpenHound` app instance.
- All three `collect`, `preproc` (optional) and `convert` decorators are attached to that app instance.
- Lazy source imports happen inside phase functions where needed to avoid cycles and improve startup performance.
- Preproc table map includes every raw table needed by lookup if required.
- Convert registers lookup when models use `self._lookup`.
- `extension.yaml` matches source credentials and parameters.
- `pyproject.toml` entry point targets `openhound_<service>.main:app`.
- Read `references/validate-extension.md` before finishing.
