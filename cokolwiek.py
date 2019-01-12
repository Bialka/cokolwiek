#!/usr/bin/env python
# encoding: utf-8

import os


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
    f = open(sciezka, 'w')

    for klucz in slownik.keys():
        f.write(klucz + '\n')

    f.close()


if __name__ == "__main__":
    print("Zaczynam")
    sciezka_pliku = 'cokolwiek.txt'
    if os.path.isfile(sciezka_pliku):
        f = open(sciezka_pliku, 'r')
        x = f.read()
        f.close()
        print(x)
        os.remove(sciezka_pliku)
    else:
        slownik = zbierz_dane_o_mp3("do_zrobienia")
        zapis(slownik, sciezka_pliku)
