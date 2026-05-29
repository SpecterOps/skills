# ATRTO Stage 3 Reference

## Purpose

Use this reference when running stage 3 on later course migrations. It records the actual ATRTO QA and polish workflow that replaced the original stage-3 stub.

## What Stage 3 Did On ATRTO

- ran representative browser checks on homepage, slides, PDF pages, image-heavy pages, lab pages, and resource pages
- compared the deployed ATRTO preview to the current template-derived shell benchmark
- verified shell/style parity instead of forcing content parity
- ran a full derived-route sweep over all discovered content routes
- applied rendering-only polish fixes
- reran local build and targeted browser checks

## Preserve-Content Rule

- preserve the original course's content and information architecture
- use the template shell as the presentation benchmark only
- do not flatten or remove richer course material just to look more like the template shell

## What Counted As A Defect

- broken assets
- failed PDF embeds or downloads
- malformed links
- spacing artifacts caused by markdown syntax
- malformed callouts
- obvious rendering leftovers from the old theme

## What Counted As Acceptable

- richer labs landing content than the template shell
- richer resources landing content than the template shell
- additional course-specific resources not present in the template shell
- denser page content when rendering was correct

## Full Route Sweep Expectation

- derive routes from the content tree
- confirm status, title, and `h1` for every route
- treat route coverage as required before closing stage 3

## Proven ATRTO Examples

- accepted difference: content-rich `/labs/` and `/resources/`
- fixed polish items:
  - callout line-break cleanup
  - malformed note block in `rundll32`
  - markdown spacing cleanup
  - trailing whitespace cleanup in references and lab content
