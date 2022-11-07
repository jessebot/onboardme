---
layout: default
title: Terminal Emulators
description: Various terminal emulators and what I know about them
has_children: true
permalink: /terminals
---

# Terminal Emulators

I use a few different terminal emulators across macOS, Debian, and Windows, and they all have their pros and cons. I'm often trying new ones because nothing really fits all use cases yet.

My main daily drivers are iTerm2 and terminator right now, but I'm trying to phase out terminator since it feels old and I want to find something cross platform.

## Explanation of what, why, how when it comes to Terminals

| App | Local Config | Pros | Cons |
|:---:|--------------|------|------|
| [iTerm2][0] | [~/Library/ApplicationSupport/iTerm2/DynamicProfiles/Profiles.json](https://github.com/jessebot/dot_files/blob/main/Library/ApplicationSupport/iTerm2/DynamicProfiles/Profiles.json) | configurable, highly supported | macOS only |
| [hyper.js](https://hyper.is/) | [~/.hyper.js](https://github.com/jessebot/dot_files/blob/main/.hyper.js) | modern feel, configurable, cross platform | Slow with a GPU/M1 or later macOS and in Javascript :( |
| [tilix](https://gnunn1.github.io/tilix-web/)| ??? | configurable | linux only |
| [kitty](https://sw.kovidgoyal.net/kitty/) | [`~/.config/kitty`](https://github.com/jessebot/dot_files/blob/main/.config/kitty) | configurable, cross platform | can't adjust non-ascii font size, run by a brilliant jerk who calls other products "inferior" and is mean in github issues |
| [cmder](https://cmder.net/) | None yet | terminal for windows that scales, splits, and supports config | kinda buggy |

You can find more Hyper.js docs [here](./hyper/README.md), thanks to @cloudymax :)

I'm still experimenting with tilix.

## Tips and Tricks
When you're using nerdfonts, you want to set the font in the terminal config itself, and you want to set the encodeing to UTF-8

### other cool stuff you do in a terminal that I wasn't sure where to put
- [qrenco.de](https://asciinema.org/a/123683)
- [additional hyper plugins](https://medium.com/cloud-native-the-gathering/hyper-terminal-plugins-that-will-make-your-life-easier-859897df79d6)

[0]: https://iterm2.com/ "iTerm2"
