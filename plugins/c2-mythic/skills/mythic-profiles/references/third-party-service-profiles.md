# Third-Party Service C2 Profiles

Use this reference for profiles that broker traffic through an external service such as chat, storage, webhook, paste, issue tracker, or queue APIs.

## Design concerns

- Credentials: token/API key scopes, storage, rotation, and redaction in logs.
- Polling: interval, jitter, backoff, and rate-limit handling.
- Message shape: encode agent messages into service-native fields, files, comments, embeds, or objects.
- Idempotency: prevent duplicate task pickup or duplicate response processing.
- Ordering: preserve task/response order when the service is eventually consistent.
- Size limits: chunk large messages and file transfers.
- OPSEC: user-agent, object names, channels, path conventions, timing, and cleanup.
- Failure modes: expired tokens, 429s, deleted channels/buckets/objects, auth revocation, and partial uploads.

## Parameter suggestions

- `callback_interval`, `callback_jitter`
- service URL or tenant/workspace/team identifier
- channel/bucket/folder/object prefix
- API token or credential reference; avoid hardcoded secrets
- proxy settings
- max chunk size
- cleanup/delete-after-read behavior
- rate-limit backoff controls

## Validation

1. Create a development service workspace or isolated test channel/bucket.
2. Build payload with the profile selected.
3. Confirm checkin creates expected service-side object/message.
4. Confirm get-tasking and post-response round trips.
5. Exercise rate-limit/backoff path intentionally if safe.
6. Confirm logs redact credentials and do not dump task contents.
7. Confirm cleanup behavior matches operator expectations.
