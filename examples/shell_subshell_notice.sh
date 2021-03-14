# shellcheck shell=sh

# Compatible with ranger-async 1.5.3 through 1.9.*
#
# Change the prompt when you open a shell from inside ranger-async
#
# Source this file from your shell startup file (.bashrc, .zshrc etc) for it to
# work.

[ -n "$RANGER_ASYNC_LEVEL" ] && PS1="$PS1"'(in ranger-async) '
