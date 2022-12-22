---
layout: default
title: Notebooks
parent: Python
has_children: false
permalink: /python/notebooks
description: "Tips and tricks for python notebooks"
---

# Setup
Before you get started, if you're on Linux, you might need to install gcc, the version I installed was gcc-11.

Next you need the ipykernel:

```bash
pip3.11 install ipykernel
```

Finally you need notebooks. There's a couple of different ways to get and interact with notebooks.

```bash
# this will get you classic notebooks
pip3.11 install notebook

# this is jupyter's current offering
pip3.11 install jupyterlab

# this is for rendering as a web app
pip3.11 install voila
```

## Notebooks in the terminal
There's no way I wouldn't talk about getting this done in a terminal.

```bash
pip3.11 install euporie
```

# Running a notebook

```
# this is with classic notebooks
jupyter notebook

# this launches a whole lab :-)
jupyter-lab
```

# Modifying a notebook


# Checking a notebook into git
