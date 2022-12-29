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

## isync (AKA `mbsync`)
[isync] is a small set of cli tools to sync your mail. The mail commandline tool
is called `mbsync`. I assume `i` in isync stood for internet, and in 2002, that
made a bit more sense, before `i` things became synonymous with Apple things.
`mb` stands for mailbox though, so we'll refer to it as `mbsync` everywhere.

Before we do anything with tagging or reading our mail, we need to have emails
synced from the remote server (gmail, protonmail, your own mail server,
wherever really), to your computer. Enter `mbsync`. First, get it installed:

```bash
# this will work on both linux and macOS
brew install isync
```

Next we need to configure it. Create a new file called `~/.mbsyncrc` (we'll get it XDG compliant later):

```config

```

## NotMuch
[NotMuch] is an email indexer and tagging system. We'll use it to index our mail,
becuase neomutt is slow and bad at this part.

## NeoMutt
[Neomutt] is an email client TUI (terminal user interface) for viewing and
sending email.


## References
It is surprisingly hard to find docs on protonmail via a TUI... so thank you very much to all the authors of these posts below!

- [Arch Wiki: Isync](https://wiki.archlinux.org/title/Isync)
- []()


[isync]: https://isync.sourceforge.io/mbsync.html "isync AKA mbsync"
[protonmail bridge]: https://proton.me/mail/bridge "ProtonMail Bridge"
[neomutt]: https://neomutt.org/ "NeoMutt"
