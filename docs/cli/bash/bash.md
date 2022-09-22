---
layout: default
parent: Command Line Interface
title: BASH
has_children: true
permalink: /cli/bash
---

## BASH notes

### `which` not working to find program
If you do a `which` and the program isn't in your path, but it shows as installed, try this. Example with `iptables`:
```bash
whereis iptables
```

### Simple Prompt that tells you if the last command failed or not

This prompt one is only if emojis already work in your terminal :3 so make sure you can enable utf-8 for your terminal first:

```bash
PS1="\`if [ \$? = 0 ]; then echo 💙; else echo 😔; fi\` \[\e[94m\][\@]\[\e[0m\]\\$ "
```

Use this one if you don't have emojis in your terminal
```bash
# prompt will show ^_^ on successful commands or O_O on failures, then user, then time
PS1="\`if [ \$? = 0 ]; then echo \[\e[32m\]^_^\[\e[0m\]; else echo \[\e[31m\]O_O\[\e[0m\]; fi\`[\u.\@]\\$ "
```
