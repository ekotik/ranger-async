# Automatically change the directory in fish after closing ranger-async
#
# This is a fish alias to automatically change the directory to the last visited
# one after ranger-async quits.
# To undo the effect of this function, you can type "cd -" to return to the
# original directory.
#
# Note: funcsave save the alias in fish's config files, you do not need to copy
# this file anywhere, just execute it once

function ranger-async-cd
    set dir (mktemp -t ranger-async_cd.XXX)
    ranger-async --choosedir=$dir
    cd (cat $dir) $argv
    rm $dir
    commandline -f repaint
end
funcsave ranger-async-cd

# To bind Ctrl-O to ranger-async-cd, save this in `~/.config/fish/config.fish`:
bind \co ranger-async-cd
