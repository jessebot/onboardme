# Learn about Hyper :D

[Hyper.js terminal](https://hyper.is/#installation)

Some cool CSS thing @cloudymax has been up to

```bash
sudo apt-get install build-essential procps curl file git
wget https://releases.hyper.is/download/deb

sudo dpkg -i hyper*

# needs npm for addons
sudo apt install npm
npm install express

# install addons
hyper install <plugin-name>
hyper uuninstall <plugin-name>
hyper list

config file is located at: ~/.hyper.js
```

### Addons

Explore the ecosystem <3

- https://github.com/bnb/awesome-hyper

```bash
hyper install hypercwd
hyper install hyper-pane
hyper install hyper-tabs-enhanced
hyper install hyper-samewd
hyper install hyper-tab-icons
hyper install hyper-htm
hyper install hyper-highlight-pane
```

## hyper themes

### basic

- [verminal](https://github.com/defringe/verminal): high-contrast + transparancy 

- [hyper-dracula](https://hyper.is/store/hyper-dracula): simple semi-dark material theme with good contrast

- [hyper-materialshell](https://github.com/carloscuesta/hyper-materialshell): similar to dracula but darker

- [hypernasa](https://www.npmjs.com/package/hypernasa): see the daily nasa picture in your terminal. looks nice, but can suck on days where th pic doesnt contrast well

- [hyper-pokemon](https://github.com/klaussinani/hyper-pokemon): configure your own poke station! configurable flat desgn pokemon walpapers with color matching text + tab iconse

## install zsh plugin manager

[oh-my-zsh](https://github.com/ohmyzsh/ohmyzsh)

### Plugins

- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md)

### zsh addons

1. [Pure Prompt](https://github.com/sindresorhus/pure)
`npm install --global pure-prompt`

2. initialize by adding the following to the top of your .zshrc

```bash
autoload -U promptinit; promptinit
prompt pure
```


