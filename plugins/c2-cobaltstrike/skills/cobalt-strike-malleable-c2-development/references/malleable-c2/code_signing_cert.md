# Code Signing Certificate

Payloads -> Windows Stager Payload and Windows Stageless Payload give you the option to sign an executable or DLL file. To use this option, you must specify a Java Keystore file with your code signing certificate and private key. Cobalt Strike expects to find the Java Keystore file in the same folder as your Malleable C2 profile.

```
code-signer {
    set keystore "keystore.jks"; 
    set password "password";
    set alias    "server";
}
```

The code signing certificate settings are:

| Option           | Example                       | Description                                     |
| ---------------- | ----------------------------- | ----------------------------------------------- |
| alias            | server                        | The keystore’s alias for this certificate       |
| digest_algorithm | SHA256                        | The digest algorithm                            |
| keystore         | keystore.jks                  | Java Keystore file with certificate information |
| password         | mypassword                    | The password to your Java Keystore              |
| timestamp        | false                         | Timestamp the file using a third-party service  |
| timestamp_url    | http://timestamp.digicert.com | URL of the timestamp service                    |
