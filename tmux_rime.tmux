#!/usr/bin/env bash 

PLUGIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$PLUGIN_DIR"/scripts/utils.sh
source "$PLUGIN_DIR"/scripts/env.sh


tmux run-shell -b "bash --norc --noprofile $PLUGIN_DIR/scripts/config.sh"
tmux run-shell -b "$PLUGIN_DIR/scripts/bindings.sh"  

tmux bind-key "$TMUX_RIME_PREFIX" run-shell "$PLUGIN_DIR/scripts/tmux_rime.sh"
