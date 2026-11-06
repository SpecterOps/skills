# agent-qa regression evidence

Use this reference within the assigned web-QA session when the project already uses agent-qa or the user chooses it. The parent skill delegates execution to its QA agent; pass the applicable instructions and selected test paths in that delegation.

agent-qa provides natural-language tests with advanced memidex memory and self-improvement. Its recorded regression results complement the session's browser observations and Lighthouse audit. This reference does not replace those checks or authorize product changes.

## Bind the test to the assigned URL

- Locate `agent-qa.config.yaml` and the requested tests or suite. Confirm that the selected target resolves to the session's authorized URL and environment. A passing run against a different target does not establish the requested result.
- Preserve the project's test data, provider, and configuration. If the CLI or project setup is absent, report the missing prerequisite; do not initialize or install it as an unrequested side effect.
- Use the installed version through the project's package manager. The examples use npm's `--no-install` to avoid downloading another version. agent-qa 0.2.3 requires Node.js 24+.

```sh
npx --no-install agent-qa --version
npx --no-install agent-qa run --help
```

Run from the configuration directory. Put a global `--config <path>` before the command. These examples were checked against 0.2.3; recheck installed help and the [CLI reference](https://vostride.com/docs/agent-qa/cli) when versions differ. The printed version is output, not a CLI subcommand.

## Separate selection from application execution

Replace `tests/checkout.yaml` with the assigned test path:

```sh
npx --no-install agent-qa validate tests/checkout.yaml
npx --no-install agent-qa run tests/checkout.yaml --dry-run
```

Validation checks structure. Dry run discovers the selected tests without exercising the application. Neither proves a user flow passes. Verify the selected IDs and target; an empty selection is unresolved, not permission to broaden to all tests.

For authorized execution, keep that selection and choose an approved report path that preserves prior evidence:

```sh
npx --no-install agent-qa run tests/checkout.yaml --junit-output results.xml
```

Application actions can change data and provider calls can incur costs. `doctor` can contact the configured provider; it is not an offline validation command.

Preserve the exit status and relevant run ID before retries:

| Exit | Interpretation |
|---|---|
| `0` | Passed or healed; inspect the recorded verdict. |
| `1` | Failed or timed-out test, or a missing required file. Determine which occurred before calling it a product defect. |
| `2` | The run could not start. |
| `130` | Cancelled; preserve partial evidence. |

Verify that the report was actually created. A successful dry run with `--junit-output` does not establish a JUnit artifact.

## Inspect the selected run

```sh
npx --no-install agent-qa runs list --json
npx --no-install agent-qa runs overview RUN_ID --json
npx --no-install agent-qa runs knowledge RUN_ID --json
```

Bind `RUN_ID` to the selected test, target, and inspected revision. An empty failed-only list does not establish success. If the run has no completed verdict or knowledge reports `evidence-incomplete`, preserve that uncertainty.

Inspect the failed step and available evidence to distinguish an application defect, an incorrect expectation, and an environment/provider failure. A healed run needs an explanation of the recorded correction and whether the original expected outcome still holds; it is not an unchanged clean pass.

The run's knowledge view shows what memidex supplied or learned. For a specific record, use `knowledge inspect --json` and the [memory inspection guide](https://vostride.com/docs/agent-qa/memory/inspect). Treat memory as diagnostic context, not an independent acceptance oracle. Do not weaken assertions or erase memory/cache records to obtain a pass.

## Include the evidence in the QA report

Record the selected test and target, exact command and exit, run ID, verdict, available evidence/report paths, and any remaining check. Separate regression evidence from smoke-test, browser, and Lighthouse findings. An unexecuted check or incomplete run remains unverified.

Retain the first failure. Rerun only the affected selection after an authorized, evidence-based correction; stop when no new information supports another attempt. Redact credentials and sensitive application data from shared findings.

These original instructions follow this repository's Apache-2.0 license. The separately installed [agent-qa package](https://github.com/vostride/agent-qa) uses FSL-1.1-ALv2.
