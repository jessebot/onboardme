---
layout: default
title: Vim
permalink: /vim
has_children: true
---

# Vim
Welcome to the wacky world of [Vim](https://www.vim.org/),

> a highly configurable text editor built to make creating and changing any kind of text very efficient. It is included as "vi" with most UNIX systems and with Apple OS X.

Vim is my daily driver for text editing. It serves as my [IDE](https://wikiless.org/wiki/Integrated_development_environment) which includes most bells and whistles of any other editor, but with a WAY smaller footprint. Vim can do anything that _x_ IDE can do, where x is visual studio or atom or pycharm or whatever the kids are using these days, but vim is generally going to be more barebones, and that's a good thing, because you don't need a new computer every other year to keep up with how bloated your current IDE is. You need a better IDE.

Here's a peak at what it looks like to work in vim:

<img src="https://raw.githubusercontent.com/jessebot/onboardme/main/docs/screenshots/vim_example_1.png" alt="screenshot of vim open with the nerdtree plugin that shows a file tree on the left handside. Also displays syntaxhighlighting and useful bottom status bar" width="800">

(Fun fact: typing `:term` will make a terminal appear without leaving vim)

This document is both for me to reference when I forget something, but also for
anyone who finds this, particularly for beginners diving in. :heart:

## Vim Tips and Tricks

### Saving and Exiting

|  Keys |            Description           |
|:-----:|:---------------------------------|
| `:w`  | save the file (does not exit)    |
| `:q`  | quit (exit) the file             |
| `:q!` | force quit: quit without saving  |
| `:wq` | write (save), then quit the file |
| `ZZ`  | alias for `:wq`, write/quit      |


### Navigation

|     Keys      |     Description    |
|:-------------:|:-------------------|
| `gg`          | top of the file    |
| `shift` + `g` | bottom of the file |

You can type a number before any of these to increase how far they go, 
e.g. `2j` will take you to down two lines.

| Keys |    Description   |
|:----:|:-----------------|
| `j`  | down a line      |
| `k`  | up a line        |
| `h`  | left a character |
| `l`  | right a character|

### Copying, Pasting, Deleting

You can type a number before all of these hot keys to change the number of
lines or words you cut, copy, and paste.

| Keys |                    Description                         |
|:----:|:-------------------------------------------------------|
| `y`  | copy the current selection (only in visual mode)       |
| `yy` | copy the current line                                  |
| `yw` | copy the current word                                  |
| `dw` | cut the current word (deletes and puts in clipboard)   |
| `dd` | cut the current line (deletes and puts in clipboard)   |
| `p`  | paste a line or selection                              |
| `]p` | paste a line or selection to match current indentation |

:star2: the `y` you're typing stands for "yank", so you're yanking a line.

### Indent and Unindent

| Keys  |              Description                 |
|:-----:|:-----------------------------------------|
| `>>`  | Indent current line *or* selection         |
| `<<`  | Unindent current line *or* selection       |
| `2>>` | Indent current line *or* selection **twice  ** |
| `2<<` | Unindent current line *or* selection **twice** |

*Note: `shiftwidth` setting in your `.vimrc` controls how many spaces to indent.*


##### Indent curly brace block
Move your cursor over *one of the curly braces*, then hit `>` followed by `%`

(From anywhere inside the curly brace block you can hit: `>` then `i` then `B`.)


### Terminal
In command mode...

|     Keys       |                    Description                      |
|:--------------:|:----------------------------------------------------|
|`:term`         | splits the current window horizonitally and puts the terminal on **TOP** of the current window   |
|`:vertical term`| splits the current window vertically and puts the terminal to the **LEFT** of the current window |
|`:below term`   | To get a terminal on the **BOTTOM OF THE ACTIVE PANE**  |
|`:botright term`| To get a terminal that spans the **ENTIRE BOTTOM**      |


### Navigate through windows
**While Holding the `Ctrl` key,** type one to switch windows in vim:

| Keys |         Description      |
|:----:|:-------------------------|
| `wh` | takes you left a window  |
| `wj` | takes you down a window  |
| `wk` | takes you up a window    |
| `wl` | takes you right a window |
| `ww` | cycle though all windows (I actually just use this one all the time and nothing else) |

## Colors

You can change the colorscheme with `:colorscheme `, do a tab after that
and it will list all the available color schemes.

This is a colorscheme editor for vim: http://bytefluent.com/vivify/

I've used it to work on the chalky colorscheme.

## Tabs

```vim
" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"                        "TAB LINE - TOP STATUS LINE"
" By default tabline does not appear unless there is more then one tab. This
" behavior is controlled by showtabline option which defaults to 1. 0 switches
" off tabline even if there is more then one tab, 2 makes tabline to be shown
" even if there is only one tab. To find out what script set the variable use
" :verbose set showtabline?
" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
" set showtabline=1
```


## Help

If there's something you want to do in vim, but you don't know how,
try searching with the built in help text. Here's an example command to explain:

```vim
:help insert
```

This will search the help text for the insert section,
and open in it in window split, which should give you something like this:

    ```
    A                       Append text at the end of the line [count] times.
                            For using "A" in Visual block mode see v_b_A.

    <insert>        or                              i insert <Insert>
    i                       Insert text before the cursor [count] times.
                            When using CTRL-O in Insert mode i_CTRL-O the count
                            is not supported.

                                                            I
    I                       Insert text before the first non-blank in the line
                            [count] times.
                            When the 'H' flag is present in 'cpoptions' and the
                            line only contains blanks, insert start just before
                            the last blank.
                            For using "I" in Visual block mode see v_b_I.

                                                            gI
    gI                      Insert text in column 1 [count] times.

    ```
The lines that look like this are search terms you can use with `:help <search term>`:
```
                                                        gi
```

To navigate the help, use `j` and `k` to go up/down `h` and `l` for left/right.
To exit the help type `:q`.
To switch back to your other window in vim without exiting help, do `crtl`+`ww`

### Vim tutor

Type `vimtutor` anywhere vim is installed to try out a vim tutorial.
Per the vim docs (`:help vimtutor`):

```
==============================================================================
01.3    Using the Vim tutor                             tutor vimtutor

Instead of reading the text (boring!) you can use the vimtutor to learn your
first Vim commands.  This is a 30-minute tutorial that teaches the most basic
Vim functionality hands-on.

On Unix, if Vim has been properly installed, you can start it from the shell:

        vimtutor

On MS-Windows you can find it in the Program/Vim menu.  Or execute
vimtutor.bat in the $VIMRUNTIME directory.

This will make a copy of the tutor file, so that you can edit it without
the risk of damaging the original.
   There are a few translated versions of the tutor.  To find out if yours is
available, use the two-letter language code.  For French:

        vimtutor fr
```

### Guides and helpful answers
- [How does the vim write with sudo trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)
- [Setting up vim for yaml](https://www.arthurkoziel.com/setting-up-vim-for-yaml/).
- [How to change the highlight color for search hits and quickfix selection](https://stackoverflow.com/questions/7103173/vim-how-to-change-the-highlight-color-for-search-hits-and-quickfix-selection)
- [Solving merge conflicts with vim](https://medium.com/prodopsio/solving-git-merge-conflicts-with-vim-c8a8617e3633)

### Awesome Lists and other neat stuff

- https://vimawesome.com/
- https://github.com/akrawchyk/awesome-vim

This is a vim bootstrapper: https://vim-bootstrap.com

