#!/usr/bin/env python
# encoding: utf-8

import os
import classes
import argparse
from zipfile import ZipFile, BadZipfile
import re
import shutil


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

def split_file_name(file_name):
    name = re.sub(r'\.[^.]+?$', "", file_name)
    ext = file_name.replace(name, "").lstrip(".")
    return name, ext


def get_format_preference_index(ext):
    format_preference = ["mp3", "mp4", "ogg", "flac"]
    try:
        return format_preference.index(ext)
    except ValueError:
        return len(format_preference)

def downloaded_to_processing(source_dir_path, target_dir_path): #ścieżka do kat jako argument, znaleźć w kat wszystkie pliki .zip, rozpakować je do kat "do obróbki"
    for dir_path, sub_dirs, files in os.walk(source_dir_path):
        for f in files:
            if f.endswith(".zip"):
                source_file_path = os.path.join(dir_path, f)
                target_subdir_path = os.path.join(target_dir_path, f.replace(".zip", ""))
                try:
                    with ZipFile(source_file_path, "r") as zf:
                        for info in zf.infolist():
                            if classes.MusicFile.is_music_file(info.filename):
                                zf.extractall(target_subdir_path)
                                break
                    os.remove(source_file_path)
                except BadZipfile:
                    print(f"Plik {f} nie jest plikiem .zip.")

                    
def processing_to_verification(processing_dir_path, verification_dir_path):
    # 1. przeprocesowanie plików z kat procecessing:
    # a) pozbyć się duplikatów
    for dir_path, sub_dirs, files in os.walk(processing_dir_path):
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if classes.MusicFile.is_music_file(file_path):
                name, ext = split_file_name(file_name)
                for another_file_name in files:
                    if file_name == another_file_name:
                        continue
                    another_name, another_ext = split_file_name(another_file_name)
                    if name == another_name:
                        if get_format_preference_index(ext) >= get_format_preference_index(another_ext):
                            try:
                                os.remove(file_path)
                            except FileNotFoundError:
                                continue # skoro tego pliku nie ma, to nie ma co tutaj robić
    # b) przekonwertować nie mp3 na mp3
       # if ext != "mp3":
            pass
    # c) dostosować bitrate'y tam, gdzie to konieczne
    # d) dostosować poziom głośności
    # e) znormalizować tagi
    # f) pozbyć się zbędnych tagów
    # 2. przeniesienie ich do verification
    for dir_path, sub_dirs, files in os.walk(processing_dir_path, topdown=False):
        if classes.MusicDir.is_music_dir(dir_path):
            dir_name = os.path.basename(dir_path)
            destination_pth = os.path.join(verification_dir_path, dir_name)
            try:
                shutil.move(dir_path, destination_pth)
            except FileNotFoundError:
                continue #jeśli pliku nie ma, to nie można go przenieść


def verification_to_ready():
    pass


if __name__ == "__main__":
    dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData"
    from_dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData/Pobrane"
    processing_dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData/Do Obróbki"
    verification_dir_path = "/home/katrzyna/Documents/cokolwiek/tests/TestData/Weryfikacja"
    #get_music_dirs(dir_path)
    args = reading_arguments_from_terminal()
    if args.p2o:
        downloaded_to_processing(from_dir_path, processing_dir_path)
    if args.o2w:
        processing_to_verification(processing_dir_path, verification_dir_path)
    if args.w2g:
        verification_to_ready()
    if not (args.o2w or args.p2o or args.w2g):
        downloaded_to_processing(from_dir_path, processing_dir_path)
        processing_to_verification(processing_dir_path, verification_dir_path)
        verification_to_ready()
