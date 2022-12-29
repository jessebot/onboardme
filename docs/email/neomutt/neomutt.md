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


<details>
  <summary>Example <code>neomuttrc</code> working with protonmail</summary>

```config
# A first attempt at using neomutt as a primary desktop email client

# ----------------------- general -------------------------------
# bell on new mails - even though I normally hate bells
set beep_new

# -------------------------- Themeing ---------------------------
# basic space_chalk color scheme
source ~/.config/neomutt/themes/spacechalk/neomutt_spacechalk_colors.muttrc

# powerline for status lines and pager lines
source ~/.config/neomutt/themes/spacechalk/powerline.neomuttrc

# ------------------------- Temp files ---------------------------
set certificate_file=~/.local/state/neomutt/certificates


# ------------- index settings, your list of emails -------------
#
# No help bar at the top of index
unset help

# sort the inbox by newest first
set sort = reverse-threads


# ----------------- viewing email attachments -------------------

# handing MIME types (html, pdf, jpg, gif, etc)
set mailcap_path = ~/.config/neomutt/mailcap

# view other kinds of plain(ish) text before html
alternative_order text/plain text/enriched text/html text/*

# set   - will always ask for a key after an external command
# unset - wait for key only if the external command returned a non-zero status
unset wait_key


# --------- composing email: new messages, replies, and forwards -------------
# use neovim by default
set editor = "nvim"

# show headers when composing
set edit_headers

# format of subject when forwarding
set forward_format = "Fwd: %s"

# reply to Reply to: field
set reply_to

# reply to person's name
set reverse_name

# include message in replies
set include

# include message in forwards
set forward_quote

# signature, this gets appended to your emails, you have to create this file
set signature= "~/.config/neomutt/signature"

# Character set on sent messages:
set send_charset = "utf-8"

# If there is no charset given on incoming msg, its probably windows:
# set assumed_charset = "iso-8859-1"

# ----------------- Email address, Password, and Name ---------------------
# sources secret variables from a file that looks like (without comments):
# $my_name="Your Name"
# $my_user="You@yourprovider.tld"
## if protonmail, $my_pass should be the password from protonmail-bridge
# $my_pass="Your Password"
source ~/.config/neomutt/keys

# --------------------- Key binding and remapping ---------------------------
# In it's own file for organization sake
source ~/.config/neomutt/key_bindings.neomuttrc

# --------------------------- IMAP settings --------------------------- #
# recieving mail
# Local protonmail-bridge host server: 127.0.0.1
# Protonmail-bridge imap port: 1143
# --------------------------------------------------------------------- #
set imap_user = $my_user
set imap_pass = $my_pass

# ("+" substitutes for `folder`)
set mbox_type     = Maildir
set folder        = imap://127.0.0.1:1143/
set record        = +Sent
set postponed     = +Drafts
# Specify where to save and/or look for postponed messages.
# set postponed = +[Protonmail]/Drafts
set trash         = +Trash
set spoolfile     = +INBOX
mailboxes         = +INBOX +Drafts +Sent +Trash

# ----------------------------- Caching ---------------------------------
# Store message headers locally to speed things up. If header_cache is a folder,
# Mutt will create sub cache folders for each account which speeds things up more
# -----------------------------------------------------------------------
# CREATE THIS FOLDER. REMOVE IT IF IT IS A FILE AND CREATE AS FOLDER
set header_cache = ~/.local/state/neomutt

# --------------------------- Caching 2 ---------------------------------
# Store mail locally to speed things up, like searching message bodies. Can be
# same folder as header_cache. Costs disk space if you have a lot of email
# -----------------------------------------------------------------------
# I'm using this folder because it's more XDG spec
set message_cachedir = ~/.local/state/neomutt

# Allow Mutt to open a new IMAP connection automatically.
unset imap_passive

# Keep the IMAP connection alive by polling intermittently (time in seconds)
# this is 5 minutes
set imap_keepalive = 300

# How often to check for new mail (time in seconds).
# this is six minutes
set mail_check = 360

# ------------ SMTP (Simple Mail Transfer Protocol) settings ----------
# sending mail
# Local protonmail-bridge host server: 127.0.0.1
# Protonmail-bridge smtp port: 1025
# ---------------------------------------------------------------------
set smtp_pass = $my_pass
set realname  = $my_name
set from      = $my_user
set use_from  = yes

set smtp_url = smtp://$my_user:$smtp_pass@127.0.0.1:1025

# ----------------------- security :shrug: ----------------------------
set ssl_force_tls = yes
set ssl_starttls = yes
# When set , postponed messages that are marked for encryption will be self-encrypted. NeoMutt will first try to encrypt using the value specified in $pgp_default_key or $smime_default_key. If those are not set, it will try the deprecated $postpone_encrypt_as. (Crypto only) Default: no
# set postpone_encrypt = yes
```

</details>

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
