#!/usr/bin/env bash

create_pipe() {
    local pipe_path=$(mktemp -u "${TMPDIR:-/tmp}/tmux_rime.XXXXXXXX")
    mkfifo -m 600 "$pipe_path"
    echo "$pipe_path"
}
