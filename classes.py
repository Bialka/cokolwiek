
import os
from os.path import join
import tags_handling
from mutagen.easyid3 import EasyID3
import mimetypes


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
        return mimetypes.guess_type(file_path)[0].startswith("audio/")

    def read_tags(self):
        for key, val in tags_handling.get_file_tags(self.file_path).items():
            setattr(self, key, val)


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
