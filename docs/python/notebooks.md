---
layout: default
title: Notebooks
parent: Python
has_children: false
permalink: /python/notebooks
description: "Tips and tricks for python notebooks"
---

# Notebooks

## Setup Notebooks
Before you get started, if you're on Linux, you might need to install gcc, the version I installed was gcc-11.

Next you need the [ipykernel]:

```bash
pip3.11 install ipykernel
```

Finally you need notebooks. There's a couple of different ways to get and interact with notebooks.

```bash
# will get you classic notebooks, lighter weight
pip3.11 install notebook

# for rendering as a web app
pip3.11 install voila

# jupyter's current full IDE-esk offering
pip3.11 install jupyterlab
```

### Notebooks in the terminal
There's no way I wouldn't talk about getting this done in a terminal. First, there's [euporie]

```bash
pip3.11 install euporie
```

There's also [nbterm] if you'd like to check it out.


## Running a notebook

### Jupyter classic notebook

```bash
# with classic notebooks
jupyter notebook
```

### "The Lab"

```bash
# this launches a whole lab :-)
jupyter-lab
```

### Euporie

```bash
# Running a notebook in the terminal :)
euporie notebook
```

## Modifying a notebook

You can just open a notebook using one of the programs listed above, modify it, and then save it.

## Checking a notebook into git

Overstory has [a blog post] on [nbdev] which is pretty cool. To sum it up, nbdev helps create a good git repo structure, and has some tooling to ensure you don't check in weird metadata, as well as help you resolve merge issues arising from having notebooks checked in.


[a blog post]: https://www.overstory.com/blog/how-nbdev-helps-us-structure-our-data-science-workflow-in-jupyter-notebooks "overstory how nbdev helps us..."
[nbdev]: https://nbdev.fast.ai/ "nbdev"
[nbterm]: https://blog.jupyter.org/nbterm-jupyter-notebooks-in-the-terminal-6a2b55d08b70
[euporie]: https://github.com/joouha/euporie
