---
layout: default
title: Terminal Emulators
description: Various terminal emulators and what I know about them
has_children: true
permalink: /terminals
---

# Terminal Emulators

I use a couple different terminal emulators across macOS, Debian, as well as
(rarely) Windows, and they all have their pros and cons. I was often trying new
terminals for a while, because nothing really fit all my use cases.

I was originally trying pretty hard to hit every feature I wanted:
cross platform, splits, tabs, images, True color (meaning any HEX color),
background transparency, two different fonts/sizes for ascii/nonascii characters,
GPU accelleration, an API, and -of course- a nice community/maintainers.

Turns out that's a tall order. I had to make some compromises here and there.

My ultimate choice was to use iTerm2 on macOS and Wezterm on Linux (and also on macOS sometimes).


## Explanation of what and why it comes to Terminals

This will just go over what terminals I tested and why I liked them :)

#### Key:

|   Symbol   | Description     |
|:----------:|:----------------|
|     🪟     | Windows         |
|     🍎     | macOS           |
|     🐧     | Linux           |
|     🗂️     | Tabs            |
|     ⿲     | Splits          |
|     🖼️     | images          |
|     🎥     | recording       |
|     🫥     | Transparency    |
|     🖥️     | GPU acellerated |
| 🧑‍💻 | API             |


|       App       | Platforms | Features         | Notable Downsides                                         |
|:---------------:|:---------:|------------------|-----------------------------------------------------------|
|   [wezterm][7]  |   🍎🐧🪟  | ⿲🗂️🫥 🖼️        | Honestly none to note so far                              |
|   [iTerm2][4]   |    〿🍎〿   | ⿲🗂️🫥 🎥🖼️      | Only on macOS :(                                          |
|  [hyper.js][0]  |   🍎🐧🪟  | ⿲🗂️🫥🧑‍💻 | Slow on older machines with no GPU, written in javascript |
|    [cmder][3]   |    〿〿🪟   | ⿲🗂️🫥           | kinda buggy, random crashes                               |
| [Terminator][5] |    〿🐧〿   | ⿲🗂️🫥           | community not as active anymore                           |
|    [kitty][1]   |   🍎🐧?   | ⿲🗂️🫥  🖼️       | non-ascii font size unajustable, community unwelcoming    |
|    [tilix][2]   |    〿🐧〿   | ?🗂️???           | small userbase                                            |

I want to say I didn't give tilix a fair shot, because I ran out of funemployment funds, and had to get back to work, where I need my terminal to just work, and it needs to be able to work fast and effeciently.

## Tips and Tricks
When you're using nerdfonts, you want to set the font in the terminal config itself,
and you want to set the encodeing to UTF-8.

For getting your colors to match another terminal, try out [terminal.sexy][6].

### other cool stuff you do in a terminal that I wasn't sure where to put
- You can find more Hyper.js docs [here](./hyper/README.md), thanks to @cloudymax :)
- [additional hyper plugins](https://medium.com/cloud-native-the-gathering/hyper-terminal-plugins-that-will-make-your-life-easier-859897df79d6)


[0]: https://hyper.is/ "hyper.is"
[1]: https://sw.kovidgoyal.net/kitty/ "kitty"
[2]: https://gnunn1.github.io/tilix-web/ "tilix"
[3]: https://cmder.net/ "cmder"
[4]: https://iterm2.com/ "iTerm2"
[5]: https://gnome-terminator.org/ "terminator"
[6]: http://terminal.sexy "terminal.sexy"
[7]: https://wezfurlong.org/wezterm/ "wezterm"
