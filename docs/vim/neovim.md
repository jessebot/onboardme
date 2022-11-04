---
layout: default
title: neovim
parent: IDE
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

(For instance: `:PlugInstall` for vim-plug users)

Most plugins will work out of the box, but you'll probably have issues with
Python/Python3 plugins, but I documented those below.

### Source Plugins for vim/neovim in the same location
Having to install a package twice in two different locations is silly and makes
maintanence and updates more of a chore. Pick a location, and stick with it,
but to do this in vimscript with both an `init.vim` from neovim and a `.vimrc`
being sourced for regular vim, we get into slightly more complicated territory,
and kind of repetitive. The quick way I found was to have a section in your 
`.vimrc` like this:

```vim
" this means: don't run this part in if we're using neovim
if !has('nvim')

    call plug#begin()

    " put all your vim plugins here, but don't include anything that only works
    " in neovim (e.g. semshi)

    " example plugin that works in vim/neovim: This is helpful for markdown
    Plug 'junegunn/limelight.vim'

    call plug#end()

endif
```

and then in your `init.vim`, have something like this AFTER you source your 
`.vimrc`, so that vim-plug knows where to source your plugin exactly:

```vim
source ~/.vimrc

call plug#begin()
" put all your vim plugins here, but don't include anything that only works
" in neovim (e.g. semshi)

" example plugin that works in vim/neovim: This is helpful for markdown
Plug 'junegunn/limelight.vim', {'dir': '~/.vim/plugged/limelight.vim'}

" Example plugin that only works in neovim: this is helpful for python highlighting
Plug 'numirias/semshi', { 'do': ':UpdateRemotePlugins' }

call plug#end()
```

### Python / Python3 Plugins

If you run into a bunch of errors about vim not being compiled with python3,
then you probably need to first install `pynvim`, which helps with this:

```bash
python3.10 -m pip install --user --upgrade pynvim
```

After that, all my plugins worked find as they do in vim.

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
set number = true
```

and put them directory into your `init.lua` file. Then run an interactive sed
to update them to lua's vim interface like this, `:%s/set number /vim.opt./`,
which should then give you this:

```lua
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

### writing little lua scripts

If you want to say, take this block from your `.vimrc`:

```vim
"                              FOLDING ZONE:
"                 "collapse an entire block or function"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Enable folding on base indent
set foldmethod=indent
set foldlevel=99
" let spacebar allow me to fold the code
nnoremap <space> za
" also allow me to see the doc strings
let g:SimpylFold_docstring_preview=1
" enable folding for markdown?
let g:markdown_folding = 1
let g:indentLine_fileTypeExclude = ['dashboard']
```

and move it to your lua config for neovim, you may not want it cluttering your
`init.lua`, because it will be difficult to maintain that file. You can create
a directory structure in your `~/.config/nvim` directory like this:

```
# tree ~/.config/nvim

nvim
├── init.lua
└── lua
    └── user
        └── folding.lua
```

In there, you can see a  a file in the path of:
`~/.config/nvim/lua/user/folding.lua`

That file can then contain the same code from your `.vimrc` written in lua, like:

```lua
--                             FOLDING ZONE:
--                 collapse an entire block or function
-- ---------------------------------------------------------------------------
-- Enable folding on base indent
vim.opt.foldmethod = 'indent'
vim.opt.foldlevel = 99
-- also allow me to see the doc strings
vim.g.SimpylFold_docstring_preview=1
-- enable folding for markdown?
vim.g.markdown_folding = 1
vim.g.indentLine_fileTypeExclude = [['dashboard']]
```

Finally, to make sure that's sourced, include the following in your `init.lua`:

```lua
require('user.folding')
```

_Note: make sure you source your lua script AFTER your plugins that you're referencing from your package manager (vim-plug, packer, etc)._

### Introducing Packer
You'll start seeing a lot of people talking about packer as you go on your neovim
journey. It's similar to vim-plug or vundle, but it's in pure lua. In your `init.lua`,
put the following:

```lua
require('plugins')
```

and then create a file in `~/.config/nvim/lua` called `plugins.lua` with the following:

```lua
-- This file can be loaded by calling `lua require('plugins')` from your init.vim

-- this function installs the packer plugin if it's not already installed
local ensure_packer = function()
  local fn = vim.fn
  local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
  if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({'git', 'clone', '--depth', '1', 'https://github.com/wbthomason/packer.nvim', install_path})
    vim.cmd [[packadd packer.nvim]]
    return true
  end
  return false
end

" this calls the above function
local packer_bootstrap = ensure_packer()

" this manages your actual plugins
return require('packer').startup(function(use)

    -- Packer can manage itself
    use 'wbthomason/packer.nvim'

    -- Example plugin for if you already have a plugin installed in vim with
    -- something like vim-plug, like: Plug 'junegunn/limelight.vim'
    use '~/.vim/plugged/limelight.vim'


    -- Example plugin where we run :Updateremoteuseins after loadin the plugin
    -- and only run it on python filetypes. 
    use {'numirias/semshi',  run = ':UpdateRemoteuseins', ft = 'py'}
    -- this would be like running this for vim-plug:
    -- Plug 'numirias/semshi', { 'do': ':UpdateRemoteuseins', 'filetype': 'py' }

    -- Automatically set up your configuration after cloning packer.nvim
    -- Put this at the end after all plugins
    if packer_bootstrap then
        require('packer').sync()
    end
end)
```

_Note: You can checkout my actual `plugins.lua` file [here](https://github.com/jessebot/dot_files/blob/main/.config/nvim/lua/plugins.lua)_

Finally, you can open up neovim and run: `:PackerCompile` and `:PackerInstall`
and you should be on your way :)
