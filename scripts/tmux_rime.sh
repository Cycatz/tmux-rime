#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$CURRENT_DIR"/utils.sh

tmux_prefix=""
commands_pipe=""

enable_rime_mode() {
    tmux set-window-option key-table tmux_rime
    tmux switch-client -T tmux_rime
    tmux_prefix="$(tmux show -gqv prefix)" # Save tmux prefix 
    tmux set-option -g prefix None
}

set_commands_pipe() {
    # Initialize the command pipe
    commands_pipe="$(create_pipe)"
    tmux set-environment COMMANDS_PIPE "$commands_pipe" 
}

handle_exit() {
    rm -f "$commands_pipe"
    tmux set-environment -u COMMANDS_PIPE
    tmux set-option -g prefix "$tmux_prefix"
    tmux set-window-option key-table root
    tmux switch-client -Troot
}


init_rime_mode() {
    trap "handle_exit" EXIT
    enable_rime_mode
    set_commands_pipe
}

main() {

    init_rime_mode

    while read -r -s statement; do
        case $statement in
            key:*)
                :    
            ;;
            exit)
                break
            ;;
        esac
    done < <(tail -f "$commands_pipe")
    exit 0
}

main "$@"

