---
layout: default
title: Features
parent: onboardme
permalink: /onboardme/features
---

# Features

## Package Management
Using a `~/.config/onboardme/packages.yaml`, you can manage what packages get
installed with which package managers, and what commands, if any,
are run to upgrade them. We install a [default packages.yaml], if you don't
create this file.

## Dot file Management
We can use any dot file URL repo you'd like to clone, along with what branch
you'd like to clone. We'll then keep those dot files up to date everytime
`onboardme` runs. If you don't specify a set of dot files, we'll try to install
some dot files anyway, but we won't overwrite anything you have locally.

<details>
  <summary>Check out more information about the defaults that installed here</summary>

  ### Default dot files
  Here's where I'm putting various aliases and tooling that get installed if you
  use my [default dot files].

  #### Shell Prompt
  We use powerline which you can learn more about [here](/cli/powerline).


  #### Aliases and the commands they run
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

  #### CLI tools
  Here's some of the cli tools we install.

  TODO: fill this in, and make sure it doesn't conflict with other areas of the docs.

  #### Neovim
  We use neovim with these plugins you can learn more about [here](/neovim).

</details>

[default dot files]: https://github.com/jessebot/dot_files "default dot files"
[default packages.yaml]: https://github.com/jessebot/onboardme/blob/main/onboardme/config/packages.yaml "default packages.yaml"
