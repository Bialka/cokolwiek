#!/usr/bin/env python
# encoding: utf-8

import os

print ("Zaczynam")
if __name__ == "__main__":
    slownik = {}
    licznik_plikow = 0
    licznik_katalogow = 0
    for x in os.walk("do_zrobienia"):
        licznik_katalogow += 1
        nowa_lista = []
        for nazwa_pliku in x[2]:
            if nazwa_pliku.endswith(".mp3"):
                nowa_lista.append(nazwa_pliku)
                licznik_plikow += 1
        if nowa_lista:
            slownik[(x[0])] = nowa_lista
    print(slownik)
    print("Znaleziono {} plików w {} katalogach.".format(licznik_plikow, licznik_katalogow))            
