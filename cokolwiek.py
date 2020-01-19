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
            ln = ln.split("|")
            if ln[0].strip() == "u":
                shutil.rmtree(ln[1].strip(), ignore_errors=True)
            elif ln[0].strip() == "p":
                przenoszenie_plik(ln[1].strip(), ln[2].strip())
            print(ln)
    os.remove(sciezka_pliku)


def przenoszenie_plik(obecny_katalog, podkatalog_docelowy):
    for x, y, z in os.walk(obecny_katalog):
        destination_pth = katalog_docelowy + os.sep + podkatalog_docelowy
        os.makedirs(destination_pth, exist_ok=True)
        for f in z:
            source_pth = x + os.sep + f
            shutil.move(source_pth, destination_pth)
        break
    # todo: usuwanie drzewa
    shutil.rmtree(obecny_katalog)



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
