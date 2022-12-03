---
layout: default
title: Python
description: "Python tips and tricks"
has_children: true
permalink: /python
---

# Python
It was inevitable I'd write a python section. I've been using python since
maybe 2012 or 2013?... and I've never been writing things down. Instead, I just
rely on ripping out some library I've writen somewhere else and making it work
in a new location. Recently I decided I should break that habit, because it is
terrible, and it is not hard to release things on PyPi, probably. I also do a
lot of contracting, and it would be great to just write some open source
software and allow others to use it where ever they want, instead of rewriting
the same few libraries for companies over and over again.

With that in mind, below you'll find all sorts of random things I told myself
I should tell others about as well.

[new in python3.11](https://12ft.io/proxy?q=https%3A%2F%2Frealpython.com%2Fpython311-new-features%2F)

## Favorite packages
I really do love certain libraries for being really useful, and I made a table.
I do love a good table.

| library | Why it's great                                               |
|:-------:|:-------------------------------------------------------------|
| rich    | Colored and stylized/formatting of text for the terminal     |
| pyyaml  | process easy yaml config files                               |
| wget    | consistently just download a file without bells and whistles |

## Linters forever
Honestly... flake8 is still the most consistent but ruff is fastest. Here's a bunch:
- pycodestyle
- pydocstyle
- flake8
- pyflakes
- ruff

## Key-Value Store
[TIL—Python has a built-in persistent key-value store](https://remusao.github.io/posts/python-dbm-module.html).

## Notebooks
Jupyter notebooks are web based program to interactively demo/test code.
I stopped using them a long time ago, but recently I saw `nbterm` announced,
which is basically a [TUI Notebook](https://blog.jupyter.org/nbterm-jupyter-notebooks-in-the-terminal-6a2b55d08b70).

## What is everyone else doing tho?
Jetbrains and the Python org regularly survey their user base and then publish
an [open report of the survey results.](https://lp.jetbrains.com/python-developers-survey-2021/)
