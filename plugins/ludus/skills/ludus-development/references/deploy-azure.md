# Azure Deployment

Reference for deploying Ludus on Azure using nested virtualization, including VM setup, install steps, troubleshooting, and ARM deployment templates.

## Overview

Azure supports nested virtualization for some VM types.
To determine if nested virtualization is supported, navigate to [this support page](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes-general), select your VM type on the left, and look for `Nested virtualization: Supported`.

Ludus has been successfully deployed on a `Standard E4bs v5 (4 vcpus, 32 GiB memory)` with NVMe disk controller and a 250GB disk.
This instance costs ~$260/month (with disk and network costs).

However, this configuration will only be functional for basic labs (~4 VMs). For anything larger, use a larger instance size.

In order to select the NVMe disk controller, the `Security type` must be set to `Standard`.

## Install

1. Copy the `ludus-server` binary to the VM once it has deployed (scp or other method).
2. Make the `ludus-server` binary executable with `chmod +x ludus-server`.
3. Run the `ludus-server` binary: `./ludus-server` but do not agree to the prompt - the public IP is likely wrong.
4. Edit the config file at `/opt/ludus/config.yml` and update the public IP to the public IP of the Azure instance.
5. Run `/opt/ludus/ludus-server` and agree to the prompt to start the install.
6. When the VM reboots, SSH back in and run `ludus-install-status` as root to monitor the install.
7. Once the install succeeds, follow the Quick start guide as normal starting at Create a User.
8. Make sure port 51820 UDP is open on the Azure firewall for the Ludus instance in order to use WireGuard.

## Troubleshooting

If the task `TASK [lae.proxmox : Perform system upgrades]` fails with the error: `Another instance of this program is already running.` manually reboot the machine by running `reboot` as root. On next boot, the install will continue automatically and should succeed.

As of v1.1.3 this error should automatically be handled.

## Azure Templates and Parameters

These json files can be used to automate the deployment of a small Ludus compatible VM in Azure (E4bs 4 CPU, 32 GiB RAM, 256 GiB NVMe disk).

### Deployment Template

```json
{
    "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "location": {
            "type": "string"
        },
        "networkInterfaceName1": {
            "type": "string"
        },
        "enableAcceleratedNetworking": {
            "type": "bool"
        },
        "networkSecurityGroupName": {
            "type": "string"
        },
        "networkSecurityGroupRules": {
            "type": "array"
        },
        "subnetName": {
            "type": "string"
        },
        "virtualNetworkName": {
            "type": "string"
        },
        "addressPrefixes": {
            "type": "array"
        },
        "subnets": {
            "type": "array"
        },
        "publicIpAddressName1": {
            "type": "string"
        },
        "publicIpAddressType": {
            "type": "string"
        },
        "publicIpAddressSku": {
            "type": "string"
        },
        "pipDeleteOption": {
            "type": "string"
        },
        "virtualMachineName": {
            "type": "string"
        },
        "virtualMachineName1": {
            "type": "string"
        },
        "virtualMachineComputerName1": {
            "type": "string"
        },
        "virtualMachineRG": {
            "type": "string"
        },
        "osDiskType": {
            "type": "string"
        },
        "osDiskSizeGiB": {
            "type": "int"
        },
        "osDiskDeleteOption": {
            "type": "string"
        },
        "diskControllerType": {
            "type": "string"
        },
        "virtualMachineSize": {
            "type": "string"
        },
        "nicDeleteOption": {
            "type": "string"
        },
        "hibernationEnabled": {
            "type": "bool"
        },
        "adminUsername": {
            "type": "string"
        },
        "virtualMachine1Zone": {
            "type": "string"
        }
    },
    "variables": {
        "nsgId": "[resourceId(resourceGroup().name, 'Microsoft.Network/networkSecurityGroups', parameters('networkSecurityGroupName'))]",
        "vnetName": "[parameters('virtualNetworkName')]",
        "vnetId": "[resourceId(resourceGroup().name,'Microsoft.Network/virtualNetworks', parameters('virtualNetworkName'))]",
        "subnetRef": "[concat(variables('vnetId'), '/subnets/', parameters('subnetName'))]"
    },
    "resources": [
        {
            "name": "[parameters('networkInterfaceName1')]",
            "type": "Microsoft.Network/networkInterfaces",
            "apiVersion": "2022-11-01",
            "location": "[parameters('location')]",
            "dependsOn": [
                "[concat('Microsoft.Network/networkSecurityGroups/', parameters('networkSecurityGroupName'))]",
                "[concat('Microsoft.Network/virtualNetworks/', parameters('virtualNetworkName'))]",
                "[concat('Microsoft.Network/publicIpAddresses/', parameters('publicIpAddressName1'))]"
            ],
            "properties": {
                "ipConfigurations": [
                    {
                        "name": "ipconfig1",
                        "properties": {
                            "subnet": {
                                "id": "[variables('subnetRef')]"
                            },
                            "privateIPAllocationMethod": "Dynamic",
                            "publicIpAddress": {
                                "id": "[resourceId(resourceGroup().name, 'Microsoft.Network/publicIpAddresses', parameters('publicIpAddressName1'))]",
                                "properties": {
                                    "deleteOption": "[parameters('pipDeleteOption')]"
                                }
                            }
                        }
                    }
                ],
                "enableAcceleratedNetworking": "[parameters('enableAcceleratedNetworking')]",
                "networkSecurityGroup": {
                    "id": "[variables('nsgId')]"
                }
            }
        },
        {
            "name": "[parameters('networkSecurityGroupName')]",
            "type": "Microsoft.Network/networkSecurityGroups",
            "apiVersion": "2019-02-01",
            "location": "[parameters('location')]",
            "properties": {
                "securityRules": "[parameters('networkSecurityGroupRules')]"
            }
        },
        {
            "name": "[parameters('virtualNetworkName')]",
            "type": "Microsoft.Network/virtualNetworks",
            "apiVersion": "2021-05-01",
            "location": "[parameters('location')]",
            "properties": {
                "addressSpace": {
                    "addressPrefixes": "[parameters('addressPrefixes')]"
                },
                "subnets": "[parameters('subnets')]"
            }
        },
        {
            "name": "[parameters('publicIpAddressName1')]",
            "type": "Microsoft.Network/publicIpAddresses",
            "apiVersion": "2020-08-01",
            "location": "[parameters('location')]",
            "properties": {
                "publicIpAllocationMethod": "[parameters('publicIpAddressType')]"
            },
            "sku": {
                "name": "[parameters('publicIpAddressSku')]"
            },
            "zones": [
                "[parameters('virtualMachine1Zone')]"
            ]
        },
        {
            "name": "[parameters('virtualMachineName1')]",
            "type": "Microsoft.Compute/virtualMachines",
            "apiVersion": "2022-11-01",
            "location": "[parameters('location')]",
            "dependsOn": [
                "[concat('Microsoft.Network/networkInterfaces/', parameters('networkInterfaceName1'))]"
            ],
            "properties": {
                "hardwareProfile": {
                    "vmSize": "[parameters('virtualMachineSize')]"
                },
                "storageProfile": {
                    "osDisk": {
                        "createOption": "fromImage",
                        "managedDisk": {
                            "storageAccountType": "[parameters('osDiskType')]"
                        },
                        "diskSizeGB": "[parameters('osDiskSizeGiB')]",
                        "deleteOption": "[parameters('osDiskDeleteOption')]"
                    },
                    "imageReference": {
                        "publisher": "debian",
                        "offer": "debian-12",
                        "sku": "12-gen2",
                        "version": "latest"
                    },
                    "diskControllerType": "[parameters('diskControllerType')]"
                },
                "networkProfile": {
                    "networkInterfaces": [
                        {
                            "id": "[resourceId('Microsoft.Network/networkInterfaces', parameters('networkInterfaceName1'))]",
                            "properties": {
                                "deleteOption": "[parameters('nicDeleteOption')]"
                            }
                        }
                    ]
                },
                "additionalCapabilities": {
                    "hibernationEnabled": false
                },
                "osProfile": {
                    "computerName": "[parameters('virtualMachineComputerName1')]",
                    "adminUsername": "[parameters('adminUsername')]",
                    "linuxConfiguration": {
                        "disablePasswordAuthentication": true
                    }
                }
            },
            "zones": [
                "[parameters('virtualMachine1Zone')]"
            ]
        }
    ],
    "outputs": {
        "adminUsername": {
            "type": "string",
            "value": "[parameters('adminUsername')]"
        }
    }
}
```

### Parameters

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "location": {
            "value": "eastus2"
        },
        "networkInterfaceName1": {
            "value": "ludus485_z1"
        },
        "enableAcceleratedNetworking": {
            "value": true
        },
        "networkSecurityGroupName": {
            "value": "ludus-nsg"
        },
        "networkSecurityGroupRules": {
            "value": [
                {
                    "name": "SSH",
                    "properties": {
                        "priority": 300,
                        "protocol": "TCP",
                        "access": "Allow",
                        "direction": "Inbound",
                        "sourceAddressPrefix": "*",
                        "sourcePortRange": "*",
                        "destinationAddressPrefix": "*",
                        "destinationPortRange": "22"
                    }
                }
            ]
        },
        "subnetName": {
            "value": "default"
        },
        "virtualNetworkName": {
            "value": "ludus-vnet"
        },
        "addressPrefixes": {
            "value": [
                "10.1.0.0/16"
            ]
        },
        "subnets": {
            "value": [
                {
                    "name": "default",
                    "properties": {
                        "addressPrefix": "10.1.0.0/24"
                    }
                }
            ]
        },
        "publicIpAddressName1": {
            "value": "ludus-ip"
        },
        "publicIpAddressType": {
            "value": "Static"
        },
        "publicIpAddressSku": {
            "value": "Standard"
        },
        "pipDeleteOption": {
            "value": "Detach"
        },
        "virtualMachineName": {
            "value": "ludus"
        },
        "virtualMachineName1": {
            "value": "ludus"
        },
        "virtualMachineComputerName1": {
            "value": "ludus"
        },
        "virtualMachineRG": {
            "value": "ludus_group_12281831"
        },
        "osDiskType": {
            "value": "Premium_LRS"
        },
        "osDiskSizeGiB": {
            "value": 256
        },
        "osDiskDeleteOption": {
            "value": "Delete"
        },
        "diskControllerType": {
            "value": "NVMe"
        },
        "virtualMachineSize": {
            "value": "Standard_E4bs_v5"
        },
        "nicDeleteOption": {
            "value": "Detach"
        },
        "hibernationEnabled": {
            "value": false
        },
        "adminUsername": {
            "value": "azureuser"
        },
        "virtualMachine1Zone": {
            "value": "1"
        }
    }
}
```
