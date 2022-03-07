Project incredibly under construction in main, because there is so much rot and tech debt. Open an issue if something doesn't make sense, and we'll help you out 💙

# OnBoardMe to [mac, mint]
We have enough productivity tools and special configs for various programs (for both Mac and Linux) that we actually need a repo for them. Example: We need to manage like 4 OS level package managers, at least 🤦

The state of personal development software is not grand, so back to the basics of IT, we start from like 10 years of basic shell/Python scripts, and chain them together using ansible.

### Notes on FOSS and Ethics
Here at this humble OnBoardMe repo, we try really hard to do the right thing. We're doing our best to get off of the giants like Google, Microsoft, Apple, Amazon, Samsung, etc... but we've still got a long way to go! Check back here for alternatives as we go on the journey ourselves! We'll link back to any orgs or projects we learn about, but free to open an issue with anything else we should link back to. :)

Living ethically under late stage capitalism is not easy, but we believe generally that software should be:

### Free and Open Source Software (FOSS)
We believe in free software, and we do our best to use and support actually free and open source software. If you don't know what we mean, please check out this [GNU article on Free SoftWare](https://www.gnu.org/philosophy/free-sw.en.html).

### Language
We are currently using the philosophy of [Terminology, Power, and Exclusionary Language in Internet-Drafts and RFCs draft](https://datatracker.ietf.org/doc/html/draft-knodel-terminology-09) and at the time of writing, this draft is currently on verison 09.

### Humane Tech Lists
We've had good luck with [Awesome Humane Tech](https://github.com/humanetech-community/awesome-humane-tech) for guides and checking out alternatives to tech from the Giants you previously used.

## Mint
Under construction, but the idea is that we keep the best of both worlds, and just have one script to support both OSes. And even better, it's run via like ansible and dockerized. The basic dev machine goal :blue_heart:

### Installation
Totally manual and awful. There is a config file with all the packages from 3 packages managers

### TODO
* add functioning arg parser
  * OS selection [Mac, Mint]
   * Coming Soon: Android, SDR notes
   * Coming Later: SmartWatch OS 
* KEYBOARD MAPPINGS: CAPSLOCK TO CONTROL - need for both debian (gnome/xfce menu mappings?) and mac osx
* Move the panel to the side, and add panelettes or whatever they're called
* Setup crontab (or whatever you do on a mac) script to automatically backup into configurable repo (default to this repo):
  * RSS feeds OPML
  * FreeTube/NewPipe subscriptions OPML
  * Shell/editor rc files
    * Ask before doing this!
* Add chat software
* Add NextCloud stuff - at least try News, Recipes, and Talk
* Overview of current configs maintained by this script?
* Add go lines before k8s/docker/kind stuff
* Check for external apt repos that may need adding
* add rc file symlinks to this repo directory
* Which email clients to support? MUTT? ThunderGuy?
* Alfred
  * Find FOSS replacement?
  * Personal settings for alfred

### TODO: Max
* ansiblify the packages in `packages.yml`

#### Note
Theorectically, most of the config and setup for Mint, also works for Ubuntu and other Debian based distros, but YMMV.

## Mac
### Installation
*Install the Required Python packages*
`pip3 install -r requirements.txt`

*Run the script*
`./onboardme_mac.py`

*You did it!* 🥳 Here, have some [free wallpapers](https://photos.app.goo.gl/mGjmG4o6JB9xxK7BA) from my old Google Pixel <3

### TODO

