---
layout: default
title: Vim Plugins
grand_parent: IDE
parent: Vim
permalink: /vim/vim-plugins
---

# Vim Plugins

Plugins are extra modules you can install written by other people. Most of the time they are hosted opensource on Github/Gitlab.
There's a lot of plugin managers, so many, that often times you'll see in the readme of a plugin: use your favorite plugin manager.

Below I'll go over my favorite plugin manager and plugins, plus some tips and tricks for them all.

## vim-plug - a vim plugin manager

I use [vim-plug](https://github.com/junegunn/vim-plug) to manage my vim plugins, because the syntax is pretty easy.

It puts your plugins into (on Linux/macOS): '~/.vim/plugged'

### Install plugins with vim-plug

Here's what you put in your `.vimrc`
```vim
" this is to start calling plugins
call plug#begin()
" you can put all your plugins below the call plug line

" indents lines and adds a line to show blocks of code
" downloads plugin from repo indentLine owned by Yggdroot
Plug 'Yggdroot/indentLine'

" plugins stop on this line
call plug#end()
```

Then you just run `:PlugInstall` when in vim and it'll install everything in your `.vimrc`.

### Uninstall plugins with vim-plug

First remove or comment out the plugin line from your `.vimrc` and then open up vim and run `:PlugClean`.


# Plugins I use

## General Plugins

### vim-clap - a modern fuzzy searcher

```vim
Plug 'liuchengxu/vim-clap'
```


### NerdTree - directory tree expolorer
The thing that made [NERDTree](https://github.com/scrooloose/nerdtree) the best was that it integrates with [vim-devicons](https://github.com/ryanoasis/vim-devicons), which adds [NerdFonts with symbols](https://nerdfonts.com) so that you can see what kind of file or directory you're looking at.

It's simple at its core, but complex enough that it has it's own plugins, so I'll just give you all the related plugins I actually use. Here's the selection from my .vimrc vim-plug block:

```vim
" NerdTree - Tree explorer plugin - use :NERDTreeToggle to try it out
"          - after nerdtree is on visible, use ? for help

" On-demand loading of nerdtree
Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }

" syntax highlighing for nerdtree
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'

" puts little glyphs for different file types
Plug 'ryanoasis/vim-devicons'

" add git awareness to see modified, merged, etc status of file in nerdtree
Plug 'Xuyuanp/nerdtree-git-plugin'

" END NerdTree
```

Once you've got it installed, while in vim, start typing `:nerd` and tab, and it will autocomplete to `:NERDTreeToggle`, which will bring up a file tree, that you can then navigate with `j`(down) and `k`(up), and then either:
- hit `return` to either open directories
- hit `s` to open a file side by side


### vim-airline - a prettier status line for vim
[vim-airline](https://github.com/vim-airline/vim-airline) written entirely in vim script, and is a bit faster than powerline's implementation. You can also use [themes](https://github.com/vim-airline/vim-airline-themes) with it.

```vim
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
```

I still wanted it to match my powerline shell theme look and feel, so I did the following:

```vim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                              Airline
"               A pure vim script status line for vim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" use powerline fonts
let g:airline_powerline_fonts = 1
" use softer colors
let g:airline_theme='murmur'
" changing separators to match personal powerline for shell
let g:airline_left_sep=' '
let g:airline_right_sep=''
" this is a smaller more consise final section
function! LinePercent()
    return line('.') * 100 / line('$') . '%'
endfunction
let g:airline_section_z = ':%l (%{LinePercent()}) :%v'
```

## Git plugins

### vim-fugitive and vim-gitgutter
Both of these are git related plugins. I use these for different things. [vim-fugitive](https://github.com/tpope/vim-fugitive) is good for letting you run git commands from vim, while [vim-gitgutter](https://github.com/airblade/vim-gitgutter) is great for showing you diff symbols in the left hand column for any changes that differ from your set origin branch.

```
" git plugin for running git commands with :git
Plug 'tpope/vim-fugitive'

" puts a git + or - in side line to show git changes in file
Plug 'airblade/vim-gitgutter'
```

I find them both great, but git-gutter was kind of ugly, and so I changed the symbols and colors to:

```vim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               vim-gitgutter
"  git gutter is a vim plugin that puts a symbol in a column before the line #
"  We need to do a little configuring to make it less ugly
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" vim-gitgutter used to do this by default:
highlight! link SignColumn LineNr
" change sign color color
highlight SignColumn guibg=#1d1d1d ctermbg=black

" change the colors back to what they should be when there are changes
highlight GitGutterAdd    guifg=#009900 ctermfg=2
highlight GitGutterChange guifg=#bbbb00 ctermfg=3
highlight GitGutterDelete guifg=#ff2222 ctermfg=1

" use the nerdfont symbols instead of -,+
let g:gitgutter_sign_added = ''
let g:gitgutter_sign_modified = ''
let g:gitgutter_sign_removed = ''
```

## Indentation, Syntaxhighlighting, and linting, oh my!
These sections are grouped together, because many plugins in any one of these categories overlap.

### General Indentation

```vim
" indents lines and adds a line to show blocks of code
Plug 'Yggdroot/indentLine'
```

### YAML Syntax highlighting

```vim
" yaml syntax highlighting better
Plug 'stephpy/vim-yaml'
```

### Python support

```vim
" python tab completion - I actually find this kind of annoying 🤷
Plug 'davidhalter/jedi-vim'
" I don't actually remember what this does...
Plug 'python-mode/python-mode', { 'for': 'python'}
```

### Bash support

```vim
" bash tab completion
Plug 'WolfgangMehner/bash-support'

" linter - will use shellcheck for bash and highlight broken code
Plug 'dense-analysis/ale'
```

### Limelight
For distraction free writing
```vim
Plug 'junegunn/limelight'
```

## Kubernetes plugins

### vim-kubernetes
Run k8s commands from vim.

```vim
" For the current buffer (including modifications not on disk)
" :KubeApply :KubeDelete :KubeCreate
" And for the current directory (read from disk)
" :KubeApplyDir :KubeDeleteDir
Plug 'andrewstuart/vim-kubernetes'
```

### helm plugins

I like the of this one, but it breaks all my auto-indents and I dont' know why, so it's disabled right now:

```vim
" helm yaml specifically (includes go support) doesn't seem to work for
" auto-indenting, so it's off for now
" Plug 'towolf/vim-helm'
```

If you have a better solution, email me, please 🤷
