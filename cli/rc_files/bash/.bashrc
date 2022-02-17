# Jessebot's personal .bash_profile/.bashrc
# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

## default editor
export EDITOR=vim

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

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# ls - human readable file sizes, show hidden files, enable colors
alias ls='ls -ha --color'
alias ll='ls -hal --color'
# colordiff - diff, but with colors for accessibility
alias diff='colordiff -uw'
# grep - always use colors
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
# typos <3
alias grpe='grep'
alias gerp='grep'
alias celar='clear'
alias gti='git'
# shorten commands
alias vi='vim'
alias tracert='traceroute'
# git speed up
alias gc='git commit -m'
# take that ghostscript
alias gs='git status'
alias gd='git diff'
alias ga='git add .'
alias gp='git push'

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

# go
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin

# brew on linux
export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin

# include external .bashrc_$application if it exists
if [ -f $HOME/.bashrc_k8s ]; then
    . $HOME/.bashrc_k8s
    . $HOME/.bashrc_k8s_completion
fi

if [ -f $HOME/.bashrc_helm ]; then
    . $HOME/.bashrc_helm
fi

if [ -f $HOME/.bashrc_azure ]; then
    . $HOME/.bashrc_azure
fi

if [ -f $HOME/.bashrc_env_variables ]; then
    . $HOME/.bashrc_env_variables
fi

# adds a smileyface on successful commands and a wat face otherwise :D
# prompt will show the user.time and that is it, for now. 
PS1="\`if [ \$? = 0 ]; then echo \[\e[32m\]^_^\[\e[0m\]; else echo \[\e[31m\]O_O\[\e[0m\]; fi\`[\u.\@]\\$ "
