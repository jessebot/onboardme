---
layout: default
title: IDE
has_children: true
permalink: /ide
description: "IDEs and what I think/know about them"
---

# Quick intro
I love vim and have been using it for ages, but recently started using neovim.
I have both a vim section for general vim notes, and a neovim section which covers
converting from vim to neovim and what's involved. This page is mostly for things
that don't quite fit between the two.

# General Tips

## How to open certain file types in vim/neovim in your favorite terminal on macOS

I found the following links helpful, so feel free to take a look there first:

- [Double click to open a file in vim from Finder in OSX](https://www.mattcrampton.com/blog/doubleclick_to_open_in_vim_on_osx/)
- [apple.stackexchange: how to open text files in vim (iTerm2)...](https://apple.stackexchange.com/a/444250)

Here's what I actually did though:

### Step one
Open [Automator](https://support.apple.com/nl-nl/guide/automator/welcome/mac) on your mac (Should already be installed). This will open a file selector in your Applications directory. Click the "New Document" button at the bottom of the window. Select App, when it prompts you for what you want to work on.

On the left hand side of Automator, you should see a search, type "apple" and then select the Apple Script option.

Finally, in the editor window that opens on the right hand side, highlight the default text there, and paste in the following code block to overwrite it.

Before you proceed, note that the following will:
- open iterm2
- clear the screen
- open the file you clicked in vim

It will not exit iterm2 when you close the file.

```applescript
on run {input, parameters}

    set filename to POSIX path of input

    set cmd to "clear && 'vim' '" & filename & "'"

    if application "iTerm" is running then
        tell application "iTerm"
            set newWindow to (create window with default profile)
            tell current session of newWindow
                write text cmd
            end tell
        end tell
    else
        activate application "iTerm"
        tell application "iTerm"
            repeat until (exists current window)
                delay 0.1
            end repeat
            set newWindow to current window
            tell current session of newWindow
                write text cmd
            end tell
        end tell
    end if

end run
```

Then at the top menu, go to File > Save. Save it in your Applications folder, and name is something like iTermVim.app or something.

Then, when you want to make sure a filetype is always opened with your little app, then you need to find a file that you want to open, and right click it and in the menu, select "open file with..." and select your app (e.g. iTermVim.app), and then click the check box for "always open with" before opening it.

If you want to edit the app, you can now open it from your applications folder with automator. If you want iTerm2 to exit when you're done editing the vim file, replace the following line:

```applescript
   set cmd to "clear && 'vim' '" & filename & "'"
```

with the following line:

```applescript
    set cmd to "clear && 'vim' '" & filename & "' && exit"
```
