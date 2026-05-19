# Google Cloud Platform (GCP) Deployment

Reference for deploying Ludus on GCP using gcloud CLI and Terraform, including install steps and troubleshooting.

## Deploying Debian 12 Using gcloud

The following command will create a GCP VM with nested virtualization enabled, 500GB of disk space, 16 CPUs and 72 GB of RAM. Adjust the values as required.

You will need to replace `{InstanceName}`, `{Zone}`, `{ProjectID}`, `{GCP UserName}`, `{UserName}`, and `{SSH KEY}` - don't forget to escape spaces with a `\`.

The `{GCP Username}` will be the user that is assigned the SSH key for the VM. Log in as this user.

```
gcloud compute instances create {InstanceName} \
  --enable-nested-virtualization \
  --zone={Zone} \
  --create-disk=auto-delete=yes,boot=yes,device-name={InstanceName},image=projects/debian-cloud/global/images/debian-12-bookworm-v20240213,mode=rw,size=500,type=projects/{ProjectID}/zones/us-central1-a/diskTypes/pd-balanced  \
  --visible-core-count 4 \
  --custom-cpu 16 \
  --custom-memory 72 \
  --metadata=ssh-keys={GCP UserName}:{Protocol}\ \
{Key}\ {UserName}
```

Example:
```
gcloud compute instances create ludus \
  --enable-nested-virtualization \
  --zone=us-central1 \
  --create-disk=auto-delete=yes,boot=yes,device-name=ludus,image=projects/debian-cloud/global/images/debian-12-bookworm-v20240213,mode=rw,size=500,type=projects/myproject/zones/us-central1-a/diskTypes/pd-balanced  \
  --visible-core-count 4 \
  --custom-cpu 16 \
  --custom-memory 72 \
  --metadata=ssh-keys=myname:ssh-ed25519\ AAAAC3NzaC1lZDI1NTE5AAAAIHm8UFxzLleq30n+CFdsPGZtOoGjZQus53ffCD9Zik3D\ username@host
```

## Deploying Debian 12 Using Terraform

You will need to replace `{InstanceName}`, `{region}`, `{Zone}`, `{project_id}`, `{SSH_User}` and `{SSH_Key}`.
This will install a new Debian 12 server with 24 cores, 82GB Memory, 500GB SSD and nested virtualization enabled (on Intel Haswell chip).

```
provider "google" {
  region = "{region}"
  project = "{project_id}"
}

resource "google_compute_instance" "{InstanceName}" {
  boot_disk {
    auto_delete = true
    device_name = "{InstanceName}"

    initialize_params {
      image = "projects/debian-cloud/global/images/debian-12-bookworm-v20240213"
      size  = 500
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src = "vm_add-tf"
  }

  machine_type     = "custom-24-81920"
  min_cpu_platform = "Intel Haswell"

  metadata = {
    ssh-keys = "{SSH_USER}:{SSH KEY}"
  }

  name = "{InstanceName}"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/{project_id}/regions/{region}/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  zone = "{Zone}"
  advanced_machine_features {
    enable_nested_virtualization   = true
  }
}
```

## Install

1. Run `curl -s https://ludus.cloud/install | bash` and enter `y` and `I understand` to start the install but *carefully* read each option and change the Public IP. It is almost certainly wrong. Enter the hostname from GCP as the node name (i.e. `debian-vm-be83d9b` instead of `ludus`) and the correct Public IP when prompted and continue through the options.
2. When the VM reboots, SSH back in and run `ludus-install-status` as root to monitor the install.
3. Once the install succeeds, follow the Quick start guide as normal starting at Create a User.

## Troubleshooting

This error will automatically be recovered (as of v1.1.3):

```
TASK [lae.proxmox : Install Proxmox VE and related packages] *******************
FAILED - RETRYING: [127.0.0.1]: Install Proxmox VE and related packages (2 retries left).
FAILED - RETRYING: [127.0.0.1]: Install Proxmox VE and related packages (1 retries left).
fatal: [127.0.0.1]: FAILED! => {"attempts": 2, "cache_update_time": 1708546691, "cache_updated": false, "changed": false, "msg": "'/usr/bin/apt-get -y -o \"Dpkg::Options::=--force-confdef\" -o \"Dpkg::Options::=--force-confold\"       install 'proxmox-ve=8.1.0'' failed: E: Sub-process /usr/bin/dpkg returned an error code (1)\n", "rc": 100, ...}
```

This is caused by `ifupdown2` reporting `error: Another instance of this program is already running.` during the Proxmox VE package installation. If encountered on older versions, manually reboot the machine by running `reboot` as root. On next boot, the install will continue automatically and should succeed.
