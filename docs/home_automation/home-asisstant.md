---
layout: default
parent: Home Automation
title: Home Assistant
description: Various things I've learned about home assistant
permalink: /home-automation/home-assistant
---

If you want to try out home asisstant quickly, a docker image is probably the best bet. Here's how I tested things:

```bash
# first, run the image, which will be pulled automatically when you run it
# Set the -e TZ=Europe/Amsterdam to YOUR time zone.
docker run -d \
           --name homeassistant \
           --privileged \
           --restart=unless-stopped \
           -e TZ=Europe/Amsterdam \
           -v ~/repos/home_asistant:/config \
           --network=host \
           ghcr.io/home-assistant/home-assistant:stable
```

In your directory you set for your volume, in my case `~/repos/home_asistant` because I can't spell, you'll find the following, which you can use to spin up home asisstant again easily somewhere else:

```
$ ls -lA
drwxr-xr-x root   root      4096  Mon Sep 12 19:32:04 2022 .cloud
.rw-r--r-- root   root         8  Mon Sep 12 19:32:04 2022 .HA_VERSION
drwxr-xr-x root   root      4096  Thu Sep 15 10:13:00 2022 .storage
.rw-r--r-- root   root         2  Mon Sep 12 19:32:04 2022 automations.yaml
drwxr-xr-x root   root      4096  Mon Sep 12 19:32:04 2022 blueprints
.rw-r--r-- root   root       220  Mon Sep 12 19:32:04 2022 configuration.yaml
drwxr-xr-x root   root      4096  Mon Sep 12 19:32:04 2022 deps
.rw-r--r-- root   root      3194  Tue Sep 13 06:47:57 2022 home-assistant.log
.rw-r--r-- root   root         0  Mon Sep 12 19:32:04 2022 home-assistant.log.
.rw-r--r-- root   root   2146304  Thu Sep 15 10:13:00 2022 home-assistant_v2.d
.rw-r--r-- root   root         0  Mon Sep 12 19:32:04 2022 scenes.yaml
.rw-r--r-- root   root         0  Mon Sep 12 19:32:04 2022 scripts.yaml
.rw-r--r-- root   root       161  Mon Sep 12 19:32:04 2022 secrets.yaml
drwxr-xr-x root   root      4096  Mon Sep 12 19:32:04 2022 tts
```
