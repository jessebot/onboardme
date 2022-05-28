## State of the project

- It's generally best right now to use 1 file per set of actions in the same family (file manipulation, users, groups, installing packages)

  This is a byproduct of how the demo script work right now. Certain design choices with the demo mean that steps in the automation pipeline run in a pre-determined order of events which can cause race-condition-like issues when combining multiple riles into one step (setting up groups, installing packages, and running commands all in the same yaml file).

  The good news is this is easily resolved in the next step of development of transitioning from a PoC bash script to using python + proper cloud-native techniques. I just have not had the time yet.


##  Build Your Own Profile

1. For any action you want the system to perform, create a yaml file starting with an index followed by an underscore and a descriptive title.

    Example:

    ```zsh
    # change to the profiles directory
    cd profiles

    # create a new profile by creating a new directory
    mkdir my_profile

    # enter the directory
    cd my_profile

    # create the first step in the automation pipeline
    touch 0_groups.yaml
    ```

2. In the `0_groups.yaml` file, we now describe the actions the system should take.
In this example I'm setting up a generic set of groups, notably lxd and docker 
which will allow me to run docker later without sudo.

    ```yaml
    Groups:
      - Name: automation
        State: present
      - Name: adm
        State: present
      - Name: cdrom
        State: present
      - Name: sudo
        State: present
      - Name: dip
        State: present
      - Name: plugdev
        State: present
      - Name: lxd
        State: present
      - Name: docker
        State: present
    ```

3. Next, lets create `1_users.yaml` and set up the users we will need:

    ```yaml
    Users:
    - Name: "vmadmin"
      State: present
      Comment: "automation user, dynamically altered at runtime - dont change"
      Shell: /bin/bash
      Create_Home: yes
      SSH_Key_file: no
      System: yes
      Groups: "sudo, docker"
      Password: "{{ 'password' | password_hash('sha512') }}"
    ```

4. As you can probably imagine, there are a host of modules that can be used to define subsequent steps for the automation pipeline. Some more examples are:

    - Run a command on the remote client

        ```yaml
        Commands:
          - Command: ""
            become:
            become_user:
            become_method:
        ```
    - Download a file or clone a repository on a remote client

        ```yaml
        Downloads:
          - Name:
            URL: ""
            Destination: ""
        Repos:
          - Source:
            Destination:
            Branch: ""
        ```
        There's no magic or anything, we're just defining a list of similar actions using ansible roles, then letting the tooling make it happen using some loopy-loops. 

## A non-complete list of available ansible roles

- wip

    ```yaml
    ---
    Apt_Keys:
      - Name:
        URL:
      - Name:
        URL:
    Apt_Pass_1:
      - Name:
        Version: (optional)
      - Name:
        Version: (optional)
    Apt_Pass_2:
      - Name:
        Version: (optional)
      - Name:
        Version: (optional)
    Apt_Repos:
      - Name:
        URL:
      - Name:
        URL:
    Brew_Path:
    Brew:
      - Name:
        State:
      - Name:
        State:
    Commands:
      - Command: ""
        become:
        become_user:
        become_method:
      - Command: ""
        become:
        become_user:
        become_method:
    Downloads:
      - Name:
        URL: ""
        Destination: ""
      - Name:
        URL: ""
        Destination: ""
    Files:
     - Name: Unarchive
       Archive: ""
       Dest: ""
       State: extract
     - Name: Create directory
       Path: ""
       Recurse:
       State: directory
     - Name: Delete directory
       Path: ""
       State: absent
     - Name: Create Simlink
       Source: ""
       Dest: ""
       State: link
     - Name: Change file ownership, group and permissions
       Path: ""
       Mode: ""
       State: permissions
     - Name: Copy files within remote client
       Source: ""
       Dest: ""
       Mode: ""
       State: copy
    Repos:
      - Source:
        Destination:
        Branch: ""
    Groups:
      - Name:
        State:
    Kernel_Upgrade:
      - Method: "yes"
        Comments: "choices are 'dist' 'full', 'no', 'safe', 'yes'"
    Package_Update:
      - Update: true
        Autoremove: true
    Path:
    Pip:
    Scripts:
    Snap:
    Sync:
    Users:
    ```

## Profiles I've been messing with

1. [Tanzu (Community Edition)](tanzu_ce)

- [Terraform](terraform)

- [vSphere (WIP)](vsphere)

- [Little Bradley](LB)

- [Big Bradley](BB)

- [Pi-hole (WiP)](dev/pihole)

- [Tanzu (on sSphere) WIP](dev/tanzu)

- [Lilu (Linux-in-Linux-Ubuntu)](dev/Lilu)

## __Linux Heads Up:__

- this linux image uses a non-standard /etc/sudoers config without requiretty
- Ansible pipelining is enabled in the included config. To enable it on your system, place the file in one of the ways directed below:

    - `ANSIBLE_CONFIG` (environment variable if set)
    - `ansible.cfg` (in the current directory)
    - `~/.ansible.cfg` (in the home directory)
    - `/etc/ansible/ansible.cfg`

## __Tanzu Heads Up:__

- For troubleshooting failed bootstraps, you can exec into a container and use the kubeconfig at /etc/kubernetes/admin.conf to access the API server directly. For example:

    ```zsh
    docker exec -it 4ae /bin/bash
    root@guest-control-plane-tcjk2:/# kubectl –kubeconfig=/etc/kubernetes/admin.conf get nodes
    ```

- If the Docker host machine is rebooted, the cluster will need to be re-created. Support for clusters surviving a host reboot is tracked in issue
https://github.com/vmware-tanzu/community-edition/issues/832
