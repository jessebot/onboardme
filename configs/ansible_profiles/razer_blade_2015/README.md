# Issues

workarounds for my laptop, [more notes and refs](https://github.com/rolandguelle/razer-blade-stealth-linux/blob/master/ubuntu-20-10.md)

## Suspend Loop

- add "button.lid_init_state=open" to grub boot options

`sudo nano /etc/default/grub`

```bash
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'

GRUB_DEFAULT=0
GRUB_TIMEOUT_STYLE=hidden
GRUB_TIMEOUT=0
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash button.lid_init_state=open video=eDP-1:1920x1080@120"
GRUB_CMDLINE_LINUX=""

# Uncomment to enable BadRAM filtering, modify to suit your needs
# This works with Linux (no patch required) and with any kernel that obtains
# the memory map information from GRUB (GNU Mach, kernel of FreeBSD ...)
#GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xefefefef"

# Uncomment to disable graphical terminal (grub-pc only)
#GRUB_TERMINAL=console

# The resolution used on graphical terminal
# note that you can use only modes which your graphic card supports via VBE
# you can see them in real GRUB with the command `vbeinfo'
#GRUB_GFXMODE=640x480

# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
#GRUB_DISABLE_LINUX_UUID=true

# Uncomment to disable generation of recovery mode menu entries
#GRUB_DISABLE_RECOVERY="true"

# Uncomment to get a beep at grub start
#GRUB_INIT_TUNE="480 440 1"
```

```bash
sudo update-grub
sudo update-initramfs -k all -u
```

## Caps-Lock Crash

sudo nano /etc/default/keyboard
XKBOPTIONS="ctrl:nocaps"

```bash
# KEYBOARD CONFIGURATION FILE

# Consult the keyboard(5) manual page.

XKBMODEL="pc105"
XKBLAYOUT="us"
XKBVARIANT=""
XKBOPTIONS="ctrl:nocaps"

BACKSPACE="guess"
```

## firefox touch

```bash
# add the following to /etc/environment
MOZ_USE_XINPUT2=1
MOZ_ENABLE_WAYLAND=1
```

## bluetooth issues

## resolution issues

Waylannd doesnt yet support high refresh rate monitors in a way that is consistent with more legacy practices that still rely on the way x11 reported information about displays. Namely, when wayland is ussed - the reported display device is XWAYLAND0, which isnt recognized by more established processes like grub, or gnome in all situations yet.

- [disabling wayland](https://linuxconfig.org/how-to-disable-wayland-and-enable-xorg-display-server-on-ubuntu-18-04-bionic-beaver-linux)

the solution to specify 120hz refresh is included int he grubfile under the suspend loop section.

## Software installation

- install github-cli

```bash
# installs github cli

sudo apt-get install curl
sudo apt-get install dirmngr
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

- auth from browser or cli w/ file

`gh auth login`

`git config --global user.name "cloudymax"`

- use your github private email for this, its in your email security settings in your github profile

`git config --global user.email "84841307+cloudymax@users.noreply.github.com"`

- install github desktop

```bash
wget -qO - https://packagecloud.io/shiftkey/desktop/gpgkey | sudo apt-key add -

sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/shiftkey/desktop/any/ any main" > /etc/apt/sources.list.d/packagecloud-shiftky-desktop.list'

sudo apt-get update

sudo apt install github-desktop


# install signal
wget -O- https://updates.signal.org/desktop/apt/keys.asc | gpg --dearmor > signal-desktop-keyring.gpg
cat signal-desktop-keyring.gpg | sudo tee -a /usr/share/keyrings/signal-desktop-keyring.gpg > /dev/null
echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/signal-desktop-keyring.gpg] https://updates.signal.org/desktop/apt xenial main' |\
  sudo tee -a /etc/apt/sources.list.d/signal-xenial.list
sudo apt update && sudo apt install signal-desktop

```

## system tweaks

- change apt repo
- change display settings
- change power settings
- firefox, lastpass, ubuntu one account information
- colors/backgrounds
- postfix server issues on 21.04?

## Snap Packages

- Click-up (community)
- Bitwarden
- Bitwarden CLI
- dbeaver
- Kubectl
- LXD
- Multipass
- podman
- buildah
- signal
- surfshark

## deb packages

- [Teams](https://www.microsoft.com/en-us/microsoft-teams/download-app#allDevicesSection)

- Discord

```Bash
 wget -O discord.deb "https://discordapp.com/api/download?platform=linux&format=deb"

 sudo dpkg -i /path/to/discord.deb
```

## Sign-ins

- Ubuntu one
- Github
- Firefox
- LastPass

## OpenVPN

```zsh

sudo apt-get install openvpn unzip

cd /etc/openvpn
sudo wget https://my.surfshark.com/vpn/api/v1/server/configurations
sudo unzip configurations

sudo openvpn nl-ams.prod.surfshark.com_tcp.ovpn

pP59jp7ER9paFCkzHAHsaBvs
LUW3LLfTKLXXrwwdVcJ8KWhs

```

## Bit Warden + Auth0

Install bitwarden from snap store, and install browser extension

create a free account for your personal user
create a free buisness account w/ an admin email
add your personal user to the organization
accept the invite on your personal account
confirm the user on the admin account

add your open vpn data and data for both accounts you just made to your vault

craete a new Auth0 Account for your Org using the orgs bitwarden account
Setup multifactor options
Send your bitwarden personal account an invite to the auth0 org
accept the invite on the personal account.

Download the Auth0 Guardian app and link it to your personal account
store all the keys as needed.

Go back to bit warden on your personal account and in the two-step login,
enable the authenticator app provider. Scan the QR code with Auth0 Guardian.

Add the bitwarden extension to your browser and sign in. enable unlocking w/ PIN and Biometrics

buy a enterprise licenses with bitwarden

follow here:

https://bitwarden.com/help/article/saml-auth0/


## Ubikey
https://support.yubico.com/hc/en-us/articles/360016649099-Ubuntu-Linux-Login-Guide-U2F

sudo wget https://raw.githubusercontent.com/Yubico/libu2f-host/master/70-u2f.rules -O /etc/udev/rules.d/70-u2f.rules

sudo apt-get install libpam-u2f
sudo apt install libu2f-udev

mkdir -p ~/.config/Yubico
pamu2fcfg > ~/.config/Yubico/u2f_keys


