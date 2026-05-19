# Create a User

Guide for creating the first Ludus user, setting the API key, and retrieving Proxmox credentials.

## Using the Ludus client to create a Ludus user

To perform user related actions, which modify the Ludus host as root, we must connect to the
admin service which only listens on localhost.

From a root shell on the Ludus host run `ludus-install-status` which will print the root
API key.

```shell-session
sudo su -
ludus-install-status
Ludus install completed successfully
Root API key: ROOT.o>T3BMm!^\As_0Fhve8B\VrD&zqc#kCk&B&?e|aF
```

Now create your first ludus user! This user will be an admin as we specify `--admin`.
Initials are commonly used for the userID.

**Warning:** If the user name you specify (converted to lowercase and spaces replaced with `-`) exists
on the system already, Ludus will refuse to overwrite it. Choose a new user name for your Ludus user.

Prepend the LUDUS_API_KEY variable to the command to authenticate properly.

**Tip:** Adding a space at the beginning of this command will prevent it from being written to the
shell's history file in most common shells.

```shell-session
LUDUS_API_KEY='ROOT.o>T3BMm!^\As_0Fhve8B\VrD&zqc#kCk&B&?e|aF' \
 ludus user add --name "John Doe" --userid JD --admin --url https://127.0.0.1:8081
+--------+------------------+-------+---------------------------------------------+
| USERID | PROXMOX USERNAME | ADMIN |                   API KEY                   |
+--------+------------------+-------+---------------------------------------------+
| JD     | john-doe         | true  | JD._7Gx2T5kTUSD%uTWZ*lFi=Os6MpFR^OrG+yT94Xt |
+--------+------------------+-------+---------------------------------------------+
```

## Set the API Key

Using the key from the previous step, we will export the `LUDUS_API_KEY` variable so it is known to future commands.

```shell-session
export LUDUS_API_KEY='JD._7Gx2T5kTUSD%uTWZ*lFi=Os6MpFR^OrG+yT94Xt'
```

With the API key set, all user commands are available!

## Get Proxmox Credentials

Ludus is built on top of the [Proxmox](https://www.proxmox.com/en/) hypervisor which has a web interface.
It's available at `https://<ludus IP>:8006` and the credentials for the web GUI can be retrieved with `ludus user creds get`.

```shell-session
ludus user creds get
+------------------+----------------------+
| PROXMOX USERNAME |   PROXMOX PASSWORD   |
+------------------+----------------------+
| john-doe         | oQjQC76Ny0HQfpNV31zK |
+------------------+----------------------+
```

**Note:** As a reminder, you can still log into the proxmox console as the `root` user for more advanced configurations such as adding a disk to your Proxmox server or adding a separate NIC to a virtual machine. Careful not to break anything!

Now that you've created the user and obtained your user creds for proxmox, you can build templates!
