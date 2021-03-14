# shellcheck shell=sh

# Compatible with ranger-async 1.4.2 through 1.9.*
#
# Automatically change the current working directory after closing ranger-async
#
# This is a shell function to automatically change the current working
# directory to the last visited one after ranger-async quits. Either put it into your
# .zshrc/.bashrc/etc or source this file from your shell configuration.
# To undo the effect of this function, you can type "cd -" to return to the
# original directory.

ranger-async_cd() {
    temp_file="$(mktemp -t "ranger-async_cd.XXXXXXXXXX")"
    ranger-async --choosedir="$temp_file" -- "${@:-$PWD}"
    if chosen_dir="$(cat -- "$temp_file")" && [ -n "$chosen_dir" ] && [ "$chosen_dir" != "$PWD" ]; then
        cd -- "$chosen_dir"
    fi
    rm -f -- "$temp_file"
}

# This binds Ctrl-O to ranger-async_cd:
bind '"\C-o":"ranger-async_cd\C-m"'
