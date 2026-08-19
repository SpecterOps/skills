# Malleable Command and Control Documentation

- checking_for_errors.md
- profile_language.md
- http_staging.md
- http_transaction_walkthrough.md
- http_host_profiles.md
- http_server_config.md
- self_signed_ssl.md
- valid_ssl.md
- profile_variants.md
- http_beacons.md
- code_signing_cert.md
- dns_beacons.md
- exercising_caution.md
- profile_overrides.md

## Overview

Beacon's HTTP indicators are controlled by a Malleable Command and Control (Malleable C2) profile. A Malleable C2 profile is a simple program that specifies how to transform data and store it in a transaction. The same profile that transforms and stores data, interpreted backwards, also extracts and recovers data from a transaction.

To use a custom profile, you must start a Cobalt Strike Team Server and specify your profile at that time.

`./teamserver [external IP] [password] [/path/to/my.profile]`

You may only load one profile per Cobalt Strike instance.

## Viewing the Loaded Profile

To view the C2 profile that was loaded when the Team Server was started select Help \ Malleable C2 Profile on the menu. This displays the profile for the currently selected Team Server when multiple Team Servers are connected. The dialog is read-only.

To close the dialog use the 'x' in the upper right corner of the dialog.

> This section covers the Malleable C2 features related to flexible network communications. See [Malleable PE, Process Injection, and Post Exploitation](../malleable-postex/index.md) for information on Malleable C2's stage, process-inject, and post-ex blocks.
