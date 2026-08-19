# Malleable Profile Overrides

By default, the Malleable Profile configuration uses static settings, which previously required users to restart the Team Server to use different settings. Starting in Cobalt Strike 4.13, you can dynamically change some settings as new payloads are generated.

These settings are overridden using syntax that matches the existing Malleable Profile configuration. You can use the Malleable Profile Override feature to override the following settings:

- useragent
- checkin_delay
- stage.* [all fields in the stage group]
- process-inject.* [all fields in the process-inject group]

## Overriding Malleable Profile Settings

To override Malleable Profile settings:

Open one of the following payload generation dialogs:

- Payload Generator (Stageless)
- Windows Executable (Stageless)
- Windows Executable (Stageless) Variants

In the Malleable Override list, select an existing Malleable Profile Override file (.mpo) or select the ellipsis button … to open the Malleable Profile Override dialog to create a new file or edit an existing one.

## Malleable Profile Override Dialog

In the Malleable Profile Override dialog, you can select and view overrides and create, view, edit, save, and validate Malleable Profile Override files (.mpo).

In the Override list, select an .mpo file to view its details. After the file loads, you can edit it in the editor and then click Verify to confirm that the changes are valid. Click Save File to save your changes.

> NOTE: An .mpo file with “(edited)” next to its name has unsaved changes. You can use these changes ad hoc to generate the current payload without saving the file.

Saved .mpo files are stored in an application-specific folder under the operating system user's data folder. The reference.mpo example file is provided and loaded from the static profiles folder in the Cobalt Strike client root folder.

A special override named “Teamserver Default” is created from the current Malleable Profile on the Team Server. Use this profile to view the default profile options.

## Aggressor Script Payload Generation

The following Aggressor Script functions support Malleable Profile overrides:

- all_payloads
- artifact_payload
- payload

## REST API Payload Generation

The REST API's Stageless Payload endpoint (/api/v1/payloads/generate/stageless) supports Malleable Profile overrides.
