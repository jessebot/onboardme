---
layout: default
title: Email
has_children: true
permalink: /email
description: "Everything to do with emailing people, and also getting emails, and looking at them, and their attachments."
---

# Email

This is to document how to email people. I know that sounds easy, but have you
ever tried to a) recieve email, and b) email people without gmail, outlook,
or thunderbird? Have you ever tried to email people from your terminal using
your preferrd IDE?

Well... it gets complicated...

Here's where I put all the little things that make using your terminal as an
email client a nice experience.

## msmtp
This serves as a bookmark, because I read about this somewhere:
[msmtp](https://marlam.de/msmtp/)


## BASH variables for email
I was reading the `bash` man page recently, looking for something else entirely,
and I found this section below. I think it might be helpful down the line for
getting specific notifications for mail. Might be something cool to integrate
with powerline too.

```bash
MAIL   If this parameter is set to a file or directory name and the MAILPATH variable is not set, bash informs the user of the
       arrival of mail in the specified file or Maildir-format directory.
MAILCHECK
       Specifies how often (in seconds) bash checks for mail.  The default is 60 seconds.  When it is time to check for mail,
       the shell does so before displaying the primary prompt.  If this variable is unset, or set to a value that is not a
       number greater than or equal to zero, the shell disables mail checking.
MAILPATH
       A colon-separated list of filenames to be checked for mail.  The message to be printed when mail arrives in a
       particular file may be specified by separating the filename from the message with a `?'.  When used in the text of the
       message, $_ expands to the name of the current mailfile.  Example:
       MAILPATH='/var/mail/bfox?"You have mail":~/shell-mail?"$_ has mail!"'
       Bash can be configured to supply a default value for this variable (there is no value by default), but the location of
              the user mail files that it uses is system dependent (e.g., /var/mail/$USER).
```
