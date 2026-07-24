# Attack Trees

Use attack trees when a high-value asset, sensitive workflow, or suspected weakness depends on multiple steps. Treat the tree as a review aid that turns a threat model into concrete code paths; do not report a vulnerability only because a theoretical branch exists.

## Purpose

Map an attacker goal into the paths, prerequisites, trust-boundary crossings, and controls that make the goal possible or prevent it. Use the result to decide which code paths deserve deep tracing and which assumptions need verification.

## Build the Tree

1. Define the root goal in attacker language.
   - Use goals such as `read another tenant's invoice`, `execute code on the worker`, `reset another user's password`, or `extract stored API keys`.
   - Tie the goal to a concrete asset or violated security invariant.

2. Decompose the goal into OR and AND branches.
   - Use OR branches for alternate routes to the same outcome.
   - Use AND branches when multiple conditions must all hold, such as `obtain token` and `bypass object check`.
   - Include alternate entry points, async handlers, imports, exports, and operational paths rather than only the primary UI flow.

3. Attach evidence to each branch.
   - Record the route, function, job, parser, policy decision, storage call, or sink that implements the step.
   - Record attacker capability, required state, trust boundary, and current control.
   - Mark unknowns explicitly instead of assuming a branch is reachable.

4. Trace each viable leaf through the code.
   - Follow source, parsing, normalization, validation, authorization, state changes, and sink.
   - Verify whether controls are present at every boundary crossing.
   - Check whether an earlier control can be bypassed through another branch.

5. Convert the tree into review outcomes.
   - Report a finding only when a path is reachable and impact is demonstrated.
   - Record blocked branches as verified controls.
   - Record unresolved branches as open questions or coverage gaps.
   - Add regression tests for the shortest realistic attack path and for the control that should block it.

## Tree Template

```text
Root goal: <attacker outcome>
Asset or invariant: <what must remain protected>
Attacker: <identity and capabilities>

OR
- Path A: <route or workflow>
  - Preconditions:
  - Code evidence:
  - Control expected:
  - Result:
- Path B: <route or workflow>
  - AND
    - Step 1:
    - Step 2:
  - Preconditions:
  - Code evidence:
  - Control expected:
  - Result:
```

## Review Prompts

- What is the shortest path from an external input to the protected asset?
- Which branches cross authentication, authorization, tenant, or privilege boundaries?
- Which branch depends on stale state, replay, race conditions, or partial failure?
- Which branch uses a different route, job, import, export, or admin surface than the expected workflow?
- Which control is assumed rather than enforced in the code path?
- Which blocked branches have tests proving that the control remains effective?

## OWASP Basis

Use this reference with the [OWASP Secure Code Review Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html) threat-based review guidance, which calls for mapping potential attack paths through the application, and the [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html), which structures analysis around system modeling, threat identification, mitigation, and validation.
