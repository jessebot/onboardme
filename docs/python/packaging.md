---
layout: default
title: Packaging
description: "Python packaging tips and tricks"
parent: Python
has_children: true
permalink: /python/packaging
---

# How to package your Python programs

## setup.py
This method is largely being deprecated, but you can read about it [here][0].

## myproject.toml
I have only just begun to do this, which is sad, because apparently this
became [a standard][1] back in 2016 :facepalm:

This stackoverflow question was helpful to get started though:
[What is pyproject.toml file for?][2]

### Poetry

Here's some basics about poetry.
```bash
# init a poetry project in a directory with a project already - interactive
poetry init

# builds the project for publishing
poetry build

# publish to pypi
poetry publish
```

## What about brew?
Well, that's a rabbit hole that I haven't had a chance to go down yet, but you
probably want to start here:
- [Adding Software To Homebrew](https://docs.brew.sh/Adding-Software-to-Homebrew#formulae)
- [https://docs.brew.sh/Formula-Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [https://docs.brew.sh/Python-for-Formula-Authors](https://docs.brew.sh/Python-for-Formula-Authors)

[0]: https://jessebot.github.io/onboardme/python/packaging/setuppy "setuppy"
[1]: https://peps.python.org/pep-0517/ "pep-0517"
[2]: https://stackoverflow.com/questions/62983756/what-is-pyproject-toml-file-for "What is pyproject.toml file for"
