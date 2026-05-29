# AzureHound / Entra ID Methodology

Use for BloodHound Azure/Entra ID analysis from AzureHound-collected data and hybrid AD/Azure paths.

## Focus areas

- Tenant and directory privilege: Global Administrator, Privileged Role Administrator, role assignments, eligible assignments where modeled, and directory-wide Graph API privileges.
- Identity control: users, groups, service principals, applications, app owners, app role assignments, credentials, managed identities, and federated credentials.
- Resource control: subscriptions, management groups, resource groups, VMs, Key Vaults, Automation Accounts, AKS, container registries, and role assignments.
- Hybrid paths: Entra Connect/AAD Connect, synced identities, Azure-to-AD or AD-to-Azure bridge edges, and cloud-to-developer-platform paths.

## Query guidance

- Azure/Entra labels and relationships are conventionally prefixed with `AZ` (for example `AZUser`, `AZGroup`, `AZServicePrincipal`, `AZRole`, `AZOwner`).
- Start from exact `objectid` where possible. Azure display names can collide.
- Bound broad Azure paths and filter edge types; tenant-scale graphs can explode quickly.
- Separate direct control edges from informational/non-traversable Graph API permission edges when explaining confidence.
- For hybrid paths, state which collector supplied each segment and what data freshness applies.

## Good starting points

- Query index: `../query-indexes/azurehound.md`
- Query snapshots: `../query-snapshots/bloodhound-query-library/queries/`
- Azure/Entra edge prefix guidance: https://bloodhound.specterops.io/resources/edges/overview
- Azure node reference entry point: https://bloodhound.specterops.io/resources/nodes/az-base
- Traversable Azure edge guidance: https://bloodhound.specterops.io/resources/edges/traversable-edges
