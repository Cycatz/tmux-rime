#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$CURRENT_DIR"/env.sh


current_status="$(tmux show -gqv status-format[0])"
tmux set-option -g status-format[0] "ㄓ"  
tmux set-option -g status-format[1] "$current_status"
tmux set-option -g status 2
