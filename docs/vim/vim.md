---
layout: default
title: Vim
permalink: /vim
---

# Vim Tips and Tricks

Guides and helpful answers:
- [How does the vim write with sudo trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)
- [Setting up vim for yaml](https://www.arthurkoziel.com/setting-up-vim-for-yaml/).

## Copying and Pasting

|Keys|Description|
|:---:|:---|
|`yy`| copy the current line |
|`yw`| copy the current word |
|`p` | paste a line |

:shooting-star: the `y` you're typing stands for "yank", so you're yanking a line. 

If you’re copying blocks of text around and need to align the indent of a block in its new location, use `]`then `p` instead of just `p`. This aligns the pasted block with the surrounding text.

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
Fun fact: I am legitmately faster with interactive sed than what you're actually supposed to do to indent lines, because I didn't learn about visualblock mode till 2022, and I hate it.

## Terminal
In command mode...

| Keys | Description |
|:---:|:---|
|`:term`| splits the current window horizonitally and puts the terminal on **TOP** of the current window |
|`:vertical term`| splits the current window vertically and puts the terminal to the **LEFT** of the current window |
|`:bottom ter`| To get a terminal on the bottom of the active pane |
|`:botright term`|To get a terminal that spans the entire bottom |

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
