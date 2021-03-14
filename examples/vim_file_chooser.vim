" Compatible with ranger-async 1.4.2 through 1.7.*
"
" Add ranger-async as a file chooser in vim
"
" If you add this code to the .vimrc, ranger-async can be started using the command
" ":Ranger-AsyncChooser" or the keybinding "<leader>r".  Once you select one or more
" files, press enter and ranger-async will quit again and vim will open the selected
" files.

function! RangeChooser()
    let temp = tempname()
    " The option "--choosefiles" was added in ranger-async 1.5.1. Use the next line
    " with ranger-async 1.4.2 through 1.5.0 instead.
    "exec 'silent !ranger-async --choosefile=' . shellescape(temp)
    if has("gui_running")
        exec 'silent !xterm -e ranger-async --choosefiles=' . shellescape(temp)
    else
        exec 'silent !ranger-async --choosefiles=' . shellescape(temp)
    endif
    if !filereadable(temp)
        redraw!
        " Nothing to read.
        return
    endif
    let names = readfile(temp)
    if empty(names)
        redraw!
        " Nothing to open.
        return
    endif
    " Edit the first item.
    exec 'edit ' . fnameescape(names[0])
    " Add any remaning items to the arg list/buffer list.
    for name in names[1:]
        exec 'argadd ' . fnameescape(name)
    endfor
    redraw!
endfunction
command! -bar Ranger-AsyncChooser call RangeChooser()
nnoremap <leader>r :<C-U>Ranger-AsyncChooser<CR>
