---
name: cobalt-strike-malleable-c2-development
description: Malleable C2 profile development for Cobalt Strike. Use when writing C2 profiles or profile overrides for Cobalt Strike.
metadata:
  author: "Outflank"
---

# Malleable C2 Development Skill

## When to Use

Use this skill when developing Malleable profiles for Cobalt Strike:
- Writing new Malleable C2 profiles
- Creating Malleable profile overrides
- Looking up Malleable C2 options

## When NOT to Use

Do not use this skill unless Malleable C2 profile development is requested.

## Malleable C2 Overview

Cobalt Strike Beacon's indicators are controlled by a Malleable profile (also known as Malleable C2). A Malleable profile is a simple program that specifies how to transform data and store it in a transaction. Malleable C2 profiles also control Beacon’s in-memory characteristics, determine how Beacon does process injection, and influence Cobalt Strike’s post-exploitation jobs too.

## References

* [Malleable Profiles - C2](./references/malleable-c2/index.md)
* [Malleable Profiles - Post-exploitation](./references/malleable-postex/index.md)
