# Random Tips and Tricks
Did you know there's a package manager for Windows by Microsoft? It's called `winget`.

🪟 key + `x` pulls up a nice little admin tool menu

## `caps lock` to `ctrl`
You need to install [PowerToys](https://github.com/microsoft/PowerToys) from either the microsoft store, or you can install it via `winget` in PowerShell:

```powershell
winget install Microsoft.PowerToys -s winget
```

## 📷 Key (Print Screen Key) mapped Snip & Sketch
Snip & Sketch is Microsoft's screenshoting tool, but it's not mapped to your "printscreen" key, because Windows is trash.

Hit the 🪟 key > Settings.

Type "Snip" in the settings bar, and you should get a prompt that says "Use the Print Screen key to launch screen snipping". Click prompt.

Scroll to the bottom of the page for "Print Screen Shortcut" and toggle to `On`.

This automatically saves snips to your clipboard, for pasting.

## Snip & Sketch save on close
Launch Snip & Sketch and go to the top right `...` button > ⚙️ Settings.

Under "Save snips (Ask to save my snip before closing)" toggle the botton to `on`.

Otherwise it will discard your snip when you close it.

# WSL (Windows Subsystem for Linux)
Should be able to get to this by first hitting 🪟 Key, and then typing "devleoper settings" and hitting `enter`. 
(Equivelent of: Settings > Update and Security > For developers)

Toggle "Developer Mode" to `on`.

Run this in powershell:
```powershell
wsl --install
```

After the install, go to Win key > turn windows features on or off (it's in control panel).

Then you should be able to scroll down to Windows Subsystem for Linux and check the box before saving and quitting.

FINALLY, you can bring up win key > microsoft store > Debian (app) and hit install.

## Disable terminal bell/beep in wsl

For BASH:
```bash
sudo sed -i 's/# set bell-style none/set bell-style none/' /etc/inputrc
```

For VIM:
```vim
set visualbell
set t_vb=
```

Requires restart of WSL app (in my case, Debian).

## VPN causing issues with DNS resolution
Edit `/etc/wsl.conf` and uncomment `generateNetworkConf=false` or whatever it's called, and set it to `false` if it isn't already. Then unlink your `etc/resolv.conf` and modify it to be the VPN's name servers only.

## Can't echo `brew` path into `.bashrc`

When you try this:

```bash
echo "export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin" >> ~/.bashrc
```

You will get some errors about characters like this `(`. It's because by default, windows puts their own awful spaced and parenthesed directories into your default path, and BASH is expanding the `$PATH` variable on the commandline, without escaping any of that nonsense.

Just open up vim and manually put in the following to it's own line in your `.bashrc`:

```bash
export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin
```
