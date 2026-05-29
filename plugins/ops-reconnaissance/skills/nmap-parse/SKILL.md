---
name: nmap-parse
description: Parse nmap scan output and generate actionable recon notes. Use when analyzing nmap XML/grepable output, planning service enumeration, or doing network reconnaissance.
metadata:
  author: "GhostWorks"
---

# Nmap Parse & Recon Planning

Parse nmap scan results and produce actionable reconnaissance notes.

Parse the user's input to determine the file and focus area:
- `$nmap-parse scan.xml` → parse XML output, all service categories
- `$nmap-parse scan.gnmap web` → parse grepable output, web services only
- `$nmap-parse scan.nmap ad` → parse normal output, Active Directory focus

Focus areas: `all` (default), `web`, `ad`, `databases`, `remote-access`

## Steps

1. Read the nmap output file provided by the user
   - Detect format: XML (look for `<?xml`), grepable (look for `Host:`), or normal output
   - XML is preferred for structured parsing — use Python's `xml.etree.ElementTree` or regex extraction
   - For grepable/normal: extract with pattern matching

2. Extract and organize by host:
   - IP address and hostname (if resolved)
   - OS detection results (if available)
   - Open ports with service name, version, and state
   - Script output (NSE results)

3. Classify services into attack categories:

### Web Services (ports 80, 443, 8080, 8443, etc.)
- Note web server version (Apache, Nginx, IIS + version)
- Flag interesting headers from NSE scripts
- Suggest: `gobuster`, `ffuf`, `nikto`, Burp Suite targets

### Active Directory (ports 88, 389, 636, 445, 135, 5985, etc.)
- Identify domain controllers (88+389+445+636 combo)
- Note SMB signing status
- Note LDAP/LDAPS availability
- Suggest: BloodHound collection, `crackmapexec`/`netexec` enumeration, Kerberos attacks

### Databases (1433, 3306, 5432, 1521, 27017, 6379, etc.)
- Note database type and version
- Flag default ports
- Suggest: authentication testing, `impacket-mssqlclient`

### Remote Access (22, 3389, 5985, 5986, 2222, etc.)
- SSH version and auth methods
- RDP availability and NLA status
- WinRM/PSRemoting availability
- Suggest: credential testing, key-based auth checks

### Other Notable Services
- FTP (21) — anonymous access?
- SNMP (161/162) — community string testing
- DNS (53) — zone transfer testing
- SMTP (25) — relay testing

4. Generate output as structured markdown:

```markdown
# Network Recon — [date]

## Host Summary
| IP | Hostname | OS | Open Ports |
|---|---|---|---|

## Priority Targets
[Hosts with the most attack surface, ordered by interest]

## Service Breakdown
### Web Servers
### Active Directory
### Databases
### Remote Access

## Suggested Next Steps
[Ordered list of enumeration commands to run next]
```

5. If the user specified a focus area, filter output to only that category but still mention other notable services in a brief "Other Services" section

6. Create the output directory if it doesn't exist (`mkdir -p recon/`) and save output to `recon/nmap-analysis-[date].md`
