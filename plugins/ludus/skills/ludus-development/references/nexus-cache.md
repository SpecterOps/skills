# Nexus Cache

For Ludus servers with more than one user, or frequent environment rebuilds, it is beneficial to cache artifacts locally to speed up deployments and prevent rate limits from 3rd party services (i.e. [Chocolatey](https://chocolatey.org/)).

Ludus has the ability to deploy a Nexus cache server into the 192.0.2.0/24 subnet that all user's ranges can access.

## Setup

As a Ludus admin user, run the following command:

```
ludus range deploy -t nexus
```

Monitor the deployment with:

```
ludus range logs -f
```

Once the deployment has finished, you must manually toggle the chocolatey-proxy repository to Nuget V2 via the web interface:

1. RDP into a windows box (or use the Proxmox web UI console) OR add `192.0.2.2/32` to the `AllowedIPs` block of your wireguard config and reload it.
2. Browse to: http://192.0.2.2:8081
3. Log in with `admin:<your proxmox password>`
4. Navigate to Repositories -> chocolatey-proxy
5. Click the radio button for NuGet V2
6. Click save (at the bottom of the page)

## Usage

With the Nexus cache set up, all [Chocolatey](https://chocolatey.org/) packages installed with Ludus will be installed through the cache automatically.

For C# development and NuGet packages in Visual Studio, manually configure the nexus proxy as a source under Options -> NuGet Package Manager -> Package Sources.
