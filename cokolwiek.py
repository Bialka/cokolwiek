#!/usr/bin/env python
# encoding: utf-8

import os

import shutil

import dir_class

def collect_data_about_mp3(directory):
    music_files_dirs = []
    for x in os.walk(directory):
        cos_dir = dir_class.Dir(x[0])
        if cos_dir.is_music_files_dir():
            music_files_dirs.append(cos_dir)
    return music_files_dirs


def record(music_files_dirs, path):
    with open(path, 'w') as f:
        for cos_dir in music_files_dirs:
            f.write(cos_dir.get_control_string())


def files_processing(file_path):
    with open(file_path, 'r') as f:
        x = f.read().strip()
        for ln in x.split("\n"):
            ln = dir_class.Dir.parse_control_string(ln)
            cos_dir = dir_class.Dir(ln[1])
            if ln[0] == "u":
                cos_dir.delete(ln[1])
            elif ln[0] == "p":
                cos_dir.move(ln[2])
    os.remove(file_path)


if __name__ == "__main__":
    print("Zaczynam")
    file_path = 'cokolwiek.txt'
    current_dir = "do_zrobienia"
    destination_dir = "zrobione"

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    if os.path.isfile(file_path):
        files_processing(file_path)
    else:
        music_files_dirs = collect_data_about_mp3("do_zrobienia")
        record(music_files_dirs, file_path)
