---
layout: default
title: Packaging
description: "Python tips and tricks"
parent: Python
has_children: true
permalink: /python/packaging
---

# How to package your Python programs
TLDR; your repo setup should be this:

```sh
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

## Important files

## `.gitignore`
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

### `setup.py`

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

### `MANIFEST.in` - For Including non-python files
This file lets you specify files that aren't python files for your package,
otherwise only files ending in `.py` will be included in your package. Here's
my default `MANIFEST.in` file:

```in
include README.md
include config.yaml
```

You don't have to include config.yaml. I just typically have a default config
file and it's always yaml.

## packaging command line scripts
Just make sure in your call to `setup()` in `setup.py` that you supply the
keyword argument `scripts=['bin/CLI_NAME']`, where `CLI_NAME` is the name of
the command you want users to run.
Then you structure your things like:


# Other helpful guides

Checkout [this guide by Scott Torborg](https://python-packaging.readthedocs.io/en/latest/). 
A lot of things I learned and mention here are from reading that.

I also read [this pypa guide](https://github.com/pypa/sampleproject) recently
and it has comments in each file to explain what's going on.
