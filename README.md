# OnBoardMe to [mac, mint]
 ♪ it only shoots t-shirts ♪

 This is a project to store config files, as well as programatically install core packages that I need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping I'd remember why it was there later, so this is now a renewed effort in remembering all the things.

Please report 🐛 in the GitHub issues, and I will get them as I have time.

## Quick Start
Run the setup script to install python dependencies and brew. This will ask for your password, because brew does that.
```bash
bash setup.sh
```

Now you can run the actual script that does the heavy lifting.
```bash
./onboardme.py
```

# Notes
You can find the bulk of my notes under the `docs` directory in this repo, but the goal is to get into some sort of wiki somewhere... soonish. Probably something like a little flask app with some sort of material design and a markdown plugin, because I don't have time for frontend at this stage of my life.

## Package Managers

This is ridiculous, but we're using: `apt`, `snap`, `flatpak`, and `brew`. Ansible is also being looked into, and provides an interface for installing more troublesome packages via the `command`, `script`, `download`, `git_clone`, `files`, and `sync` modules. We do this because you often can't use a package manager to install another package manager. For more info on Ansible, visit the `ansible` directory and check out the readme there :3

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


