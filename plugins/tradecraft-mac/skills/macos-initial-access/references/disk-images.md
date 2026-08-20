# Disk Images

Treat a DMG as a delivery container, commonly holding an app bundle, package, documentation, or a shortcut to `/Applications`.

```sh
mkdir -p dmg-root
ditto Example.app dmg-root/Example.app
hdiutil create \
  -srcFolder dmg-root \
  -volname "Example" \
  -format UDZO \
  -ov \
  -o Example.dmg
```

## Layout and validation

`-srcFolder` places the contents of the source directory at the image root. Stage the app inside a separate directory so the DMG contains `Example.app`, rather than placing the app's `Contents` directory at the root.

```text
dmg-root/
└── Example.app/
```

Validate nested code before creating the image, then verify the completed DMG:

```sh
codesign --verify --deep --strict --verbose=2 dmg-root/Example.app

hdiutil verify Example.dmg
hdiutil imageinfo Example.dmg
shasum -a 256 Example.dmg
```

`hdiutil verify` validates the disk-image checksum; it does not validate the signature of code inside the image.

The `-ov` option overwrites an existing output image. Omit it when existing artifacts must be preserved.

## Troubleshooting

If `hdiutil` reports `Device not configured`, the current sandbox, container, remote session, or CI runner may not have access to macOS's DiskImages service. Retry from an authorized macOS execution context; this error does not necessarily indicate that the source app bundle is malformed.
