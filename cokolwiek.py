#!/usr/bin/env python
# encoding: utf-8

import os

print ("Zaczynam")
if __name__ == "__main__":
    for x in os.walk("do_zrobienia"):
        juz_wyprintowany = False
        for nazwa_pliku in x[2]:
            if nazwa_pliku.endswith(".mp3"):
                if not juz_wyprintowany:
                    print (x[0])
                    juz_wyprintowany = True
                print("\t", nazwa_pliku)
