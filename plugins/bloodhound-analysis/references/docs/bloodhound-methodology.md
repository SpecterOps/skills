# BloodHound AD/ADCS Methodology

Use for classic BloodHound Active Directory and ADCS analysis.

## Focus areas

- Tier Zero and privileged group exposure: Domain Admins, Enterprise Admins, Administrators, domain controllers, certificate authorities, and identity infrastructure.
- Effective admin paths: group nesting, ACL control, sessions, local admin, RDP/WinRM/PSRemote, GPO control, delegation, trusts, LAPS/gMSA, and DCSync.
- ADCS: ESC paths, enrollment agent abuse, vulnerable templates, CA trust, NTAuth/published CA relationships, and certificate-template control.
- Hygiene/risk: stale privileged accounts, disabled controls, pre-auth disabled, SPNs, unconstrained/constrained/RBCD delegation, password policies, admincount, SIDHistory, and inactive high-privilege objects.

## Query guidance

- BloodHound AD names are usually uppercase and domain-suffixed, for example `DOMAIN ADMINS@EXAMPLE.LOCAL`.
- Use lowercase property names such as `name`, `objectid`, `enabled`, `admincount`, `hasspn`, `lastlogontimestamp`, and `pwdlastset`.
- Prefer relationship-specific patterns (`MemberOf`, `GenericAll`, `GenericWrite`, `Owns`, `WriteDacl`, `AddMember`, `ForceChangePassword`, `AllowedToDelegate`, `ADCSESC*`) over unbounded `[*]`.
- Treat composite edges and non-traversable prerequisite edges differently. For example, investigate non-traversable ADCS/replication edges when explaining why a higher-level traversable risk exists.
- For trusts, verify source/target domains and direction before summarizing blast radius.

## Good starting points

- Query index: `../query-indexes/bloodhound.md`
- Query snapshots: `../query-snapshots/bloodhound-query-library/queries/`
- Official edge docs: https://bloodhound.specterops.io/resources/edges/overview
- Traversability docs: https://bloodhound.specterops.io/resources/edges/traversable-edges
