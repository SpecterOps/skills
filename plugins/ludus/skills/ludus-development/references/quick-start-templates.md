# Build Templates

Guide for building Ludus templates, monitoring build progress, and checking template status.

Before you can deploy a range, you first must build the template VMs (base VMs without customization) that will be used in your range.

Templates are the basis of every VM deployed by Ludus.
Unlike other solutions, Ludus templates are built from scratch (ISO), and by design don't contain any customization.
This allows users to modify base templates into arbitrary VMs during a deploy without having to maintain a library of stale, customized VMs.
This focus on infrastructure as code allows Ludus users to create fresh, up to date VMs every deployment.

The first step is to start the template build process. First, we can view the available templates.

```shell-session
ludus templates list
+------------------------------------+-------+
|              TEMPLATE              | BUILT |
+------------------------------------+-------+
| debian-11-x64-server-template      | FALSE |
| debian-12-x64-server-template      | FALSE |
| kali-x64-desktop-template          | FALSE |
| win11-22h2-x64-enterprise-template | FALSE |
| win2022-server-x64-template        | FALSE |
+------------------------------------+-------+
```

On a fresh install, no templates are built. Ludus will build them from ISO files (with checksums) with the following command.

```shell-session
ludus templates build
[INFO]  Template building started - this will take a while. Building 1 template(s) at a time.
```

**Tip:** If you have decently powerful hardware, you can build more than 1 template at a time with the `--parallel` option to specify how many
templates to build concurrently. Be aware that when building in parallel, no template logs will be generated.

To check the status of the template build, you can run `templates status`, `templates list` again, or follow the packer logs with

```shell-session
ludus templates logs -f
2024/08/16 20:11:17 ui: ==> proxmox-iso.debian11: Retrieving ISO
2024/08/16 20:11:17 ui: ==> proxmox-iso.debian11: Trying https://cdimage.debian.org/cdimage/archive/11.7.0/amd64/iso-cd/debian-11.7.0-amd64-netinst.iso
2024/08/16 20:11:17 ui: ==> proxmox-iso.debian11: Trying https://cdimage.debian.org/cdimage/archive/11.7.0/amd64/iso-cd/debian-11.7.0-amd64-netinst.iso?checksum=sha512%4460ef6470f6d8ae193c268e213d33a6a5a0da90c2d30c1024784faa4e4473f0c9b546a41e2d34c43fbbd43542ae4fb93cfd5cb6ac9b88a476f1a6877c478674
2024/08/16 20:11:18 ui: ==> proxmox-iso.debian11: https://cdimage.debian.org/cdimage/archive/11.7.0/amd64/iso-cd/debian-11.7.0-amd64-netinst.iso?checksum=sha512%4460ef6470f6d8ae193c268e213d33a6a5a0da90c2d30c1024784faa4e4473f0c9b546a41e2d34c43fbbd43542ae4fb93cfd5cb6ac9b88a476f1a6877c478674 => /opt/ludus/users/john-doe/packer/packer_cache/50c7c8865f6fecec41b10c36bf86b3bd9bdb1eaf.iso
2024/08/16 20:11:22 ui: ==> proxmox-iso.debian11: Creating VM
...
```

**Note:** Building templates will take a while (up to a few hours depending on your internet and hardware speed). If multiple VMs time out without getting created, there may be a network issue.

Use `control+c` to stop following the logs.

You can also monitor template builds using the Proxmox web GUI. It is available at `https://<ludus IP>:8006` and the credentials for the web GUI can be retrieved with `ludus user creds get`.

Once all the templates have been built, you can deploy a range.

Curious how templates work? Check out the Templates documentation page.
