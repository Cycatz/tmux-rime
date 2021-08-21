#!/bin/bash

set -x
tmux_rime_directory="$1"
tmux_rime_server_log="$tmux_rime_directory/tmux_rime/tmux_rime_server.log"
tmux_rime_client_log="$tmux_rime_directory/tmux_rime/tmux_rime_client.log"
tmux_session_name="tmux_rime_debug"

tmux kill-session -t "$tmux_session_name"
tmux new-session -d -s "$tmux_session_name" -c "$tmux_rime_directory"
tmux split-window -t "$tmux_session_name" -h "tail -f $tmux_rime_server_log"
tmux split-window -t "$tmux_session_name" -v "tail -f $tmux_rime_client_log"
tmux attach-session -d -t tmux_rime_debug
