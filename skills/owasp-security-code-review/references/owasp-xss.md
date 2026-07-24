# OWASP Cross-Site Scripting Prevention

Use this reference when untrusted data reaches HTML, attributes, JavaScript, CSS, URLs, templates, or browser DOM operations.

## Review Checks

- Identify the exact output context before evaluating the encoding control.
- Prefer framework auto-escaping and safe DOM sinks, but verify escape hatches and custom rendering.
- Treat HTML, attribute, JavaScript, CSS, and URL contexts as different sinks with different encoding needs.
- Review rich-text features for dedicated sanitization rather than ad hoc filtering.
- Check that CSP is defense in depth, not the only XSS control.

## Pattern Examples

### Unsafe DOM sink

```js
// Vulnerable
preview.innerHTML = comment;
```

```js
// Safer for plain text
preview.textContent = comment;
```

### Raw template rendering

```html
<!-- Vulnerable when `bio` contains untrusted HTML -->
<div>{{{ bio }}}</div>
```

```html
<!-- Safer when the template engine escapes by default -->
<div>{{ bio }}</div>
```

### Attribute injection

```js
// Vulnerable: attacker controls both value and execution context.
node.innerHTML = `<img src="${avatarUrl}" onerror="${handler}">`;
```

```js
// Safer: hardcode the attribute name and assign a validated URL.
node.setAttribute("src", validateImageUrl(avatarUrl));
```

### Rich HTML

```js
// Vulnerable
article.innerHTML = markdownToHtml(userMarkdown);
```

```js
// Safer when HTML is intentionally allowed
article.innerHTML = htmlSanitizer.sanitize(markdownToHtml(userMarkdown));
```

## Review Prompts

- What parser context receives the value: HTML body, attribute, JS string, CSS value, or URL?
- Does the code use an unsafe sink such as `innerHTML`, `outerHTML`, or `document.write`?
- Are attributes hardcoded and non-executable?
- Is user-controlled HTML sanitized with a maintained library?
- Are JSON responses served with the correct content type instead of being rendered as HTML?

## Source

Local summary based on the OWASP Cross Site Scripting Prevention Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html`
