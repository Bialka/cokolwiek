from os.path import dirname, join, realpath
import unittest

from ogarniacz_mp3 import get_music_dirs
from classes import MusicDir, MusicFile

_current_dir = realpath(dirname(__file__))
_test_data_dir = join(_current_dir, "TestData")


class TestMainDataGathering(unittest.TestCase):

    def test_getting_music_dirs(self):
        music_dirs = get_music_dirs(join(_test_data_dir, "Do Obróbki"))

        # check if all music dirs were found
        self.assertEqual(len(music_dirs), 6)
        # check if MusicFile objects were created within MusicDirs
        for music_dir in music_dirs:
            self.assertTrue(len(music_dir.music_files) > 0)
            # use an example file check if music files read the tags from mp3 files
            if music_dir.base_dir.endswith("Dolce Fine Giornata"):
                for music_file in music_dir.music_files:
                    if music_file.file_path.endswith("1. Fishermen.mp3"):
                        self.assertEqual(music_file.tracknumber, 1)
                        self.assertEqual(music_file.title, "Fishermen")
                        self.assertEqual(music_file.artist, "Daniel Bloom")
                        self.assertEqual(music_file.album_artist, "Daniel Bloom")
                        self.assertEqual(music_file.album_title, "Dolce Fine Giornata (feat. Leszek Możdżer)")


class TestRecognisingMusic(unittest.TestCase):

    def test_recognising_music_dirs(self):
        # a true music dir
        self.assertTrue(MusicDir.is_music_dir(join(_test_data_dir, "Do Obróbki", "Castle Rock (Single)")))
        # a dir that doesn't contain any music
        self.assertFalse(MusicDir.is_music_dir(_current_dir))
        # a dir that has music in sub-dirs
        self.assertFalse(MusicDir.is_music_dir(_test_data_dir))

    def test_recognising_music_files(self):
        self.assertFalse(MusicFile.is_music_file(__file__))
        self.assertTrue(MusicFile.is_music_file(
            join(_test_data_dir, "Do Obróbki", "Castle Rock (Single)", "05. 40 Below (From Castle Rock).mp3")))
        self.assertFalse(MusicFile.is_music_file(
            join(_test_data_dir, "Do Obróbki", "Castle Rock (Single)", "cover.jpg")))
        self.assertTrue(MusicFile.is_music_file(
            join(_test_data_dir, "Do Obróbki", "Castle Rock (Single)", "I don't exist.mp3")))
