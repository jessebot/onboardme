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

## Colorschemes and Themes
It's [256-xterm colors] again. TUIs can just be like that sometimes :/
Check out an example colorscheme here: [neonwolf]
And then checkout the one I hacked together here: [spacechalk powerline]
It was hacked together in part from this: [neomutt powerline nerdfonts]

## Configuring NeoMutt with Protonmail
You'll need the protonmail-bridge (which you can `brew install`).

Launch the protonmail bridge, login with your protonmail account, and then copy
the password it spits out. This will be your password that you're free to source
in your `neomuttrc` which should be located in `~/.config/neomutt/neomuttrc`.

You can check out an example [here](https://github.com/jessebot/dot_files/blob/main/.config/neomutt/neomuttrc).

## Displaying html in the terminal
I use w3m for this right now.
You can to by creating `~/.config/neomutt/mailcap` with this line:

```
# I'm using sixel with w3m, but you could use any image renderer of your choice
text/html; w3m -sixel -o auto_image=TRUE -o display_image=1 -T text/html %s; nametemplate=%s.html; needsterminal
```

## Displaying images in the terminal

Check this out for more inof: https://neomutt.org/guide/mimesupport

On macOS, I'm using iterm2, so I use imgcat, but can't figure out why it
doesn't work in neomutt, so I'm instead just sixel there too:

```
image/*; (clear && img2sixel %s); needsterminal
```

## Helpful links
- [NeoMutt Cheatsheet](https://cheatsheets.stephane.plus/productivity/neomutt/)
- [reddit neomutt megathread](https://www.reddit.com/r/commandline/comments/fsm3sj/neomutt_config_megathread/)
- [Very good info to Neomutt](https://gideonwolfe.com/posts/workflow/neomutt/intro/)

[256-xterm colors]: (https://www.ditig.com/256-colors-cheat-sheet)
[neonwolf]: https://gitlab.com/h3xx/mutt-colors-neonwolf
[spacechalk powerline]: https://github.com/jessebot/dot_files/blob/main/.config/neomutt/themes
[neomutt powerline nerdfonts]: https://github.com/sheoak/neomutt-powerline-nerdfonts
