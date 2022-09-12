---
layout: default
title: Vim
parent: Command Line Interface
permalink: /cli/vim
---

# Vim Tips and Tricks

Guides and helpful answers:
- [How does the vim write with sudo trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)
- [Setting up vim for yaml](https://www.arthurkoziel.com/setting-up-vim-for-yaml/).

## Navigation 

|Keys|Description|
|:---:|:---|
|`gg`| top of the file|
|`shift` + `g`| bottom of the file|

You can type a number before any of these to increase how far they go, e.g. `2j` will take you to down two lines.

|Keys|Description|
|:---:|:---|
|`j`| down a line|
|`k`| up a line|
|`h`| left a character|
|`l`| right a character|

## Copying, Pasting, Deleting

You can type a number before all of these hot keys to change the number of lines or words you cut, copy, and paste.

|Keys|Description|
|:---:|:---|
|`y`| copy the current selection (only in visual mode) |
|`yy`| copy the current line |
|`yw`| copy the current word |
|`dw`| cut the current word (deletes and puts in clipboard)|
|`dd`| cut the current line (deletes and puts in clipboard)|
|`p` | paste a line or selection |
|`]p` | paste a line or selection to match current indentation|

:star2: the `y` you're typing stands for "yank", so you're yanking a line. 

## Indent and Unindent

|Keys|Description|
|:---:|:---|
| `>>` | Indent current line *or* selection |
| `<<` | Unindent current line *or* selection |
| `2>>` | Indent current line *or* selection **twice** |
| `2<<` | Unindent current line *or* selection **twice** |

*Note: `shiftwidth` setting in your `.vimrc` controls how many spaces to indent.*

#### Indent curly brace block
Move your cursor over *one of the curly braces*, then hit `>` followed by `%`

(From anywhere inside the curly brace block you can hit: `>` then `i` then `B`.)

## Visual modes

|Keys|Description|
|:---:|:---|
|`v`          | Enter *v*isual mode - highlight multiple characters from left to right `h`,`l` |
|`shift` + `v`| Enter *V*isual (capital V) mode - highlight multiple lines up and down with `j`,`k` |
|`ctrl` + `v` | Enter Visual**Block** mode - highlight a visual block of character and lines in all directions with `j`,`k`,`l`,`h` |

Once you've highlighted a selection, you can then operate on just that selection, so you can cut it, copy it, indent it, and use interactive sed on it. It's pretty helpful.

### Insert into all selected visualblock lines
After you have a visual block selected:
`shift` + `i` takes you into insert for all lines, and you can type whatever you want, including indentation like spaces or tabs.

*NOTE: It will only look like you're editing one line, and that is ok!*

Hit `esc` **twice**!

### Interactive sed example
This will prepend each line with "meep ":
```vim
:%s/^/meep /
```

## Terminal
In command mode...

| Keys | Description |
|:---:|:---|
|`:term`| splits the current window horizonitally and puts the terminal on **TOP** of the current window |
|`:vertical term`| splits the current window vertically and puts the terminal to the **LEFT** of the current window |
|`:below term`| To get a terminal on the **BOTTOM OF THE ACTIVE PANE** |
|`:botright term`|To get a terminal that spans the **ENTIRE BOTTOM** |

## Navigate through windows 
**While Holding the `Ctrl` key,** type one to switch windows in vim:

| Keys | Description |
|:---:|:---|
|`ww`| cycle though all windows (I actually just use this one all the time and nothing else) |
|`wh`| takes you left a window  |
|`wj`| takes you down a window  |
|`wk`| takes you up a window    |
|`wl`| takes you right a window |


## Plugins
### NerdTree

While in vim, start typing `:nerd` and tab, and it will autocomplete to `:NERDTreeToggle`, which will bring up a file tree, that you can then navigate with `j`(down) and `k`(up), and then either:
- hit `return` to either open directories
- hit `s` to open a file side by side
