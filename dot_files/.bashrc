##############################################################################
#             @jessebot's personal .bashrc (and .bash_profile)               #
##############################################################################


# -------------------------------------------------------------------------- #
#                                 General                                    #
# -------------------------------------------------------------------------- #

# I hate bells
set bell-style none

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# default editor
export EDITOR=vim

# make all colors work by default
export TERM=xterm-256color

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"


# -------------------------------------------------------------------------- #
#                                 History                                    #
# -------------------------------------------------------------------------- #

# don't put duplicate lines or lines starting with space in the history.
HISTCONTROL=ignoreboth
# append to the history file, don't overwrite it
shopt -s histappend
# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=10000
HISTFILESIZE=20000
# for setting time stamps on history
HISTTIMEFORMAT="%d/%m/%y %T "


# -------------------------------------------------------------------------- #
#                                 Pathing                                    #
# -------------------------------------------------------------------------- #

# go
GOROOT=$HOME
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin

# python packages' default location when you do pip3 install --user package
export PATH=$PATH:$HOME/.local/bin

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Linux PATH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [[ $(uname) == *"Linux"* ]]; then
    # this is for iptables on debian, which is elusive
    export PATH=$PATH:/usr/sbin:/usr/share
    # for snap package manager packages
    export PATH=$PATH:/snap/bin
    # ~ HomeBrew on Linux ~ #
    export HOMEBREW_PREFIX=/home/linuxbrew/.linuxbrew
    export HOMEBREW_CELLAR=/home/linuxbrew/.linuxbrew/Cellar
    export HOMEBREW_REPOSITORY=/home/linuxbrew/.linuxbrew/Homebrew
    export MANPATH=$MANPATH:/home/linuxbrew/.linuxbrew/share/man
    export INFOPATH=$INFOPATH:/home/linuxbrew/.linuxbrew/share/info
    export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin
    pip_packages="/home/linuxbrew/.linuxbrew/lib/python3.10/site-packages"
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ macOS PATH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [[ $(uname) == *"Darwin"* ]]; then
    # don't warn me that BASH is deprecated, becasuse it is already upgraded
    export BASH_SILENCE_DEPRECATION_WARNING=1
    # bash completion on macOS
    [[ -r "/usr/local/etc/profile.d/bash_completion.sh" ]] && \
        . "/usr/local/etc/profile.d/bash_completion.sh"

    # check if this an M1/M2 mac
    if [ $(uname -a | grep arm > /dev/null ; echo $?) -eq 0 ]; then
        # On M1/M2: brew default installs here
        export PATH=/opt/homebrew/bin:$PATH
        pip_packages="/opt/homebrew/lib/python3.10/site-packages"
    else
        # For older macs before the M1, pre-2020
        pip_packages="/usr/local/lib/python3.10/site-packages"
    fi

    # Load GNU sed, called gsed, instead of MacOS's POSIX sed
    export PATH=/usr/local/opt/gnu-sed/libexec/gnubin:$PATH
    # Always use GNU sed
    alias sed='gsed'
fi


# -------------------------------------------------------------------------- #
#                                 ALIASES                                    #
# -------------------------------------------------------------------------- #

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Typos <3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
alias pign='ping'
alias gtop='gotop'
# can never spell clear
alias celar='clear'
alias clar='clear'
# clear, but in dutch
alias leegmaken='clear'
alias gti='git'
alias gtt='git'
# can't spell tree
alias ter='tree'
alias tre='tree'
alias tere='tree'
# can't spell python
alias pthyon='python3.10'
alias ptyhon='python3.10'
alias pythong='python3.10'
# alias because python2-python3.9 still in some places
alias python='python3.10'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ General ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# colordiff - diff, but with colors for accessibility
alias diff='colordiff -uw'
# always use vim instead of vi, TODO: check if vim installed?
alias vi='vim'
# we love a good tracer t
alias tracert='traceroute'
# whoami, whereami, whoareyou?
alias whereami='hostname'
alias whoareyou='echo "Your friend :)"'
# scrncpy installs adb for you, but it's awkward to use, so we just alias it
alias adb='scrcpy.adb'
# quick to do
alias todo='vim ~/todo.md'
# I never remember what the img2sixel command is called
alias sixel='img2sixel'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ls ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# lsd instead of ls for colors/icons
alias ls='lsd -a'
# lsd and list long, human readable file sizes, show hidden files
alias ll='lsd -hal'
# sort by most recent and reversed, so the most recent file is the last
# helpful for directories with lots of files
alias lt='lsd -atr'
# same as above, but long
alias llt='lsd -haltr'
# lsd already has a fancier tree command with icons
alias tree='lsd --tree --depth=2'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ grep ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# always use colors
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias grpe='grep'
alias gerp='grep'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ cat ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# TODO: Write those docs with links to both apps (rich, and batcat)
# Function to use the best syntax highlighting app for the job
function dog {
    # if file has more lines than legnth of the terminal use app with pager
    too_long=false
    if [ $(wc -l $1 | awk '{print $1}') -gt $(tput lines) ]; then
        too_long=true
    fi

    # if this is a markdown or csv file, ALWAYS use rich to print the data
    if [[ "$1" == *".md" ]] || [[ "$1" == *".csv" ]]; then
        if $too_long; then
            # pager allows moving with j for down, k for up, and :q for quit
            rich --pager $1
        else
            rich $1
            echo ""
        fi
    else
        # On Linux, use batcat - sytnax highlighting + git support and pager
        if [[ $(uname) == *"Linux"* ]]; then
            batcat $1
        else
            # add line numbers
            rich -n $1
            echo ""
        fi
    fi
}

alias cat='dog'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ git ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
alias gc='git commit -m'
alias gs='git status'
# check all directories below current directory for their git status
alias gsa='ls -1 -A | xargs -I % sh -c "figlet % | lolcat ; cd %; git status --short; cd - > /dev/null; echo ''"'
alias gd='git diff'
alias ga='git add .'
alias gph='git push && git push --tags'
alias gpl='git pull'
# glab is gitlab's cli, but I always type gl by accident
alias gl='glab'


# -------------------------------------------------------------------------- #
#                               COMPLETION                                   #
# -------------------------------------------------------------------------- #

# ~~~~~~~~~~~~~~~~ enable programmable completion features ~~~~~~~~~~~~~~~~~ #
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ nvm ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
export NVM_DIR="$HOME/.nvm"
# This loads nvm
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
# This loads nvm bash_completion
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Terraform ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
complete -C /usr/local/bin/terraform terraform


# -------------------------------------------------------------------------- #
# --------------------------  CUSTOM FUNCTIONS ----------------------------- #
# -------------------------------------------------------------------------- #

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ base64 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
function b64 {
    echo -n $1 | base64
}
function b64d {
    echo -n $1 | base64 --decode
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ag (search repos) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
function agr {
    if [ $2 = "y"]; then
        for $repo in $(ls -1 $REPOS); do
            cd $REPOS/$repo && git pull
        done
    fi

    ag $1 $REPOS
}

# -------------------------------------------------------------------------- #
#                            Other Load on start                             #
# -------------------------------------------------------------------------- #

# include external .bashrc_$application if it exists
# example: if there's a .bashrc_k8s, source that as well
for bash_file in `ls -1 $HOME/.bashrc_*`; do
    . $bash_file
done

# This is for powerline, a fancy extensible prompt: https://powerline.readthedocs.io
if [ -f $pip_packages/powerline/bindings/bash/powerline.sh ]; then
    powerline-daemon -q
    POWERLINE_BASH_CONTINUATION=1
    POWERLINE_BASH_SELECT=1
    . $pip_packages/powerline/bindings/bash/powerline.sh
fi

# -------------------------------------------------------------------------- #
#                            PERSONAL MOTD                                   #
# -------------------------------------------------------------------------- #

# run neofetch, a system facts cli script, immediately when we login anywhere
echo ""
neofetch
echo -e "\n"
export KUBECONFIG=~/.kube/kubeconfig
export KUBECONFIG=~/.kube/kubeconfig
