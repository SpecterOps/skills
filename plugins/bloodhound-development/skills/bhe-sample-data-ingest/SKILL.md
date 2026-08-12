---
name: bhe-sample-data-ingest
description: Download and ingest official BloodHound sample data into a local BloodHound Enterprise (BHE) or BloodHound CE development instance. Use when the user wants to load, reload, verify, or troubleshoot Active Directory and Azure/Entra sample data from the BloodHound quickstart into `bhe.localhost`, including API automation for `/api/v2/file-upload`, local admin login, ingest polling, and environment verification.
---

# BHE Sample Data Ingest

## Purpose

Use this skill to repeatably load the official BloodHound sample datasets into a local BHE/BHCE dev environment. Keep this separate from general BHE bootstrap: this skill assumes the app is already running or guides the user to start it first.

Official docs: `https://bloodhound.specterops.io/get-started/quickstart/ce-ingest-sample-data#ingest-sample-data`

## Preconditions

Confirm the local app is running:

```bash
curl -I http://bhe.localhost
```

Confirm local login credentials from the repo config instead of assuming them:

```bash
rg -n "default_admin|email_address|password" local-harnesses/build.config.json
```

Common local defaults are username `admin` and password `admin`, but always verify.

## Scripted Ingest

Prefer the bundled script for repeatability:

```bash
BHE_SAMPLE_SKILL_DIR="<directory containing this SKILL.md>"
node "$BHE_SAMPLE_SKILL_DIR/scripts/ingest_sample_data.cjs" \
  --base-url http://bhe.localhost \
  --repo <absolute-bhe-worktree-path> \
  --username admin@example.com \
  --password 'ChangeMe123!'
```

The script:

1. Downloads the official AD and Entra sample ZIPs into `local-harnesses/sample-data`.
2. Authenticates with `/api/v2/login`.
3. Starts an ingest job with `/api/v2/file-upload/start`.
4. Uploads both ZIPs with `Content-Type: application/zip` and `X-File-Upload-Name`.
5. Ends the job with `/api/v2/file-upload/{id}/end`.
6. Polls `/api/v2/file-upload` until complete or failed.
7. Prints available environments from `/api/v2/available-domains`.

Use `--help` to see options. If the user wants only AD or only Entra, pass `--dataset ad` or `--dataset entra`.

## Manual API Flow

If the script needs debugging, use this sequence:

1. `POST /api/v2/login`
   ```json
   {"login_method":"secret","username":"admin","secret":"admin"}
   ```

2. `POST /api/v2/file-upload/start`

3. For each ZIP, `POST /api/v2/file-upload/{ingestId}` with:
   ```text
   Authorization: Bearer <session_token>
   Content-Type: application/zip
   X-File-Upload-Name: ad_sampledata.zip
   ```

4. `POST /api/v2/file-upload/{ingestId}/end`

5. Poll:
   ```bash
   GET /api/v2/file-upload?limit=5
   GET /api/v2/file-upload/{ingestId}/completed-tasks
   GET /api/v2/available-domains
   ```

Expected success shape:

```text
status_message: Complete
failed_files: 0
partial_failed_files: 0
available environments include active-directory and azure entries
```

## Troubleshooting

- If `GET /api/v2/file-upload/accepted-types` returns 401, login first and include the bearer token.
- If upload returns an empty response body, treat HTTP 2xx as success; do not require JSON.
- If completed tasks only show AD files, still check overall job status and API logs. Azure/Entra may appear as one ZIP task while analysis logs show Azure post-processing.
- If ingest is stale or data needs a clean reload, ask before clearing volumes or using `just init clean`; that destroys local data.
- If `bhe.localhost` does not resolve, confirm Docker Compose proxy is running with:
  ```bash
  docker compose --profile dev -f docker-compose.dev.yml ps
  ```

## When To Update This Skill

Update this skill if official sample-data URLs change, endpoint shapes change, the local default repo path changes, or repeated manual verification steps emerge.
