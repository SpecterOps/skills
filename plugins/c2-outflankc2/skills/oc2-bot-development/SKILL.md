---
name: oc2-bot-development
description: Develop Outflank C2 event-driven Python bots. Use when creating or debugging OC2 automations.
metadata:
  author: Outflank
---

# Outflank C2 (OC2) Bot Development

Outflank C2 Server has support for running bots. These bots are written in Python and react on events that happen in the server. Currently, these events are:

- on_new_implant: When a new implant arrives.
- on_implant_checkin: When an existing implant checks in.
- on_task_request: When a task has been sent to the implant.
- on_task_response: When the implant has sent the response to a task

Bots can be used to automate certain tasks, such as automatically sending a few tasks to the implant, exiting when the implant is not in the correct domain or notifying the operator when a new implant arrives.

## When NOT to Use

Do not use this skill unless Outflank C2 support is requested.

## References

- [Bot model](./references/bot-development.md) — discovery, execution context, reliability, and troubleshooting.
- [Runtime API](./references/bot-runtime-api.md) — events, services, and common accessors.
- [Examples](./references/bot-examples.md) — typed task scheduling and task-event lookup.
