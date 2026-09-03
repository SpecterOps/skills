# Mythic 3.4 to 4.0 repository audit

Use this checklist to find likely migration work. Adapt file globs to the repository and prefer `rg`. A text match is evidence to inspect, not proof of an incompatibility.

## Establish the baseline

- Identify `requirements*.txt`, `pyproject.toml`, lockfiles, `go.mod`, Dockerfiles, container entrypoints, Mythic install metadata, eventing YAML, GraphQL documents, browser scripts, and integration tests.
- Record the current Mythic branch/tag, Python `mythic-container` version, Go `MythicContainer` module version, and Python `mythic` scripting version.
- Locate generated, vendored, fixture, and archived files so their hits can be classified separately.

## Suggested searches

Run only the searches relevant to present file types:

```bash
rg -n 'mythic[-_ ]?container|MythicContainer|(^|[" ])mythic([<=>~!]|$)' \
  -g 'requirements*.txt' -g 'pyproject.toml' -g 'poetry.lock' -g 'uv.lock' \
  -g 'go.mod' -g 'go.sum' -g 'Dockerfile*'

rg -n 'apitoken|[Aa]uthorization|[Bb]earer|mythic.*cookie|/api/v1\.4'

rg -n 'callbackgraphedge_(add|remove)|config_check|download_bulk|dynamic_query_function|rebuild_payload|redirect_rules|reissue_task(_handler)?|typedarray_parse_function|meHook'

rg -n '\b(task_ids?|tasks|callback_ids?|callbacks|parent_task_id)\b'

rg -n 'mythic\.apitoken|API_TOKEN|scopes:' -g '*.yaml' -g '*.yml' -g '*.json'

rg -n 'wrapped_payloads|supported_wrapper_payload_types|wrapper_payload_requirements|build_metadata'

rg -n 'browser_script|BrowserScript|\b(screenshot|download|search)\b'

rg -n '"processes"|process_id|parent_process_id|update_deleted'

rg -n 'SendMythicRPCAgentstorageCreateMessage|SendMythicRPCAgentStorageCreateMessage'

rg -n 'agent_file_id|file_id|host_file|download.*token|Authorization.*Bearer'
```

If a shell has difficult quoting, split a combined expression into smaller literal searches rather than weakening the audit.

## Classify each result

For every relevant match, record:

| Field | Meaning |
|---|---|
| Component | Server integration, scripting client, payload, wrapper, C2 profile, translation/consuming container, eventing, browser script, or agent response |
| Contract | Dependency, authentication, route, GraphQL action, identifier, RPC context, schema, or message shape |
| Confidence | Confirmed incompatibility, needs schema/context review, or false positive |
| Required change | Exact migration or further evidence needed |
| Validation | Unit, build, RPC, GraphQL, callback, file-transfer, or UI test that proves the change |

## High-risk review points

- Cookie-only and `apitoken`-header authentication no longer works for protected HTTP/GraphQL requests.
- Every v3.4 API token must be regenerated. Inventory consumers and required scopes, never token values.
- `/api/v1.4` was removed from action and webhook routes. Do not invent a replacement version prefix.
- Snake-case Hasura action names changed to camelCase. Regenerate clients or update stored documents.
- Public actions moved ambiguous task/callback arguments to display IDs. Confirm the called schema before renaming.
- Older container libraries cannot preserve v4 authenticated RPC context.
- Legacy scalar `mythic.apitoken` eventing input requests broad `*` access; migrate to the object form with explicit scopes.
- Wrapper compatibility fields were replaced by `wrapper_payload_requirements`, and builders should return architecture/format metadata.
- Legacy `screenshot`, `download`, and `search` browser-script renderers were removed.
- Process-browser response data moved host, OS, and deletion metadata around the process list.
- The Python agent-storage RPC class corrected `storage` to `Storage` in its name.
- C2 file hosting now receives a collection with per-file state, `agent_file_id`, and a short-lived bearer download token.

## Completion gate

Re-run the searches after migration. For every remaining match, either change it or document why it is valid under the v4 schema. Do not declare the migration complete from a clean build alone.
