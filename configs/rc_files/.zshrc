# locale asshattery
export LANG=en_US.UTF-8
export LC_CTYPE=$LANG

# make noise stop
unsetopt beep

# Turn on the magic completion!
fpath=($fpath $HOME/.zsh) # For extra zsh completion files
export FPATH
zstyle :compinstall filename ~/.zshrc
autoload -U compinit
compinit

# Set up the magic for vcs_info
autoload +X vcs_info 2>/dev/null || vcs_info() {}
zstyle ':vcs_info:*' enable git cvs svn #hg #bzr is slower than balls
zstyle ':vcs_info:*' disable-patterns "$HOME"
zstyle ':vcs_info:*' formats '%s %b'
zstyle ':vcs_info:git*:*' get-revision true
zstyle ':vcs_info:git*:*' formats '%8>>%i%>> %s %b'
zstyle ':vcs_info:git*:*' actionformats '%8>>%i%>> %B%F{red}%a%f%%b %b'
#### Monkeypatch+botch
VCS_INFO_detect_git() {
    setopt localoptions NO_shwordsplit

    [[ $1 == '--flavours' ]] && { print -l git-p4 git-svn; return 0 }

    if VCS_INFO_check_com ${vcs_comm[cmd]} && ${vcs_comm[cmd]} rev-parse --is-inside-work-tree &> /dev/null ; then
        vcs_comm[gitdir]="$(${vcs_comm[cmd]} rev-parse --git-dir 2> /dev/null)" || return 1
        if   [[ -d ${vcs_comm[gitdir]}/svn ]]             ; then vcs_comm[overwrite_name]='git-svn'
        elif [[ -d ${vcs_comm[gitdir]}/refs/remotes/p4 ]] ; then vcs_comm[overwrite_name]='git-p4' ;
        elif [[ $HOME/.git == ${vcs_comm[gitdir]} ]]      ; then return 1                          ; fi
        return 0
    fi
    return 1
}

setopt extended_glob
# Set variables of useful.
#xport PS1='Pi!%n@%h [#%~] ' IRC style nick!user@host :)
export PROMPT='🐧 %n@%m:%~ ' # jesse@host:~/public_html $ 
# VCS info, if available, stopped jobs and number of shell levels on the right
setopt PROMPT_SUBST
setopt TRANSIENT_RPROMPT
export RPROMPT='${vcs_info_msg_0_} %(1j.%B%j%b.)%(2L.%U%L%u.)'
export HOSTNAME=`hostname`
export CORRECT_IGNORE="_*"

# Set a non-shit history
export HISTSIZE=2000
export HISTFILE=~/.zsh_history
export SAVEHIST=2000
setopt APPEND_HISTORY
setopt EXTENDED_HISTORY
setopt HIST_NO_STORE
setopt HIST_IGNORE_DUPS
setopt INC_APPEND_HISTORY
#this is irritating, so I commented it.
#setopt SHARE_HISTORY

# Set miscellaneous options/variables
setopt CORRECT
setopt NOHUP
setopt AUTO_CONTINUE
setopt NO_CHECK_JOBS
setopt INTERACTIVECOMMENTS
setopt NO_BG_NICE
setopt PROMPT_SP
setopt PROMPTCR
setopt COMPLETE_IN_WORD

# tab completion for PID :D
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:kill:*' force-list always

# Ignore _functions for commands that don't exist
zstyle ':completion:*:functions' ignored-patterns '_*'

# With commands like `rm' it's annoying if one gets offered the same
# filename again even if it is already on the command line. To avoid
# that:
zstyle ':completion:*:rm:*' ignore-line yes

## on processes completion complete all user processes
if [[ $UID == 0 ]] {
    zstyle ':completion:*:processes' command 'ps axuw'
} else {
    zstyle ':completion:*:processes' command 'ps -fu$USER ww'
}

# Set options for cd
export DIRSTACKSIZE=20
setopt AUTO_PUSHD
#setopt PUSHD_MINUS
setopt PUSHDTOHOME
setopt PUSHD_IGNORE_DUPS
alias dirs='builtin dirs -v'
cdpath=( ~ )
swapd() {
    emulate -L zsh
    unsetopt PUSHDTOHOME
    pushd
}

# Set some aliases
alias history="history 0"
alias nukehost="ssh-keygen -R"
alias now="date +%H%M%S"
alias now:="date +%T"
alias today="date +%Y%m%d"
alias today_="date +%Y_%m_%d"
alias vi=vim
alias sharehistory="fc -RI"

if which lesspipe 1>/dev/null 2>&1; then
    eval "`lesspipe`"
fi

# SSH key magic
if which keychain 1>/dev/null 2>&1;then 
    [[ -o interactive ]] && keychain --inherit any -q -Q --ignore-missing --nogui id_dsa id_rsa identity 
    test -f ~/.keychain/$HOSTNAME-sh && . ~/.keychain/$HOSTNAME-sh
fi

# Set a decent ls depending on environment
LSOPTS="aFGh"
#get color
case `uname -s` in
    FreeBSD|Darwin)
        LSOPTS="G$LSOPTS"
        ;;
    Linux)
        LSOPTS="$LSOPTS --color"
        ;;
esac

alias ls="ls -$LSOPTS"
alias ll="ls -hal | less"

# title magicking 
function title {
    [[ "$TERM_PROGRAM" == "Apple_Terminal" && -z "$INSIDE_EMACS" ]] && \
	printf '\e]7;%s\a' "file://$HOSTNAME${PWD// /%20}"

    if [[ $TERM == screen* ]] {
      # Use these two for GNU Screen:
      print -nR $'\033k'$1$'\033'\\\

      print -nR $'\033]0;'$2$'\a'
    } elif [[ $TERM == xterm* || $TERM == "rxvt" ]] {
      # Use this one instead for XTerms:
      print -nR $'\033]0;'$*$'\a'
    }
}

function precmd {
    title "${USER:#pi}@$HOSTNAME $PWD"
    vcs_info
}

function preexec {
    emulate -L zsh
    local -a cmd; cmd=(${(z)1})
    title "${USER:#pi}@$HOSTNAME $cmd[1]:t" "$cmd[2,-1]"
}

# Some better bindings ripped off of, for some reason, redhate.
bindkey ' ' magic-space
bindkey "^R" redisplay

# meta-q pushes to the command stack, pops it back up after the next cmd.
bindkey '\033q' push-line

# Create an undo binding
bindkey "^Z" undo
bindkey -M vicmd "^Z" undo

# create a binding like meta-x for emacs mode
bindkey "^X^X" execute-named-cmd
bindkey -M vicmd "^X^X" execute-named-cmd

# fsr this is bound to _expand_word, and I don't think that's correct.
bindkey "^Xe" expand-word
bindkey "^Xe" expand-word

# Default bindings for these suck.
[[ -z "$terminfo[kcuu1]" ]] || bindkey -M viins "$terminfo[kcuu1]" up-line-or-history
[[ -z "$terminfo[kcud1]" ]] || bindkey -M viins "$terminfo[kcud1]" down-line-or-history
bindkey -M viins "\033[A" up-line-or-history
bindkey -M viins "\033[B" down-line-or-history
#[[ -z "$terminfo[kcuu1]"  ]] && bindkey -M viins "${terminfo[kcuu1]/O/[}" up-line-or-history
#[[ -z "$terminfo[kcud1]"  ]] && bindkey -M viins "${terminfo[kcud1]/O/[}" down-line-or-history


# Uniquify my $PATH
#source ${ZDOTDIR:-~}/.zshenv
#typeset -gU path cdpath manpath fpath

[[ -f ~/bin/xtfix ]] && ~/bin/xtfix
MAILCHECK=0
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"

autoload -U +X bashcompinit && bashcompinit

# terraform
complete -o nospace -C /usr/local/bin/terraform terraform
