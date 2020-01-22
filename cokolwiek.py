#!/usr/bin/env python
# encoding: utf-8

import os

import shutil

import dir_class

def zbierz_dane_o_mp3(katalog):
    music_files_dirs = []
    for x in os.walk(katalog):
        cos_dir = dir_class.Dir(x[0])
        if cos_dir.is_music_files_dir():
            music_files_dirs.append(cos_dir)
    return music_files_dirs


def zapis(music_files_dirs, sciezka):
    with open(sciezka, 'w') as f:
        for cos_dir in music_files_dirs:
            f.write(cos_dir.get_control_string())


def obrobka_plikow(sciezka_pliku):
    with open(sciezka_pliku, 'r') as f:
        x = f.read().strip()
        for ln in x.split("\n"):
            ln = dir_class.Dir.parse_control_string(ln)
            cos_dir = dir_class.Dir(ln[1].strip())
            if ln[0].strip() == "u":
                cos_dir.delete(ln[1].strip())
            elif ln[0].strip() == "p":
                cos_dir.move(ln[1].strip(), ln[2].strip())
            print(ln)
    os.remove(sciezka_pliku)


if __name__ == "__main__":
    print("Zaczynam")
    sciezka_pliku = 'cokolwiek.txt'
    obecny_katalog = "do_zrobienia"
    katalog_docelowy = "zrobione"

    if not os.path.exists(katalog_docelowy):
        os.makedirs(katalog_docelowy)

    if os.path.isfile(sciezka_pliku):
        obrobka_plikow(sciezka_pliku)
    else:
        music_files_dirs = zbierz_dane_o_mp3("do_zrobienia")
        zapis(music_files_dirs, sciezka_pliku)
