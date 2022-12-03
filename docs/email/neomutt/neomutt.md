---
layout: default
title: NeoMutt
parent: Email
has_children: true
permalink: /email/neomutt
description: "How to configure neomutt and what we've learned so far"
---

# NeoMutt
[NeoMutt] is a terminal based email client from the 1990's. It's forked from an even older 90's client called [Mutt](http://mutt.org). They, like many ancient TUIs from the 90's, have a pretty rough looking config language and documentation website, but it's a really really solid client, and they recently (in 2017) added support for [lua scripting], so it ain't all bad.

A lot of people use neomutt with [notmuch].

## Colorschemes and Themes
It's [256-xterm colors] again. TUIs can just be like that sometimes :/
Check out an example colorscheme here: [neonwolf]
And then checkout the one I hacked together here: [spacechalk powerline]
It was hacked together in part from this: [neomutt powerline nerdfonts]

Here's [another pretty example neomutt example].

## Configuring NeoMutt with Protonmail

You'll need protonmail-bridge (which you can `brew install`).

Steps:
1. Launch protonmail-bridge
2. login with your protonmail account
3. copy the password it spits out

This will be your password that you can source in your `neomuttrc` which should be located in `~/.config/neomutt/neomuttrc`.

You can check out an [example neomuttrc file](https://github.com/jessebot/dot_files/blob/main/.config/neomutt/neomuttrc) if you'd like.

## Nesting virtual folders

[github: Nested virtual folders #1594](https://github.com/neomutt/neomutt/issues/1594)


## neomuttrc syntax examples from neomutt.org

neomutt.org has examples for most things and a lot of documentation generally,
but much of it isn't syntax highlighted, so I'm just posting this here for people who may need to quickly check something, but with syntax highlighting.

<details>
  <summary>Example neomuttrc configuration with syntax highlighting</summary>

```conf
  # Example NeoMutt config file for the status-color feature.

  # The 'status-color' feature allows you to theme different parts of
  # the status bar (also when it's used by the index).

  # For the examples below, set some defaults
  set status_format='-%r-NeoMutt: %f [Msgs:%?M?%M/?%m%?n? New:%n?%?o? Old:%o?%?d? Del:%d?%?F? \
  Flag:%F?%?t? Tag:%t?%?p? Post:%p?%?b? Inc:%b?%?l? %l?]---(%s/%S)-%>-(%P)---'
  set index_format='%4C %Z %{%b %d} %-15.15L (%?l?%4l&%4c?) %s'
  set use_threads=yes
  set sort=last-date-received
  set sort_aux=date

  # 'status color' can take up to 2 extra parameters
  # color status foreground background [ regex [ num ]]
  # 0 extra parameters
  # Set the default color for the entire status line
  color status blue white

  # 1 extra parameter
  # Set the color for a matching pattern
  # color status foreground background regex
  # Highlight New, Deleted, or Flagged emails
  color status brightred white '(New|Del|Flag):[0-9]+'

  # Highlight mailbox ordering if it's different from the default
  # First, highlight anything (*/*)
  color status brightred default '\([^)]+/[^)]+\)'

  # Then override the color for one specific case
  color status default default '\(threads/last-date-received\)'

  # 2 extra parameters
  # Set the color for the nth submatch of a pattern
  # color status foreground background regex num
  # Highlight the contents of the []s but not the [] themselves
  color status red default '\[([^]]+)\]' 1

  # The '1' refers to the first regex submatch, which is the inner
  # part in ()s
  # Highlight the mailbox
  color status brightwhite default 'NeoMutt: ([^ ]+)' 1
  # Search for 'NeoMutt: ' but only highlight what comes after it

  # vim: syntax=neomuttrc
```

</details>

Neomutt also has a [vim syntax repo](https://github.com/neomutt/syntax) that you could could use locally when editing neomuttrc files.

## Helpful links
- [Stephane: NeoMutt Cheatsheet](https://cheatsheets.stephane.plus/productivity/neomutt/)
- [reddit neomutt megathread](https://www.reddit.com/r/commandline/comments/fsm3sj/neomutt_config_megathread/)
- [Gideon Wolfe: Very good intro to Neomutt](https://gideonwolfe.com/posts/workflow/neomutt/intro/)
- [aliquote: Tips and tricks for Neomutt](https://aliquote.org/post/tipx-on-neomutt/)
- [Macro for opening text/html attachment](https://demu.red/blog/2017/11/neomutt-macro-opening-texthtml-attachment-from-the-index-view/)
- [notmuch docs on mutt](https://notmuchmail.org/notmuch-mutt/)
- [Gideon Wolfe: nextcloud and mutt](https://www.gideonwolfe.com/posts/sysadmin/nextcloud/nextcloudworkflow/#files) (goes over [khard] as well)
- [Brian Thompson: Setting up mutt client with protonmail](https://brian-thompson.medium.com/setting-up-the-mutt-mail-client-with-protonmail-49c042486b3) (goes over notably mbox and Maildir)

[256-xterm colors]: (https://www.ditig.com/256-colors-cheat-sheet)
[neonwolf]: https://gitlab.com/h3xx/mutt-colors-neonwolf
[spacechalk powerline]: https://github.com/jessebot/dot_files/blob/main/.config/neomutt/themes
[neomutt powerline nerdfonts]: https://github.com/sheoak/neomutt-powerline-nerdfonts
[lua scripting]: https://neomutt.org/2017/04/29/lua#algolia:p:nth-of-type(8)
[another pretty example neomutt example]: https://imgur.com/a/7yZbPrs
[notmuch]: https://notmuchmail.org/
[kard]: https://github.com/lucc/khard
