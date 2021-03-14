#!/usr/bin/env python
# This file is part of ranger-async, the console file manager.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

from __future__ import (absolute_import, division, print_function)

from hashlib import sha512
import os
import shutil

from setuptools import setup
from setuptools.command.install_lib import install_lib

import ranger_async


SCRIPTS_PATH = 'build_scripts'
EXECUTABLES_PATHS = ['/ranger_async/data/scope.sh']


def findall(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]


def hash_file(path):
    with open(path, 'rb') as fobj:
        return sha512(fobj.read()).digest()


def scripts_hack(*scripts):
    ''' Hack around `pip install` temporary directories '''
    if not os.path.exists(SCRIPTS_PATH):
        os.makedirs(SCRIPTS_PATH)
    scripts_path = []
    for src_path, basename in scripts:
        dest_path = os.path.join(SCRIPTS_PATH, basename)
        if not os.path.exists(dest_path) or \
                (os.path.exists(src_path) and hash_file(src_path) != hash_file(dest_path)):
            shutil.copy(src_path, dest_path)
        scripts_path += [dest_path]
    return scripts_path


class InstallLib(install_lib):
    def run(self):
        install_lib.run(self)

        # Make executables executable
        for path in self.get_outputs():
            for exe_path in EXECUTABLES_PATHS:
                if path.endswith(exe_path):
                    mode = ((os.stat(path).st_mode) | 0o555) & 0o7777
                    print('changing mode of %s to %o' % (path, mode))
                    os.chmod(path, mode)


def main():
    setup(
        name='ranger-async-fm',
        description='Vim-like file manager',
        long_description=ranger_async.__doc__,
        version=ranger_async.__version__,
        author=ranger_async.__author__,
        author_email=ranger_async.__email__,
        license=ranger_async.__license__,
        url='https://ranger-async.github.io',
        keywords='file-manager vim console file-launcher file-preview',
        classifiers=[
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: MacOS',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Desktop Environment :: File Managers',
            'Topic :: Utilities',
        ],

        cmdclass={'install_lib': InstallLib},

        scripts=scripts_hack(
            ('ranger_async.py', 'ranger-async'),
            ('ranger_async/ext/rifle.py', 'rifle'),
        ),
        data_files=[
            ('share/applications', [
                'doc/ranger-async.desktop',
            ]),
            ('share/man/man1', [
                'doc/ranger-async.1',
                'doc/rifle.1',
            ]),
            ('share/doc/ranger-async', [
                'doc/colorschemes.md',
                'CHANGELOG.md',
                'HACKING.md',
                'README.md',
            ]),
            ('share/doc/ranger-async/config', findall('doc/config')),
            ('share/doc/ranger-async/config/colorschemes', findall('doc/config/colorschemes')),
            ('share/doc/ranger-async/examples', findall('examples')),
            ('share/doc/ranger-async/tools', findall('doc/tools')),
        ],
        package_data={
            'ranger-async': [
                'data/*',
                'config/rc.conf',
                'config/rifle.conf',
            ],
        },
        packages=(
            'ranger_async',
            'ranger_async.api',
            'ranger_async.colorschemes',
            'ranger_async.config',
            'ranger_async.container',
            'ranger_async.core',
            'ranger_async.ext',
            'ranger_async.ext.vcs',
            'ranger_async.gui',
            'ranger_async.gui.widgets',
        ),
    )


if __name__ == '__main__':
    main()
