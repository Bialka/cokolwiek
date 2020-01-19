
import os


class Dir:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def is_music_files_dir(self):
        for item in os.listdir(self.base_dir):
            pth = os.path.join(self.base_dir, item)
            if os.path.isfile(pth) and self.is_music_file(pth):
                return True
        return False

    def is_music_file(self, pth):
        return pth.endswith(".mp3")

    def get_control_string(self):
        target_dir_name = self.base_dir.split(os.sep)[-1]
        music_files_count = self.get_music_files_count()
        return " - | {0: <50}|{1: <25} | {2: >3}\n".format(self.base_dir, target_dir_name, music_files_count)

    def get_music_files_count(self):
        files_count = 0
        for item in os.listdir(self.base_dir):
            pth = os.path.join(self.base_dir, item)
            if os.path.isfile(pth) and self.is_music_file(pth):
                files_count += 1
        return files_count
