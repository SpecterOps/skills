---
description: Configure ghostwriter-oplog settings (oplog ID, operator name, source IP)
arguments:
  - name: options
    description: "Options: --oplog-id ID, --operator NAME, --source-ip IP"
    required: true
---

Run the ghostwriter-oplog configuration script:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/gw-oplog-config.sh $ARGUMENTS
```

Report the output to the user.
