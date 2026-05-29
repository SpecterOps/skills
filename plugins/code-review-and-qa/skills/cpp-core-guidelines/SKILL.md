---
name: cpp-core-guidelines
description: Apply a condensed version of the ISO C++ Core Guidelines to C++ design, implementation, refactoring, modernization, and code review. Use for .cpp, .cc, .cxx, .h, .hpp, CMake-backed C++ projects, API design, ownership/lifetime decisions, RAII, const-correctness, templates, concurrency, error handling, performance, C interop, and standard-library usage.
---

# C++ Core Guidelines

## Overview

Use this skill to apply modern C++ guidance derived from the ISO C++ Core Guidelines. Prefer safer, clearer, statically checkable C++ without sacrificing zero-overhead design.

## Workflow

1. Identify the task shape: new design, implementation, refactor, modernization, review, or bug fix.
2. Read `references/core-guidelines-condensed.md` when the task touches C++ behavior, APIs, ownership, templates, concurrency, performance, or code review.
3. Apply the guidelines pragmatically:
   - Prefer explicit interfaces, strong types, invariants, RAII, standard-library facilities, and compile-time checking.
   - Preserve project conventions when they conflict only cosmetically.
   - Treat raw ownership, unchecked bounds, data races, invalid lifetimes, implicit global state, naked allocation, C casts, and macro-based code as high-priority risks.
4. When reviewing, lead with concrete bugs and maintenance risks, not style preferences. Reference the relevant Core Guidelines family, such as `R` for resources, `F` for functions, or `CP` for concurrency.
5. When changing code, keep edits scoped, add regression tests for behavior changes, and prefer mechanical/tool-enforceable improvements.

## Resource

- `references/core-guidelines-condensed.md`: condensed concept map and review checklist covering the guideline families: philosophy, interfaces, functions, classes, enums, resources, expressions/statements, performance, concurrency, errors, constants, templates, C interop, source files, standard library, architecture, profiles, GSL, and naming/layout.
