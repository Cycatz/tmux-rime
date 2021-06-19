#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$CURRENT_DIR"/utils.sh

enable_tmux_rime () {
  tmux set-window-option key-table tmux_rime
  tmux switch-client -T tmux_rime
  state[tmux_prefix]="$(tmux show -gqv prefix)"
  tmux set-option -g prefix None
}

main() {

    # Initialize the command pipe
    COMMANDS_PIPE="$(create_pipe)"
    tmux set-environment COMMANDS_PIPE "$COMMANDS_PIPE" 
    # while read -r -s statement; do
    #     if [[ "$statement" == "exit" ]]; then
    #        break;
    #     fi
    # done < <(tail -f "$COMMANDS_PIPE")
    exit 0
}

main "$@"

