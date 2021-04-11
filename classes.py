
import os
from os.path import join

from mutagen.easyid3 import EasyID3


class MusicFile:
    def __init__(self, file_path):
        self.file_path = file_path

        self.tracknumber = None
        self.title = None
        self.artist = None
        self.album_artist = None
        self.album_title = None
        self.year = None

        self.read_tags()
        print(self.album_title, self.tracknumber, self.title)

    @classmethod
    def is_music_file(cls, file_path):
        return file_path.endswith(".mp3")

    def read_tags(self):
        audio = EasyID3(self.file_path)
        self.tracknumber = int(audio["tracknumber"][0])  # TODO: konwertuj do int
        self.title = audio["title"][0]
        self.artist = audio["artist"][0]
        try:
            self.album_artist = audio["albumartist"][0]
        except KeyError:
            pass
        self.album_title = audio["album"][0]
        self.year = audio["date"][0]


class MusicDir:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.music_files = []
        for file_name in os.listdir(self.base_dir):
            file_path = join(self.base_dir, file_name)
            if MusicFile.is_music_file(file_path):
                dir_cos = MusicFile(file_path)
                self.music_files.append(dir_cos)

    @classmethod
    def is_music_dir(cls, dir_path):
        for file_path in os.listdir(dir_path):
            if MusicFile.is_music_file(file_path):
                return True
        return False

    def get_control_string(self):
        pass  # TODO
