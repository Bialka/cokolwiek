import os
from os import path
import subprocess
import sys

_current_dir = path.realpath(path.dirname(__file__))


def check_ffmpeg():
    proc = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if proc.returncode != 0:
        sys.exit("Chyba ffmpeg nie jest dobrze zainstalowany :(")


def convert_to_flac(file_path):
    # get names and dirs
    dir_path = path.dirname(file_path)
    file_name = path.basename(file_path)
    new_file_name = file_name.replace(".mp3", ".flac")
    new_file_path = path.join(dir_path, new_file_name)
    # conversion
    proc = subprocess.run(["ffmpeg", "-i", file_path, "-b:a", "320000", new_file_path],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if proc.returncode != 0:
        print(f"Coś poszło nie tak przy konwersji na flac pliku: {file_path}")
        sys.exit(1)


if __name__ == "__main__":
    check_ffmpeg()
    # convert 1917 to flac
    _1917_dir = path.join(_current_dir, "tests/TestData/Do Obróbki/1917FYC/1917 (FYC)")
    for file_name in ("01. Meadow , First Trench.mp3", "02. Trench to Yorks.mp3"):
        file_path = path.join(_1917_dir, file_name)
        convert_to_flac(file_path)
        os.remove(file_path)

    # create duplicate for How to train your dragon
    httyd_path = path.join(_current_dir, "tests/TestData/Do Obróbki/How to Train Your Dragon - The Hidden World",
                           "01. Raiders Return to Busy, Busy Berk.mp3")
    convert_to_flac(httyd_path)

    print("Zrobione")
