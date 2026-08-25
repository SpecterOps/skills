# Changelog

## 0.3.0

- Support arbitrary Go packages, including libraries and CLIs without a service surface.
- Make worker execution client-neutral and inherit the current model by default.
- Treat bundled agent files as portable protocols with a sequential fallback.
- Reduce false-positive SQL capability detection and expand analyzer tests.
- Document output sensitivity, portability, and syntax-analysis limitations.

## 0.2.0

- Replace regex-oriented Python inventory with a Go AST-backed analyzer.
- Add source provenance for the analyzer and review taxonomy.
