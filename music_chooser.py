# -*- coding: utf-8 -*-

import random
import os
import shutil


def copy_to_player(dest):
    files = os.listdir(u"music")

    while True:
        print("Files: %d" % len(files))

        _file = random.choice(files)

        del files[files.index(_file)]

        try:
            shutil.copy(u"music" + os.sep + _file, dest)
        except Exception:
            print("Error when try to copy file...")

            return


copy_to_player(u"d:" + os.sep)
