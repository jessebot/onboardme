# OnBoardMe to [mac, mint]
I have enough productivity tools and special configs for various programs (for both Mac and Linux) that I actually need a repo for them. Example: I need to manage like 4 OS level package managers, at least 🤦

The state of personal development software is not grand, so back to the basics of IT, we start from like 10 years of basic shell/Python scripts, and chain them together using ansible.

## Mint
Under construction, but the idea is that we keep the best of both worlds, and just have one script to support both OSes. And even better, it's run via like ansible and dockerized. The basic dev machine goal :blue_heart:

### Installation
Totally manual and awful. There is a config file with all the packages from 3 packages managers

### TODO
* add functioning arg parser
* ansible? 🤔
* KEYBOARD MAPPINGS: CAPS TO CONTROL
* Move the panel on the side and add panelettes or whatever they're called
* Setup script to automatically back up into configurable repo (default to this repo):
  * rss feeds OPML
  * YouTube subscriptions OPML
* 
* Overview of current configs maintained by this script?

#### Note
Theorectically, most of the config and setup for mint, also works for Ubuntu and other debian based systems, but YMMV.

## Mac
### Installation
*Install the Required Python packages*
`pip3 install -r requirements.txt`

*Run the script*
`./onboardme.py`

**You did it! :D **
Here, have some [free wallpapers](https://photos.app.goo.gl/mGjmG4o6JB9xxK7BA) from my old Google Pixel <3

### TODO
* alfred
  * get better URLs like 'latest', not pinned version
  * Personal settings for iterm/alfred
* process files from.... brew... file?
