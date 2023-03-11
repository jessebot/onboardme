---
layout: default
title: Packaging
description: "Python packaging tips and tricks"
parent: Python
has_children: true
permalink: /python/packaging
---

# How to package your Python programs

# setup.py
This method is largely deprecated, but you can read about it [here](https://jessebot.github.io/onboardme/python/packaging/setuppy).

# pyproject.toml
I have only just begun to do [this](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/), which is sad, because apparently this
[became a standard](https://peps.python.org/pep-0518/) back in 2016 🤦

Helpful reading:
- [Brett Cannon: What the heck is pyproject.toml?](https://snarky.ca/what-the-heck-is-pyproject-toml/)
- [Stackoverflow: What is pyproject.toml file for?](https://stackoverflow.com/questions/62983756/what-is-pyproject-toml-file-for)

TLDR; basically the dict you passed into setuptools to specify everything from required python version to cli tooling, is now a prettier [toml](https://github.com/toml-lang/toml/blob/main/README.md#toml) file. That toml file is then used by not just pip, but other tooling like poetry (poetry seems to be the most popular tool).

Also, I like this weird duck thing:
[![Purple Packaging Platypus](https://monotreme.club/img/sticker.png)](https://monotreme.club/#/)

### Poetry
Poetry is
> a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

Poetry's [basic guide](https://python-poetry.org/docs/basic-usage/) is actually pretty good.

Here's some basics about poetry.
```bash
# init a poetry project in a directory with a project already - interactive
poetry init

# installs your current project, and dependencies, in a virtual env
poetry install

# sources your python virtual env for you to test your package
poetry shell

# builds the project for publishing
poetry build

# publish to pypi, $PYPI_TOKEN must be exported as your current pypi api token
poetry publish --username __token__ --password $PYPI_TOKEN
```

Here's a github action that does it for you: [JRubics/poetry-publish][3]

## What about brew?
Well, that's a rabbit hole that I haven't had a chance to go down yet, but you
probably want to start here:
- [Adding Software To Homebrew](https://docs.brew.sh/Adding-Software-to-Homebrew#formulae)
- [https://docs.brew.sh/Formula-Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [https://docs.brew.sh/Python-for-Formula-Authors](https://docs.brew.sh/Python-for-Formula-Authors)

[0]: https://jessebot.github.io/onboardme/python/packaging/setuppy "setuppy"
[1]: https://peps.python.org/pep-0517/ "pep-0517"
[2]: https://stackoverflow.com/questions/62983756/what-is-pyproject-toml-file-for "What is pyproject.toml file for"
[3]: https://github.com/JRubics/poetry-publish "poetry-publish"
