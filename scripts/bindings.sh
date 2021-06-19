#!/usr/bin/env bash 

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$CURRENT_DIR"/env.sh

tmux_rime_bind() {
    local key="$1"
    local command="$2"

    tmux bind-key -T tmux_rime "$key" run-shell -b "$CURRENT_DIR/send_input.sh '$command'"
}

bind_reg_keys() {
    # for char in $TMUX_RIME_REG_KEYS; do
    for char in {a..z} {A..Z}; do
        tmux_rime_bind "$char"   "key:$char:main"
        tmux_rime_bind "C-$char" "key:$char:ctrl"
        tmux_rime_bind "M-$char" "key:$char:alt"
    done
}

bind_special_keys() {
    tmux_rime_bind "Escape" "exit"
    tmux_rime_bind "?"      "toggle-help"
    tmux_rime_bind "Tab"    "noop"
    tmux_rime_bind "Any"    "noop"
}

main() {
    bind_reg_keys
    bind_special_keys
}

main "$@"
exit 0
