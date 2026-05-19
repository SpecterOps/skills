# Hyper-V Deployment

Reference for deploying Ludus inside a Hyper-V virtual machine, including VM setup, Generation 2 configuration, and nested virtualization.

## VM Setup

1. Create a Generation 2 VM with typical settings.

2. Before booting the VM for the first time, disable `Checkpoints` in VM Settings.

3. If your host is a server edition of Windows, run the following PowerShell command to enable nested virtualization:

```powershell
Set-VMProcessor -VMName <Ludus VM Name> -ExposeVirtualizationExtensions $true
```

4. Boot the VM and install Debian 12/13.

## Install

1. Follow the Install Ludus quick-start guide.
