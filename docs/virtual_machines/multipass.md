---
layout: default
title: Multipass
parent: Virtual Machines
permalink: /docs/vm/multipass
---

## Multipass
*note: multipass ended up giving me problems, so I just kept on truckin with KIND for right now.*

```bash
# launches a vm with 2 vCPU, 32G disk, name of node: k8s-worker-1, Ubuntu Image verion 20.04
multipass launch -c 2 -d 32G -m 2G -n k8s-wkr-1 20.04
multipass launch -c 2 -d 32G -m 2G -n k8s-wkr-2 20.04

# I just don't wanna call it a master
multipass launch -c 2 -d 32G -m 2G -n k8s-manager-1 20.04

# to access a multipass instance if you need to
multipass shell k8s-worker-1
```
