---
name: macos-initial-access
description: Provide concise, macOS guidance for authorized initial-access delivery using app bundles, installer packages, and disk images, including current Gatekeeper behavior and pkgbuild and hdiutil examples.
metadata:
  author: "Outflank"
---

# macOS Initial Access

## Overview

- Some of the format-specific commands will only run on macOS.
- Clearly label any behavior that depends on signing, quarantine, management policy, or Office configuration.
- You aren't limited to the formats described in this skill.
- Keep commands copyable, explain the expected directory layout in one sentence.

## Trust controls

Explain these in one short paragraph unless the user asks for detail:

- Code signing: Binds developer identity and integrity metadata to code; signatures also carry entitlements. Sign every nested executable, framework, and helper before signing the outer bundle.
- Hardened Runtime: Adds runtime restrictions against injection, process tampering, unsigned executable memory, DYLD manipulation, and untrusted libraries. Exceptions require specific entitlements. It is required for notarization.
- Notarization: Apple's automated malware and signing check for Developer ID-signed software. Successful submissions receive a ticket that Gatekeeper can retrieve or that can be stapled to apps, flat packages, and DMGs.
- Gatekeeper: Evaluates downloaded or quarantined software using signature, notarization, provenance, integrity, and known-malware checks, then asks for user approval when appropriate.

## Format routing

Identify the format or formats the user asks about, then read only the matching reference files. Do not preload unrelated format references. If the user asks only about trust controls, read no format reference. If the user requests a comparison of all options, read all four.

- App bundles (`.app`): Applications containing an `Info.plist` and a Mach-O executable. See [references/app-bundles.md](references/app-bundles.md).
- Installer packages (`.pkg`): Component or product packages containing payload files and optional `preinstall` or `postinstall` scripts, with system or current-user installation domains. See [references/installer-packages.md](references/installer-packages.md).
- Disk images (`.dmg`): Delivery containers commonly used to distribute app bundles. See [references/disk-images.md](references/disk-images.md).
