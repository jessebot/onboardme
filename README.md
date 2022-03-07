Project incredibly under construction in main, because there is so much rot and tech debt. Open an issue if something doesn't make sense, and we'll help you out 💙

# OnBoardMe to [mac, mint]
We have enough productivity tools and special configs for various programs (for both Mac and Linux) that we actually need a repo for them. Example: We need to manage like 4 OS level package managers, at least 🤦

The state of personal development software is not grand, so back to the basics of IT, we start from like 10 years of basic shell/Python scripts, and chain them together using ansible.

### Quick Note on FOSS, Ethics, and Surviellance
Here at this humble OnBoardMe repo, we try really hard to do the right thing. We're doing our best to get off of the giants like Google, Microsoft, Apple, Amazon, Samsung, etc... but we've still got a long way to go! Check back here for alternatives as we go on the journey ourselves! We'll link back to any orgs or projects we learn about, but free to open an issue with anything else we should link back to. :)

## Mint
Under construction, but the idea is that we keep the best of both worlds, and just have one script to support both OSes. And even better, it's run via like ansible and dockerized. The basic dev machine goal :blue_heart:

### Installation
Totally manual and awful. There is a config file with all the packages from 3 packages managers

### TODO
* add functioning arg parser
  * OS selection [mac, mint] 
* ansible? 🤔 ...in docker?
  * start with just like package manager managed packages
    * easier to have later offering of "deplay this config to other machines"
* KEYBOARD MAPPINGS: CAPSLOCK TO CONTROL
* Move the panel to the side, and add panelettes or whatever they're called
* Setup script to automatically backup into configurable repo (default to this repo):
  * RSS feeds OPML
  * YouTube subscriptions OPML
  * Shell/editor rc files
    * Ask before doing this!
* Add chat software
* Add NextCloud stuff - at least try News, Recipes, and Talk
* Add email config
* Overview of current configs maintained by this script?
* Add go lines before k8s/docker/kind stuff
* Check for external apt repos that may need adding
* Alfred replacement
* add iptables configs
* add rc file symlinks to this repo directory

#### Note
Theorectically, most of the config and setup for mint, also works for Ubuntu and other debian based systems, but YMMV.

## Mac
### Installation
*Install the Required Python packages*
`pip3 install -r requirements.txt`

*Run the script*
`./onboardme.py`

*You did it! :D* Here, have some [free wallpapers](https://photos.app.goo.gl/mGjmG4o6JB9xxK7BA) from my old Google Pixel <3

### TODO
* alfred
  * get better URLs like 'latest', not pinned version
  * Personal settings for iterm/alfred
* process files from.... brew... file?
