---
layout: default
title: Terminal Emulators
description: Various terminal emulators and what I know about them
has_children: true
permalink: /terminals
---

# Terminal Emulators

I use a few different terminal emulators across macOS, Debian, as well as
Windows, and they all have their pros and cons. I'm often trying new ones right
now, because nothing really fits all use cases yet.

My main daily drivers are iTerm2 (macOS) and terminator (linux) right now,
but I'm trying to phase out terminator since it feels old, and I want to find
something cross platform.

Update (2022-11-11 22:25:57.0 +0100): I have learned so much more about terminal
emulators now, and I gotta say, iTerm2 really is a fantastic terminal, and I really
wish it existed on Linux.

## Explanation of what, why, how when it comes to Terminals

|      App      | Pros                       | Cons                        |
|:-------------:|----------------------------|-----------------------------|
| [hyper.js][0] | css?, crossplatform        | Slow on older machines with no GPU/in JS |
| [kitty][1]    | cross platform             | non-ascii font size unajustable, community unwelcoming |
| [tilix][2]    | :shrug:                    | linux only                   |
| [cmder][3]    | on windows & scales/splits | kinda buggy                  |
| [iTerm2][4]   | highly supported           | macOS only, but really good features like native image rendering and session recording |
| [Terminator][5] | Old reliable, splits/scales/transparent | Not as customizable as I'd like |
| [wezterm][7] | Rust?                       | I can't remember why I uninstalled it 🤔|

You can find more Hyper.js docs [here](./hyper/README.md), thanks to @cloudymax :)

I'm still experimenting with tilix.

## Tips and Tricks
When you're using nerdfonts, you want to set the font in the terminal config itself,
and you want to set the encodeing to UTF-8.

For getting your colors to match another terminal, try out [terminal.sexy][6].

### other cool stuff you do in a terminal that I wasn't sure where to put
- [additional hyper plugins](https://medium.com/cloud-native-the-gathering/hyper-terminal-plugins-that-will-make-your-life-easier-859897df79d6)

[0]: https://hyper.is/ "hyper.is"
[1]: https://sw.kovidgoyal.net/kitty/ "kitty"
[2]: https://gnunn1.github.io/tilix-web/ "tilix"
[3]: https://cmder.net/ "cmder"
[4]: https://iterm2.com/ "iTerm2"
[5]: https://gnome-terminator.org/ "terminator"
[6]: http://terminal.sexy "terminal.sexy"
[7]: https://wezfurlong.org/wezterm/ "wezterm"
