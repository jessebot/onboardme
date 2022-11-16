---
layout: default
title: Contributing
parent: onboardme
permalink: /onboardme/contributing
---

# Status
Currently in later alpha :3 Testing actively on macOS Monterey 13.0.1, and Debian 12 (Bookworm). Please report 🐛 in the GitHub issues, and we will get them as we have time. You can also just open a pull request, and we're happy to take a look and probably merge it.

## Development
If you're not familiar with python packaging, go read some of my docs and further reading links [here](/onboardme/python/packaging).

There's no automated tests yet, but it's on the list of things to do. In the meantime, please just test the script works on both the latest version of Debian desktop and macOS (doesn't matter the architechture). I'll write some basic tests and put them in github actions soonish.

In the meantime, you should at least be making sure that you can run this in the repo root dir:

```bash
# build a package: a python wheel
poetry build

# install the current package and dependencies
poetry install

# loads a virtual enviornment with the installed package
poetry shell
onboardme --help
```
