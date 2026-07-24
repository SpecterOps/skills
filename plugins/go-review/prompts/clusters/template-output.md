---
cluster_id: template-output
consolidated: true
---

# Template and Response Output Review

Inventory template packages, response writers, header construction, redirect
targets, and any conversion to trusted HTML or JS content.

## Passes

| Prefix | Bug class | Look for |
|--------|-----------|----------|
| TEXTTPL | text-template-html | `text/template` used for HTML or browser-facing output |
| TPLBYPASS | unsafe-template-bypass | `template.HTML`, `template.JS`, `template.URL`, or custom escaping bypass on attacker data |
| RESPHDR | response-header-injection | attacker data reaches `Header().Set`, redirects, or content disposition without validation |

File only when output reaches a browser or protocol consumer that interprets it.
