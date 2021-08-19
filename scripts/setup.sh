#!/usr/bin/env bash
set -x

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$CURRENT_DIR"/utils.sh


commands_pipe='/tmp/tmux-rime.client'


create_rime_window() {
    local current_pane
    local rime_window_pane
    current_pane="$(tmux display-message -p -F ':#{window_id}.#{pane_id}')"
    rime_window_pane=$(tmux new-window -F ":#{window_id}.#{pane_id}" -P -d -n "[rime]" "bash --norc --noprofile")
    pane_exec "$rime_window_pane" "$CURRENT_DIR/tmux_rime.sh '$current_pane' '$rime_window_pane'"
}

setup_status_bar() {
    current_status="$(tmux show -gqv status-format[0])"
    tmux set-option -g status-format[0] "[ㄓ]"
    tmux set-option -g status-format[1] "$current_status"
    tmux set-option -g status 2
}

create_commands_pipe() {
    # TODO consider the condition that "$commands_pipe" is a regular file
    if [[ ! -p "$commands_pipe" ]]; then
        mkfifo -m 600 "$commands_pipe"
    fi
}

main() {
    create_rime_window
    create_commands_pipe
    setup_status_bar
    exit 0
}

main "$@"
