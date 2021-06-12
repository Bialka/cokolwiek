#!/usr/bin/env python
# encoding: utf-8

import os
import classes
import argparse
from zipfile import ZipFile


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
    return args


def downloaded_to_processing(source_dir_path, target_dir_path): #ścieżka do kat jako argument, znaleźć w kat wszystkie pliki .zip, rozpakować je do kat "do obróbki"
    for dir_path, sub_dirs, files in os.walk(source_dir_path):
        for f in files:
            if f.endswith(".zip"):
                source_file_path = os.path.join(dir_path, f)
                target_subdir_path = os.path.join(target_dir_path, f.replace(".zip", ""))
                with ZipFile(source_file_path, "r") as zf:
                    zf.extractall(target_subdir_path)
                os.remove(source_file_path)


def processing_to_verification():
    pass


def verification_to_ready():
    pass


if __name__ == "__main__":
    dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData"
    from_dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData/Pobrane"
    final_dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData/Do Obróbki"
    #get_music_dirs(dir_path)
    args = reading_arguments_from_terminal()
    if args.p2o:
        downloaded_to_processing(from_dir_path, final_dir_path)
    if args.o2w:
        processing_to_verification()
    if args.w2g:
        verification_to_ready()
    if not (args.o2w or args.p2o or args.w2g):
        downloaded_to_processing()
        processing_to_verification()
        verification_to_ready()
