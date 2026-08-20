# Installer Packages

Use this pattern by default for installer packages unless the user explicitly asks for different installation or launch behavior:

- Require no administrator authorization.
- Carry an app inside its scripts archive.
- Copy the app into `~/Applications`.
- Launch the copied app during installation.
- Restrict installation to the current user's home directory.

Put an executable `preinstall` or `postinstall` shell script beside the app in the scripts directory. The examples below use `preinstall`; when `postinstall` timing is required, rename the script and update the matching verification commands without removing the launch step.

## Directory layout

The scripts directory contains the installer script and the complete app bundle:

```text
scripts/
├── preinstall
└── Example.app/
    └── Contents/
        ├── Info.plist
        ├── MacOS/
        │   └── Example
        └── Resources/
```

The app is stored beside `preinstall` so the script can copy it from PackageKit's temporary scripts directory.

## Installer script

Create `scripts/preinstall` with mode `755`:

```sh
#!/bin/sh

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DESTINATION_DIR="${HOME}/Applications"
DESTINATION_APP="${DESTINATION_DIR}/Example.app"

/bin/mkdir -p "${DESTINATION_DIR}" || exit 1
/bin/rm -rf "${DESTINATION_APP}" || exit 1
/usr/bin/ditto "${SCRIPT_DIR}/Example.app" "${DESTINATION_APP}" || exit 1
/usr/bin/open -n "${DESTINATION_APP}" >/dev/null 2>&1

exit 0
```

Behavior:

- `SCRIPT_DIR` resolves the temporary directory from which PackageKit extracted the scripts archive.
- `mkdir` creates the current user's Applications directory when necessary.
- `rm -rf` replaces only the fixed `~/Applications/Example.app` destination. Keep this path fixed and never derive it from untrusted input.
- `ditto` preserves the app-bundle structure and relevant metadata.
- `open -n` always asks Launch Services to start a new instance of the copied app.
- A directory-creation, removal, or copy failure aborts installation.
- A launch-request failure does not fail installation because the script intentionally ends with `exit 0`.
- A successful `open` return means Launch Services accepted the request; it does not prove the process remained running.

Make the script executable and validate its syntax:

```sh
chmod 755 scripts/preinstall
sh -n scripts/preinstall
```

To use `postinstall` instead, rename the file and keep the same copy-and-launch sequence:

```sh
mv scripts/preinstall scripts/postinstall
chmod 755 scripts/postinstall
sh -n scripts/postinstall
```

## Distribution.xml

Wrap the component package in a product archive whose Distribution permits only current-user-home installation. For an ARM64-only app:

```xml
<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="2">
    <title>Example</title>

    <options customize="never"
             require-scripts="false"
             hostArchitectures="arm64"/>

    <domains enable_anywhere="false"
             enable_currentUserHome="true"
             enable_localSystem="false"/>

    <choices-outline>
        <line choice="default"/>
    </choices-outline>

    <choice id="default" title="Example" visible="false">
        <pkg-ref id="com.example.example.arm64"/>
    </choice>

    <pkg-ref id="com.example.example.arm64"
             version="1.0"
             onConclusion="none">Example.component.pkg</pkg-ref>
</installer-gui-script>
```

Important details:

- `enable_currentUserHome="true"` and `enable_localSystem="false"` restrict installation to the current user's home directory.
- A current-user-home installation runs its component script as the current user, requires no administrator authorization, and cannot write outside that user's home directory.
- `hostArchitectures="arm64"` prevents installation on incompatible Intel Macs and prevents ARM64 package scripts from being evaluated under Rosetta.
- `require-scripts` refers to JavaScript expressions in the Distribution XML. It does not disable `preinstall` or `postinstall` shell scripts.
- `minSpecVersion="2"` is appropriate for modern macOS Distribution definitions.
- `onConclusion="none"` does not request a logout or restart.
- Give the component package and app stable identifiers so later versions can be distinguished in receipts and logs.

## Build the component package

Verify the source app before packaging:

```sh
file scripts/Example.app/Contents/MacOS/Example
codesign --verify --deep --strict --verbose=2 scripts/Example.app
```

Build a script-only component:

```sh
pkgbuild \
  --nopayload \
  --scripts scripts \
  --identifier com.example.example.arm64 \
  --version 1.0 \
  Example.component.pkg
```

The app is archived under `Scripts/`. The installer script is responsible for replacing the destination, copying the app, and requesting its launch.

## Build the product package

```sh
productbuild \
  --distribution Distribution.xml \
  --package-path . \
  Example.pkg
```

Distribute the resulting product package, not the raw component package. The product Distribution is what restricts installation to the current-user domain.

## Verification

Confirm that the final product permits only a current-user installation:

```sh
installer -dominfo -pkg Example.pkg
```

Expected output:

```text
CurrentUserHomeDirectory
```

Expand the component package without installing it:

```sh
pkgutil --expand-full Example.component.pkg ExpandedComponent
```

The expanded component should have this shape:

```text
ExpandedComponent/
├── PackageInfo
└── Scripts/
    ├── preinstall
    └── Example.app/
```

Confirm that `PackageInfo` contains a `preinstall` entry and inspect the archived script:

```sh
sed -n '1,220p' ExpandedComponent/PackageInfo
sed -n '1,160p' ExpandedComponent/Scripts/preinstall
sh -n ExpandedComponent/Scripts/preinstall
```

Verify that the archived script still includes the launch request:

```sh
grep -F '/usr/bin/open -n "${DESTINATION_APP}"' \
  ExpandedComponent/Scripts/preinstall
```

Verify the embedded app:

```sh
codesign \
  --verify \
  --deep \
  --strict \
  --verbose=2 \
  ExpandedComponent/Scripts/Example.app
```

Inspect signing status and record a hash:

```sh
pkgutil --check-signature Example.pkg
shasum -a 256 Example.pkg
```

Do not execute the package or app merely to validate its archive structure.

## Troubleshooting

### Installer requests administrator authorization

Confirm that the final product, rather than the raw component package, is being opened. Then check its permitted domain:

```sh
installer -dominfo -pkg Example.pkg
```

The output should contain only `CurrentUserHomeDirectory`. Also confirm that the Distribution sets `enable_currentUserHome="true"` and both other domains to `false`.

### Installer reports that installation failed

Inspect `/var/log/install.log` for the package identifier and script name. A message such as:

```text
An error occurred while running scripts from the package
```

normally means `preinstall` or `postinstall` returned nonzero. Check that:

- The script begins with `#!/bin/sh`.
- The script has mode `755`.
- The referenced source app exists beside the script in the scripts archive.
- Required directory, removal, and copy operations intentionally return nonzero on failure.
- `set -e` is not causing an unintended early exit.

### App is missing from `~/Applications`

Check that:

- `HOME` identifies the expected current user's home directory.
- `DESTINATION_APP` is exactly `${HOME}/Applications/Example.app`.
- The archived app name matches the name passed to `ditto`.
- The copy command is reached before the script exits.
- `/var/log/install.log` does not report a `ditto` failure.

### App does not launch or remain running

`open -n` only submits a Launch Services request. Check:

- The app's `CFBundleExecutable` value.
- Execute permission on the Mach-O executable.
- CPU architecture compatibility.
- Code-signature validity.
- Crash reports and application logs.
- Gatekeeper, quarantine, TCC, management policy, and endpoint controls.

If launch failure should also fail installation, make the request explicit:

```sh
/usr/bin/open -n "${DESTINATION_APP}" >/dev/null 2>&1 || exit 1
```
