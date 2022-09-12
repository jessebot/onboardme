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
