---
cluster_id: filesystem-archive
consolidated: true
---

# Filesystem and Archive Review

Inventory path joins, archive extraction, temp files, symlinks, file modes,
uploads, downloads, and cleanup logic.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| PATH | path-traversal | attacker path escapes an intended root through join, clean, or absolute path handling |
| ARCHIVE | archive-slip | archive entry paths or symlinks escape extraction directories |
| TOCTOU | symlink-toctou | check-then-open, symlink following, or rename races across trust boundaries |
| TEMP | unsafe-temp-file | predictable temp paths, broad permissions, or unsafe reuse of attacker-visible files |

Trace the filesystem root invariant explicitly in each finding.
