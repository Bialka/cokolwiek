#!/usr/bin/env python
# encoding: utf-8

import os
import classes
import argparse


def get_music_dirs(dir_path):
    music_dirs = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        if classes.MusicDir.is_music_dir(dirpath):
            music_dirs.append(classes.MusicDir(dirpath))
    return music_dirs


def reading_arguments_from_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument("--p2o", action="store_true")
    parser.add_argument("--o2w", action="store_true")
    parser.add_argument("--w2g", action="store_true")
    args = parser.parse_args()
    print(args)
    return args


def downloaded_to_processing():
    pass


def processing_to_verification():
    pass


def verification_to_ready():
    pass


if __name__ == "__main__":
    dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData"
    get_music_dirs(dir_path)
    args = reading_arguments_from_terminal()
    if args.p2o:
        downloaded_to_processing()
        print("a")
    if args.o2w:
        processing_to_verification()
        print("b")
    if args.w2g:
        verification_to_ready()
        print("c")
    if not args.o2w and args.p2o and args.w2g:
        downloaded_to_processing()
        processing_to_verification()
        verification_to_ready()
        print("e")
