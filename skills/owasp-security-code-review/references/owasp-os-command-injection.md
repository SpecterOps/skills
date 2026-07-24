# OWASP OS Command Injection Defense

Use this reference when reviewing shell execution, process spawning, CLI wrappers, build scripts, or utilities that pass attacker-controlled values to system commands.

## Review Checks

- Prefer language/library APIs over OS commands.
- When commands are unavoidable, keep the executable fixed and pass arguments as a structured array.
- Validate commands and arguments with allowlists and bounded formats.
- Check for argument injection even when shell metacharacters are escaped.
- Use end-of-options markers such as `--` where supported.
- Verify the process runs with the lowest privileges needed.

## Pattern Examples

### String-built shell command

```ts
// Vulnerable
exec("convert " + req.body.filename + " output.png");
```

```ts
// Safer
const input = validateBasename(req.body.filename);
spawn("convert", ["--", input, "output.png"], { shell: false });
```

### Command selection from user input

```python
# Vulnerable
subprocess.run([request.json["tool"], request.json["target"]])
```

```python
tool = request.json["tool"]
if tool not in {"ping", "traceroute"}:
    raise BadRequest("unsupported tool")
target = validate_hostname(request.json["target"])
subprocess.run([tool, "--", target], check=True)
```

### Escaped but still injectable argument

```php
// Still risky: user can inject another curl option.
system("curl " . escapeshellarg($url));
```

```php
// Better: fix command options and separate the operand.
system("curl -- " . escapeshellarg($url));
```

## Review Prompts

- Can a library API replace the command entirely?
- Is the attacker choosing the executable, flags, working directory, or environment?
- Can a value beginning with `-` become an unintended option?
- Does the process inherit privileged environment variables or filesystem access?

## Source

Local summary based on the OWASP OS Command Injection Defense Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html`
