#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)

import sys
import time

sys.path.insert(0, '../..')
sys.path.insert(0, '.')


def main():
    import ranger_async.container.directory
    import ranger_async.core.shared
    import ranger_async.container.settings
    import ranger_async.core.fm
    from ranger_async.ext.openstruct import OpenStruct
    ranger_async.args = OpenStruct()
    ranger_async.args.clean = True
    ranger_async.args.debug = False

    settings = ranger_async.container.settings.Settings()
    ranger_async.core.shared.SettingsAware.settings_set(settings)
    fm = ranger_async.core.fm.FM()
    ranger_async.core.shared.FileManagerAware.fm_set(fm)

    time1 = time.time()
    fm.initialize()
    try:
        usr = ranger_async.container.directory.Directory('/usr')
        usr.load_content(schedule=False)
        for fileobj in usr.files:
            if fileobj.is_directory:
                fileobj.load_content(schedule=False)
    finally:
        fm.destroy()
    time2 = time.time()
    print("%dms" % ((time2 - time1) * 1000))


if __name__ == '__main__':
    main()
