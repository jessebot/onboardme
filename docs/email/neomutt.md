---
layout: default
title: NeoMutt
parent: Email
has_children: false
permalink: /email/neomutt
description: "How to configure neomutt and what we've learned so far"
---

# NeoMutt
[NeoMutt] is a terminal based email client from the 1990's. It's forked from an
even older 90's client called Mutt. They, like many ancient TUIs from the 90's,
have a pretty rough looking config language and documentation website,
but it's a really really solid client, and they recently (in 2017) added support
for [lua scripting], so it ain't all bad.

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

<details>
  <summary>w3m with no images directly in neomutt</summary>

  Create `~/.config/neomutt/mailcap` with this line:

  ```ini
  # I'm using sixel with w3m, but you could use any image renderer of your choice
  text/html; w3m -sixel -o auto_image=TRUE -o display_image=1 -T text/html %s; nametemplate=%s.html; needsterminal; copiousoutput
  ```

</details>

<details>
  <summary>w3m with images in neomutt, but autoview doesn't work</summary>

  Create `~/.config/neomutt/mailcap` with this line:

  ```ini
  # I'm using sixel with w3m, but you could use any image renderer of your choice
  text/html; w3m -sixel -o auto_image=TRUE -o display_image=1 -T text/html %s; nametemplate=%s.html; needsterminal; copiousoutput
  ```

</details>

<details>
  <summary>Display images in neomutt, in an iterm2 split (macOS only)</summary>

  This is a rat hole. TLDR; [neomutt does not support sixel] right now, so I
  decided to write some stuff to open w3m with sixel in an iterm2 split to
  avoid all the hassle.

  There's basically no way to easily and quickly view an attachment in my particular
  situation where I don't want to press as many keys, so I wrote a couple of things
  to help out, first of all, I created a new profile in iterm2 called minimal,
  and it runs this as the startup command:

  ```bash
  bash --noprofile --rcfile .bash_profile_minimal
  ```

  `.bash_profile_minimal` just sets up my default PATH and nothing else,
  so that I can still source homebrew installed applications such as w3m and sixel.

  Then I wrote a small script to open w3m in a iterm2 new split using that profile,
  and you can view it here (it's not terribly complicated, I wrote it in an or hour or so):
  [w3m-splits](https://github.com/jessebot/dot_files/blob/main/.local/bin/w3m-splits)


  Then I updated my mailcap file to have the following:

  ```mailcap
  # for displaying html files in a new split in iterm2 with w3m and sixel
  text/html; (clear && w3m-splits %s); nametemplate=%s.html
  ```

  I also ended updating my `~/.w3m/config` to have the following
  (that you can just hit q and it won't prompt for confirmation when quitting):

  ```bash
  confirm_qq false
  ```

  Finally, I needed a key map for this, because it still requires you to view the message, then view the attachments, then find the text/html mime type, and then select it. I found a neat little post on how to do this and implemented it like so:

  ```ini
  # Unbinds V from version (which just printed the version of neomutt)
  bind index,pager V  noop

  # quick html view macro; won't mark message as read for some reason :shrug:
  macro index,pager V "<view-attachments><search>html<enter><view-mailcap><exit>"
  ```

  Now when I want to view an email from the index (list of mail in mutt), I just hit shift+v , and it opens a split in iterm2 with the rendered w3m email with images working via sixel. It takes maybe 2 full seconds to open an email in the split, but it has the images and it works and that's good enough for me on macOS right now.

  Currently looking at creating a homebrew tap for zathura to do it even faster though I still wanted to document this, in case people find this when searching, because there's surprisingly very little out there for this hyper specific issue.

</details>


## Displaying images in the terminal

Check this out for more info: [neomutt mimesupport](https://neomutt.org/guide/mimesupport)

On macOS, I'm using iterm2, so I use imgcat, but can't figure out why it
doesn't work in neomutt, so I'm instead just sixel there too:

```
image/*; (clear && img2sixel %s); needsterminal
```

## Helpful links
- [Stephane: NeoMutt Cheatsheet](https://cheatsheets.stephane.plus/productivity/neomutt/)
- [reddit neomutt megathread](https://www.reddit.com/r/commandline/comments/fsm3sj/neomutt_config_megathread/)
- [Gideon Wolfe: Very good info to Neomutt](https://gideonwolfe.com/posts/workflow/neomutt/intro/)
- [Macro for opening text/html attachment](https://demu.red/blog/2017/11/neomutt-macro-opening-texthtml-attachment-from-the-index-view/)

[256-xterm colors]: (https://www.ditig.com/256-colors-cheat-sheet)
[neonwolf]: https://gitlab.com/h3xx/mutt-colors-neonwolf
[spacechalk powerline]: https://github.com/jessebot/dot_files/blob/main/.config/neomutt/themes
[neomutt powerline nerdfonts]: https://github.com/sheoak/neomutt-powerline-nerdfonts
[lua scripting]: https://neomutt.org/2017/04/29/lua#algolia:p:nth-of-type(8)
[neomutt does not support sixel]: https://github.com/neomutt/neomutt/issues/471
