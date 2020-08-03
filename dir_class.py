import os
import shutil
import subprocess

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
                if self.is_music_file(f):
                    self.update_tags(album_artist, album_title, destination_pth + os.sep + f)
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

    def update_tags(self, album_artist, album_title, f):
        audio = EasyID3(f)
        audio["album"] = album_title
        audio["albumartist"] = album_artist
        audio.save()

    def edit(self):
        file_name = "dane_plikow.txt"
        tags = self.data_about_files()
        # todo: przenieś zapisywanie pliku do oddzielnej funkcji
        with open(file_name, "w") as f:
            for value in tags:
                file_path = value["file_path"][0] if value.get("file_path", False) else "-"
                file_tracknumber = value["file_tracknumber"][0] if value.get("file_tracknumber", False) else "-"
                file_title = value["file_title"][0] if value.get("file_title", False) else "-"
                file_artist = value["file_artist"][0] if value.get("file_artist", False) else "-"
                file_album = value["file_album"][0] if value.get("file_album", False) else "-"
                album_artist = value["file_artist"][0] if value.get("file_artist", False) else "-"
                year = value["year"][0] if value.get("year", False) else "-"
                f.write("- | {0: <50}|{1: <25} |{2: <25} | {3: <25}|{4: <25}|{5: <25}|{6: <25}\n".format( file_path,
                                                                                                          file_tracknumber, file_title, file_artist, file_album, album_artist, year))
        subprocess.call(["notepad", file_name])
        self.reading_data_from_text_file(file_name)

    def data_about_files(self):
        files_data = []
        for item in os.listdir(self.base_dir):
            if self.is_music_file(item):
                audio = EasyID3(os.path.join(self.base_dir, item))
                file_title = audio["title"]
                file_tracknumber = audio["tracknumber"]
                file_artist = audio["artist"]
                file_album = audio["album"]
                album_artist = audio["albumartist"]
                year = audio["date"]
                file_path = [os.path.join(self.base_dir, item)]
                tags = {"file_title": file_title, "file_tracknumber": file_tracknumber, "file_artist": file_artist, "file_album": file_album,
                        "album_artist": album_artist, "year": year, "file_path": file_path}
                files_data.append(tags)
        return files_data

    def reading_data_from_text_file(self, file_name):
        with open(file_name, "r") as f:
            x = f.read()
            for line in x.split("\n"):
                if line == "":
                    continue
                line_elements = line.split("|")
                action = line_elements[0].strip()
                file_path = line_elements[1].strip()
                file_tracknumber = line_elements[2].strip()
                file_title = line_elements[3].strip()
                file_artist = line_elements[4].strip()
                file_album = line_elements[5].strip()
                album_artist = line_elements[6].strip()
                file_year = line_elements[7].strip()
                if action == "-":
                    pass
                elif action == "e":
                    audio = EasyID3(file_path)
                    audio["title"] = file_title
                    audio["tracknumber"] = file_tracknumber
                    audio["artist"] = file_artist
                    audio["album"] = file_album
                    audio["albumartist"] = album_artist
                    audio["date"] = file_year
                    audio.save()
                elif action == "u":
                    os.remove(file_path)

