
import os

import shutil

class Dir:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.music_files = self.get_music_files()

    def get_music_files(self):
        music_files = []
        for item in os.listdir(self.base_dir):
            pth = os.path.join(self.base_dir, item)
            if os.path.isfile(pth) and self.is_music_file(pth):
                music_files.append(item)
        return music_files

    def is_music_files_dir(self):
        return bool(self.music_files)

    def is_music_file(self, pth):
        return pth.endswith(".mp3")

    def get_control_string(self):
        target_dir_name = self.base_dir.split(os.sep)[-1]
        music_files_count = self.get_music_files_count()
        return " - | {0: <50}|{1: <25} | {2: >3}\n".format(self.base_dir, target_dir_name, music_files_count)

    def get_music_files_count(self):
        return len(self.music_files)

    def move(self, obecny_katalog, podkatalog_docelowy):
        katalog_docelowy = "zrobione"
        for x, y, z in os.walk(obecny_katalog):
            destination_pth = katalog_docelowy + os.sep + podkatalog_docelowy
            os.makedirs(destination_pth, exist_ok=True)
            for f in z:
                source_pth = x + os.sep + f
                shutil.move(source_pth, destination_pth)
            break
            # todo: usuwanie drzewa
        shutil.rmtree(obecny_katalog)

    def delete(self, to_delete):
        shutil.rmtree(to_delete, ignore_errors=True)
