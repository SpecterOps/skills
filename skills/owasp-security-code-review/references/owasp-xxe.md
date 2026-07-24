# OWASP XML External Entity Prevention

Use this reference when untrusted XML reaches DOM, SAX, StAX, XML schema validation, XPath, XSLT, or XML-backed import/export workflows.

## Review Checks

- Disable DTDs completely whenever possible.
- Disable external entities, external DTD loading, XInclude, and external schema fetches.
- Enable secure processing and entity expansion limits where supported.
- Verify parser defaults for the actual library and version rather than assuming safe defaults.
- Treat XXE as a path to file disclosure, SSRF, internal port scanning, and parser DoS.

## Pattern Examples

### Default Java parser

```java
// Vulnerable
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(inputStream);
```

```java
// Safer
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
factory.setXIncludeAware(false);
factory.setExpandEntityReferences(false);
DocumentBuilder builder = factory.newDocumentBuilder();
```

### Unsafe Python parser

```python
# Vulnerable when parser resolves external entities.
doc = lxml.etree.fromstring(xml_bytes)
```

```python
# Safer
parser = lxml.etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True)
doc = lxml.etree.fromstring(xml_bytes, parser=parser)
```

## Review Prompts

- Does any parser allow `DOCTYPE`, external entities, or remote schema resolution?
- Can XML processing read local files or make outbound requests?
- Are parser hardening flags applied before parsing every untrusted input path?
- Are entity expansion and oversized XML inputs bounded?

## Source

Local summary based on the OWASP XML External Entity Prevention Cheat Sheet:
`https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html`
