#!/bin/bash
column -t -s, -n "$@" | less -F -S -X -F
