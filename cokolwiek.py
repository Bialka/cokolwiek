#!/usr/bin/env python
# encoding: utf-8

import os

print ("Zaczynam")
if __name__ == "__main__":
    for x in os.walk("do_zrobienia"):
        print(x)
