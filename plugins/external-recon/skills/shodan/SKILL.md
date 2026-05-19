---
name: shodan
description: Query Shodan for reconnaissance, target enrichment, and exposed service discovery. Builds queries, parses results, and highlights interesting findings. Requires SHODAN_API_KEY environment variable.
---

# Shodan Reconnaissance Skill

Query Shodan for exposed services, target enrichment, and attack surface discovery.

Parse the user's input to determine the action:
- `$shodan search "org:Acme port:443"` → run a Shodan search query
- `$shodan target 203.0.113.1` → enrich a specific IP
- `$shodan target example.com` → enrich a domain (DNS + per-IP lookup)
- `$shodan dorking "Acme Corp"` → build advanced Shodan dorks for a target
- `$shodan monitor "Acme Corp"` → exposure report for an organization
- `$shodan cve CVE-2024-3400` → find hosts vulnerable to a specific CVE
- `$shodan cve CVE-2024-3400 "Acme Corp"` → CVE search scoped to an org

## Prerequisites

- **API key**: Set `SHODAN_API_KEY` environment variable
  - Free tier: limited searches, good for IP lookups
  - Membership ($49 one-time): unlocks search filters, bulk lookups
  - Small Business+: monitor, alerts, on-demand scanning
- **CLI**: Install with `pip install shodan` or `uv add shodan`
- **Verify access**: `shodan info` (shows query/scan credits remaining)

If the API key is not set, inform the user and show how to set it:
```bash
export SHODAN_API_KEY="your-key-here"
# Or add to ~/.zshrc for persistence
echo 'export SHODAN_API_KEY="your-key-here"' >> ~/.zshrc
```

## Actions

### search — Run a Shodan query

1. Build the query from the user's input
2. Execute: `shodan search --fields ip_str,port,org,hostnames,product,version,os "<query>" --limit 100`
3. Parse and format results into a table:

   ```
   IP              Port   Service          Version    Org              Hostnames
   ─────────────────────────────────────────────────────────────────────────────
   203.0.113.1     443    nginx            1.25.3     Target Corp      www.target.com
   203.0.113.2     22     OpenSSH          8.9p1      Target Corp      ssh.target.com
   ```

4. Highlight interesting findings:
   - **Critical**: Known vulnerable versions, default credentials services, exposed admin panels
   - **Interesting**: Uncommon ports, development/staging services, database ports, ICS/SCADA
   - **Note**: Self-signed certs, expired certs, outdated software

5. Group results by service type when there are many results

### target — Enrich a specific IP or domain

1. For IPs: `shodan host <ip>`
2. For domains: `shodan domain <domain>` then lookup each IP found
3. Collect and present:

   **Host Summary:**
   - IP, ASN, organization, ISP, country/city
   - Open ports and services (with versions)
   - Hostnames and reverse DNS
   - Last scan date
   - Known vulnerabilities (CVEs) Shodan has flagged
   - SSL/TLS certificate details (issuer, expiry, SANs)
   - Technologies detected

   **Domain Summary** (if domain provided):
   - DNS records (A, AAAA, MX, NS, TXT, CNAME)
   - Subdomains discovered
   - Per-IP breakdown of services

4. Flag anything juicy:
   - Ports that shouldn't be public (3389, 5900, 27017, 6379, 9200, 5432, 3306, 445)
   - Services with known CVEs
   - Expired or self-signed SSL certs
   - Development/staging environments exposed
   - Default pages or install wizards

### dorking — Build advanced Shodan queries

Based on what the user describes, build targeted Shodan dorks.

**Query building reference:**

```
# Organization targeting
org:"Target Corp"
org:"Target Corp" port:443

# Network range
net:203.0.113.0/24
net:203.0.113.0/24 port:22

# Service-specific
product:"Apache httpd" version:"2.4.49"    # Path traversal CVE-2021-41773
product:"Microsoft Exchange" port:443       # Exchange servers
product:"OpenSSH" version:"7.6"            # Older SSH
"Server: Apache/2.4.49"                    # Raw banner match

# Exposed services (shouldn't be public)
org:"Target" port:3389                     # RDP
org:"Target" port:445                      # SMB
org:"Target" port:27017                    # MongoDB
org:"Target" port:6379                     # Redis
org:"Target" port:9200                     # Elasticsearch
org:"Target" port:5432                     # PostgreSQL
org:"Target" port:3306                     # MySQL
org:"Target" port:11211                    # Memcached
org:"Target" "port:2379"                   # etcd

# Web technologies
org:"Target" http.title:"Dashboard"
org:"Target" http.title:"Login"
org:"Target" http.title:"Index of /"       # Directory listing
org:"Target" http.component:"WordPress"
org:"Target" http.component:"Jira"
org:"Target" http.component:"Jenkins"
org:"Target" http.component:"Grafana"
org:"Target" http.favicon.hash:           # Favicon hash matching

# SSL/TLS
org:"Target" ssl.cert.expired:true
org:"Target" ssl.cert.issuer.cn:"Let's Encrypt"
ssl.cert.subject.cn:"target.com"          # Find all IPs for a cert

# Vulnerable services
vuln:CVE-2021-44228                       # Log4Shell
vuln:CVE-2023-22515                       # Confluence
vuln:CVE-2024-3400                        # PAN-OS

# ICS/SCADA (if in scope)
org:"Target" tag:ics
org:"Target" port:502                     # Modbus
org:"Target" port:44818                   # EtherNet/IP

# Cloud metadata
org:"Amazon" http.title:"Target"
"X-Powered-By" org:"Target"

# Country/city filtering
org:"Target" country:"US" city:"New York"

# Screenshot available
org:"Target" has_screenshot:true

# Honeypot detection
org:"Target" tag:honeypot
```

Present 5-10 relevant queries for the scenario with explanations of what each finds and why it matters.

### monitor — Check exposure for an organization

1. Run multiple targeted queries for the org:
   ```bash
   shodan search 'org:"<org_name>"' --fields ip_str,port,product,version --limit 500
   ```

2. Build an exposure report:

   **Attack Surface Summary:**
   - Total IPs discovered
   - Total open ports
   - Unique services and versions

   **Exposed Services by Risk:**

   | Risk | Service | Count | Details |
   |---|---|---|---|
   | Critical | RDP (3389) | 3 | Direct RDP exposure to internet |
   | Critical | MongoDB (27017) | 1 | No auth likely |
   | High | SSH (22) | 15 | Check for password auth |
   | High | Expired SSL | 4 | Trust issues, possible neglect |
   | Info | HTTPS (443) | 42 | Normal |

   **Version Intelligence:**
   - Outdated software detected (with CVE references)
   - End-of-life products

   **Recommendations:**
   - Prioritized list of what to investigate or report

3. If the user asks, save the full report as markdown

### cve — Find hosts vulnerable to a specific CVE

1. Search: `shodan search "vuln:<cve_id>"` (or if targeting an org: `shodan search "vuln:<cve_id> org:\"<org>\""`)
2. If Shodan doesn't index that CVE, fall back to service/version matching:
   - Look up affected product/versions for the CVE
   - Build a query matching those versions
3. Present results with:
   - Affected hosts and their details
   - CVE description and severity
   - Whether exploitation requires authentication or special conditions
   - Suggested next steps (verify, exploit, report)

## Python API Fallback

If the Shodan CLI isn't available or for complex queries, use the Python API:

```python
import shodan
import os

api = shodan.Shodan(os.environ["SHODAN_API_KEY"])

# Search
results = api.search("org:\"Target Corp\" port:443")
for result in results["matches"]:
    print(f"{result['ip_str']}:{result['port']} - {result.get('product', 'unknown')}")

# Host lookup
host = api.host("203.0.113.1")
print(f"Ports: {host['ports']}")
print(f"Vulns: {host.get('vulns', [])}")

# DNS lookup
dns = api.dns.domain_info("target.com")
```

## Output Formatting

- Default: Rich tables to terminal with color-coded severity
- With `--output <file>`: Markdown report file with full details
- Always include the Shodan query used so the user can repeat or modify it
- Note the scan date — Shodan data can be days/weeks old
