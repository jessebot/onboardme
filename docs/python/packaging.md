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
├──  config.yaml
│
├──  onboardme
│   └──  __init__.py
│
├──  MANIFEST.in
│
├──  README.md
│
├──  setup.cfg
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
File that has your actual script.

### `setup.cfg`
toml file for you to define various data about your project, but this is
where I put the license info. additional license info.

```toml
[metadata]
# This includes the license file(s) in the wheel.
# https://wheel.readthedocs.io/en/stable/user_guide.html#including-license-files-in-the-generated-wheel-file
license_files = LICENSE.txt
```

### `setup.py`

You need this for creating packages. Here's my basic `setup.py` for a package
 called `onboardme` that I wrote. You can see that the only function is the readme
 function, which adds the readme as the longer description for pypi usage.

Other things to note that many forget are `keywords` and `classifiers`, which
 help other users find your package.

```python
def readme():
    """
    grab and return contents of README.md for use in long description
    """
    with open('README.md') as f:
        return f.read()


lic_class = ('License :: OSI Approved :: GNU Affero General Public License v3'
             'or later (AGPLv3+)')

setup(name='onboardme',
      description='An onboarding tool to install dot files and packages',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3.10',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX :: Linux',
                   'Intended Audience :: End Users/Desktop',
                   'TOPIC :: SYSTEM :: INSTALLATION/SETUP',
                   lic_class],
      python_requires='>3.10',
      keywords='onboardme, onboarding, desktop-setup, setuptools, development',
      version='0.13.7',
      project_urls={
          'Documentation': 'https://jessebot.github.io/onboardme/onboardme',
          'Source': 'http://github.com/jessebot/onboardme',
          'Tracker': 'http://github.com/jessebot/onboardme/issues'},
      author='jessebot',
      author_email='jessebot@linux.com',
      license='GPL version 3 or later',
      packages=['onboardme'],
      install_requires=['wget', 'GitPython', 'PyYAML', 'rich', 'click'],
      data_files=[('config', ['config/config.yml',
                              'config/packages.yml',
                              'config/brew/Brewfile_Darwin',
                              'config/brew/Brewfile_Linux',
                              'config/brew/Brewfile_devops'])],
      entry_points={'console_scripts': ['onboardme = onboardme:main']},
      include_package_data=True,
      zip_safe=False)
```

### `MANIFEST.in` - For Including non-python files
This file lets you specify files that aren't python files for your package,
otherwise only files ending in `.py` will be included in your package. Here's
my default `MANIFEST.in` file:

```in
include README.md
include LICENSE.txt
```

You don't have to include config.yaml. I just typically have a default config
file and it's always yaml.


## packaging command line scripts

That's where this bit from the above `setup.py` comes in:

```python
entry_points={'console_scripts': ['onboardme = onboardme:main']},
```

It translates to: Create a command called `onboardme` that calls the `main`
function of the `onboardme` package.


# Other helpful guides

- This is probably the most official guide, and where you should start:
  [packaging.python.org/.../packaging-your-project](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#packaging-your-project)

- Checkout [this guide by Scott Torborg](https://python-packaging.readthedocs.io/en/latest/). 
  A lot of things I learned and mention here are from reading that.

- I also read [this pypa guide](https://github.com/pypa/sampleproject) recently
  and it has comments in each file to explain what's going on.
