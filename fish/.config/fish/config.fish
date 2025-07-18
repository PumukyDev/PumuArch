if status is-interactive
    # Commands to run in interactive sessions can go here
end

set fish_greeting


############
## PROMPT ##
############
function fish_prompt
    set -l last_status $status
    set -l cyan (set_color -o cyan)
    set -l yellow (set_color -o yellow)
    set -l white (set_color -o white)
    set -g red (set_color -o red)
    set -g blue (set_color -o blue)
    set -l green (set_color -o green)
    set -g normal (set_color normal)

    set -l ahead (_git_ahead)
    set -g whitespace ' '

    if test $last_status = 0
        #set initial_indicator "$white󰣇 "
        set status_indicator "$white❯"
    else
        set initial_indicator "$red✖ $last_status"
        set status_indicator "$red❯$red❯$red❯"
    end
    set -l cwd $cyan(basename (prompt_pwd))

    if [ (_git_branch_name) ]

        if test (_git_branch_name) = master
            set -l git_branch (_git_branch_name)
            set git_info "$normal git:($red$git_branch$normal)"
        else
            set -l git_branch (_git_branch_name)
            set git_info "$normal git:($blue$git_branch$normal)"
        end

        if [ (_is_git_dirty) ]
            set -l dirty "$yellow ✗"
            set git_info "$git_info$dirty"
        end
    end

    # Notify if a command took more than 5 minutes
    if [ "$CMD_DURATION" -gt 300000 ]
        echo The last command took (math "$CMD_DURATION/1000") seconds.
    end

    echo -n -s $initial_indicator $whitespace $cwd $git_info $whitespace $ahead $status_indicator $whitespace
end

function _git_ahead
    set -l commits (command git rev-list --left-right '@{upstream}...HEAD' 2>/dev/null)
    if [ $status != 0 ]
        return
    end
    set -l behind (count (for arg in $commits; echo $arg; end | grep '^<'))
    set -l ahead (count (for arg in $commits; echo $arg; end | grep -v '^<'))
    switch "$ahead $behind"
        case '' # no upstream
        case '0 0' # equal to upstream
            return
        case '* 0' # ahead of upstream
            echo "$blue↑$normal_c$ahead$whitespace"
        case '0 *' # behind upstream
            echo "$red↓$normal_c$behind$whitespace"
        case '*' # diverged from upstream
            echo "$blue↑$normal$ahead $red↓$normal_c$behind$whitespace"
    end
end

function _git_branch_name
    echo (command git symbolic-ref HEAD 2>/dev/null | sed -e 's|^refs/heads/||')
end

function _is_git_dirty
    echo (command git status -s --ignore-submodules=dirty 2>/dev/null)
end

#Alias executables

function doomemacs
    nohup ~/.emacs.d/bin/doom run >/dev/null 2>&1 &
end

#############
## Aliases ##
#############

# Cd
alias cd.="cd .."
alias cd.2="cd ../.."
alias cd.3="cd ../../.."
alias cd.4="cd ../../../.."


alias cd.5="cd ../../../../.."

alias hm="cd ~"

# grep
alias grep="rg"
alias egrep="eg -E"
alias fgrep="rg -F"

## Listing stuff ##

# Normal listing
#alias l="eza -F --icons --group-directories-first"
#alias ls="eza -F --icons --group-directories-first"

# All listing (show stuff hidden)
#alias la="eza -aF --icons --group-directories-first"

# Long listing
alias ll="eza -lahF --icons --group-directories-first"

# Rescursive listing
#alias lr="eza -RF --icons --group-directories-first"

# Tree listing
#alias lt="eza -TF --icons --group-directories-first"

# Directory listing
#alias ls="eza -DF --icons --group-directories-first" #-F displays type indicator by file names


# Confirm before overwriting files and make it verbose
alias cp="cp -iv"
alias mv="mv -iv"
alias rm="rm -iv"

# Mkdir will create parents dirs and will be verbose
alias mkdir="mkdir -pv"

# Human readbale flags
alias df="df -h"
alias du="du -h"
alias free="free -h"

# Better showing content
alias cat="bat"

# Simpling quitting shell
alias q="exit"

# Show IP
alias myip="curl ipinfo.io/ip"

# Simple clear
alias cl="clear"


alias img="kitten icat"


alias cleartarget='echo "" > ~/.config/qtile/themes/environment/target.txt'

#Export environment variables#
set -x DYLAN ~/Desktop/Adrian/VSCode/DYLAN
set -x OPEN_DYLAN_HOME $DYLAN/opendylan-2024.1


#PATH configuration#
set -x PATH $PATH ~/Bin $OPEN_DYLAN_HOME/bin

## THEMING ##

fish_config theme choose "Dracula Official"

# default umask #
umask 027

set -x LIBVIRT_DEFAULT_URI 'qemu:///system'




alias vu='vagrant up --provision'
alias vh='vagrant halt'
alias vr='vagrant reload --provision'
alias vs='vagrant ssh'
alias vd='vagrant destroy -f'
alias vp='vagrant provision'


alias 'vpnon'='wg-quick up wg0'
alias 'vpnoff'='wg-quick down wg0'


alias 'kali'='docker run -it --rm -v /home/adrian/desktop/VSCode/bowwe-security:/bowwe-security kalilinux/kali-rolling /bin/bash'
