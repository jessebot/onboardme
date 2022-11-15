---
layout: default
title: Features
grand_parent: onboardme
parent: Getting Started
permalink: /onboardme/getting-started/features
---

# Features

## Shell Prompt
We use powerline which you can learn more about [here](/cli/powerline).

## Default dot files
Here's where I'm putting various aliases and tooling that get installed if you
use my [default dot files][0].

### Aliases and the commands they run
Here's some default aliases you get when you use the default `.bashrc`

| alias | command(s) the alias runs                   |
|-------|---------------------------------------------|
| `cat` | `rich` or `bat` (varies by file type)       |
| `gph` | `git push && git push --tags`               |
| `gs`  | `git status`                                |
| `gsa` | prints `git status` for every sub directory |
| `utc` | `date --utc`                                |

- `rich`: This adds syntax highlighting and line numbers. We use `rich --pager`,
  for files longer than your current terminal height.
- `bat`: (sometimes known as `batcat`) adds syntax highlighting, line numbers,
         and git diff features.

### CLI tools
Here's some of the cli tools we install.

TODO: fill this in, and make sure it doesn't conflict with other areas of the docs.

### Vim
We use vim with these plugins you can learn more about [here](/vim).

### Neovim
We use neovim alongside vim with these plugins you can learn more about [here](/neovim).

[0]: https://github.com/jessebot/dot_files "default dot files"
