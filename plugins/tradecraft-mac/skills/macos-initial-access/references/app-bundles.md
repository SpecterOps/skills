# App Bundles

Use this pattern when the user asks for a macOS .app, app bundle, or Application.

- Make the Mach-O executable and ensure `Info.plist` names it correctly.
- Do not say that every unsigned app always prompts. Gatekeeper behavior depends on quarantine, provenance, policy, signature, and notarization state.
- Changing any bundle resource after signing invalidates the signature.

Describe an app as a directory with this minimum shape:

```text
Example.app/
└── Contents/
    ├── Info.plist
    ├── MacOS/
    │   └── Example        # executable Mach-O named by CFBundleExecutable
    └── Resources/         # optional
        └── AppIcon.icns   # optional; named by CFBundleIconFile
```

Here is an example Info.plist:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>Example</string>
    <key>CFBundleExecutable</key>
    <string>Example</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.Example</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Example</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
</dict>
</plist>
```

The icon is optional. If the user has not mentioned an icon, ask whether they
want one. If they do not, omit `CFBundleIconFile`, `AppIcon.icns`, and the
`Resources` directory when it has no other contents.

## Converting an image to an icon (ICNS) file

Use the bundled converter on macOS to turn user-provided artwork into the ten
standard PNG renditions and package them as an ICNS file. A Python 3 script uses
the built-in `sips` command for image processing and writes the ICNS container
directly. It accepts any image format that the local `sips` installation can read;
PNG, JPEG, and ICNS are common inputs. Run `sips --formats` to see the formats
supported on the current host.

From the directory containing this skill's `SKILL.md`, run:

```bash
mkdir -p Example.app/Contents/Resources
./scripts/image-to-icns.py /path/to/image.png \
  Example.app/Contents/Resources/AppIcon.icns
```

The optional second argument is the output path; without it, the script writes
an `.icns` file beside the input image. It refuses to overwrite an existing
output. Add the icon before signing the app; replacing it later invalidates the
bundle signature and requires signing the app again.

Verify the result and keep the file name aligned with `CFBundleIconFile`:

```bash
file Example.app/Contents/Resources/AppIcon.icns
sips -g format Example.app/Contents/Resources/AppIcon.icns
```
