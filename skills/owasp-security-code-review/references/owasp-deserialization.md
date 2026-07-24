# OWASP Deserialization

Use this reference when reviewing native object serialization, polymorphic JSON/XML, YAML loaders, signed blobs, caches, queue messages, or framework features that rebuild objects from untrusted data.

## Review Checks

- Prefer simple data formats plus explicit schemas over native object graphs.
- Search for dangerous APIs such as Python `pickle`, unsafe PyYAML loaders, Java `ObjectInputStream`, PHP `unserialize`, .NET `BinaryFormatter`, and type-enabled JSON serializers.
- Check whether the data stream controls the type or class being instantiated.
- Verify signatures or MACs before deserialization, not after.
- Allowlist expected types when deserialization is unavoidable.
- Review sensitive fields that should never be serialized or restored from user data.

## Pattern Examples

### Python pickle

```python
# Vulnerable
payload = base64.b64decode(request.json["blob"])
obj = pickle.loads(payload)
```

```python
# Safer
payload = json.loads(request.json["blob"])
obj = validate_order_schema(payload)
```

### Unsafe YAML loader

```python
# Vulnerable
config = yaml.load(user_yaml, Loader=yaml.Loader)
```

```python
# Safer
config = yaml.safe_load(user_yaml)
validate_config_schema(config)
```

### Java native deserialization

```java
// Vulnerable
ObjectInputStream in = new ObjectInputStream(request.getInputStream());
Object value = in.readObject();
```

```java
// Safer concept: restrict the allowed classes before object construction.
AllowedTypeObjectInputStream in =
    new AllowedTypeObjectInputStream(request.getInputStream(), Set.of(OrderDto.class));
OrderDto value = (OrderDto) in.readObject();
```

## Review Prompts

- Can the attacker choose the serialized type, class metadata, or gadget chain?
- Is the payload from a request, cookie, queue, cache, upload, or lower-trust database?
- Does the application verify integrity before rebuilding objects?
- Would a schema-driven DTO or plain JSON structure remove the need for native deserialization?

## Source

Local summary based on the OWASP Deserialization Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html`
