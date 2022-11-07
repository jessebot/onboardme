---
layout: default
title: neovim
parent: IDE
has_children: true
permalink: /neovim
description: "Neovim is vim, but with faster plugins and better syntax highlighting"
---

# neovim
[Neovim](https://neovim.io) is

> a refactor, and sometimes redactor, in the tradition of Vim (which itself derives from Stevie). It is not a rewrite but a continuation and extension of Vim. Many clones and derivatives exist, some very clever—but none are Vim. Neovim is built for users who want the good parts of Vim, and more.

It's supposed to be faster than vim at a lot of things, and there's more
extensible plugins and active communities, it would seem anyway, from my casual
observation over the past year-ish (it's October 2022 at the time of writing).

To be honest, I've been using vim since 2011, and even though neovim has been
around since 2015, since I was using vi before vim, I never really gave it a
ton of thought. But recently there finally came
[a plugin](https://github.com/numirias/semshi#readme) that looked too good
not to try, but was only available for neovim, so I figured, at very least,
I should give it a go. I'll document anything interesting I learn here.

# Getting Started with Neovim

You can install neovim with: `brew install neovim`

You can run neovim with: `nvim`

## Config

The config file is located at:

|        OS          |                   Location                     |
|:-------------------|:-----------------------------------------------|
| Unix               | ~/.config/nvim/init.vim		(or init.lua)     |
| Windows            | ~/AppData/Local/nvim/init.vim	(or init.lua) |
| `$XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME`/nvim/init.vim	(or init.lua) |

And if you want to just get your vim stuff working, you want to these contents
in your `~/.config/nvim/init.vim`:

```vim
set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc
```

After that, launch neovim with `nvim` and then do your normal plugin manager flow.

## Plugins

Most plugins will work out of the box, but you'll probably have issues with
Python plugins. You can learn more about those and other things to do with vim-plug
and packer [here](https://jessebot.github.io/onboardme/neovim/plugins).

## Known issues between vim and neovim

If you get an error complaining about `bash\ --login`, then it's probably
because of this line in your `.vimrc`:

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

## init.lua
This file should be located in `~/.config/nvim/init.lua`, but you'll have to
create it. When you're in lua land, vim-plug becomes more difficult in weird ways
and the alternative does require a bit of a conversion, but it's worth it, I think,
because a lot of the latest trendy plugins are written in lua anyway, and you can
still source vimscript files.

### Converting an `init.vim`/`.vimrc` to an `init.lua`

#### setting variables

To start converting, you can fist grab all your variables, for instance:

```vim
" enable line number column
set number = true
```

and put them directory into your `init.lua` file. Then run an interactive sed
to update them to lua's vim interface like this, `:%s/set number /vim.opt./`,
which should then give you this:

```lua
-- enable line number column
vim.opt.number = true
```

#### Remapping a key

Here's an example in my `.vimrc`:

```vim
" let spacebar allow me to fold the code
nnoremap <space> za
```

And here's what that translated to in my `init.lua`:

```lua
-- let spacebar allow me to fold the code
-- in vimscript, this was: nnoremap <space> za
vim.keymap.set('n', '<space>', 'za')
```

#### vim commands
Sometimes you have a command that doesn't have a vim lua interface, or maybe you
just can't find it. There's a `vim.cmd` you can call instead. Example:

I have my colorscheme set to [spacechalk](https://github.com/jessebot/space-chalk) in my `.vimrc` like this:

```vim
colorscheme spacechalk
```

The eqivelent in my `init.lua` is this:

```lua
vim.cmd [[colorscheme spacechalk]]
```

# Helpful links
[Floating windows in neovim](http://www.statox.fr/posts/2021/03/breaking_habits_floating_window/)
