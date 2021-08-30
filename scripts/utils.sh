#!/usr/bin/env bash

create_pipe() {
    local pipe_path=$(mktemp -u "${TMPDIR:-/tmp}/tmux_rime.XXXXXXXX")
    mkfifo -m 600 "$pipe_path"
    echo "$pipe_path"
}

pane_exec() {
  local pane_id="$1"
  local pane_command="$2"

  tmux send-keys -t "$pane_id" "$pane_command"
  tmux send-keys -t "$pane_id" Enter
}
