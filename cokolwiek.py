#!/usr/bin/env python
# encoding: utf-8

import os

print ("Zaczynam")
if __name__ == "__main__":
    for x in os.walk("do_zrobienia"):
        print ("\t", x[0])
        print ("\t", x[1])
        for nazwa_pliku in x[2]:
            if nazwa_pliku.endswith(".mp3"):
                print("\t", nazwa_pliku)
