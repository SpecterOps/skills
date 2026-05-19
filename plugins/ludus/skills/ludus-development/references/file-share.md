# File Share

For Ludus servers with more than one user, or frequent sharing of files between ranges, it is beneficial to have a persistent file share that all user's ranges can access.

Ludus has the ability to deploy a file share server (SMB) at 192.0.2.3 that all user's ranges can access.

## Setup

As a Ludus admin user, run the following command:

```
ludus range deploy -t share
```

Monitor the deployment with:

```
ludus range logs -f
```

## Usage

Once the deployment has finished, two shares will be available to all ranges (assuming their firewall rules allow access):

* `\\192.0.2.3\readonlyshare` - A shared folder that only allows read access (useful for malware samples, etc)
* `\\192.0.2.3\readwriteshare` - A second shared folder for general purpose use

On the file share server, the shares are at `/srv/samba/readonlyshare` and `/srv/samba/readwriteshare`.

### Windows additional steps

Windows won't allow anonymous share access by default. To allow anonymous access to the shares you can do either of the following:

1. Add the `anon_share_access` GPO to the primary domain controller of the range (if the Windows machines are in the domain). See [Configuration](./configuration.md) for more information.
2. Run `ludus range deploy -t allow-share-access` which will run the following commands on each Windows VM:

```
Set-SmbClientConfiguration -EnableInsecureGuestLogons $true -Confirm:$false
Set-SmbClientConfiguration -RequireSecuritySignature $false -Confirm:$false
```

### Linux mounting

On Linux machines, these shares can be accessed by entering the following in the file manager `Connect` dialog:

```
smb://192.0.2.3/readonlyshare
smb://192.0.2.3/readwriteshare
```

Headless/Command line users can mount the shares by running the following commands:

```
mkdir readonlyshare
sudo mount -t cifs //192.0.2.3/readonlyshare readonlyshare

mkdir readwriteshare
sudo mount -t cifs //192.0.2.3/readwriteshare readwriteshare -o noperm
```
