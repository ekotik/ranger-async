#!/usr/bin/python -O
# This file is part of ranger-async, the console file manager.  (coding: utf-8)
# License: GNU GPL version 3, see the file "AUTHORS" for details.

# =====================
# This embedded bash script can be executed by sourcing this file.
# It will cd to ranger-async's last location after you exit it.
# The first argument specifies the command to run ranger-async, the
# default is simply "ranger-async". (Not this file itself!)
# The other arguments are passed to ranger-async.
"""":
temp_file="$(mktemp -t "ranger-async_cd.XXXXXXXXXX")"
ranger-async="${1:-ranger-async}"
if [ -n "$1" ]; then
    shift
fi
"$ranger-async" --choosedir="$temp_file" -- "${@:-$PWD}"
return_value="$?"
if chosen_dir="$(cat -- "$temp_file")" && [ -n "$chosen_dir" ] && [ "$chosen_dir" != "$PWD" ]; then
    cd -- "$chosen_dir"
fi
rm -f -- "$temp_file"
return "$return_value"
"""

from __future__ import absolute_import, division, print_function

import asyncio
import sys

# Need to find out whether or not the flag --clean was used ASAP,
# because --clean is supposed to disable bytecode compilation
ARGV = sys.argv[1 : sys.argv.index("--")] if "--" in sys.argv else sys.argv[1:]
sys.dont_write_bytecode = "-c" in ARGV or "--clean" in ARGV

# Start ranger-async
import ranger_async  # NOQA pylint: disable=import-self,wrong-import-position

sys.exit(asyncio.run(ranger_async.main()))  # pylint: disable=no-member
