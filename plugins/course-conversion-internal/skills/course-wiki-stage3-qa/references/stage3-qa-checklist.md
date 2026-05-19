# Course Wiki Stage 3 QA Checklist

## Stage 1 QA

- homepage loads
- page title matches the course
- `Labs`, `Resources`, and `Slides` load
- branding assets render
- search/navigation shell renders
- local preview uses a Hugo binary compatible with the Hextra theme

## Stage 2 QA

- homepage matches the template-style shape
- slides page works
- representative cheatsheet PDF works
- representative image-heavy lab page works
- representative resource page works
- representative lab page shows docs-style sidebar when expected
- representative lab-solution page shows docs-style sidebar when expected
- expand/callout UI remains readable in dark mode
- representative page with long sample-output blocks renders without leaked Hextra copy-button chrome
- moved links still resolve
- no obvious rendering leftovers from the old theme remain

## Full Route Sweep

- derive all expected routes from the course `content/` tree
- confirm `200` status for every derived route
- confirm page title for every derived route
- confirm primary `h1` for every derived route

## Build Output Sanity Sweep

- grep built HTML/XML for leaked Hextra chrome inside article content:
  - `hextra-code-copy-btn`
  - `hextra-copy-icon`
  - `Copy code`
- confirm no migrated pages leak escaped button/div markup into code or prose
- confirm no known broken internal route casing remains
- spot-check for bare prose URLs that should be descriptive links instead

## Template Comparison

- compare homepage to the template shell
- compare labs landing to the template shell
- compare resources landing to the template shell
- compare slides page to the template shell
- compare one shared resource-style page such as Guacamole
- preserve course-specific content when it is working; do not flatten content only for parity

## Targeted Polish

- fix only rendering and presentation defects
- preserve course text and structure
- rerun build and affected browser checks after fixes
- prefer layout/css/markdown normalization over content rewriting
- normalize bare output fences to `text` where that prevents rendering defects
- replace HTML-like placeholder tokens in sample output when they break markdown/Hextra rendering

## Findings Format

Group findings under:
- navigation
- broken assets
- PDF rendering
- layout or spacing mismatches
- content placement issues
- dark-mode issues
- code-block rendering issues
- deployed-preview authentication or asset-loading issues

Also include:
- acceptable intentional differences from the template shell
- full route sweep summary
- build-output sanity sweep summary
- post-fix validation status
- residual risks
