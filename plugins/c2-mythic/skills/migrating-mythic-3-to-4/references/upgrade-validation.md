# Mythic 4 upgrade validation and rollback

Use this reference for a server upgrade or an end-to-end development test. Repository-only migrations should run their local tests and clearly state which live checks were not performed.

## Before changing a server

1. Schedule downtime and identify the decision-maker for rollback.
2. Back up the database and Mythic-managed files to explicit destinations:

   ```bash
   sudo ./mythic-cli backup database /path/to/mythic-backup
   sudo ./mythic-cli backup files /path/to/mythic-files-backup
   ```

3. Verify both backup artifacts exist and test restoration in a disposable environment when practical.
4. Record the running Mythic commit/tag, `mythic-cli` version, installed services, external integration configuration, and current health.
5. Inventory token consumers and intended v4 scopes without recording token values.

Do not execute these commands merely because this reference was loaded. A live upgrade requires explicit authorization for the named environment.

## Development upgrade sequence

1. Check out the intended Mythic v4 branch/tag and rebuild `mythic-cli`.
2. Start Mythic and allow its database migrations to complete.
3. Install or rebuild v4-compatible payload types, C2 profiles, translation containers, and consuming services.
4. Confirm server and UI versions, then inspect Installed Services for incompatible or offline containers.
5. Recreate automation tokens with minimum scopes, save each value directly to its secret store, and update callers to bearer authentication.
6. Do not print tokens in shell history, command output captured for reports, or test logs.

During the public beta, official examples use the `Mythic-v4.0.0` branch for Mythic and public compatible services. Verify that convention and dependency versions against current primary sources before use.

## Smoke-test matrix

| Area | Minimum evidence |
|---|---|
| Authentication | Login works; bearer access succeeds; missing/insufficient scopes fail as expected |
| GraphQL/actions | Updated action names resolve; display-ID arguments affect the intended operation-scoped object |
| Installed services | Every in-scope container syncs and remains online without missing-context errors |
| Payload builds | Normal payload and each wrapper combination build; unsupported wrapper combinations are rejected |
| Callback tasking | Checkin, get-tasking, create task, post-response, and cancellation/error behavior work |
| Files | Upload and download work; C2-hosted files use refreshed per-file tokens; resume/offset mode works if implemented |
| Process browser | Host/OS grouping and deletion updates render correctly |
| Eventing | Scoped token inputs work; insufficient scopes fail; approvals/input resume if used |
| Browser scripts | Supported text/table/media rendering works with authenticated URLs |
| External automation | Every inventoried script, bot, webhook, proxy, and custom client passes its focused test |

Keep exact commands and observed results. A UI-only check is not sufficient evidence for API or RPC compatibility.

## Rollback rule

Never point v3.4 services at a database after v4 migrations have run. To roll back:

1. Stop Mythic.
2. Restore the v3.4 code.
3. Restore both the pre-upgrade database and file backups.
4. Rebuild `mythic-cli` for the old version and start it.
5. Reapply external configuration changes made after the backup separately.

If either required backup is missing or unverified, report rollback as not ready and do not characterize the production upgrade as safe to begin.
