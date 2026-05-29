# OpenGraph Node and Edge Reference

Use this compact reference to avoid inventing labels or relationship kinds. Confirm exact labels in installed schemas, saved-query snapshots, or live BloodHound schema output before running queries.

## GitHub / GitHound

Key node labels:

- `GH_Enterprise`, `GH_Organization`, `GH_User`, `GH_Team`, `GH_EnterpriseTeam`, `GH_Repository`
- `GH_Branch`, `GH_BranchProtectionRule`, `GH_Environment`, `GH_Workflow`
- `GH_OrgSecret`, `GH_RepoSecret`, `GH_EnvironmentSecret`
- `GH_OrgVariable`, `GH_RepoVariable`, `GH_EnvironmentVariable`
- `GH_App`, `GH_AppInstallation`, `GH_PersonalAccessToken`, `GH_ExternalIdentity`, `GH_SamlIdentityProvider`

High-value relationship families:

- Containment and membership: `GH_Contains`, `GH_MemberOf`, team/role relationships.
- Repository control: `GH_AdminTo`, `GH_CanWriteBranch`, `GH_CanCreateBranch`, `GH_CanEditProtection`, `GH_BypassBranchProtection`.
- Pull request / workflow risk: `GH_CanPwnRequest`, `GH_CallsWorkflow`, `GH_CanDispatchTo`, `GH_CanUseRunner`.
- Secret and alert exposure: `GH_CanAccess`, `GH_CanReadSecretScanningAlert`.
- Identity bridges: `GH_CanAssumeIdentity`, external identity links, SAML links, and SCIM links through `SCIM_Provisioned`.

Primary upstream docs:

- GitHound node docs: https://github.com/SpecterOps/GitHound/tree/main/Documentation/NodeDescriptions
- GitHound edge docs: https://github.com/SpecterOps/GitHound/tree/main/Documentation/EdgeDescriptions

## Jamf / JamfHound

Key node labels and primary kinds:

- `jamf_Tenant`, `jamf_Site`, `jamf_Account`, `jamf_Group`, `jamf_Computer`, `jamf_ApiClient`
- Policy/control surfaces such as scripts, policies, profiles, and scoped device objects are represented through Jamf schema/object payloads and saved-search edge patterns.

High-value relationship families:

- Tenant/site containment and scoping relationships.
- Account/group/API-client administration edges to tenant, site, account, and computer objects.
- Policy/script/profile management edges to managed computers.
- Tiering properties such as `Tier` and `primarykind` used by saved searches.
- Traversability marker `r.traversable = True` in Jamf path queries.

Local examples:

- Jamf schema examples: `references/examples/jamfhound/schema/`
- Jamf object examples: `references/examples/jamfhound/objects/`

## Okta / OktaHound

Key node labels:

- `Okta_Organization`, `Okta_User`, `Okta_Group`, `Okta_Application`
- `Okta_Role`, `Okta_BuiltinRole`, `Okta_CustomRole`, `Okta_RoleAssignment`, `Okta_ResourceSet`
- `Okta_ApiServiceIntegration`, `Okta_ApiToken`, `Okta_ClientSecret`, `Okta_JWK`
- `Okta_Device`, `Okta_Agent`, `Okta_AgentPool`, `Okta_IdentityProvider`, `Okta_Policy`, `Okta_Realm`

High-value relationship families:

- Containment and assignment: `Okta_Contains`, role/application/group assignment edges.
- Synchronization: `Okta_UserPull`, `Okta_UserPush`, `Okta_GroupPull`, `Okta_GroupPush`.
- App/secret exposure: `Okta_ReadPasswordUpdates`, client secret/JWK/application credential edges from saved searches.
- Hybrid bridges to AD, Entra, GitHub, Jamf, OnePassword, Snowflake, and SCIM data where collected.

Primary local sources:

- Okta saved searches: `references/query-snapshots/openhound-okta/saved-searches/`
- Okta model source index: `references/docs/collector-source-index.md`

## SCIM

Node labels:

- `SCIM_Organization`, `SCIM_User`, `SCIM_Group`, `SCIM_Role`

Edges:

- `SCIM_Contains` — traversable.
- `SCIM_HasRole` — traversable.
- `SCIM_ManagerOf` — non-traversable.
- `SCIM_MemberOf` — traversable.
- `SCIM_Provisioned` — traversable bridge to another extension node.

Primary local sources:

- SCIM methodology: `references/docs/scim-methodology.md`
- Small GitHound SCIM sample: `references/examples/githound/samples/githound_scim_O_kgDOCoV2OQ.json`
