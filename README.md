# OnBoardMe to [mac, mint]

> **This project in pre-alpha state, and incredibly **Under Construction** in the `main` branch, because there is so much rot and tech debt. Open an issue if something doesn't make sense, and we'll help you out 💙**

## Why?

- We have enough productivity tools and special configs for various programs (for both Mac and Linux) that we actually need a repo for them. Example: We need to manage like 4 native OS package managers, at least 🤦 The state of personal development software is not grand, so back to the basics of IT, we start from like 10 years of basic shell/Python scripts, and chain them together using ansible, but even the research phase of this project has taken forever, because there's many things to test and reproduce. This is slow, but trust me, worth it.

## Package Managers

This is ridiculous, but we're using: `apt`, `snap`, `flatpak`, `brew`, as well as `pip`, and... (researching [deb-get](http://manpages.ubuntu.com/manpages/bionic/man1/debget.1p.html)) Ansible also provides an interface for installing more troublesome packages via the `command`, `script`, `download`, `git_clone`, `files`, and `sync` modules. We do this because you often can't use a package manager to install another package manager.

## Ansible Automated Installation (Under Construction)

  1. `cd onboardme/ansible`
  2. `bash demo.sh create`
  3. When you see a login prompt press "ctrl + b" then "d" to detach from the tmux session
  4. `bash demo.sh provision`
  5. `bash demo.sh ssh_to_vm`

## Ansible Manual Installation

1. Select or Create a profile

    - Existing profiles/templates can be found in the [ansible_profiles](onboardme/configs/ansible_profiles) directoy

    - Follow the instructions [HERE](onboardme/configs/ansible_profiles/README.md) to customize or create a profile

2. Create an Ansible inventory file for the client

    - Create an inventory file for your target machine. See [demo.sh add_vm_to_inventory](/home/max/onboardme/ansible/demo.sh) for an automated example

3. Provision the client by running a playbook

    - Run an ansible playbook to gether facts, run a single step, or a full profile against the target host. See [demo.sh](/home/max/onboardme/ansible/demo.sh) for automated examples.

## Important Notes on FOSS and Ethics

- Here at this humble OnBoardMe repo, we try really hard to do the right thing. We're doing our best to get off of the giants like Google, Microsoft, Apple, Amazon, Samsung, etc... but we've still got a long way to go! Check back here for alternatives as we go on the journey ourselves! We'll link back to any orgs or projects we learn about, but feel free to open an issue with anything else we should link back to. :)

  Living ethically under late stage capitalism is not easy, but we believe generally that software should be Free and Open Source.

## What is (FOSS), Free and Open Source Software

- We believe in free software, and we do our best to use and support actually free and open source software. If you don't know what we mean, please check out this [GNU article on Free SoftWare](https://www.gnu.org/philosophy/free-sw.en.html).

## Language

- We are currently using the philosophy of [Terminology, Power, and Exclusionary Language in Internet-Drafts and RFCs draft](https://datatracker.ietf.org/doc/html/draft-knodel-terminology-09) and at the time of writing, this draft is currently on verison 09.

## Humane Tech Lists

- We've had good luck with [Awesome Humane Tech](https://github.com/humanetech-community/awesome-humane-tech) for guides and checking out alternatives to tech from the Giants you previously used.


### TODOs
Stuff that needs doing
<details>
  <summary>Coming Soon</summary>
  <ul>
  <li>Android notes</li>
  <li>SDR notes</li>
  </ul>
</details>

<details>
  <summary>Coming Later</summary>
  <ul>
  <li>SmartWatch OS</li>
  </ul>
</details>

<details>
  <summary>Should have already come</summary>
  <ul>
  <li> KEYBOARD MAPPINGS: CAPSLOCK TO CONTROL - need for both debian (gnome/xfce menu mappings?) and mac osx</li>
  <li> Move the panel to the side, and add panelettes or whatever they're called</li>
  <li> Setup crontab (or whatever you do on a mac) script to automatically backup into configurable repo (default to this repo):</li>
    <li> RSS feeds OPML</li>
    <li> FreeTube/NewPipe subscriptions OPML/db</li>
  <li> Add chat software</li>
  <li> Add NextCloud stuff <li> at least try News, Recipes, and Talk</li>
  <li> Overview of current configs maintained by this script?</li>
  <li> Which email clients to support? MUTT? ThunderGuy?</li>
  <li> Alfred</li>
    <ul>
    <li> Find FOSS replacement?</li>
    <li> Personal settings for alfred</li>
    </ul>
  </ul>
</details>

#### Note

Theorectically, most of the config and setup for Mint, also works for Ubuntu and other Debian based distros, but YMMV.
Current attempts at getting the Debian portions of the onboardme script working, and then merging them both. Trying to gather thoughts generally here for first pass.

# Current Ecoscape of Personal Tech

### News

- RSS client: Fluent Reader

## Apple/Mac replacements

- `albert` instead of alfred
*albert fails to install via apt or dpkg, but works via the linux mint software manager :shrug:*

## Google Replacements

### Email

- ProtonMail and Bridge for Linux

### Generic Storage

- NextCloud for Google photos/drive (In the works)
- minio for AWS S3 storage
  (Even if you don't want to host it yourself, you should contact your local datacenters and see if they offer an object storage service, because they might, and it could be really cheap. Don't give your money to AWS.)

### Youtube

- FreeTube
- PeerTube (Currently just using this via web URLs and not hosting my own)

### Search

- Startpage for anonymous google search
- Duckduckgo for alternative Google search


# Extra notes

Brew tips [here](https://gist.github.com/ChristopherA/a579274536aab36ea9966f301ff14f3f)

great vim yaml walkthrough:
https://www.arthurkoziel.com/setting-up-vim-for-yaml/
