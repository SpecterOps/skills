# OWASP File Upload

Use this reference when reviewing uploads, imports, archive extraction, generated files, or any path built from attacker-influenced filenames.

## Review Checks

- Validate after decoding filenames and paths.
- Use allowlisted extensions and content-aware validation; never trust `Content-Type` alone.
- Generate storage names server-side and keep user-supplied names as metadata only.
- Store files outside the webroot or on a separate host where possible.
- Apply size limits before and after decompression, and validate archive member paths.
- Check permissions, antivirus/sandbox processing, CSRF protection, and safe download authorization.

## Pattern Examples

### Original filename used as storage path

```python
# Vulnerable
dest = os.path.join(UPLOAD_DIR, upload.filename)
upload.save(dest)
```

```python
# Safer
ext = detect_allowed_extension(upload)
storage_name = f"{uuid.uuid4()}.{ext}"
dest = os.path.join(PRIVATE_UPLOAD_DIR, storage_name)
upload.save(dest)
```

### Trusting MIME type

```ts
// Vulnerable
if (file.mimetype === "image/png") {
  await save(file);
}
```

```ts
// Safer
const type = detectFileSignature(file.buffer);
if (!ALLOWED_IMAGE_TYPES.has(type) || file.size > MAX_IMAGE_BYTES) {
  throw new BadRequest("invalid image");
}
await saveOutsideWebroot(randomStorageName(type), file.buffer);
```

### Archive traversal

```python
# Vulnerable
zip_file.extractall(EXTRACT_DIR)
```

```python
# Safer
base = EXTRACT_DIR.resolve()
for member in zip_file.infolist():
    target = (base / member.filename).resolve()
    if target != base and base not in target.parents:
        raise BadRequest("invalid archive path")
    if member.file_size > MAX_MEMBER_BYTES:
        raise BadRequest("archive member too large")
```

## Review Prompts

- Can the attacker choose a filename, path, extension, or archive member path?
- Can uploaded content execute, render active content, overwrite files, or exhaust storage?
- Does retrieval require authorization, or are uploaded files public by default?
- Does any downstream parser receive untrusted files without hardening?

## Source

Local summary based on the OWASP File Upload Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html`
