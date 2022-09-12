# @jessebot's personal .bash_profile/.bashrc
# I hate bells
set bell-style none

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

## default editor
export EDITOR=vim

## silences the macos zsh default terminal message
export BASH_SILENCE_DEPRECATION_WARNING=1

GOROOT=$HOME

################# HISTORY ####################
# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth
# append to the history file, don't overwrite it
shopt -s histappend
# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=10000
HISTFILESIZE=20000
# for setting time stamps on history
HISTTIMEFORMAT="%d/%m/%y %T "

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

################# ls aliases ####################
# lsd instead of ls for colors/icons, human readable file sizes, show hidden files
alias ls='lsd -a'
alias ll='lsd -hal'
# list, sorted by most recent and reversed, so the most recent
# file is the last ouputted line, helpful for directories with lots of files
alias lt='lsd -atr'
# same as above, but long
alias llt='lsd -haltr'
# lsd already has a fancier tree command with icons
alias tree='lsd --tree --depth=2'


# colordiff - diff, but with colors for accessibility
alias diff='colordiff -uw'

# python3 alias because python2 is still in some places
alias python='python3'

# grep - always use colors
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

####################### typos <3 ########################
alias grpe='grep'
alias gerp='grep'
alias celar='clear'
alias clar='clear'
alias gti='git'
alias gtt='git'
alias ter='tree'
alias tre='tree'
alias pthyon='python3'
alias ptyhon='python3'
alias pythong='python'
alias gtop='gotop'

# shorten commands
alias vi='vim'
alias tracert='traceroute'

# cat with syntax highlighting
if [[ $(uname) == *"Linux"* ]]; then
    alias cat='batcat'
    alias bat='batcat'
else
    alias cat='ccat'
fi

# git speed up
alias gc='git commit -m'
alias gs='git status'
# check all directories below my current directory for their git status
alias gsa='ls -1 -A | xargs -I % sh -c "figlet % | lolcat ; cd %; git status --short; cd - > /dev/null; echo ''"'
alias gd='git diff'
alias ga='git add .'
alias gph='git push'
alias gpl='git pull'

# quick to do
alias todo='vim ~/todo.md'

# whoami, whereami, whoareyou?
alias whereami='hostname'
alias whoareyou='echo "Your friend :)"'

# scrncpy install adb for you, but it's awkward to use
alias adb='scrcpy.adb'

########## Extra Functions/One-Liners ###########
# move faster with base 64
function b64 {
    echo -n $1 | base64
}
function b64d {
    echo -n $1 | base64 --decode
}

# allow for searching of all repos with ag
function agr {
    if [ $2 = "y"]; then
        for $repo in $(ls -1 $REPOS); do
            cd $REPOS/$repo && git pull
        done
    fi

    ag $1 $REPOS
}

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
# bash completion for nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# terraform bash completion
complete -C /usr/local/bin/terraform terraform

########################## PATHING #################################

# go
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin

# python packages default location when you do pip3 install --user somepackage
export PATH=$PATH:$HOME/.local/bin

# special linux pathing
if [[ $(uname) == *"Linux"* ]]; then
    # this is for iptables on debian, which is elusive
    export PATH=$PATH:/usr/sbin:/usr/share
    # for snap package manager packages
    export PATH=$PATH:/snap/bin
    ############################## Brew on Linux #########################
    export HOMEBREW_PREFIX=/home/linuxbrew/.linuxbrew
    export HOMEBREW_CELLAR=/home/linuxbrew/.linuxbrew/Cellar
    export HOMEBREW_REPOSITORY=/home/linuxbrew/.linuxbrew/Homebrew
    export MANPATH=$MANPATH:/home/linuxbrew/.linuxbrew/share/man
    export INFOPATH=$INFOPATH:/home/linuxbrew/.linuxbrew/share/info
    export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin
    pip_packages="/home/linuxbrew/.linuxbrew/lib/python3.10/site-packages"
else
    # this is so bash completion works on MacOS
    [[ -r "/usr/local/etc/profile.d/bash_completion.sh" ]] && . "/usr/local/etc/profile.d/bash_completion.sh"
    # don't warn me that BASH is deprecated, I already upgraded it
    export BASH_SILENCE_DEPRECATION_WARNING=1

    # check if this an M1 mac or not
    if [ $(uname -a | grep arm > /dev/null ; echo $?) -eq 0 ]; then
        # for the M1/M2 brew default installs here
        export PATH=/opt/homebrew/bin:$PATH
        pip_packages="/opt/homebrew/lib/python3.10/site-packages" 
    else
        pip_packages="/usr/local/lib/python3.10/site-packages" 
    fi

    # this is to use GNU sed, called gsed, instead of MacOS's POSIX
    export PATH=/usr/local/opt/gnu-sed/libexec/gnubin:$PATH
    # this is so we always use gsed
    alias sed='gsed'
fi

# include external .bashrc_$application if it exists
for bash_file in `ls -1 $HOME/.bashrc_*`; do
    . $bash_file
done

# This is for powerline, a prompt I've been playing with: https://powerline.readthedocs.io
if [ -f $pip_packages/powerline/bindings/bash/powerline.sh ]; then
    powerline-daemon -q
    POWERLINE_BASH_CONTINUATION=1
    POWERLINE_BASH_SELECT=1
    . $pip_packages/powerline/bindings/bash/powerline.sh
fi

# TODO: put old prompts into docs for future travelers
# this prompt one is only if emojis already work in your terminal :3
# PS1="\`if [ \$? = 0 ]; then echo 💙; else echo 😔; fi\` \[\e[94m\][\@]\[\e[0m\]\\$ "
# use this one if you don't have emojis in your terminal
# adds a smileyface on successful commands and a wat face otherwise :D
# prompt will show the user.time and that is it, for now. 
# PS1="\`if [ \$? = 0 ]; then echo \[\e[32m\]^_^\[\e[0m\]; else echo \[\e[31m\]O_O\[\e[0m\]; fi\`[\u.\@]\\$ "
