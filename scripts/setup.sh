#!/usr/bin/env bash
set -x

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$CURRENT_DIR"/utils.sh

create_rime_window() {
    local current_pane, rime_window_pane
    current_pane="$(tmux display-message -p -F ':#{window_id}.#{pane_id}')"
    rime_window_pane=$(tmux new-window -F ":#{window_id}.#{pane_id}" -P -d -n "[rime]" "bash --norc --noprofile")
    pane_exec "$rime_window_pane" "$CURRENT_DIR/tmux_rime.sh '$current_pane' '$rime_window_pane'"
}

setup_status_bar() {
    current_status="$(tmux show -gqv status-format[0])"
    tmux set-option -g status-format[0] "Rime ㄓ"
    tmux set-option -g status-format[1] "$current_status"
    tmux set-option -g status 2
}

main() {
    create_rime_window
    setup_status_bar
    exit 0
}

main "$@"
