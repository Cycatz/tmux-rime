#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

gmake -C "$CURRENT_DIR"/tmux_rime/rime_wrapper/
