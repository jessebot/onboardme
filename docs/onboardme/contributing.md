---
layout: default
title: Contributing 
parent: onboardme
permalink: /onboardme/contributing
---

# Status
Currently in beta :3 Testing actively on macOS Monterey 12.6, and Debian 11 (Bullseye). Please report 🐛 in the GitHub issues, and I will get them as I have time. You can also just open a pull request, and I'm happy to take a look and probably merge it.

## Development
If you're not familiar with python packaging, go read some of my docs and further reading links [here](/onboardme/python/packaging).

There's no automated tests yet, but it's on the list of things to do. In the meantime, please just test the script works on both the latest version of Debian desktop and macOS (doesn't matter the architechture). I'll write some basic tests and put them in github actions soonish.

In the meantime, you should at least be making sure that you can run this in the repo root dir:

```python
pip3.10 install -e .
onboardme --help
```

That should install onboardme locally and run the help to make sure it works. Then, you can actually build the thing:

```python
python3.10 -m build --wheel

# this makes sure nothing is broken
twine check dist/*
```

## Current Contributors
- [@cloudymax]()

### Special Thanks
Thank you to [@cloudymax]() for all their direct contributions for gaming on Linux, virtualization, rc file edits, and the hyper terminal configs. Also great engineer to rubberduck with generally. Couldn't have polished a lot of this without their patience during my late night ramblings about my 8 different package managers and why utf-8 isn't called utf-14 :3 :blue_heart:
