# OpenHound Jamf Query Index

Generated from vendored upstream saved-query snapshots. Use this file to find starting points; inspect the referenced snapshot before adapting a query.

- Generated: `2026-04-17T00:26:42+00:00`
- Query count: `18`

| Query | Category / Platform | Snapshot | Notes |
| --- | --- | --- | --- |
| Jamf: API Client Attack Paths to Tenant | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_API_Client_Attack_Paths_to_Tenant.json` | Display up to 4 edges in attack paths originating from Jamf API Clients with a matching name or name starting… |
| Jamf: API Client Immediate Edges | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_API_Client_Immediate_Edges.json` | View immediate edges and impacted principals for Jamf API Clients |
| Jamf: Account Access by Name | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Account_Access_by_Name.json` | Filter to view access of a Jamf Account named or starting with 'LC' - increase the maximum edges to see more… |
| Jamf: Account to Account Attack Paths | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Account_to_Account_Attack_Paths.json` | Display Jamf Accounts with Attack-Paths impacting other Jamf Accounts - increase the maximum edges to see mor… |
| Jamf: Account to Tenant Edges | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Account_to_Tenant_Edges.json` | Show edges from Jamf Accounts to the Jamf Tenant |
| Jamf: All Account Paths | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_All_Account_Paths.json` | View paths originating from Jamf Accounts with up to 4 edges - increase edges to see more |
| Jamf: All Computers | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_All_Computers.json` | Get all Computers |
| Jamf: All Groups | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_All_Groups.json` | Get Jamf Groups |
| Jamf: All Nodes and Edges | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_All_Nodes_and_Edges.json` | Retrieve all nodes and edges where either a JamfHound node has an inbound or outbound relationship, limits re… |
| Jamf: Chained Targeted Filtering | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Chained_Targeted_Filtering.json` | An example of chained targeted filtering with multiple conditions in series that creates multiple proprety fi… |
| Jamf: Expanded Tier 1 to Tier 0 Paths | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Expanded_Tier_1_to_Tier_0_Paths.json` | Expand the graph by one edge showing nodes with edges to Tier 1 nodes with edges to Tier 0 nodes |
| Jamf: Group Administrators Filtered Relationships | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Group_Administrators_Filtered_Relationships.json` | Targeted Filtering that limits results to starting jamf_Group nodes starting with 'TENANT' in the name and on… |
| Jamf: Group Administrators Targeted Edges | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Group_Administrators_Targeted_Edges.json` | Targeted Filtering Query, display nodes with edges between 'GROUP_ADMINISTRATORS' and 'UPDATE' or 'GROUP_ADMI… |
| Jamf: Group Edges to Accounts | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Group_Edges_to_Accounts.json` | Get immediate edges impacting Jamf Accounts originating from Jamf Groups, swap jamfGroup for jamfTenant to se… |
| Jamf: Matched Email Edges | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Matched_Email_Edges.json` | Show nodes with the edge jamfMatchedEdmail |
| Jamf: Tier 1 to Tier 0 Attack Paths | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Tier_1_to_Tier_0_Attack_Paths.json` | Retrieve attack paths between Tier 1 nodes and Tier 0 nodes that are fully traversable - excludes tenant and… |
| Jamf: Tier 1 to Tier 0 Direct Edges | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Tier_1_to_Tier_0_Direct_Edges.json` | Retrieve direct edges between Tier 1 nodes and Tier 0 nodes |
| Jamf: Tier 1 to Tier 0 Without Contains | openhound-jamf | `references/query-snapshots/openhound-jamf/saved-searches/Jamf_Tier_1_to_Tier_0_Without_Contains.json` | Filter out jamf_Contains edges from Tiered node query |
