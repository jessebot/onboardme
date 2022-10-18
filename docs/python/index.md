---
layout: default
title: Python
description: "Python tips and tricks"
parent: Welcome
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

## Favorite packages
I really do love certain libraries for being really useful, and I made a table.
I do love a good table.

| library | Why it's great                                           |
| rich    | Colored and stylized/formatting of text for the terminal |
| pyyaml  | process easy yaml config files                           |
| pip     | package your software for others to use :)               |

## How to package your Python programs
Checkout [this guide by Scott Torborg](https://python-packaging.readthedocs.io/en/latest/).
A lot of things I learned and mention here are from reading that.

TLDR; your repo setup should be this:

```
# This is a tree of my repo for lsimg, a python program I wrote

├──  .gitignore
│
├──  bin
│   └──  lsimg
│
├──  config.yaml
│
├──  lsimg
│   └──  __init__.py
│
├──  MANIFEST.in
│
├──  README.md
│
└──  setup.py
```

### Important files

### `.gitignore`
For the python stuff you don't want in git, such as:

```gitignore
**/__pycache__/**
**/*.egg-info/**
```

### `bin/{COMMAND}`
The bin directory is where I keep my cli script that I want to end up in the
user's `$PATH`. As an example, the command my users run for lsimg is `lsimg`,
so I create a file called that which has something like:

```python
#!/usr/bin/env python3.10
import lsimg

lsimg.main()
```

### `__init__.py`
file that has your actual script.

#### `setup.py`

You need this for creating packages. Here's my basic `setup.py` for a package
 called `lsimg` that I wrote. You can see that the only function is the readme
 function, which adds the readme as the longer description for pypi usage.

Other things to note that many forget are `keywords` and `classifiers`, which
 help other users find your package.

```python
from setuptools import setup

def readme():
    """
    this adds the README.md file in this repo as the long description
    for the package
    """
    with open('README.md') as f:
        return f.read()

setup(name='lsimg',
      version='0.1.2',
      description='a cli tool written in python to ls images in a directory',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha'
          'Programming Language :: Python :: 3.10'
          'Topic :: Image Processing',
      ],
      keywords='lsimg img image ls',
      url='http://github.com/jessebot/lsimg',
      author='Jesse Hitch',
      author_email='jessebot@linux.com',
      license='GPL version 3 or later',
      packages=['lsimg'],
      install_requires=[
          'click',
          'PyYAML',
          'rich',
          'wget',
      ],
      scripts=['bin/lsimg'],
      include_package_data=True,
      zip_safe=False)
```

#### `MANIFEST.in` - For Including non-python files
This file lets you specify files that aren't python files for your package,
otherwise only files ending in `.py` will be included in your package. Here's
my default `MANIFEST.in` file:

```in
include README.md
include config.yaml
```

You don't have to include config.yaml. I just typically have a default config
file and it's always yaml.

### packaging command line scripts
Just make sure in your call to `setup()` in `setup.py` that you supply the
keyword argument `scripts=['bin/CLI_NAME']`, where `CLI_NAME` is the name of
the command you want users to run.
Then you structure your things like:

