# OpenHound Validate Extension

Use this reference before finishing changes to an OpenHound collector.

## Structural Checks

Review these before finishing:

- Kind strings are defined only in `kinds/nodes.py` and `kinds/edges.py`.
- Model files import kind constants instead of hardcoding strings.
- Node IDs are stable strings and not raw integer primary keys.
- The collector defines and emits a root/environment node.
- Every emitted node sets `environmentid` to the root/environment node ID.
- Every OpenGraph property dataclass field is documented in the class docstring's `Attributes` section.
- Every node-bearing asset declares `NodeDef(properties=...)`.
- `EdgeDef(...)` declarations match edges actually yielded by the same asset class.
- Edges to existing nodes use `ConditionalEdgePath` when property-based resolution is more reliable than constructing or guessing an ID.
- Edge properties use `yield` or `yield from` unless a list is explicitly justified.
- Models using `self._lookup` have `@app.convert(lookup=...)` registered.
- Tables required by lookup methods are included in the `preproc` map or created by transforms.
- `source.py` credentials are declared with `dlt.secrets.value`.
- `extension.yaml` credentials and parameters match the source function inputs.
- `models/__init__.py` exports newly added models.

## Validation Commands

Use an isolated uv virtual environment outside the repository so validation does not modify the user's local `.venv`:

```bash
export UV_PROJECT_ENVIRONMENT=/tmp/openhound-<source>-venv
uv run pytest
uv run ruff check src/
uv run mypy src/
```

Run the checks that are available for the generated collector.

If a command cannot run because dependencies, credentials, generated template variables, or external services are unavailable, report the skipped check and reason.

## Common Anti-Patterns

| Do not | Prefer |
|---|---|
| Hardcode `"EX_Asset"` in a model | Import `nk.ASSET` or `ek.RELATIONSHIP` from `kinds/`. |
| Use `id: int` as the OpenGraph node ID | Assign `self.id` from a stable string property or `BaseNode.guid(...)`. |
| Call `self._lookup` without preproc data | Register lookup and load or transform the required tables. |
| Add dataclass fields without descriptions | Add an `Attributes` entry describing each dataclass field. |
| Create multiple `OpenHound` app instances | Keep one app in `main.py`. |
| Declare edges on a different asset than the emitter | Put `EdgeDef(...)` on the emitting asset. |
| Emit nodes without `environmentid` | Set `environmentid` to the root/environment node ID. |
| Guess another node's ID manually | Use `ConditionalEdgePath` with stable `PropertyMatch` constraints. |

## Search Checks

Use AST or search checks where practical:

- No enum-style kind classes or kinds using fixed strings remain in model code.
- No `NodeDef(...)` is missing `properties=...`.
- Node property instantiations include required base fields such as `environmentid`.


## Final Response Guidance

When reporting completion, include:

- What nodes/edges are added or modified.
- What changes are made to the collection pipeline.
- Which validation commands ran or were skipped.
- Any other relevant changes.
- Any remaining risks or follow-up work.
