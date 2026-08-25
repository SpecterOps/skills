# Source Provenance

This plugin draws on the following primary project sources. They were consulted
on 2026-08-25. The links and notes below record design influence; no source code
from these projects is vendored or copied into the plugin.

## OWASP Developer Guide: Go Secure Coding Practices

- Source: [OWASP Developer Guide — Go Secure Coding Practices](https://devguide.owasp.org/en/05-implementation/01-documentation/02-go-scp/)
- Provenance role: identifies the Go Secure Coding Practices material as
  implementation-focused documentation for secure Go web development.
- Influence here: supports actionable secure-coding checks for web-facing
  packages while the plugin also covers non-service Go packages.

## OWASP Go Secure Coding Practices Guide project

- Source: [OWASP project page](https://owasp.org/www-project-go-secure-coding-practices-guide/)
- Provenance role: canonical OWASP project identity and publication page for the
  Go guide.
- Influence here: anchors the plugin's Go-specific secure-coding scope and the
  attribution trail to the upstream OWASP project.

## OWASP Go-SCP repository

- Source: [OWASP/Go-SCP](https://github.com/OWASP/Go-SCP)
- Provenance role: primary repository for the hands-on Go web application secure
  coding guide, adapted topic-by-topic from OWASP secure coding practices.
- Influence here: informs the review taxonomy across input handling,
  authentication, storage, filesystem, cryptography, and web-service behavior.
- License note: the guide states that its documentation is CC BY-SA 4.0. This
  plugin references its concepts and URL; it does not reproduce guide text or
  examples.

## gosec

- Source: [securego/gosec](https://github.com/securego/gosec)
- Provenance role: primary implementation and documentation for a Go security
  checker that analyzes Go AST and SSA representations and supports the standard
  Go analysis interface.
- Influence here: motivates implementing source inventory in Go and inspecting
  parsed syntax rather than matching source text with regular expressions. The
  current inventory deliberately starts with the standard-library `go/parser`,
  `go/ast`, and `go/token` packages; SSA and taint analysis remain possible
  future extensions rather than implied current capabilities.
- License note: gosec is Apache-2.0. The plugin does not depend on or copy gosec
  code.

## Scope of the attribution

These sources guide taxonomy and architecture. They do not establish that a
specific target is vulnerable, and the skill must not cite them as evidence for
a finding. Every reported issue still requires an attacker-controlled path,
security-sensitive behavior, and target-specific evidence.
