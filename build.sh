#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

gmake -C "$CURRENT_DIR"/rime-server/rime_wrapper/
