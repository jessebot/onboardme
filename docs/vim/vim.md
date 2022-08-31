---
layout: default
title: Vim tips/tricks
has_children: false
permalink: /docs/vim
---

# Vim tips and tricks
- [How does the vim write with sudo trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)

If you’re copying blocks of text around and need to align the indent of a block in its new location, use `]`then `p` instead of just `p`. This aligns the pasted block with the surrounding text.

## Visual modes
|keys|description|
---|---
|`v`          |Enter *v*isual mode - highlight multiple characters from left to right `h`,`l`|
|`shift` + `v`|Enter *V*isual mode - highlight multiple lines up and down with `j`,`k`|
|`Ctrl` + `v` |Enter Visual**Block** mode - highlight a visual block of character and lines in all directions with `j`,`k`,`l`,`h`|

### Indent and Unindent

After you have a visual block selected:
Indent: `>` **twice**
Unindent: `<` **twice**

*Note: `shiftwidth` setting in your `.vimrc` controls how many spaces to indent.*

#### Indent multiple times
Examples for (un)indenting two visual blocks over:
Indent: `2` then `>` **twice**
UnIndent: `2` then `<` **twice**

#### Indent curly brace block
Move your cursor over *one of the curly braces*, then hit `>` followed by `%`

(From anywhere inside the curly brace block you can hit: `>` then `i` then `B`.)

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

### Great vim yaml walkthrough
https://www.arthurkoziel.com/setting-up-vim-for-yaml/

## Plugins
### NerdTree
I will never remember these, but they need to be held at the same time:

`Ctrl` + `ww` cycle though all windows (I actually just use this one all the time and nothing else)

`Ctrl` + `wh` takes you left a window

`Ctrl` + `wj` takes you down a window

`Ctrl` + `wk` takes you up a window

`Ctrl` + `wl` takes you right a window

