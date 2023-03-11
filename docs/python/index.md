---
layout: default
title: Python
description: "Python tips and tricks"
has_children: true
permalink: /python
---

# Python
It was inevitable I'd write a python section. I've been using python since
maybe 2012 or 2013?... and I never wrote things down. Instead, I just
relied on ripping out some library I'd written somewhere else and made it work
in a new location. Recently, I decided I should break that habit, because it is
terrible, and it is not hard to release things on PyPi. I also do a
lot of contracting, and it would be great to just write some open source
software and allow others to use it where ever they want, instead of rewriting
the same few libraries for companies over and over again.

With that in mind, below you'll find all sorts of random things I told myself
I should tell others about as well.

[new in python3.11](https://12ft.io/proxy?q=https%3A%2F%2Frealpython.com%2Fpython311-new-features%2F)

## Packages
### Favorite packages
I really do love certain libraries for being really useful, and I made a table.
I do love a good table.

|  module  | Why it's great                                                                                        |
|:--------:|:------------------------------------------------------------------------------------------------------|
|  [rich]  | Colored and stylized/formatting of text for the terminal                                              |
| [pyyaml] | process easy yaml config files                                                                        |
|  [wget]  | consistently just download a file without bells and whistles                                          |
|   [xdg]  | Grab the user's configured `XDG` env vars or use defaults for things such as caching and config files |

### Installing Packages and Managing Environments

#### pip
pip is a package installer

#### pipx
[pipx] allows you to Install and Run Python Applications in Isolated Environments.

> pip is a general-purpose package installer for both libraries and apps with no environment isolation. pipx is made specifically for application installation, as it adds isolation yet still makes the apps available in your shell: pipx creates an isolated environment for each application and its associated packages.

> pipx does not ship with pip, but installing it is often an important part of bootstrapping your system.

#### conda
conda is a data science focused package installer that installs into managed environments.

#### poetry
poetry is a package installer.

## Linters forever
Honestly... flake8 is still the most consistent but ruff is fastest. Here's a bunch:
- pycodestyle
- pydocstyle
- flake8
- pyflakes
- ruff
- autoimport

## Key-Value Store
[Python has a built-in persistent key-value store](https://remusao.github.io/posts/python-dbm-module.html).

## Notebooks
Jupyter notebooks are web based program to interactively demo/test code. There's more info over on our [notebook page](/python/notebook)


## What is everyone else doing tho?
Jetbrains and the Python org regularly survey their user base and then publish
an [open report of the survey results.](https://lp.jetbrains.com/python-developers-survey-2021/)


[pipx]: https://pypa.github.io/pipx/
[rich]: https://github.com/Textualize/rich
[pyyaml]: https://github.com/yaml/pyyaml
[wget]: https://pypi.org/project/wget/
[xdg]: https://pypi.org/project/xdg/
