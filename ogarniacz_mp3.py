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
    if reading_arguments_from_terminal().p2o == True:
        downloaded_to_processing()
    if reading_arguments_from_terminal().o2w == True:
        processing_to_verification()
    if reading_arguments_from_terminal().w2g == True:
        verification_to_ready()
    if reading_arguments_from_terminal().p2o and reading_arguments_from_terminal().o2w == True:
        downloaded_to_processing()
        processing_to_verification()
        print("hello")
    if reading_arguments_from_terminal().p2o and reading_arguments_from_terminal().o2w and reading_arguments_from_terminal().w2g == False:
        print("hello")
        downloaded_to_processing()
        processing_to_verification()
        verification_to_ready()
