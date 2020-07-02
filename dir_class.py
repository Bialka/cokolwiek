
import os

import shutil

from mutagen.easyid3 import EasyID3


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
        music_files_count = self.get_music_files_count()
        tags = self.get_tags()
        print(tags)
        album_title = str(tags["album_title"][0]) if len(tags["album_title"]) == 1 else "Wiele"
        album_artist = str(tags["album_artist"][0]) if len(tags["album_artist"]) == 1 else "Wiele"
        return " - | {0: <50}|{1: <25} |{2: <25} | {3: >3}\n".format(self.base_dir, album_title, album_artist, music_files_count)

    def get_music_files_count(self):
        return len(self.music_files)

    def move(self, destination_dir, album_artist, album_title):
        destination_pth = destination_dir + os.sep + album_artist + os.sep + album_title
        os.makedirs(destination_pth, exist_ok=True)
        for x, y, z in os.walk(self.base_dir):
            for f in z:
                source_pth = x + os.sep + f
                shutil.move(source_pth, destination_pth)
            break
        shutil.rmtree(self.base_dir)

    def delete(self):
        shutil.rmtree(self.base_dir, ignore_errors=True)

    @classmethod
    def parse_control_string(cls, control_string):
        return [s.strip() for s in control_string.split("|")]

    def get_tags(self):
        cos = {}
        selected_album_artist = [0, "whoever"]
        selected_album_title = [0, "whatever"]
        for f in self.music_files:
            audio = EasyID3(self.base_dir + os.sep + f)
            try:
                album_title = audio["album"][0]
            except KeyError:
                album_title = ""
            try:
                album_artist = audio["albumartist"][0]
            except KeyError:
                album_artist = ""

            if album_artist != "":
                if album_artist not in cos:
                    cos[album_artist] = 0
                cos[album_artist] += 1
                if selected_album_artist[0] < cos[album_artist]:
                    selected_album_artist = [cos[album_artist], album_artist]
                elif selected_album_artist[0] == cos[album_artist]:
                    selected_album_artist += [album_artist]

            if album_title != "":
                if album_title not in cos:
                    cos[album_title] = 0
                cos[album_title] += 1
                if selected_album_title[0] < cos[album_title]:
                    selected_album_title = [cos[album_title], album_title]
                elif selected_album_title[0] == cos[album_title]:
                    selected_album_title += [album_title]
        r1 = (selected_album_artist[1:] if selected_album_artist[0] else None)
        r2 = (selected_album_title[1:] if selected_album_title[0] else None)
        return {"album_artist": r1, "album_title": r2}
