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
        self.assertEqual(len(music_dirs), 8)
        # check if MusicFile objects were created within MusicDirs
        for music_dir in music_dirs:
            self.assertTrue(len(music_dir.music_files) > 0)
            # use an example file check if music files read the tags from mp3 files
            if music_dir.base_dir.endswith("Dolce Fine Giornata"):
                for music_file in music_dir.music_files:
                    if music_file.file_path.endswith("1. Fishermen.mp3"):
                        self.assertEqual(music_file.track_number, 1)
                        self.assertEqual(music_file.title, "Fishermen")
                        self.assertEqual(music_file.artist, "Daniel Bloom")
                        self.assertEqual(music_file.album_artist, "Daniel Bloom")
                        self.assertEqual(music_file.album, "Dolce Fine Giornata (feat. Leszek Możdżer)")
            elif music_dir.base_dir.endswith("The Hidden World"):
                for music_file in music_dir.music_files:
                    if music_file.file_path.endswith("Busy Berk.mp3"):
                        self.assertEqual(music_file.track_number, 1)
                        self.assertEqual(music_file.title, "Raiders Return to Busy, Busy Berk")
                        self.assertEqual(music_file.artist, "John Powell")
                        self.assertEqual(music_file.album_artist, None)
                        self.assertEqual(music_file.album, "How to Train Your Dragon: "
                                                           "The Hidden World (Original Motion Picture Soundtrack)")
                        self.assertEqual(music_file.date, 2019)
            elif music_dir.base_dir.endswith("Castle Rock (Single)"):
                for music_file in music_dir.music_files:
                    if music_file.file_path.endswith("01 Castle Rock (Main Theme) [From Castle Rock].mp3"):
                        self.assertEqual(music_file.track_number, 1)
                        self.assertEqual(music_file.title, "Castle Rock (Main Theme) [From \"Castle Rock\"]")
                        self.assertEqual(music_file.artist, "Thomas Newman")
                        self.assertEqual(music_file.album_artist, "Thomas Newman")
                        self.assertEqual(music_file.album, "Castle Rock (Main Theme) [From \"Castle Rock\"]")
                        self.assertEqual(music_file.date, 2018)

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


class TestReadingMp3Tags(unittest.TestCase):

    def test_happy_path(self):
        from tags_handling import get_file_info
        # test on a file that has all required fields filled the right way
        file_info = get_file_info(join(_test_data_dir, "Do Obróbki", "26-06-19", "Dolce Fine Giornata", "1. Fishermen.mp3"))
        tags = file_info["tags"]
        self.assertEqual(tags["track"], "1")
        self.assertEqual(tags["title"], "Fishermen")
        self.assertEqual(tags["artist"], "Daniel Bloom")
        self.assertEqual(tags["album_artist"], "Daniel Bloom")
        self.assertEqual(tags["album"], "Dolce Fine Giornata (feat. Leszek Możdżer)")
        self.assertEqual(tags["date"], "2019")

    def test_sad_paths(self):
        from tags_handling import get_file_info
        # TODO: a file without any mp3 tags present
        # a file without album artist
        file_info = get_file_info(join(_test_data_dir, "Do Obróbki", "How to Train Your Dragon - The Hidden World",
                                       "01. Raiders Return to Busy, Busy Berk.mp3"))
        tags = file_info["tags"]
        self.assertEqual(tags["track"], "01")
        self.assertEqual(tags["title"], "Raiders Return to Busy, Busy Berk")
        self.assertEqual(tags["artist"], "John Powell")
        self.assertEqual(tags.get("album_artist"), None)
        self.assertEqual(tags["album"], "How to Train Your Dragon: "
                                              "The Hidden World (Original Motion Picture Soundtrack)")
        self.assertEqual(tags["date"], "2019")
        # a file with x/y tracknumber format

        file_info = get_file_info(join(_test_data_dir, "Do Obróbki", "Castle Rock (Single)",
                                       "01 Castle Rock (Main Theme) [From Castle Rock].mp3"))
        tags = file_info["tags"]
        self.assertEqual(tags["track"], "1/1")
        self.assertEqual(tags["title"], "Castle Rock (Main Theme) [From \"Castle Rock\"]")
        self.assertEqual(tags["artist"], "Thomas Newman")
        self.assertEqual(tags["album_artist"], "Thomas Newman")
        self.assertEqual(tags["album"], "Castle Rock (Main Theme) [From \"Castle Rock\"]")
        self.assertEqual(tags["date"], "2018")
