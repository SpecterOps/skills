# Ludus CLI

The Ludus CLI is the primary method of interacting with a Ludus server. It uses the Ludus REST API to perform actions for the user, and has helpful wrappers designed to aid troubleshooting issues.

The Ludus CLI uses the pattern `ludus COMMAND ARG --FLAG`. Each command has its own help that can be accessed with `ludus [command] --help`.

## Configuration

All global flags can also be set with environment variables in the format `LUDUS_FLAG` where FLAG is the flag long form string in all upper case.

```
local:~$ LUDUS_URL=https://192.168.1.103:8080
local:~$ ludus version --verbose
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:102 Using config file: /Users/user/.config/ludus/config.yml
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:106 --- Configuration from cli and read from file ---
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:108 	url = https://10.98.108.2:8080
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:108 	proxy =
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:108 	verify = %!s(bool=false)
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:108 	user =
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:108 	verbose = %!s(bool=true)
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:108 	json = %!s(bool=false)
[DEBUG] 2024/02/09 15:38:31 ludus/cmd.initConfig:root.go:123 ---
```

The ludus CLI looks for a configuration file at `$HOME/.config/ludus/config.yml`, and if found, uses its values during execution.
The configuration file values are the lowest precedence, followed by ENV variables, and finally command line flags.

An example configuration file is shown below. You only need to set the values you wish to change.
The API key cannot be set in the config file and must be set in the system keyring or environment variable `LUDUS_API_KEY`.

```yaml
# config.yml
url: https://192.168.1.103:8080
json: false
verify: false
proxy: http://127.0.0.0.1:8000
user: JD
```

## Ludus

```
Usage:
  ludus [command]

Available Commands:
  ansible     Perform actions related to ansible roles and collections
  apikey      Store your Ludus API key in the system keyring
  completion  Generate the autocompletion script for the specified shell
  power       Control the power state of range VMs
  range       Perform actions on your range
  templates   List, build, add, or get the status of templates
  testing     Control the testing state of the range
  users       Perform actions related to users
  version     Prints the version of this ludus binary

Flags:
      --config string   config file (default is $HOME/.config/ludus/config.yml)
  -h, --help            help for ludus
      --json            format output as json
      --proxy string    HTTP(S) Proxy URL
      --url string      Server Host URL (default "https://198.51.100.1:8080")
      --user string     A user ID to impersonate (only available to admins)
      --verbose         verbose client output
      --verify          verify the HTTPS certificate of the Ludus server
```

## Ansible

The ansible command allows a Ludus user to add ansible roles and collections to the Ludus server for use in their range deployment. Additional roles can be added with the `roles` key and configured with the `role_vars` key (see [Configuration](./configuration.md)).

### Ansible Role

When adding an ansible role, you must specify a role name (to pull from galaxy.ansible.com), a URL, or a local path to a role directory (with `-d`). Specific versions can be specified with the `--version` flag.

```
Usage:
  ludus ansible role [command]

Aliases:
  role, roles

Available Commands:
  add         Add an ansible role to the ludus host
  list        List available Ansible roles on the Ludus host
  rm          Remove an ansible role from the ludus host
```

### Ansible Collection

Ansible collections can be added but not removed, as that is [not supported](https://github.com/ansible/ansible/issues/67759) by the `ansible-galaxy` command.

```
Usage:
  ludus ansible collection [command]

Aliases:
  collection, collections

Available Commands:
  add         Add an ansible collection to the ludus host
  list        List available user Ansible collections on the Ludus host
```

## Apikey

This command stores the Ludus API key in the system keyring.
This is implemented differently on different OS's but is more secure than writing unencrypted to a file.

If your machine does not have a keyring (headless Linux) you can set the api key in the `LUDUS_API_KEY` environment variable.

```
Usage:
  ludus apikey [flags]
```

## Completion

Generate the autocompletion script for ludus for the specified shell.
See each sub-command's help for details on how to use the generated script.

On macOS (assuming brew is installed) you will need to add the following to `~/.zshrc`:

```
fpath=(/opt/homebrew/share/zsh/site-functions/ $fpath)
autoload -U compinit; compinit
```

and then run `ludus completion zsh > $(brew --prefix)/share/zsh/site-functions/_ludus`.
Any new shells will have ludus completion loaded.

```
Usage:
  ludus completion [command]

Available Commands:
  bash        Generate the autocompletion script for bash
  fish        Generate the autocompletion script for fish
  powershell  Generate the autocompletion script for powershell
  zsh         Generate the autocompletion script for zsh
```

## Power

Control the power state of range VMs.
This command allows a user to power on or off one, multiple (comma separated), or all VMs in their range.

```
Usage:
  ludus power [command]

Available Commands:
  off         Power off all range VMs
  on          Power on all range VMs
```

## Range

The range command contains many subcommands related to deploying a range as well as getting useful files for range access (i.e. RDP or /etc/hosts).

```
Usage:
  ludus range [command]

Available Commands:
  abort       Kill the ansible process deploying a range
  access      Grant or revoke access to a range
  config      Get or set a range configuration
  deploy      Deploy a range, running specific tags if specified
  errors      Parse the latest deploy logs from your range and print any non-ignored fatal errors
  etc-hosts   Get an /etc/hosts formatted file for all hosts in the range
  gettags     Get the ansible tags available for use with deploy
  inventory   Get the ansible inventory file for a range
  list        List details about your range (alias: status)
  logs        Get the latest deploy logs from your range
  rdp         Get a zip of RDP configuration files for all Windows hosts in a rage
  rm          Delete your range (all VMs will be destroyed)
```

## Templates

List, build, add, or get the status of templates.

```
Usage:
  ludus templates [command]

Aliases:
  templates, template

Available Commands:
  abort       Kill any running packer processes for the given user (default: calling user)
  add         Add a template directory to ludus
  build       Build templates
  list        List all templates
  logs        Get the latest packer logs
  rm          Remove a template for the given user (default: calling user)
  status      Get templates being built
```

## Testing

Control the testing state of the range.
The update command currently only works with Windows VMs.

```
Usage:
  ludus testing [command]

Available Commands:
  allow       allow a domain, IP, or file containing domains and IPs during testing
  deny        deny a previously allowed domain, IP, or file containing domains and IPs during testing
  start       Snapshot all testing VMs and block all outbound connections and DNS from testing VMs
  status      Get the current testing status as well as any allowed domains and IPs (alias: list)
  stop        Revert all testing VMs and enable all outbound connections and DNS from testing VMs
  update      Update a VM or group of VMs
```

## Users

Perform actions related to users.
To use the `add` or `rm` commands, the admin API endpoint must be used.
This endpoint listens on 127.0.0.1:8081 on the Ludus server.
Use an SSH tunnel to access this endpoint to perform administrative actions.

```
Usage:
  ludus users [command]

Aliases:
  users, user

Available Commands:
  add         Add a user to Ludus
  apikey      Get a new Ludus apikey for a user
  creds       Perform actions related to Proxmox credentials
  list        List information about a user (alias: status)
  rm          Remove a user from Ludus
  wireguard   Get the Ludus wireguard configuration for a user
```

## Version

Prints the version of this ludus binary and the server (if an API key is available).
The version includes the SemVer version and the first 8 character of the git commit hash of the commit this binary was built from.

```
Usage:
  ludus version [--verbose]
```
