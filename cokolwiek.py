#!/usr/bin/env python
# encoding: utf-8

import os

print ("Zaczynam")
if __name__ == "__main__":
    for x in os.walk("do_zrobienia"):
        for nazwa_pliku in x[2]:
            print("\t", nazwa_pliku)
