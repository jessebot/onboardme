# Windows Notes
Did you know there's a package manager for Windows by Microsoft? It's called `winget`.

## Capslock to Control
You need to install [PowerToys](https://github.com/microsoft/PowerToys) from either the microsoft store, or you can install it via `winget` in PowerShell:

```powershell
winget install Microsoft.PowerToys -s winget
```

## Windows Subsystem for Linux
```powershell
wsl --install
```

## Tips and Tricks
`win key` + `x` pulls up a nice little admin tool menu

## VPN causing issues with DNS resolution
Edit `/etc/wsl.conf` and uncomment generateNetworkConf or whatever it's called, and set it to false. Then unlink your `etc/resolv.conf` and modify it to be the VPN's name servers only.
