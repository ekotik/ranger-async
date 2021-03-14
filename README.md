ranger-async 1.9.3
============

ranger-async is unstable, fake and buggy personal learning project for Python
asyncio stuff which brings `None` improvements to the ranger FM.

Use https://github.com/ranger/ranger original instead.

<img src="https://ranger-async.github.io/ranger-async_logo.png" width="150">

[![Build Status](https://travis-ci.org/ranger-async/ranger-async.svg?branch=master)](https://travis-ci.org/ranger-async/ranger-async)
<a href="https://repology.org/metapackage/ranger-async/versions">
  <img src="https://repology.org/badge/latest-versions/ranger-async.svg" alt="latest packaged version(s)">
</a>

ranger-async is a console file manager with VI key bindings.  It provides a
minimalistic and nice curses interface with a view on the directory hierarchy.
It ships with `rifle`, a file launcher that is good at automatically finding
out which program to use for what file type.

![screenshot](https://raw.githubusercontent.com/ranger-async/ranger-async-assets/master/screenshots/screenshot.png)

For `mc` aficionados there's also the multi-pane viewmode.

<p>
<img src="https://raw.githubusercontent.com/ranger-async/ranger-async-assets/master/screenshots/twopane.png" alt="two panes" width="49%" />
<img src="https://raw.githubusercontent.com/ranger-async/ranger-async-assets/master/screenshots/multipane.png" alt="multiple panes" width="49%" />
</p>

This file describes ranger-async and how to get it to run.  For instructions on the
usage, please read the man page (`man ranger-async` in a terminal).  See `HACKING.md`
for development-specific information.

For configuration, check the files in `ranger_async/config/` or copy the
default config to `~/.config/ranger-async` with `ranger-async --copy-config`
(see [instructions](#getting-started)).

The `examples/` directory contains several scripts and plugins that demonstrate how
ranger-async can be extended or combined with other programs.  These files can be
found in the git repository or in `/usr/share/doc/ranger-async`.

A note to packagers: Versions meant for packaging are listed in the changelog
on the website.


About
-----
* Authors:     see `AUTHORS` file
* License:     GNU General Public License Version 3
* Website:     *TODO: fix website link*
* Download:    *TODO: fix download link*
* Bug reports: https://github.com/ekotik/ranger-async/issues
* git clone    https://github.com/ekotik/ranger-async.git


Design Goals
------------
* An easily maintainable file manager in a high level language
* A quick way to switch directories and browse the file system
* Keep it small but useful, do one thing and do it well
* Console-based, with smooth integration into the unix shell


Features
--------
* UTF-8 Support  (if your Python copy supports it)
* Multi-column display
* Preview of the selected file/directory
* Common file operations (create/chmod/copy/delete/...)
* Renaming multiple files at once
* VIM-like console and hotkeys
* Automatically determine file types and run them with correct programs
* Change the directory of your shell after exiting ranger-async
* Tabs, bookmarks, mouse support...


Dependencies
------------
* Python (`>=2.6` or `>=3.1`) with the `curses` module
  and (optionally) wide-unicode support
* A pager (`less` by default)

### Optional dependencies

For general usage:

* `file` for determining file types
* `chardet` (Python package) for improved encoding detection of text files
* `sudo` to use the "run as root" feature
* `python-bidi` (Python package) to display right-to-left file names correctly
  (Hebrew, Arabic)

For enhanced file previews (with `scope.sh`):

* `img2txt` (from `caca-utils`) for ASCII-art image previews
* `w3mimgdisplay`, `ueberzug`, `mpv`, `iTerm2`, `kitty`, `terminology` or `urxvt` for image previews
* `convert` (from `imagemagick`) to auto-rotate images and for SVG previews
* `ffmpegthumbnailer` for video thumbnails
* `highlight`, `bat` or `pygmentize` for syntax highlighting of code
* `atool`, `bsdtar`, `unrar` and/or `7z` to preview archives
* `bsdtar`, `tar`, `unrar`, `unzip` and/or `zipinfo` (and `sed`) to preview
  archives as their first image
* `lynx`, `w3m` or `elinks` to preview html pages
* `pdftotext` or `mutool` (and `fmt`) for textual `pdf` previews, `pdftoppm` to
  preview as image
* `djvutxt` for textual DjVu previews, `ddjvu` to preview as image
* `calibre` or `epub-thumbnailer` for image previews of ebooks
* `transmission-show` for viewing BitTorrent information
* `mediainfo` or `exiftool` for viewing information about media files
* `odt2txt` for OpenDocument text files (`odt`, `ods`, `odp` and `sxw`)
* `python` or `jq` for JSON files
* `fontimage` for font previews
* `openscad` for 3D model previews (`stl`, `off`, `dxf`, `scad`, `csg`)

Installing
----------
Use the package manager of your operating system to install ranger-async.
You can also install ranger-async through PyPI: ```pip install ranger-async-fm```.

<details>
  <summary>
    Check current version:
    <sub>
      <a href="https://repology.org/metapackage/ranger-async/versions">
        <img src="https://repology.org/badge/tiny-repos/ranger-async.svg" alt="Packaging status">
      </a>
    </sub>
  </summary>
  <a href="https://repology.org/metapackage/ranger-async/versions">
    <img src="https://repology.org/badge/vertical-allrepos/ranger-async.svg" alt="Packaging status">
  </a>
</details>

### Installing from a clone
Note that you don't *have* to install ranger-async; you can simply run `ranger_async.py`.

To install ranger-async manually:
```
sudo make install
```

This translates roughly to:
```
sudo python setup.py install --optimize=1 --record=install_log.txt
```

This also saves a list of all installed files to `install_log.txt`, which you can
use to uninstall ranger-async.


Getting Started
---------------
After starting ranger-async, you can use the Arrow Keys or `h` `j` `k` `l` to
navigate, `Enter` to open a file or `q` to quit.  The third column shows a
preview of the current file.  The second is the main column and the first shows
the parent directory.

Ranger-Async can automatically copy default configuration files to `~/.config/ranger-async`
if you run it with the switch `--copy-config=( rc | scope | ... | all )`.
See `ranger-async --help` for a description of that switch.  Also check
`ranger_async/config/` for the default configuration.


Going Further
---------------
* To get the most out of ranger-async, read the [Official User Guide](https://github.com/ranger/ranger/wiki/Official-user-guide).
* For frequently asked questions, see the [FAQ](https://github.com/ranger/ranger/wiki/FAQ%3A-Frequently-Asked-Questions).
* For more information on customization, see the [wiki](https://github.com/ranger/ranger/wiki).


Community
---------------
For help, support, or if you just want to hang out with us, you can find us here:
* **IRC**: channel **#ranger-async** on [freenode](https://freenode.net/kb/answer/chat)
* **Reddit**: [r/ranger-async](https://www.reddit.com/r/ranger-async/)
