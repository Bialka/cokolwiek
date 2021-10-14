
import os
from os.path import join
import getting_file_info
import mimetypes
import subprocess


class MusicFile:
    def __init__(self, file_path):
        self.file_path = file_path

        self.file_info = getting_file_info.get_file_info(file_path)

    def __getattr__(self, item):
        if item in self.file_info:
            return self.file_info[item]
        if item in self.file_info.get("tags", {}):
            return self.file_info["tags"][item]
        raise AttributeError(f"'MusicFile' has no attribute '{item}'")

    @property
    def track_number(self):
        track_nr = self.file_info.get("tags", {}).get("track")
        if track_nr is None:
            return None
        return int(self.track.split("/")[0])

    @property
    def album_artist(self):
        return self.file_info.get("tags", {}).get("album_artist")

    @property
    def date(self):
        try:
            return int(self.file_info.get("tags", {}).get("date"))
        except ValueError:
            return None

    @classmethod
    def is_music_file(cls, file_path):
        return (mimetypes.guess_type(file_path)[0] or '').startswith("audio/")

    def get_volume_info(self, input_file):
        proc = subprocess.run(["ffmpeg", "-i", input_file.mp3, "-af", "volumedetect", "-vn", "-sn", "-dn", "-f",
                               "null", "/dev/null"])
        if proc.returncode == 0:
            txt = proc.stderr.decode()
            lines = txt.split("\n")
            for line in lines:
                if line.startswith("[Parsed_volumedetect"):
                    print(line)
        else:
            print(proc.stderr.decode())


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

    def adjust_loudness(self, processing_dir_path):
        for f in self.music_files:
            volume_info = MusicFile.get_volume_info(f, f)
            print(volume_info)

