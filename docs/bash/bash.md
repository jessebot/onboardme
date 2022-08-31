---
layout: default
title: BASH
has_children: true
permalink: /docs/bash
---

## Random collection of stuff I forget all the time

### `which` not working to find program
If you do a `which` and the program isn't in your path, but it shows as installed, try this. Example with `iptables`:
```bash
whereis iptables
```
