#!/usr/bin/env python
# encoding: utf-8

import os

import shutil

def zbierz_dane_o_mp3(katalog):
    slownik = {}
    licznik_plikow = 0
    licznik_katalogow = 0
    for x in os.walk(katalog):
        nowa_lista = []
        for nazwa_pliku in x[2]:
            if nazwa_pliku.endswith(".mp3"):
                nowa_lista.append(nazwa_pliku)
                licznik_plikow += 1
        if nowa_lista:
            slownik[(x[0])] = nowa_lista
            licznik_katalogow += 1
    print("Znaleziono {} plików w {} katalogach.".format(licznik_plikow, licznik_katalogow))
    return slownik


def zapis(slownik, sciezka):
    with open(sciezka, 'w') as f:
        for klucz, pliki in slownik.items():
            ilosc_plikow = len(pliki)
            podkatalog_docelowy = klucz.split(os.sep)[-1]
            f.write(" - | {0: <50}|{1: <25} | {2: >3}\n".format(klucz, podkatalog_docelowy, ilosc_plikow))


def obrobka_plikow(sciezka_pliku):
    with open(sciezka_pliku, 'r') as f:
        x = f.read().strip()
        for ln in x.split("\n"):
            ln = ln.split("|")
            if ln[0].strip() == "u":
                shutil.rmtree(ln[1].strip(), ignore_errors=True)
            elif ln[0].strip() == "p":
                przenoszenie_plik(ln[1].strip())
            print(ln)
    os.remove(sciezka_pliku)


def przenoszenie_plik(obecny_katalog):
    podkatalog_docelowy = obecny_katalog.split(os.sep)[-1]
    for x, y, z in os.walk(obecny_katalog):
        for f in z:
            source_pth = x + os.sep + f
            destination_pth = katalog_docelowy + os.sep + podkatalog_docelowy
            os.makedirs(destination_pth)
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
        slownik = zbierz_dane_o_mp3("do_zrobienia")
        zapis(slownik, sciezka_pliku)
