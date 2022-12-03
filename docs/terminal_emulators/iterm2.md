---
layout: default
title: iTerm2
has_children: false
parent: Terminal Emulators
permalink: /terminals/iterm2
---

# iTerm2
[iTerm2](https://iterm2.com/) is a terminal emulator for macOS. It supports dynamic profiles, images in terminals, and all sorts of other stuff.

## Color Schemes
I use the Chalk and ChalkBoard color schemes:

#### Chalk
<img src="https://raw.githubusercontent.com/mbadolato/iTerm2-Color-Schemes/master/docs/screenshots/chalk.png">

#### ChalkBoard
<img src="https://raw.githubusercontent.com/mbadolato/iTerm2-Color-Schemes/master/docs/screenshots/chalkboard.png">

### Other Colorschemes
You can configure your own, or download other color schemes here:

[https://iterm2colorschemes.com/](https://iterm2colorschemes.com/)


## How to use create a split and send a command to it in Python
make sure you've already done a `pip install iterm2`

```
#!/usr/bin/env python3.11
"""
       Name: Run a command in a split
     AUTHOR: https://github.com/jessebot
DESCRIPTION: I wrote this quickly to just run a command in a split on iterm2
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""

import iterm2
import argparse

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("command4split",
                    help="str to run as a command in an iterm2 split")
args = parser.parse_args()
print()


async def main(connection):
    """
    Create split pane to the right, make the right pane active, and send a
    command to the newly created split
    """

    app = await iterm2.async_get_app(connection)

    # Create split pane to the right and make the right one active
    left_pane = app.current_terminal_window.current_tab.current_session
    right_pane = await left_pane.async_split_pane(vertical=True)

    # send the command to the newly created split
    await right_pane.async_send_text(args.command4split + "\n")

# run the iterm2 stuff
iterm2.run_until_complete(main)
```
