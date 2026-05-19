# Ludus Developer Reference

## Contributing Guide

Thank you for your interest in contributing to Ludus. This is a
generic guide that details how to contribute to Ludus in a way that
is efficient for everyone. If you want a specific documentation for
different parts of the platform, please refer to `docs/` directory.

### Reporting Bugs

We are using [GitLab Issues](https://gitlab.com/badsectorlabs/ludus/-/issues)
for our public bugs. We keep a close eye on this and try to make it
clear when we have an internal fix in progress. Before filing a new
task, try to make sure your problem doesn't already exist.

If you found a bug, please report it, if possible with:

- a detailed explanation of steps to reproduce the error
- verbose output from the Ludus CLI

If you found a bug that you consider better discuss in private (for
example: security bugs), please submit a confidential issue.

**We don't have formal bug bounty program for security reports; this
is an open source application and your contribution will be recognized
in the changelog.**

### Pull requests

If you want propose a change or bug fix with the Pull-Request system
firstly you should carefully read the **DCO** section and format your
commits accordingly.

If you intend to fix a bug it's fine to submit a pull request right
away but we still recommend to file an issue detailing what you're
fixing. This is helpful in case we don't accept that specific fix but
want to keep track of the issue.

If you want to implement or start working in a new feature, please
open a **question** / **discussion** issue for it. No pull-request
will be accepted without previous chat about the changes,
independently if it is a new feature, already planned feature or small
quick win.

If possible, please test all changes locally in your own CI environment.

### Commit Guidelines

We have very precise rules over how our git commit messages can be formatted.

The commit message format is:

```
<type> <subject>

[body]

[footer]
```

Where type is:

- fix: a commit that fixes a bug
- feat: a commit with new feature
- refactor: a commit that introduces a refactor
- style: a commit with cosmetic changes
- docs: a commit that improves or adds documentation
- wip: a wip commit
- perf: a commit with performance improvements
- revert: a commit that reverts changes
- test: a commit that adds missing tests or corrects existing tests
- chore: a commit with other changes that don't modify src or test files
- build: a commit with changes that affect the build system or external dependencies
- ci: a commit that changes our CI configuration files and scripts

We encourage you to use a tool like [koji](https://github.com/its-danny/koji) to enforce these standards.

Each commit should have:

- A concise subject using imperative mood.
- The subject should have capitalized the first letter, without period
  at the end and no larger than 65 characters.
- A blank line between the subject line and the body.

Examples of good commit messages:

- `fix: fix the case where parallel > number of templates and 'template build' is called more than once before templates are done building`
- `refactor: clean up parallel builds`
- `fix(config): force the user to define all defaults if any defaults are defined as it completely replaces the server's default dict object`
- `docs: center image in readme`
- `ci: fix baseUrl setting for gitlab pages deployment`

### Developer's Certificate of Origin (DCO)

By submitting code you agree to and can certify the below:

```
    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.
```

All your code patches should
contain a sign-off at the end of the patch/commit description body. It
can be automatically added on adding `-s` parameter to `git commit`.

This is an example:

```
    Signed-off-by: Erik [Bad Sector Labs] <555113-badsectorlabs@users.noreply.gitlab.com>
```

To do this in combination with koji, this alias may be helpful:

```
alias ko="koji -c ~/.config/koji/config.toml && git commit --amend --no-edit -s"
```

## Building from Source

**Warning:** The main branch is not guaranteed to be stable. For guaranteed stability, use the most recent release's tag:

```shell
STABLE_VERSION=$(curl -s https://gitlab.com/api/v4/projects/54052321/releases/ | \
  jq '.[]' | jq -r '.name' | head -1 | egrep -o '[0-9]+\.[0-9]+\.[0-9]+')
git clone https://gitlab.com/badsectorlabs/ludus.git
cd ludus
git checkout tags/$STABLE_VERSION
```

### Server

#### Building without embedded documentation

Assuming a Debian 12/13 or Proxmox 8/9 host, install the build dependencies

```shell
# Install Go
wget https://go.dev/dl/go1.24.0.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.24.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

Build Ludus

```shell
git clone https://gitlab.com/badsectorlabs/ludus.git
cd ludus
export GIT_COMMIT_SHORT_HASH=$(git rev-parse --short HEAD)
export VERSION=$(git rev-parse --abbrev-ref HEAD)
cd ludus-server
GOOS=linux GOARCH=amd64 go build -trimpath -ldflags "-s -w -X main.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual-no-docs -X main.VersionString=$VERSION" -o ludus-server
```

#### Building with embedded documentation

Assuming a Debian 12/13 or Proxmox 8/9 host, install the build dependencies

```shell
# Install yarn
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | tee /etc/apt/trusted.gpg.d/dl.yarnpkg.com.asc
apt update
apt install yarn
# Install Go
wget https://go.dev/dl/go1.24.0.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.24.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

Build Ludus

```shell
# Get the code
git clone https://gitlab.com/badsectorlabs/ludus.git
cd ludus
export GIT_COMMIT_SHORT_HASH=$(git rev-parse --short HEAD)
export VERSION=$(git rev-parse --abbrev-ref HEAD)
# Build the docs
cd docs
yarn install
yarn build
# Remove videos to make the binary smaller
rm -f ./build/video/*
rm -f ./build/img/hardware/Debian_12_RAID0.mp4
# Move the docs to the location the server expects to embed them
mv ./build ../ludus-server/src/docs
cd ../ludus-server
# Build Ludus
GOOS=linux GOARCH=amd64 go build -tags=embeddocs -trimpath -ldflags "-s -w -X main.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual-with-docs -X main.VersionString=$VERSION" -o ludus-server
```

### Client

First, install [Go](https://go.dev/doc/install) for your operating system.

#### Building for your current OS/Arch

```shell
git clone https://gitlab.com/badsectorlabs/ludus.git
export GIT_COMMIT_SHORT_HASH=$(git rev-parse --short HEAD)
export VERSION=$(git rev-parse --abbrev-ref HEAD)
cd ludus-client
go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X main.VersionString=$VERSION"
```

#### Building for all OS/Archs

```shell
git clone https://gitlab.com/badsectorlabs/ludus.git
export GIT_COMMIT_SHORT_HASH=$(git rev-parse --short HEAD)
export VERSION=$(git rev-parse --abbrev-ref HEAD)
cd ludus-client
# Use the fork that doesn't break the terminal on control+c for Linux and macOS
git clone https://github.com/zimeg/spinner
cd spinner && git checkout unhide-interrupts && cd .. && go mod edit -replace github.com/briandowns/spinner=./spinner
GOOS=linux GOARCH=amd64 go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X ludus/cmd.VersionString=$VERSION" -o ./binaries/ludus-client_linux-amd64
GOOS=linux GOARCH=arm64 go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X ludus/cmd.VersionString=$VERSION" -o ./binaries/ludus-client_linux-arm64
GOOS=darwin GOARCH=amd64 go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X ludus/cmd.VersionString=$VERSION" -o ./binaries/ludus-client_macOS-amd64
GOOS=darwin GOARCH=arm64 go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X ludus/cmd.VersionString=$VERSION" -o ./binaries/ludus-client_macOS-arm64
# The forked spinner library doesn't compile for windows, so switch back to the original
go mod edit -dropreplace=github.com/briandowns/spinner
GOOS=windows GOARCH=amd64 go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X ludus/cmd.VersionString=$VERSION" -o ./binaries/ludus-client_windows-amd64.exe
GOOS=windows GOARCH=386 go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X ludus/cmd.VersionString=$VERSION" -o ./binaries/ludus-client_windows-386.exe
GOOS=windows GOARCH=arm64 go build -trimpath -ldflags "-s -w -X ludus/cmd.GitCommitHash=${GIT_COMMIT_SHORT_HASH}-manual -X ludus/cmd.VersionString=$VERSION" -o ./binaries/ludus-client_windows-arm64.exe
# All client binaries will be in the `binaries` folder
```

## Developing Ansible Roles

### Role structure

Ansible roles should follow the [standard structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-directory-structure) and must have a `meta` folder with a `main.yml` file.

**Tip:** Use the [ludus role template](https://github.com/badsectorlabs/ludus_ansible_role_template) to quickly get started.

If you've built a cool role you'd like to share with us, let us know via email (info@badsectorlabs.com), ping us on X (@badsectorlabs), or in our Discord server and submit a pull request to have it added to the roles page.

### Testing roles

To quickly test roles, use the `-t user-defined-roles`, `--limit` and `--only-roles` flags to execute only the role you are testing on the machine you are testing it on.

For example, given the following range config that begins:

```yaml
ludus:
  - vm_name: "{{ range_id }}-ad-dc-win2022-server-x64-1"
    hostname: "{{ range_id }}-DC01-2022"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 11
    ram_gb: 6
    cpus: 4
    windows:
      sysprep: true
    domain:
      fqdn: ludus.domain
      role: primary-dc
    roles:
      - testing_role
      - a_stable_role
      - another_stable_role
...
```

If you wish to only run the `testing_role` role on `JD-ad-dc-win2022-server-x64-1` (assuming range_id is JD) you would run:

```shell-session
ludus range deploy -t user-defined-roles --limit JD-ad-dc-win2022-server-x64-1 \
 --only-roles testing_role
```

This command construct enables the rapid testing of ansible roles in a loop such as:

1. Update role code locally in an editor
2. Update role code on the server with `ludus ansible roles add -d ./testing_role --force`
3. Run just the role on the test host with the command described above
4. Examine logs with `ludus range logs -f` or `ludus range errors`
5. Goto: 1

### Ludus specific variables

When developing a role for Ludus, you may want to access information about a host for use in your role.
The following variables are available for your use and reflect the values for the specific host that is executing your role:

```
ludus_dns_server          # Will always be the .254 of this VMs VLAN (i.e. 10.2.10.254 for a VM in VLAN 10)
ludus_domain_fqdn         # The full domain, if the VM has a domain defined, (i.e. ludus.internal.domain)
ludus_domain_netbios_name # The netbios part of the VM's domain, if the VM has a domain defined (i.e. ludus)
ludus_domain_fqdn_tail    # The non-netbios part of the VM's domain, if the VM has a domain defined (i.e. internal.domain)
ludus_dc_vm_name          # The name of the VM that is the primary DC for this VM's domain, if the VM has a domain defined
ludus_dc_ip               # The IP of the VM that is the primary DC for this VM's domain, if the VM has a domain defined
ludus_dc_hostname         # The hostname of the VM that is the primary DC for this VM's domain, if the VM has a domain defined
```

All other ansible variables (i.e. `ansible_hostname`) and Ludus variables are also available to custom roles, such as `defaults`, `ludus`, or `network` as defined in the user's config.

## CI/CD

### Requirements

**Warning:** This will nest a full Ludus install for every pipeline in an existing Ludus server. Going more than 1 layer deep of nested virtualization is not supported.

To set up a CI/CD runner for Ludus development you must meet the following requirements:

1. A functional, fast, Ludus server with at least 32GB of free RAM, 250GB of free disk space, and 8 cores available (can over-provision cores if necessary)
2. The `debian-13-x64-server-template` must be built
3. Root access to the Ludus server
4. A Gitlab account with the ability to create a runner token (gitlab.com or self-hosted)
5. Network access from the Ludus server to the Gitlab instance/gitlab.com

### Setup

To setup the CI/CD runner and template follow these steps:

1. Create a Gitlab runner with the tag `ludus-proxmox-runner`. Do not check `Run untagged jobs`.

2. Copy the Gitlab runner token

3. Review the settings in `/opt/ludus/ci/setup.sh` to ensure they match your environment (i.e. `PROXMOX_VM_STORAGE_POOL`)

4. Run `/opt/ludus/ci/setup.sh` with appropriate env variables as root on the Ludus server:

```
PROXMOX_USERNAME=root@pam PROXMOX_PASSWORD=password /opt/ludus/ci/setup.sh
```

5. When the playbook finishes running, you will see a `debian-12-x64-server-ludus-ci-template` template in the Proxmox web UI and `ludus templates list` (admins only).

6. Review the settings in `/opt/ludus/ci/base.sh`, specifically the `PROXMOX_NODE` setting and modify it as necessary.

Now that CI is setup and configured, any commits that are pushed to the Ludus project will build and test as appropriate.

### Tags

The CI system is set up to run the appropriate tests depending on what part of the code base has been modified.
However, sometimes you want to override the defaults.
To manually control the CI pipeline, you can add "tags" to the final commit message before a push.
To use these, simply include one or more of the "tag" strings in your commit message, including the brackets.

The available tags are listed below:

- `[skip ci]` - this tag skips all CI jobs
- `[skip build]` - skips the documentation build and the binary build stages
- `[build docs]` - force a documentation build
- `[build pages]` - force a documentation build and pages deploy
- `[full build]` - run every step of the CI pipeline, no matter how small the change to the code base
- `[manual]` - only run the documentation build (if docs have changed) and binary build, then push the code to an already running CI VM (typically used with the `[VMID-XYZ]` tag, defaults to the runner with least uptime)
- `[VMID-XYZ]` - run jobs on the specified VM where `XYZ` is the numeric VMID of the CI/CD VM.
- `[client tests]` - test basic client commands that do not deploy templates or ranges
- `[template tests]` - run a template build and wait for all templates to complete building
- `[range tests]` - run a range deploy and wait for it to succeed. This uses the `simple-domain.yml` range config.
- `[post-deploy tests]` - runs all tests related post-deployment tasks (testing mode, allowing and denying domains and IPs, powering on and off a VM, adding and removing users, etc)
- `[testing-mode tests]` - runs tests to determine if testing mode functions properly
- `[ansible tests]` - runs tests to determine if ansible features function properly
- `[user tests]` - runs tests to determine if the functions related to user management function properly
- `[template tests]` - runs tests related to adding, building, and removing custom templates
- `[start-at templates]` - run all test starting at the template builds
- `[start-at range-admin]` - run all test starting at the deployment of the admin user range
- `[start-at post-deploy-admin]` - run all test starting after the admin range has deployed
- `[start-at range-user]` - run all test starting at the deployment of the standard user range
- `[start-at post-deploy-user]` - run all test starting after the deployment of the standard user range
- `[start-at integration]` - just run the final integration test

### Releases

Any time a version tag is created in Gitlab, two additional CI jobs are added to the pipeline: `upload` and `release`.
These jobs are manually triggered (you must click the play button in the pipeline) and upload the compiled binaries to the package registry as well as create the actual release. If you use conventional commits (perhaps created with koji), then git-cliff will automatically generate a change log for the release.

### Manual CI VM Setup

Run these commands on a Debian 13 VM, then power it off and save it as a template

```
hostname ludus-ci-debian-13

# Resize the disk by hand if needed (should be ~250GB)
fdisk /dev/vda1
p
d
n
1
2048
[End]
N
w

resize2fs /dev/vda1

# Install Go
apt install curl wget ca-certificates
wget https://go.dev/dl/go1.25.1.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.25.1.linux-amd64.tar.gz
# This is required since gitlab-runner ignores .bashrc
echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile


# Add the gitlab-runner user and allow them to sudo
useradd -m -s /bin/bash -c "Gitlab Runner" gitlab-runner
# This breaks gitlab-runner, remove it
rm /home/gitlab-runner/.bash_logout
echo 'gitlab-runner ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Install needed components
curl -L 'https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh' | bash
curl -s 'https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh' | bash
apt install gitlab-runner git git-lfs build-essential vim tmux htop jq python3-debian

# Install node/yarn for documentation building
curl -fsSL https://deb.nodesource.com/setup_21.x | bash - && apt-get install -y nodejs
npm install --global yarn

# Helpful to auto-load the key on login for troubleshooting
echo 'if [ -f /opt/ludus/ci/.apikey-admin ]; then export LUDUS_API_KEY=$(cat /opt/ludus/ci/.apikey-admin); fi' >> /home/gitlab-runner/.bashrc
echo 'if [ -f /opt/ludus/ci/.apikey-user ]; then export LUDUS_API_KEY=$(cat /opt/ludus/ci/.apikey-user); fi' >> /home/gitlab-runner/.bashrc

# Warm the caches
su gitlab-runner -
cd /tmp
git clone https://gitlab.com/badsectorlabs/ludus

cd ludus/ludus-server
GOOS=linux GOARCH=amd64 go build -trimpath -ldflags "-s -w"

cd ../ludus-client
git clone https://github.com/zimeg/spinner
cd spinner && git checkout unhide-interrupts && cd .. && go mod edit -replace github.com/briandowns/spinner=./spinner
GOOS=linux GOARCH=amd64 go build -trimpath -ldflags "-s -w"
GOOS=linux GOARCH=arm64 go build -trimpath -ldflags "-s -w"
GOOS=darwin GOARCH=amd64 go build -trimpath -ldflags "-s -w"
GOOS=darwin GOARCH=arm64 go build -trimpath -ldflags "-s -w"
# The forked spinner library doesn't compile for windows, so switch back to the original
go mod edit -dropreplace=github.com/briandowns/spinner
GOOS=windows GOARCH=amd64 go build -trimpath -ldflags "-s -w"
GOOS=windows GOARCH=386 go build -trimpath -ldflags "-s -w"
GOOS=windows GOARCH=arm64 go build -trimpath -ldflags "-s -w"

cd ../docs
yarn install
yarn build
```
