---
layout: default
title: NeoMutt
parent: Email
has_children: false
permalink: /email/neomutt
description: "How to configure neomutt and what we've learned so far"
---

# NeoMutt
[NeoMutt] is a terminal based email client.

## Colorschemes
It's [256-xterm colors] again. TUIs can just be like that sometimes :/
Check out an example colorscheme here: [neonwolf]

## Configuring NeoMutt with Protonmail
You'll need the protonmail-bridge (which you can `brew install`).

Launch the protonmail bridge, login with your protonmail account, and then copy
the password it spits out. This will be your password that you're free to source
in your `neomuttrc` which should be located in `~/.config/neomutt/neomuttrc`.

You can check out an example [here](https://github.com/jessebot/dot_files/blob/main/.config/neomutt/neomuttrc).

## Helpful links
- [NeoMutt Cheatsheet](https://cheatsheets.stephane.plus/productivity/neomutt/)


[256-xterm colors]: (https://www.ditig.com/256-colors-cheat-sheet)
[neonwolf]: https://gitlab.com/h3xx/mutt-colors-neonwolf
