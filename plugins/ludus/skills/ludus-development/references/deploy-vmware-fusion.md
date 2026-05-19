# VMware Fusion Deployment

Reference for deploying Ludus inside a VMware Fusion virtual machine, including VM settings and limitations.

**Warning:** Using a type 2 hypervisor is not recommended. However, using the settings below allow for acceptable performance.

**Danger:** Apple Silicon macs (M1, M2, M3, etc.) are not supported!

## VM Setup

Create a Debian 12/13 VM with the following settings (disk can be larger than 250GB as available):

- Allocate sufficient CPU cores and RAM for your intended lab size
- In Advanced settings, enable virtualization extensions (Intel VT-x/EPT or AMD-V/RVI) for the VM
- Set disk size to at least 250GB

## Install

Once Debian 12/13 is installed and running, follow the Install Ludus quick-start guide.
