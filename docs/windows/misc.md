---
layout: default
title: Tips and Tricks
parent: Windows
permalink: /windows/trips-and-tricks
---

## Tips and Tricks

### Package Managers for Windows

Did you know there's a package manager for Windows by Microsoft? It's called `winget`.

The other alternatives are [chocolately](https://chocolatey.org/install) and [scoop](https://scoop.sh/).

---
### Admin tool menu

🪟 key + `x` pulls up a nice little admin tool menu

---
### cmder - a useable terminal for windows
[cmdr](https://cmder.net/) absolutely remains my favorite windows terminal. It supports all the important things like transparency, easy on the eyes colors, and splitting. Seems to struggle with some utf-8/emojis, but allows for access of powershell, cmd, and wsl, and is fairly configurable.

---
### Fonts Installation

```powershell
git clone https://github.com/ryanoasis/nerd-fonts.git --depth 1

cd nerd-fonts

.\install.ps1 Hack
```

## Permissions errors
If you're getting a permission error, try this:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
And when you're done, do this:
```powershell
Set-ExecutionPolicy Restricted
```

---
## `caps lock` to `ctrl`
You need to install [PowerToys](https://github.com/microsoft/PowerToys) from either the microsoft store, or you can install it via `winget` in PowerShell:

```powershell
winget install Microsoft.PowerToys -s winget
```
