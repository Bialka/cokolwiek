#!/usr/bin/env python
# encoding: utf-8

import os

import classes


def get_music_dirs(dir_path):
    music_dirs = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        if classes.MusicDir.is_music_dir(dirpath):
            music_dirs.append(classes.MusicDir(dirpath))
    return music_dirs


if __name__ == "__main__":
    dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData"
    get_music_dirs(dir_path)
