---
layout: default
title: Visual Mode
parent: Vim
permalink: /vim/visual
---

# Visual modes

|      Keys     |                  Description                  |
|:-------------:|:----------------------------------------------|
| `v`           | Enter *v*isual mode - highlight multiple characters from left to right `h`,`l` |
| `shift` + `v` | Enter *V*isual (capital V) mode - highlight multiple lines up and down with `j`,`k` |
| `ctrl` + `v`  | Enter Visual**Block** mode - highlight a visual block of character and lines in all directions with `j`,`k`,`l`,`h` |

Once you've highlighted a selection, you can then operate on just that selection, so you can cut it, copy it, indent it, and use interactive sed on it. You can also search for a selection. It's pretty helpful.


## Searching for a selection
Thank you to the [people on stackoverflow](https://stackoverflow.com/a/16783292) for this one:

- Select the text using a visual selection, e.g. `v`
- Yank it (this is copying), `y`
- Search, `/`
- Paste the last yanked text using
  <C-r>0 (`Ctrl` while holding `r` and then pressing `0`)
  Actually inserts the content from register `0`, see `:h i_ctrl-r`

Another example is using the command line:

- Select the text using a visual selection, e.g. `v`
- Yank it, `y`
- Enter command-line mode with editing an Ex command, `q/`
- Paste yanked text, `p`, and search by pressing Enter

In short: `yq/p<Enter>`


### searching selection: shorter short cut

My personal `.vimrc` includes these lines, so that I can just highlight a
selection and then immediately search it with `*`:

```vim
xnoremap * :<C-u>call <SID>VSetSearch()<CR>/<C-R>=@/<CR><CR>
xnoremap # :<C-u>call <SID>VSetSearch()<CR>?<C-R>=@/<CR><CR>

function! s:VSetSearch()
    let temp = @s
    norm! gv"sy
    let @/ = '\V' . substitute(escape(@s, '/\'), '\n', '\\n','g')
    let @s = temp
endfunction
```


## Insert into all selected visualblock lines
After you have a visual block selected:

`shift` + `i` takes you into insert for all lines, and you can type whatever you want, including indentation like spaces or tabs.

*NOTE: It will only look like you're editing one line, and that is ok!*

Hit `esc` **twice**!


## Interactive sed example
This will prepend "meep " only on the current line your cursor is on:
```vim
:s/^/meep /
```

Adding `%` will prepend _every line_ in the file with "meep ":
```vim
:%s/^/meep /
```
