#!/usr/bin/env bash
set -x

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$CURRENT_DIR"/utils.sh
TMUX_RIME_SERVER="$CURRENT_DIR"/../tmux_rime/tmux_rime_server.py

current_window_pane=""
rime_window_pane=""
tmux_prefix=""
commands_pipe='/tmp/tmux-rime.client'

enable_rime_mode() {
    tmux set-window-option key-table tmux_rime
    tmux switch-client -T tmux_rime
    tmux_prefix="$(tmux show -gqv prefix)" # Save tmux prefix 
    tmux set-option -g prefix None
}

handle_exit() {
    # Restore status bar
    # TODO: Save status and status-format before start
    tmux set-option -g status on
    tmux set-option -g -u status-format

    # Restore prefix and key table
    tmux set-option -g prefix "$tmux_prefix"
    tmux set-window-option key-table root
    tmux switch-client -Troot

    local rime_window_id
    rime_window_id="$(echo $rime_window_pane | cut -d "." -f 2)"
    tmux kill-window -t "$rime_window_id"
}

init_rime_mode() {
    trap "handle_exit" EXIT
    "$TMUX_RIME_SERVER" &
    enable_rime_mode
}

insert_text() {
    local inserted_text
    inserted_text="${1#insert }"
    tmux send-key -l -t "$current_window_pane" "$inserted_text"
}

update_status() {
    local status_str

    if [[ "$1" == "status" ]]; then
        status_str="[ㄓ]"
    else
        status_str="${1#status }"
    fi
    tmux set -g status-format[0] "$status_str"
}


main() {
    current_window_pane="$1"
    rime_window_pane="$2"
    init_rime_mode

    while read -r -s statement; do
        echo "$current_window_pane" >> /tmp/pane
        echo "$statement" >> /tmp/statement
        case $statement in
            insert*)
                insert_text "$statement"
            ;;
            status*)
                update_status "$statement"
            ;;
            toggle-help)
                :
            ;;
            noop)
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
