# Windows General - Tips/Tricks
Did you know there's a package manager for Windows by Microsoft? It's called `winget`.

🪟 key + `x` pulls up a nice little admin tool menu

---
## `caps lock` to `ctrl`
You need to install [PowerToys](https://github.com/microsoft/PowerToys) from either the microsoft store, or you can install it via `winget` in PowerShell:

```powershell
winget install Microsoft.PowerToys -s winget
```

---
## 📷 Key (Print Screen Key) mapped Snip & Sketch
Snip & Sketch is Microsoft's screenshoting tool, but it's not mapped to your "printscreen" key, because Windows is trash.

Hit the 🪟 key > Settings.

Type "Snip" in the settings bar, and you should get a prompt that says "Use the Print Screen key to launch screen snipping". Click prompt.

Scroll to the bottom of the page for "Print Screen Shortcut" and toggle to `On`.

This automatically saves snips to your clipboard, for pasting.

---
## Snip & Sketch save on close
Launch Snip & Sketch and go to the top right `...` button > ⚙️ Settings.

Under "Save snips (Ask to save my snip before closing)" toggle the botton to `on`.

Otherwise it will discard your snip when you close it.
