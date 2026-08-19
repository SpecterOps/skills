# Valid SSL Certificates with SSL Beacon

You have the option to use a Valid SSL certificate with Beacon. Use a Malleable C2 profile to specify a Java Keystore file and a password for the keystore. This keystore must contain your certificate’s private key, the root certificate, any intermediate certificates, and the domain certificate provided by your SSL certificate vendor. Cobalt Strike expects to find the Java Keystore file in the same folder as your Malleable C2 profile.

```
https-certificate {
     set keystore "domain.store"; 
     set password "mypassword";
}
```

The parameters to use a valid SSL certificate are:

| Option   | Example      | Description                                     |
| -------- | ------------ | ----------------------------------------------- |
| keystore | domain.store | Java Keystore file with certificate information |
| password | mypassword   | The password to your Java Keystore              |

Here are the steps to create a Valid SSL certificate for use with Cobalt Strike’s Beacon:

1. Use the keytool program to create a Java Keystore file. This program will ask "What is your first and last name?" Make sure you answer with the fully qualified domain name to your Beacon server. Also, make sure you take note of the keystore password. You will need it later.
    `$ keytool -genkey -keyalg RSA -keysize 2048 -keystore domain.store`
2. Use keytool to generate a Certificate Signing Request (CSR). You will submit this file to your SSL certificate vendor. They will verify that you are who you are and issue a certificate. Some vendors are easier and cheaper to deal with than others.
    `$ keytool -certreq -keyalg RSA -file domain.csr -keystore domain.store`
3. Import the Root and any Intermediate Certificates that your SSL vendor provides.
    `$ keytool -import -trustcacerts -alias FILE -file FILE.crt -keystore domain.store`
4. Finally, you must install your Domain Certificate.
    `$ keytool -import -trustcacerts -alias mykey -file domain.crt -keystore domain.store`

And, that’s it. You now have a Java Keystore file that’s ready to use with Cobalt Strike’s Beacon.
