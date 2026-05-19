# MITRE Pattern Mapping

Use this reference when adding or tuning MITRE ATT&CK tags in the consolidator.

## Sample technique patterns
- Discovery: whoami, ipconfig, net user, net share, systeminfo, tasklist, nmap, masscan
- Credential Access: mimikatz, sekurlsa, hashdump, dcsync, kerberoast, asreproast, rubeus, keylog, password spray, responder
- Lateral Movement: psexec, wmiexec, ssh, rdesktop, mstsc, winrm, pass the hash/ticket
- Execution: powershell, cmd, bash, python, mshta, rundll32, certutil
- Persistence: schtasks, cron, reg add, service create, webshell
- Privilege Escalation: getsystem, sudo, token, potato, uac bypass
- Defense Evasion: obfuscate, inject, amsi bypass, timestomp, clear log
- Collection: screenshot, clipboard, zip, tar
- Exfiltration: exfil, upload, transfer, dnscat
- Command & Control: beacon, callback, tunnel, proxy, proxychains, chisel

## Tuning
- Patterns are case-insensitive regexes evaluated over the combined action + details text.
- Each match adds the technique ID (e.g., T1018) to the entry's mitre_tags list.
- Keep the list of regex/technique pairs centralized here for easy updates.
