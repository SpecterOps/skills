# Component-specific Mythic 4 changes

Read only the sections matching the components found during the audit. Confirm exact language APIs against the current compatible container library; these examples describe contracts, not immutable package syntax.

## HTTP, GraphQL, and scripting integrations

- Send access tokens and API tokens as `Authorization: Bearer <token>`; remove the legacy `apitoken` header and cookie-only assumptions.
- Recreate v3.4 API tokens with minimum scopes. Store a created token immediately in the caller's secret store because Mythic shows it only once and stores only a hash.
- Remove `/api/v1.4` from Mythic action and webhook paths. Consult current Hasura metadata or supported libraries instead of substituting a new prefix.
- Rename affected Hasura actions:

| Mythic 3.4 | Mythic 4 |
|---|---|
| `callbackgraphedge_add` | `callbackgraphedgeAdd` |
| `callbackgraphedge_remove` | `callbackgraphedgeRemove` |
| `config_check` | `configCheck` |
| `download_bulk` | `downloadBulk` |
| `dynamic_query_function` | `dynamicQueryFunction` |
| `rebuild_payload` | `rebuildPayload` |
| `redirect_rules` | `redirectRules` |
| `reissue_task` | `reissueTask` |
| `reissue_task_handler` | `reissueTaskHandler` |
| `typedarray_parse_function` | `typedarrayParseFunction` |
| `meHook` | `whoami` |

- For public actions, migrate ambiguous `task_id`, `task_ids`, `callback_id`, `callback_ids`, and `parent_task_id` arguments to their `*_display_id` forms when the v4 schema requires it. Do not alter direct table queries or internal messages that explicitly use primary-key `id` fields.
- Use `apiTokenScopeDefinitions`, `scopeCheck`, and `whoami` to inspect available scopes and the active identity.

## Containers and RabbitMQ RPC

- Move Python and Go services to a currently supported v4 container-library release before debugging authorization-context errors.
- Hand-written RabbitMQ clients must preserve authenticated context when forwarding work. Validate both allowed and denied RPC calls.
- Update Python references from `SendMythicRPCAgentstorageCreateMessage` to `SendMythicRPCAgentStorageCreateMessage`.
- Remove obsolete payload/C2/translation resync send paths when the installed library no longer exposes them.

## Eventing workflows

Replace broad scalar token input with a scoped object:

```yaml
inputs:
  API_TOKEN:
    type: mythic.apitoken
    scopes:
      - callback.read
      - task.write
      - response.read
```

The step token is temporary and invalidated when the step completes. Grant only scopes required by that function. Also test workflows that pause for approval or typed input if they adopt the new v4 capability.

## Payload builders and wrappers

- Replace `wrapped_payloads` and `supported_wrapper_payload_types` with `wrapper_payload_requirements`.
- Have normal payload builders return `build_metadata` describing architecture and format; Mythic already records the selected OS.
- Have wrappers declare accepted OS/architecture/format combinations and any conditions on their own build parameters.
- Test every supported combination and at least one rejected combination. Compatibility discovery in the UI is part of the contract.

Consult `$mythic-implant-development` for payload definitions and build behavior after applying these v4 deltas.

## Browser scripts

- Replace removed `screenshot`, `download`, and `search` result renderers with currently supported plaintext, table, or media structures.
- Use authenticated current file/media URLs.
- Remove assumptions about obsolete operation-specific browser-script mappings.
- Test empty, malformed, and large results as well as the successful rendering path.

## Agent process-browser messages

In v4, `processes` is an object containing shared metadata and the process list. Move repeated `host`, `os`, and `update_deleted` values out of each process item:

```json
{
  "processes": {
    "host": "workstation1",
    "os": "windows",
    "update_deleted": true,
    "processes": [
      {"process_id": 5, "parent_process_id": 2}
    ]
  }
}
```

Preserve the outer post-response envelope and task UUID required by the current agent-message contract. Consult `$mythic-implant-development` for the complete wire flow.

## C2 profile file hosting

- Accept the v4 host-file message containing all hosted files rather than assuming one add/remove event per message.
- Track each file's add/remove state, path, and `agent_file_id`.
- Use its download token as `Authorization: Bearer <token>` when retrieving that file. The token is scoped to one `agent_file_id`, is not permanent, and can change after a Mythic restart.
- Update cached tokens when Mythic sends refreshed state; never log them.

Consult `$mythic-profiles` for listener/container implementation details after applying these v4 deltas.

## Optional v4 capabilities

Offset-based and resumable transfers, interactive file editing, richer parameters, task references, operator aliases, agent RPC, and extended custom RPC timeouts are enhancements, not automatic migration requirements. Add them only when requested or when existing behavior depends on them; keep compatibility remediation separate from feature expansion.
