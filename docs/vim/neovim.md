---
layout: default
title: neovim
parent: Vim
permalink: /neovim
description: "Neovim is vim, but with faster plugins and better syntax highlighting"
---

# neovim
[Neovim](https://neovim.io) is 

> a refactor, and sometimes redactor, in the tradition of Vim (which itself derives from Stevie). It is not a rewrite but a continuation and extension of Vim. Many clones and derivatives exist, some very clever—but none are Vim. Neovim is built for users who want the good parts of Vim, and more. 

It's supposed to be faster than vim at a lot of things, and there's more 
extensible plugins and active communities, it would seem anyway, from my casual
observation over the past year-ish (it's October 2022 at the time of writing).

To be honest, I've been using vim since 2012, and even though neovim has been
around since 2015, since I was using vi before vim, I never really gave it a
ton of thought. But recently there finally came a plugin that looked too good
not to try, but was only available for neovim, so I figured, at very least,
I should give it a go. I'll document anything interesting I learn here.

You can install neovim with: `brew install neovim`

You can run neovim with: `nvim`

## Config

The config file is located at:

|        OS          |                   Location                     |
|:-------------------|:-----------------------------------------------|
| Unix               | ~/.config/nvim/init.vim		(or init.lua)     |
| Windows            | ~/AppData/Local/nvim/init.vim	(or init.lua) |
| `$XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME`/nvim/init.vim	(or init.lua) |

And if you want to just get your vim stuff working, you want to these contents:

```vim
set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc
```

After that, launch neovim with `nvim` and then do your normal plugin manager flow.

(For instance: `:PlugInstall` for vim-plug users)

Most plugins will work out of the box, but you'll probably have issues with:

### Python / Python3 Plugins

If you run into a bunch of errors about vim not being compiled with python3,
then you probably need to first install `pynvim`, which helps with this:

```bash
python3.10 -m pip install --user --upgrade pynvim
```

After that, all my plugins worked find as they do in vim.

## Known issues

If you get an error complaining about `bash\ --login`, then it's probably
because of this line in your .vimrc:

```vim
" this works in vim, but not neovim
set shell=bash\ --login
```

Fix it by changing the above to:

```vim
" this ignores neovim when setting shell
if !has('nvim')
    set shell=bash\ --login
endif
```
