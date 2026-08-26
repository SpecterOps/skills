---
name: bhe-dev-bootstrap
description: Deprecated compatibility entrypoint for BloodHound Enterprise development. Use bhe-dev-environment for worktrees and local stacks, bhe-change-delivery for product changes and pull requests, and bhe-enterprise-review for review-only work.
---

# BHE Dev Bootstrap Compatibility Stub

This skill name is retained only as a compatibility entrypoint after the BHE development workflow was split by responsibility.

Route the request without performing the workflow here:

- Use `$bhe-dev-environment` for worktrees, prerequisites, local credentials, Docker or Compose stacks, startup troubleshooting, and safe stack release.
- Use `$bhe-change-delivery` for implementation, BHE/BHCE parity, validation, commits, pull-request preparation, CI diagnosis, and delivery follow-through.
- Use `$bhe-enterprise-review` for mutation-free review of an immutable candidate.
- Use `$bhe-ui-playwright` for browser validation and `$bhe-sample-data-ingest` for official sample-data loading.
