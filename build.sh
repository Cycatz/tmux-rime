#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

make -C "$CURRENT_DIR"/tmux_rime/rime_wrapper/
