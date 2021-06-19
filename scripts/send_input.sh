#!/usr/bin/env bash 
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$CURRENT_DIR"/env.sh

tmux wait-for -L tmux_rime_commands

echo "$1" >> "$COMMANDS_PIPE"

tmux wait-for -U tmux_rime_commands

exit 0
