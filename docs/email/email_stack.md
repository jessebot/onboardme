---
layout: default
title: Current Email Stack
parent: Email
has_children: false
permalink: /email/current-stack
description: "The current stack we use to check email in the terminal"
---

# Using Protonmail through the terminal
All of the below stuff assumes you're using protonmail, just because that's what I use.
Before you get started below, please install the [protonmail bridge] on macOS or Linux.

## `offlineimap`
GET YOUR EMAILS LOCALLY, this time with python.

Install offlineimap:

```bash
# this should work on macOS and Linux
brew install offlineimap
```

You can view the man pages([1], [2]) in w3m:

```bash
w3m https://www.offlineimap.org/doc/offlineimap.html
w3m https://www.offlineimap.org/doc/offlineimapui.html
```

Edit the config file (`~/.config/offlineimap/config`):

```toml
# Offlineimap configuration file for protonmail
#
# examples on linux: /home/linuxbrew/.linuxbrew/etc/offlineimap.conf.minimal
#                    /home/linuxbrew/.linuxbrew/etc/offlineimap.conf

[general]
accounts = protonmail
# this just runs a line of python to env vars below: from os import environ
pythonfile = ~/.config/offlineimap/offlineimap_account_setup.py
metadata = ~/.cache/offlineimap

[Account protonmail]
remoterepository = protonmail-remote
localrepository = protonmail-local

[Repository protonmail-local]
type = Maildir
localfolders = ~/.local/share/offlineimap
sync_deletes = no

[Repository protonmail-remote]
type = IMAP
# These are just environment variables, and won't work without the python file
remotehosteval = environ["MAIL_SERVER"]
remoteporteval = int(environ["MAIL_PORT"])
remoteusereval = environ["MAIL_USER"]
remotepasseval = environ["MAIL_PASS"]

# this part is important for protonmail
starttls = yes
ssl = no
ssl_version = tls1_2
sslcacertfile = ~/.config/protonmail/bridge/cert.pem
# I don't know what this does
expunge = yes

# --------- section for what folders and labels you pull ------------
nametrans = lambda foldername: re.sub ('^Folders.', '', foldername)
folderfilter = lambda foldername: foldername not in ['All Mail']
```

Then, if you chose to use the `remote*eval` parameters above, you'll need
a python file with the following in it:

```python
# this file would be named whatever you called your pythonfile in your config
#!/usr/bin/env python3.11
from os import environ
```

As an example, my pythonfile above is called, but you could name it anything:
`~/.config/offlineimap/offlineimap_account_setup.py`

After that, you can go ahead and run: `offlineimap`

Then you _should_ have all your email locally in `~/.local/share/offlineimap/`.

## NotMuch
[NotMuch] is an email indexer and tagging system. We'll use it to index our mail,
because neomutt is slow and bad at this part. You can get started with:

Make sure to set the maildir to `~/.local/share/offlineimap`.

```bash
notmuch setup
```

And after that, you can run notmuch for the first time with:

```bash
notmuch new
```

## NeoMutt
[Neomutt] is an email client TUI (terminal user interface) for viewing and
sending email.


## References
It is surprisingly hard to find docs on protonmail via a TUI... so thank you very much to all the authors of these posts below!

- []()

[1]: https://www.offlineimap.org/doc/offlineimap.html
[2]: https://www.offlineimap.org/doc/offlineimapui.html
[protonmail bridge]: https://proton.me/mail/bridge "ProtonMail Bridge"
[neomutt]: https://neomutt.org/ "NeoMutt"
