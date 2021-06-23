#!/usr/bin/env bash
set -x

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$CURRENT_DIR"/utils.sh

create_rime_window() {
    local rime_window_pane
    rime_window_pane=$(tmux new-window -F ":#{window_id}.#{pane_id}" -P -d -n "[rime]" "bash --norc --noprofile")
    pane_exec "$rime_window_pane" "$CURRENT_DIR/tmux_rime.sh $rime_window_pane"
}

main() {
    create_rime_window
    exit 0
}

main "$@"
