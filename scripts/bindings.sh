#!/usr/bin/env bash 


CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TMUX_RIME_CLIENT="$CURRENT_DIR"/../tmux_rime/tmux_rime_client.py

source "$CURRENT_DIR"/env.sh
source "$CURRENT_DIR"/utils.sh


tmux_rime_bind() {
    local key="$1"
    local command="$2"

    tmux bind-key -T tmux_rime "$key" run-shell -b "'${TMUX_RIME_CLIENT}' ${command}"
}

bind_reg_keys() {
    # for char in $TMUX_RIME_REG_KEYS; do
    for char in {0..9} {a..z} {A..Z} "." "," "/" ; do
        tmux_rime_bind "$char"   "key -k '$char'"
        tmux_rime_bind "C-$char" "key -k '$char' -m ctrl"
        tmux_rime_bind "M-$char" "key -k '$char' -m alt"
    done

    # Special case for semicolon ';'
    tmux_rime_bind "\;"   "key -k ';'"
    tmux_rime_bind "C-\;" "key -k ';' -m ctrl"
    tmux_rime_bind "M-\;" "key -k ';' -m alt"
}

bind_special_keys() {
    tmux_rime_bind "DS"     "key -k Delete"
    tmux_rime_bind "BSpace" "key -k Backspace"
    tmux_rime_bind "Space"  "key -k Space"
    tmux_rime_bind "Escape" "exit"
    tmux_rime_bind "?"      "toggle-help"
    tmux_rime_bind "Any"    "noop"
}

main() {
    bind_reg_keys
    bind_special_keys
}

main "$@"
exit 0
